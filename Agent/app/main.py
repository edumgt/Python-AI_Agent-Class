from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.agent_service import QnaAgent
from app.config import settings
from app.curriculum_service import CurriculumIndex
from app.ingest import run_ingestion
from app.query_router import QueryRouter
from app.rag_engine import RepoRAG
from app.schemas import AskRequest, AskResponse, ReindexResponse, SourceItem

app = FastAPI(title="Curriculum RAG Agent", version="1.0.0")
STATIC_DIR = Path(__file__).resolve().parent / "static"

rag = RepoRAG(
    db_path=settings.vector_db_path,
    collection_name=settings.vector_collection,
    embed_dim=settings.embedding_dim,
)
agent = QnaAgent()
curriculum = CurriculumIndex(repo_root=settings.repo_root)
router = QueryRouter(curriculum_index=curriculum)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "collection": rag.collection_name,
        "documents": rag.count(),
        "curriculum_index": curriculum.index_path,
    }


@app.post("/v1/reindex", response_model=ReindexResponse)
def reindex(force: bool = True) -> ReindexResponse:
    indexed_files, indexed_chunks, collection = run_ingestion(
        repo_root=str(settings.repo_root),
        db_path=str(settings.vector_db_path),
        collection=settings.vector_collection,
        embed_dim=settings.embedding_dim,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        force=force,
        skip_if_exists=False,
    )
    curriculum.reload()
    return ReindexResponse(
        indexed_files=indexed_files,
        indexed_chunks=indexed_chunks,
        collection=collection,
    )


@app.post("/v1/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    routed = router.route(question)

    if routed.mode == "concept_definition" and routed.concept:
        answer = curriculum.answer_concept_definition(routed.concept)
        if answer:
            return AskResponse(
                answer=answer,
                sources=[
                    SourceItem(
                        path="curriculum_index.csv",
                        score=1.0,
                        chunk="개념형 질문은 구조화 Glossary + curriculum_index.csv 범위 매핑으로 응답합니다.",
                    )
                ],
                mode="concept_definition",
                matched_subject=routed.subject_name,
                matched_class_id=routed.class_id,
            )

    if routed.mode == "subject_range" and routed.subject_name:
        answer = curriculum.answer_subject_range(routed.subject_name)
        if answer:
            source_line = "과목 범위 매핑은 curriculum_index.csv의 class/day/subject_name 컬럼 기준으로 계산됩니다."
            return AskResponse(
                answer=answer,
                sources=[
                    SourceItem(
                        path="curriculum_index.csv",
                        score=1.0,
                        chunk=source_line,
                    )
                ],
                mode="subject_range",
                matched_subject=routed.subject_name,
                matched_class_id=routed.class_id,
            )

    if routed.class_id:
        class_sources = curriculum.class_local_search(
            class_id=routed.class_id,
            question=question,
            top_k=payload.top_k or settings.default_top_k,
        )
        if class_sources:
            class_subject = routed.subject_name or curriculum.class_subject(routed.class_id)
            class_answer = curriculum.answer_class_scoped(
                class_id=routed.class_id,
                question=question,
                sources=class_sources,
            )
            return AskResponse(
                answer=class_answer or "",
                sources=[SourceItem(path=s["path"], score=s["score"], chunk=s["chunk"]) for s in class_sources],
                mode="class_scoped",
                matched_subject=class_subject,
                matched_class_id=routed.class_id,
            )

    if rag.count() == 0:
        run_ingestion(
            repo_root=str(settings.repo_root),
            db_path=str(settings.vector_db_path),
            collection=settings.vector_collection,
            embed_dim=settings.embedding_dim,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            force=False,
            skip_if_exists=False,
        )

    sources = rag.query(
        question=question,
        top_k=payload.top_k or settings.default_top_k,
        class_hint=routed.class_id,
    )
    answer = agent.answer(
        question=question,
        sources=sources,
        use_llm=payload.use_llm,
        mode="rag",
    )

    return AskResponse(
        answer=answer,
        sources=[SourceItem(path=s["path"], score=s["score"], chunk=s["chunk"]) for s in sources],
        mode="rag",
        matched_subject=routed.subject_name,
        matched_class_id=routed.class_id,
    )
