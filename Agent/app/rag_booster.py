from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

import httpx


@dataclass
class RAGBoostResult:
    sources: list[dict[str, Any]]
    diagnostics: dict[str, Any]


class RAGBooster:
    def __init__(
        self,
        *,
        cohere_api_key: str,
        cohere_rerank_model: str,
        tavily_api_key: str,
        tavily_search_depth: str,
        tavily_topic: str,
        web_search_fallback_threshold: float,
    ) -> None:
        self._cohere_api_key = cohere_api_key.strip()
        self._cohere_rerank_model = cohere_rerank_model
        self._tavily_api_key = tavily_api_key.strip()
        self._tavily_search_depth = tavily_search_depth if tavily_search_depth in {"basic", "advanced"} else "advanced"
        self._tavily_topic = tavily_topic if tavily_topic in {"general", "news"} else "general"
        self._threshold = max(0.05, min(0.95, web_search_fallback_threshold))

    @property
    def capabilities(self) -> dict[str, bool]:
        return {
            "cohere_rerank": bool(self._cohere_api_key),
            "tavily_web_search": bool(self._tavily_api_key),
        }

    def enhance(
        self,
        *,
        question: str,
        local_sources: list[dict[str, Any]],
        top_k: int,
        use_web_search: bool,
        web_search_top_k: int,
        use_rerank: bool,
        rerank_provider: str,
    ) -> RAGBoostResult:
        normalized_local = [self._normalize_source(source, default_type="repo") for source in local_sources]
        diagnostics: dict[str, Any] = {
            "cohere_enabled": bool(self._cohere_api_key),
            "tavily_enabled": bool(self._tavily_api_key),
            "local_count": len(normalized_local),
            "web_count": 0,
            "used_web_search": False,
            "used_rerank": False,
            "rerank_provider": "none",
            "fallback_reason": "",
        }

        candidates = list(normalized_local)

        if use_rerank:
            reranked, rerank_info = self._rerank_sources(
                question=question,
                sources=candidates,
                top_n=max(top_k, len(candidates)),
                provider=rerank_provider,
            )
            candidates = reranked
            diagnostics["used_rerank"] = bool(rerank_info.get("used", False))
            diagnostics["rerank_provider"] = str(rerank_info.get("provider", "none"))
            if rerank_info.get("note"):
                diagnostics["fallback_reason"] = str(rerank_info["note"])

        best_local_score = max((float(s.get("score", 0.0)) for s in candidates), default=0.0)
        should_use_web = bool(use_web_search)

        if not should_use_web and self._tavily_api_key:
            if not candidates:
                should_use_web = True
                diagnostics["fallback_reason"] = diagnostics["fallback_reason"] or "no_local_sources"
            elif best_local_score < self._threshold:
                should_use_web = True
                diagnostics["fallback_reason"] = diagnostics["fallback_reason"] or f"low_local_score<{self._threshold:.2f}"

        web_sources: list[dict[str, Any]] = []
        if should_use_web and self._tavily_api_key:
            web_sources = self._tavily_search(question=question, max_results=max(1, min(10, web_search_top_k)))
            diagnostics["used_web_search"] = bool(web_sources)
            diagnostics["web_count"] = len(web_sources)

        merged = self._dedupe_sources(candidates + web_sources)

        if use_rerank and len(merged) > 1:
            reranked, rerank_info = self._rerank_sources(
                question=question,
                sources=merged,
                top_n=top_k,
                provider=rerank_provider,
            )
            merged = reranked
            diagnostics["used_rerank"] = diagnostics["used_rerank"] or bool(rerank_info.get("used", False))
            diagnostics["rerank_provider"] = str(rerank_info.get("provider", diagnostics["rerank_provider"]))
            if rerank_info.get("note") and not diagnostics["fallback_reason"]:
                diagnostics["fallback_reason"] = str(rerank_info["note"])

        merged.sort(key=lambda item: float(item.get("score", 0.0)), reverse=True)
        final_sources = merged[: max(1, top_k)]
        diagnostics["final_count"] = len(final_sources)

        return RAGBoostResult(sources=final_sources, diagnostics=diagnostics)

    def _rerank_sources(
        self,
        *,
        question: str,
        sources: list[dict[str, Any]],
        top_n: int,
        provider: str,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        chosen = (provider or "auto").strip().lower()
        if chosen in {"none", "off", "false"}:
            return sources[: max(1, top_n)], {"used": False, "provider": "none"}

        if self._cohere_api_key and chosen in {"auto", "cohere"}:
            try:
                reranked = self._rerank_with_cohere(question=question, sources=sources, top_n=top_n)
                return reranked, {"used": True, "provider": "cohere"}
            except Exception as exc:
                lexical = self._lexical_rerank(question=question, sources=sources)
                return lexical[: max(1, top_n)], {
                    "used": True,
                    "provider": "lexical",
                    "note": f"cohere_rerank_failed:{exc}",
                }

        lexical = self._lexical_rerank(question=question, sources=sources)
        return lexical[: max(1, top_n)], {"used": True, "provider": "lexical"}

    def _rerank_with_cohere(self, *, question: str, sources: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
        documents = [f"path={s.get('path','')}\n{s.get('chunk','')}" for s in sources]
        payload = {
            "model": self._cohere_rerank_model,
            "query": question,
            "documents": documents,
            "top_n": max(1, min(len(documents), top_n)),
            "return_documents": False,
        }
        headers = {
            "Authorization": f"Bearer {self._cohere_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        with httpx.Client(timeout=25.0) as client:
            resp = client.post("https://api.cohere.com/v2/rerank", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        ranked: list[dict[str, Any]] = []
        seen: set[int] = set()
        for item in data.get("results", []):
            idx = int(item.get("index", -1))
            if idx < 0 or idx >= len(sources):
                continue
            seen.add(idx)
            base = dict(sources[idx])
            score = float(item.get("relevance_score", base.get("score", 0.0)))
            base["score"] = max(0.0, min(1.0, score))
            base["provider"] = "cohere"
            ranked.append(base)

        for idx, source in enumerate(sources):
            if idx in seen:
                continue
            ranked.append(source)

        return ranked[: max(1, top_n)]

    def _tavily_search(self, *, question: str, max_results: int) -> list[dict[str, Any]]:
        payload = {
            "api_key": self._tavily_api_key,
            "query": question,
            "search_depth": self._tavily_search_depth,
            "topic": self._tavily_topic,
            "max_results": max(1, min(10, max_results)),
            "include_raw_content": False,
            "include_answer": False,
        }
        with httpx.Client(timeout=20.0) as client:
            resp = client.post("https://api.tavily.com/search", json=payload)
            resp.raise_for_status()
            data = resp.json()

        output: list[dict[str, Any]] = []
        for row in data.get("results", [])[:max_results]:
            url = str(row.get("url", "")).strip()
            title = str(row.get("title", "")).strip()
            content = str(row.get("content", "")).strip()
            if not url and not content:
                continue
            snippet = f"{title}\n{content}".strip()
            if len(snippet) > 1200:
                snippet = snippet[:1200] + "..."
            score = float(row.get("score", 0.55))
            output.append(
                {
                    "path": url or title or "web_result",
                    "score": max(0.0, min(1.0, score)),
                    "chunk": snippet,
                    "source_type": "web",
                    "provider": "tavily",
                }
            )
        return output

    @staticmethod
    def _lexical_rerank(question: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
        q_tokens = set(RAGBooster._tokenize(question))
        ranked: list[dict[str, Any]] = []
        for source in sources:
            chunk = str(source.get("chunk", ""))
            d_tokens = set(RAGBooster._tokenize(chunk))
            lexical = 0.0
            if q_tokens and d_tokens:
                lexical = len(q_tokens & d_tokens) / max(1, len(q_tokens))
            base = float(source.get("score", 0.0))
            merged = max(0.0, min(1.0, (base * 0.72) + (lexical * 0.28)))
            row = dict(source)
            row["score"] = merged
            if not row.get("provider"):
                row["provider"] = "lexical"
            ranked.append(row)
        ranked.sort(key=lambda item: float(item.get("score", 0.0)), reverse=True)
        return ranked

    @staticmethod
    def _normalize_source(source: dict[str, Any], default_type: str) -> dict[str, Any]:
        path = str(source.get("path", "")).strip()
        chunk = str(source.get("chunk", "")).strip()
        score = float(source.get("score", 0.0))
        source_type = str(source.get("source_type", default_type)).strip().lower() or default_type
        if source_type not in {"repo", "web"}:
            source_type = default_type
        provider = str(source.get("provider", "")).strip() or None

        normalized = dict(source)
        normalized["path"] = path
        normalized["chunk"] = chunk
        normalized["score"] = max(0.0, min(1.0, score))
        normalized["source_type"] = source_type
        normalized["provider"] = provider
        return normalized

    @staticmethod
    def _dedupe_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for source in sources:
            path = str(source.get("path", "")).strip()
            chunk = str(source.get("chunk", ""))[:220].strip()
            sig = (path, chunk)
            if sig in seen:
                continue
            seen.add(sig)
            out.append(source)
        return out

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [token for token in re.findall(r"[0-9a-zA-Z가-힣_]+", (text or "").lower()) if len(token) >= 2]
