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
    query_expansions: list[str] | None = None


class QueryRouter:
    """Route question to structured handler or RAG search."""

    def __init__(self, curriculum_index: CurriculumIndex) -> None:
        self._index = curriculum_index

    def route(self, question: str) -> RoutedQuery:
        subject = self._index.detect_subject_in_question(question)
        class_id = self._extract_class_id(question)
        concept = self._extract_concept(question)
        expansions = self._build_query_expansions(question, concept)
        if concept and (concept.startswith("aws_") or self._is_definition_question(question)):
            return RoutedQuery(
                mode="concept_definition",
                subject_name=subject,
                class_id=class_id,
                concept=concept,
                query_expansions=expansions,
            )
        if subject and self._index.is_range_question(question):
            return RoutedQuery(
                mode="subject_range",
                subject_name=subject,
                class_id=class_id,
                concept=concept,
                query_expansions=expansions,
            )
        return RoutedQuery(mode="rag", subject_name=subject, class_id=class_id, concept=concept, query_expansions=expansions)

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
        if ("aws" in q or "아마존" in question) and any(k in q for k in ["stt", "transcribe", "speech", "음성"]):
            return "aws_stt"
        if ("aws" in q or "아마존" in question) and any(k in q for k in ["tts", "polly", "음성합성"]):
            return "aws_tts"
        if ("aws" in q or "아마존" in question) and any(k in q for k in ["번역", "translate", "다국어", "translation"]):
            return "aws_translate"
        if ("aws" in q or "아마존" in question) and any(k in q for k in ["요약", "summarize", "summary"]):
            return "aws_summarize"
        if ("aws" in q or "아마존" in question) and any(
            k in q for k in ["감정", "개체", "분석", "nlp", "comprehend", "sentiment", "entity"]
        ):
            return "aws_comprehend"
        return None

    @staticmethod
    def _build_query_expansions(question: str, concept: str | None) -> list[str]:
        q = question.lower()
        expansions: list[str] = []
        if concept == "aws_stt" or (
            ("aws" in q or "아마존" in question) and any(k in q for k in ["stt", "transcribe", "speech", "음성"])
        ):
            expansions.extend(
                [
                    "AWS STT Amazon Transcribe 실시간 배치 연동",
                    "음성 인식 speech to text aws transcribe",
                    "S3 Transcribe Streaming API Gateway Lambda ECS EKS",
                ]
            )
        if concept == "aws_tts" or (
            ("aws" in q or "아마존" in question) and any(k in q for k in ["tts", "polly", "음성합성"])
        ):
            expansions.extend(
                [
                    "AWS TTS Amazon Polly 음성 합성",
                    "텍스트 음성 변환 aws polly neural voice",
                    "S3 Polly Lambda API Gateway ECS EKS",
                ]
            )
        if concept == "aws_translate" or (
            ("aws" in q or "아마존" in question) and any(k in q for k in ["번역", "translate", "다국어", "translation"])
        ):
            expansions.extend(
                [
                    "AWS 번역 Amazon Translate 다국어",
                    "text translation aws translate",
                    "API Gateway Lambda ECS EKS translation pipeline",
                ]
            )
        if concept == "aws_summarize" or (
            ("aws" in q or "아마존" in question) and any(k in q for k in ["요약", "summarize", "summary"])
        ):
            expansions.extend(
                [
                    "AWS 요약 Amazon Bedrock summarize",
                    "LLM text summarization aws bedrock",
                    "S3 Bedrock Lambda ECS EKS summarization service",
                ]
            )
        if concept == "aws_comprehend" or (
            ("aws" in q or "아마존" in question)
            and any(k in q for k in ["감정", "개체", "분석", "nlp", "comprehend", "sentiment", "entity"])
        ):
            expansions.extend(
                [
                    "AWS NLP Amazon Comprehend sentiment entity keyphrase",
                    "텍스트 감정 분석 개체명 인식 aws comprehend",
                    "Comprehend API Gateway Lambda ECS EKS 분석 서비스",
                ]
            )
        return expansions

    @staticmethod
    def _is_definition_question(question: str) -> bool:
        q = question.replace(" ", "").lower()
        patterns = [
            r"뭔가요",
            r"무엇인가요",
            r"무엇인가",
            r"어떤리소스",
            r"무슨리소스",
            r"연동가능",
            r"설명",
            r"뜻",
            r"개념",
            r"정의",
            r"whatis",
        ]
        return any(re.search(p, q) for p in patterns)
