from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import chromadb
from chromadb.errors import NotFoundError
from sklearn.feature_extraction.text import HashingVectorizer

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


ALLOWED_EXTENSIONS = {
    ".md",
    ".py",
    ".html",
    ".txt",
    ".csv",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ps1",
    ".sh",
    ".bat",
}

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    ".idea",
    ".vscode",
    "Agent/data",
}

EXCLUDED_FILE_PATTERNS = (
    re.compile(r".*_assignment_.*\.py$", re.IGNORECASE),
    re.compile(r".*instructor_notes\.md$", re.IGNORECASE),
)


@dataclass
class ChunkDocument:
    doc_id: str
    text: str
    path: str
    chunk_index: int


class LocalEmbedding:
    def __init__(self, dim: int = 1024) -> None:
        self._vectorizer = HashingVectorizer(
            n_features=dim,
            alternate_sign=False,
            norm="l2",
            token_pattern=r"(?u)\\b\\w+\\b",
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        matrix = self._vectorizer.transform(texts)
        return matrix.toarray().tolist()


class OpenAIEmbedding:
    def __init__(self, api_key: str, model: str, dim: int | None = None) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for openai embedding provider")
        if OpenAI is None:
            raise ValueError("openai package is unavailable")
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._dim = dim if isinstance(dim, int) and dim > 0 else None

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors: list[list[float]] = []
        batch_size = 64
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                kwargs = {"model": self._model, "input": batch}
                if self._dim is not None:
                    kwargs["dimensions"] = self._dim
                resp = self._client.embeddings.create(**kwargs)
            except TypeError:
                # Older SDK/model combinations may not support dimensions.
                resp = self._client.embeddings.create(model=self._model, input=batch)
            vectors.extend([list(item.embedding) for item in resp.data])
        return vectors


class RepoRAG:
    def __init__(
        self,
        db_path: Path,
        collection_name: str,
        embed_dim: int = 1024,
        embedding_provider: str = "local",
        openai_api_key: str = "",
        openai_embedding_model: str = "text-embedding-3-large",
    ) -> None:
        self._db_path = db_path
        self._db_path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self._db_path))
        self._collection_name = collection_name
        self._collection = self._client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
        provider = (embedding_provider or "local").strip().lower()
        self._embedding_provider = "local"
        if provider == "openai":
            try:
                self._embedder = OpenAIEmbedding(
                    api_key=openai_api_key,
                    model=openai_embedding_model,
                    dim=embed_dim,
                )
                self._embedding_provider = "openai"
            except Exception:
                self._embedder = LocalEmbedding(embed_dim)
                self._embedding_provider = "local"
        else:
            self._embedder = LocalEmbedding(embed_dim)
            self._embedding_provider = "local"

    @property
    def collection_name(self) -> str:
        return str(self._collection_name)

    @property
    def embedding_provider(self) -> str:
        return self._embedding_provider

    def count(self) -> int:
        self._ensure_collection()
        return int(self._collection.count())

    def reload_collection(self) -> None:
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self) -> None:
        self._ensure_collection()
        self._client.delete_collection(self._collection_name)
        self.reload_collection()

    def ingest(self, repo_root: Path, chunk_size: int = 900, chunk_overlap: int = 150) -> tuple[int, int]:
        self._ensure_collection()
        chunk_docs = list(self._iter_chunks(repo_root, chunk_size=chunk_size, chunk_overlap=chunk_overlap))
        if not chunk_docs:
            return (0, 0)

        ids = [d.doc_id for d in chunk_docs]
        docs = [d.text for d in chunk_docs]
        metas = [
            {
                "path": d.path,
                "chunk_index": d.chunk_index,
                "root_dir": d.path.split("/", 1)[0] if "/" in d.path else d.path,
            }
            for d in chunk_docs
        ]
        embs = self._embedder.embed(docs)

        batch_size = 128
        for i in range(0, len(ids), batch_size):
            self._collection.add(
                ids=ids[i : i + batch_size],
                documents=docs[i : i + batch_size],
                metadatas=metas[i : i + batch_size],
                embeddings=embs[i : i + batch_size],
            )

        unique_files = len({d.path for d in chunk_docs})
        return unique_files, len(chunk_docs)

    def query(
        self,
        question: str,
        top_k: int = 6,
        class_hint: str | None = None,
        preferred_dirs: list[str] | None = None,
        query_expansions: list[str] | None = None,
    ) -> list[dict]:
        self._ensure_collection()
        top_k = max(1, top_k)
        raw_k = min(max(top_k * 4, 12), 80)
        docs_triplets: list[tuple[str, dict, float]] = []
        preferred_dir_set = {d.lower() for d in (preferred_dirs or []) if d}
        expansions = [e for e in (query_expansions or []) if e.strip()]

        def collect(query_text: str) -> None:
            q_emb = self._embedder.embed([query_text])[0]
            result = self._collection.query(
                query_embeddings=[q_emb],
                n_results=raw_k,
                include=["documents", "metadatas", "distances"],
            )
            documents = result.get("documents", [[]])[0]
            metadatas = result.get("metadatas", [[]])[0]
            distances = result.get("distances", [[]])[0]
            docs_triplets.extend(zip(documents, metadatas, distances))

        collect(question)
        for expansion in expansions[:3]:
            collect(expansion)
        if class_hint:
            collect(f"{class_hint} 학습 가이드 예제 과제 퀴즈")

        output = []
        for doc, meta, dist in docs_triplets:
            vector_score = self._distance_to_score(float(dist))
            lexical = self._lexical_overlap(question, doc)
            score = round((vector_score * 0.72) + (lexical * 0.28), 6)
            path = str((meta or {}).get("path", ""))
            if class_hint and class_hint in path.lower():
                score = min(1.0, score + 0.35)
            root_dir = path.split("/", 1)[0].lower() if path else ""
            if preferred_dir_set and root_dir in preferred_dir_set:
                score = min(1.0, score + 0.28)
            score = min(1.0, max(0.0, score + self._path_intent_bonus(question=question, path=path)))
            if self._is_noise_file(path):
                score = max(0.0, score - 0.35)
            output.append(
                {
                    "path": path,
                    "score": score,
                    "vector_score": vector_score,
                    "lexical_score": lexical,
                    "chunk": doc,
                    "source_type": "repo",
                    "provider": f"chromadb:{self._embedding_provider}",
                }
            )
        output.sort(key=lambda x: x["score"], reverse=True)
        if output:
            best = output[0]["score"]
            threshold = max(0.08, best * 0.45)
            filtered = [item for item in output if item["score"] >= threshold]
            output = filtered if filtered else output[:1]
        deduped: list[dict] = []
        seen_pairs: set[tuple[str, str]] = set()
        for item in output:
            path = item.get("path", "")
            sig = (path, (item.get("chunk", "")[:180]).strip())
            if sig in seen_pairs:
                continue
            seen_pairs.add(sig)
            deduped.append(item)
            if len(deduped) >= top_k:
                break
        return deduped

    def _iter_chunks(self, repo_root: Path, chunk_size: int, chunk_overlap: int) -> Iterable[ChunkDocument]:
        for file_path in self._iter_files(repo_root):
            rel_path = file_path.relative_to(repo_root).as_posix()
            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            chunks = self._split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            for idx, chunk in enumerate(chunks):
                doc_id = f"{rel_path}::{idx}"
                yield ChunkDocument(doc_id=doc_id, text=chunk, path=rel_path, chunk_index=idx)

    def _iter_files(self, repo_root: Path) -> Iterable[Path]:
        for path in repo_root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue
            rel = path.relative_to(repo_root).as_posix()
            if any(part in EXCLUDED_DIRS for part in rel.split("/")):
                continue
            if rel.startswith("Agent/data/"):
                continue
            if self._is_noise_file(rel):
                continue
            yield path

    def _ensure_collection(self) -> None:
        try:
            self._collection.count()
        except NotFoundError:
            self.reload_collection()

    @staticmethod
    def _is_noise_file(path: str) -> bool:
        path_lower = (path or "").lower()
        return any(pattern.match(path_lower) for pattern in EXCLUDED_FILE_PATTERNS)

    @staticmethod
    def _split_text(text: str, chunk_size: int = 900, chunk_overlap: int = 150) -> list[str]:
        cleaned = text.strip()
        if not cleaned:
            return []

        if len(cleaned) <= chunk_size:
            return [cleaned]

        chunks: list[str] = []
        start = 0
        n = len(cleaned)
        step = max(1, chunk_size - chunk_overlap)

        while start < n:
            end = min(n, start + chunk_size)
            piece = cleaned[start:end]
            if end < n:
                # Prefer splitting at a newline near the boundary.
                split_pos = piece.rfind("\n")
                if split_pos >= math.floor(chunk_size * 0.6):
                    end = start + split_pos
                    piece = cleaned[start:end]
            piece = piece.strip()
            if piece:
                chunks.append(piece)
            if end >= n:
                break
            start += step

        return chunks

    @staticmethod
    def _distance_to_score(distance: float) -> float:
        score = 1.0 - distance
        if score < 0.0:
            return 0.0
        if score > 1.0:
            return 1.0
        return score

    @staticmethod
    def _lexical_overlap(question: str, doc: str) -> float:
        q_tokens = RepoRAG._tokenize(question)
        if not q_tokens:
            return 0.0
        d_tokens = set(RepoRAG._tokenize(doc))
        if not d_tokens:
            return 0.0
        overlap = sum(1 for t in q_tokens if t in d_tokens)
        return min(1.0, overlap / max(1, len(set(q_tokens))))

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [t for t in re.findall(r"[0-9a-zA-Z가-힣_]+", (text or "").lower()) if len(t) >= 2]

    @staticmethod
    def _path_intent_bonus(question: str, path: str) -> float:
        q = (question or "").lower()
        q_norm = re.sub(r"[^0-9a-zA-Z가-힣]", "", q)
        p = (path or "").lower()
        root = p.split("/", 1)[0] if p else ""

        llm_roots = {"llmtextgen", "prompteng", "langchainlab", "ragpipeline"}
        rag_roots = {"ragpipeline", "langchainlab"}
        project_roots = {"mlopsautomation", "aiopsintelligence"}

        bonus = 0.0

        if any(k in q_norm for k in ["llm", "거대언어모델", "언어모델", "생성형ai"]):
            if root in llm_roots:
                bonus += 0.12
            elif root in {"nlpspeechai", "speechttsstt"}:
                bonus -= 0.08

        if "rag" in q_norm or "벡터db" in q_norm or "임베딩" in q_norm:
            if root in rag_roots:
                bonus += 0.10
            elif root in {"speechttsstt"}:
                bonus -= 0.06

        if any(k in q_norm for k in ["devops", "mlops", "aiops", "llmops", "프로젝트"]):
            if root in project_roots:
                bonus += 0.16
            elif root in {"nlpspeechai", "speechttsstt"}:
                bonus -= 0.10

        if "학습내용" in q_norm or "무엇" in q_norm:
            if p.endswith(".md"):
                bonus += 0.05

        return bonus
