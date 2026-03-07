from __future__ import annotations

from dataclasses import dataclass
import re

from app.curriculum_service import CurriculumIndex


@dataclass
class RoutedQuery:
    mode: str
    subject_name: str | None = None
    class_id: str | None = None
    concept: str | None = None


class QueryRouter:
    """Route question to structured handler or RAG search."""

    def __init__(self, curriculum_index: CurriculumIndex) -> None:
        self._index = curriculum_index

    def route(self, question: str) -> RoutedQuery:
        subject = self._index.detect_subject_in_question(question)
        class_id = self._extract_class_id(question)
        concept = self._extract_concept(question)
        if concept and self._is_definition_question(question):
            return RoutedQuery(mode="concept_definition", subject_name=subject, class_id=class_id, concept=concept)
        if subject and self._index.is_range_question(question):
            return RoutedQuery(mode="subject_range", subject_name=subject, class_id=class_id, concept=concept)
        return RoutedQuery(mode="rag", subject_name=subject, class_id=class_id, concept=concept)

    @staticmethod
    def _extract_class_id(question: str) -> str | None:
        m = re.search(r"class\s*([0-9]{3})", question, flags=re.IGNORECASE)
        if not m:
            return None
        return f"class{m.group(1)}"

    @staticmethod
    def _extract_concept(question: str) -> str | None:
        q = question.lower()
        if "llm" in q or "거대 언어 모델" in question:
            return "llm"
        if "rag" in q:
            return "rag"
        if "langchain" in q or "랭체인" in question:
            return "langchain"
        if "프롬프트" in question:
            return "prompt"
        if "임베딩" in question:
            return "embedding"
        if "벡터" in question and "db" in q:
            return "vector_db"
        return None

    @staticmethod
    def _is_definition_question(question: str) -> bool:
        q = question.replace(" ", "").lower()
        patterns = [
            r"뭔가요",
            r"무엇인가요",
            r"무엇인가",
            r"설명",
            r"뜻",
            r"개념",
            r"정의",
            r"whatis",
        ]
        return any(re.search(p, q) for p in patterns)
