# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
REPORT_FILE = ROOT / "docs" / "curriculum_alignment_report.md"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


EXPECTED = OrderedDict(
    [
        (
            "Python 프로그래밍",
            {
                "hours": 40,
                "checks": [
                    ("기초 문법(상수/변수/함수/제어/반복)", ["상수", "변수", "함수", "조건문", "반복문"]),
                    ("객체지향 이해 및 프로그래밍", ["객체지향", "class", "__init__"]),
                ],
            },
        ),
        (
            "Python 전처리 및 시각화",
            {
                "hours": 40,
                "checks": [
                    ("Pandas/NumPy 전처리", ["pandas", "numpy", "전처리"]),
                    ("Matplotlib/Seaborn 시각화", ["matplotlib", "seaborn", "시각화"]),
                ],
            },
        ),
        (
            "머신러닝과 딥러닝",
            {
                "hours": 48,
                "checks": [
                    ("지도·비지도 및 예측/추론 기초", ["지도학습", "분류", "회귀", "예측"]),
                    ("신경망/딥러닝 모델 이해", ["신경망", "딥러닝", "모델"]),
                ],
            },
        ),
        (
            "자연어 및 음성 데이터 활용 및 모델 개발",
            {
                "hours": 96,
                "checks": [
                    ("자연어·음성 데이터 특성/전처리", ["자연어", "음성", "토큰", "오디오 전처리"]),
                    ("멀티모달/모델 검증·평가", ["멀티모달", "모델", "평가"]),
                ],
            },
        ),
        (
            "음성 데이터 활용한 TTS와 STT 모델 개발",
            {
                "hours": 64,
                "checks": [
                    ("음성 데이터 처리 이론·실습", ["음성", "stt", "tts", "라벨링", "전처리"]),
                    ("오픈소스 기반 음성 모델 학습", ["파이프라인", "학습", "튜닝"]),
                ],
            },
        ),
        (
            "거대 언어 모델을 활용한 자연어 생성",
            {
                "hours": 64,
                "checks": [
                    ("LLaMA/LLM 생성 실습", ["llm", "생성", "프롬프트", "요약"]),
                    ("Transformer 아키텍처 이해", ["토큰", "컨텍스트", "파라미터"]),
                ],
            },
        ),
        (
            "프롬프트 엔지니어링",
            {
                "hours": 40,
                "checks": [
                    ("답변 형식 최적화", ["프롬프트", "출력 포맷", "질문 구조화", "튜닝"]),
                ],
            },
        ),
        (
            "Langchain 활용하기",
            {
                "hours": 56,
                "checks": [
                    ("LangChain 프레임워크 이해", ["langchain", "chain", "prompttemplate"]),
                    ("DB/시스템 통합", ["vectorstore", "문서 로딩", "도구", "애플리케이션"]),
                ],
            },
        ),
        (
            "RAG(Retrieval-Augmented Generation)",
            {
                "hours": 52,
                "checks": [
                    ("검색 증강 생성 이해", ["rag", "문서 청크", "임베딩", "벡터db"]),
                    ("외부 데이터 연동 + 프롬프트 최적화", ["검색 품질", "프롬프트 결합", "출처화"]),
                ],
            },
        ),
    ]
)


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return rows


def build_subject_corpus(rows: list[dict[str, str]]) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for row in rows:
        subject = row["subject_name"]
        grouped.setdefault(subject, [])
        grouped[subject].append(row["module"])
        md_rel = (row.get("md_file") or "").strip()
        if md_rel:
            md_path = ROOT / md_rel
            if md_path.exists():
                grouped[subject].append(md_path.read_text(encoding="utf-8"))
    return {subject: "\n".join(parts).lower() for subject, parts in grouped.items()}


def evaluate() -> tuple[list[dict[str, str]], dict[str, int]]:
    rows = read_rows()
    corpus_by_subject = build_subject_corpus(rows)

    count_by_subject: dict[str, int] = {}
    for row in rows:
        count_by_subject[row["subject_name"]] = count_by_subject.get(row["subject_name"], 0) + 1

    results: list[dict[str, str]] = []
    for subject, expected in EXPECTED.items():
        corpus = corpus_by_subject.get(subject, "")
        actual_hours = count_by_subject.get(subject, 0)
        expected_hours = int(expected["hours"])
        hour_status = "PASS" if actual_hours == expected_hours else "WARN"

        check_statuses: list[str] = []
        check_details: list[str] = []
        for label, keywords in expected["checks"]:
            hits = [kw for kw in keywords if kw.lower() in corpus]
            ok = len(hits) >= max(1, len(keywords) // 2)
            check_statuses.append("PASS" if ok else "WARN")
            check_details.append(f"{label}: {', '.join(hits) if hits else '키워드 미탐지'}")

        overall = "PASS" if hour_status == "PASS" and all(s == "PASS" for s in check_statuses) else "WARN"
        results.append(
            {
                "subject": subject,
                "hours": f"{actual_hours}/{expected_hours} ({hour_status})",
                "status": overall,
                "details": " / ".join(check_details),
            }
        )

    summary = {
        "subjects": len(EXPECTED),
        "pass_count": sum(1 for row in results if row["status"] == "PASS"),
        "warn_count": sum(1 for row in results if row["status"] != "PASS"),
    }
    return results, summary


def render_report(results: list[dict[str, str]], summary: dict[str, int]) -> str:
    lines = [
        f"<!-- {COPYRIGHT_TEXT} -->",
        "# 교육과정 반영 점검 리포트",
        "",
        "- 기준: 사용자 첨부 커리큘럼 표(교과목/세부내용/훈련시간)",
        f"- 점검일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"- 과목 수: {summary['subjects']}",
        f"- PASS: {summary['pass_count']}",
        f"- WARN: {summary['warn_count']}",
        "",
        "| 교과목 | 시간 점검 | 반영 상태 | 세부 근거 |",
        "| --- | --- | --- | --- |",
    ]
    for row in results:
        lines.append(f"| {row['subject']} | {row['hours']} | {row['status']} | {row['details']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    results, summary = evaluate()
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(render_report(results, summary), encoding="utf-8", newline="\n")
    print(f"Report written: {REPORT_FILE}")
    print(f"PASS={summary['pass_count']} WARN={summary['warn_count']}")


if __name__ == "__main__":
    main()
