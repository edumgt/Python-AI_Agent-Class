from __future__ import annotations

import argparse
from pathlib import Path

from app.config import Settings
from app.rag_engine import RepoRAG


def run_ingestion(
    repo_root: str,
    db_path: str,
    collection: str,
    embed_dim: int,
    chunk_size: int,
    chunk_overlap: int,
    force: bool = False,
    skip_if_exists: bool = False,
) -> tuple[int, int, str]:
    rag = RepoRAG(
        db_path=Path(db_path),
        collection_name=collection,
        embed_dim=embed_dim,
    )

    if force:
        rag.reset()

    if skip_if_exists and rag.count() > 0:
        return 0, rag.count(), rag.collection_name

    indexed_files, indexed_chunks = rag.ingest(
        repo_root=Path(repo_root),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return indexed_files, indexed_chunks, rag.collection_name


def main() -> int:
    settings = Settings()

    parser = argparse.ArgumentParser(description="Repository RAG indexing")
    parser.add_argument("--repo-root", default=str(settings.repo_root))
    parser.add_argument("--db-path", default=str(settings.vector_db_path))
    parser.add_argument("--collection", default=settings.vector_collection)
    parser.add_argument("--embedding-dim", type=int, default=settings.embedding_dim)
    parser.add_argument("--chunk-size", type=int, default=settings.chunk_size)
    parser.add_argument("--chunk-overlap", type=int, default=settings.chunk_overlap)
    parser.add_argument("--force", action="store_true", help="Drop/recreate collection before ingest")
    parser.add_argument(
        "--skip-if-exists",
        action="store_true",
        help="Skip ingestion when collection already has documents",
    )
    args = parser.parse_args()

    indexed_files, indexed_chunks, collection = run_ingestion(
        repo_root=args.repo_root,
        db_path=args.db_path,
        collection=args.collection,
        embed_dim=args.embedding_dim,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        force=args.force,
        skip_if_exists=args.skip_if_exists,
    )

    print(f"collection={collection}")
    print(f"indexed_files={indexed_files}")
    print(f"indexed_chunks={indexed_chunks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
