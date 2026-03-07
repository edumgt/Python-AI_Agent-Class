# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
TIERS = ("basic", "advanced", "challenge")
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


TRACK_TIPS = {
    "python": {
        "kid_point": "작은 규칙을 코드로 바꾸는 연습을 해요.",
        "core_hint": "입력 -> 처리 -> 출력 흐름을 먼저 종이에 써 보고 코드를 작성하세요.",
        "debug_hint": "print()로 중간 값을 찍어 보면 대부분의 실수를 바로 찾을 수 있어요.",
    },
    "data": {
        "kid_point": "표 데이터를 정리해서 의미를 찾는 연습을 해요.",
        "core_hint": "열 이름을 먼저 확인하고, 어떤 숫자를 계산할지 순서를 정하세요.",
        "debug_hint": "shape/columns를 출력하면 데이터 구조 오류를 빠르게 찾을 수 있어요.",
    },
    "ml": {
        "kid_point": "데이터에서 규칙을 찾는 모델 사고를 연습해요.",
        "core_hint": "입력(X)과 정답(y)의 형태를 먼저 확인하고 학습 함수를 호출하세요.",
        "debug_hint": "오차(MSE/MAE)가 너무 크면 입력 스케일/분할 방식을 먼저 점검하세요.",
    },
    "nlp": {
        "kid_point": "문장을 토큰으로 나누고 패턴을 찾는 연습을 해요.",
        "core_hint": "정제 -> 토큰화 -> 집계 순서를 고정하면 코드가 깔끔해져요.",
        "debug_hint": "토큰 리스트를 먼저 출력해 전처리 결과를 눈으로 확인하세요.",
    },
    "speech": {
        "kid_point": "음성 데이터를 규칙적으로 다루는 연습을 해요.",
        "core_hint": "파일/길이/라벨 같은 필수 항목이 있는지 먼저 확인하세요.",
        "debug_hint": "샘플 3개만 먼저 출력해서 형식이 맞는지 검증하세요.",
    },
    "prompt": {
        "kid_point": "좋은 질문 구조를 만들어 더 좋은 답을 얻는 연습을 해요.",
        "core_hint": "역할(role)과 질문(question)을 분리해 템플릿으로 만드세요.",
        "debug_hint": "렌더링된 프롬프트 문자열을 출력해 누락 변수가 없는지 확인하세요.",
    },
    "langchain": {
        "kid_point": "작은 단계를 연결해 큰 작업을 만드는 연습을 해요.",
        "core_hint": "단계 함수의 입력/출력을 명확히 분리하면 체인이 안정적이에요.",
        "debug_hint": "각 단계 결과를 한 줄씩 출력하면 어디서 실패하는지 바로 보여요.",
    },
    "rag": {
        "kid_point": "자료를 찾고 근거로 답을 만드는 연습을 해요.",
        "core_hint": "검색 결과와 최종 답변을 분리해서 출력하세요.",
        "debug_hint": "유사도 점수와 선택 문서 id를 출력하면 검색 품질을 점검하기 쉬워요.",
    },
    "generic": {
        "kid_point": "문제를 작은 단계로 나눠 해결하는 연습을 해요.",
        "core_hint": "한 번에 다 구현하지 말고 TODO를 1개씩 완료하세요.",
        "debug_hint": "오류가 나면 최근에 수정한 5줄을 먼저 다시 읽어 보세요.",
    },
}


def choose_track(subject_name: str, module: str) -> str:
    text = f"{subject_name} {module}"
    lowered = text.lower()
    if "rag" in lowered or "retrieval-augmented generation" in lowered:
        return "rag"
    if "langchain" in lowered:
        return "langchain"
    if any(keyword in text for keyword in ["프롬프트", "LLM", "언어모델", "생성 파라미터", "응답 설계"]):
        return "prompt"
    if any(keyword in text for keyword in ["음성", "TTS", "STT", "오디오", "발화", "화자"]):
        return "speech"
    if any(keyword in text for keyword in ["자연어", "NLP", "텍스트", "토큰", "임베딩", "시퀀스"]):
        return "nlp"
    if any(keyword in text for keyword in ["머신러닝", "딥러닝", "회귀", "분류", "모델", "학습", "MSE"]):
        return "ml"
    if any(keyword in text for keyword in ["전처리", "시각화", "데이터프레임", "pandas", "numpy"]):
        return "data"
    if "python" in lowered:
        return "python"
    return "generic"


def tier_text(tier: str) -> tuple[str, str, str]:
    if tier == "basic":
        return (
            "Basic(입문)",
            "핵심 TODO를 완성해서 코드가 끝까지 실행되게 만들기",
            "TODO 한 칸을 채울 때마다 바로 실행해서 확인하세요.",
        )
    if tier == "advanced":
        return (
            "Advanced(심화)",
            "입력 검증/구조화/결과 저장까지 포함한 실무형 코드로 확장하기",
            "기본 동작을 유지하면서 예외 처리와 결과 구조를 추가하세요.",
        )
    return (
        "Challenge(챌린지)",
        "리팩토링, 자체 테스트, 성능 확인까지 포함한 완성형으로 발전시키기",
        "함수 분리 -> assert 테스트 -> 성능 로그 순서로 진행하세요.",
    )


def build_docstring(row: dict[str, str], tier: str, track: str) -> str:
    class_id = row["class"]
    subject_name = row["subject_name"]
    module = row["module"]
    day = int(row["day"])
    slot = int(row["slot"])
    level = row["level"]

    tier_label, goal_text, process_tip = tier_text(tier)
    tips = TRACK_TIPS[track]

    doc = f'''
"""
{class_id} {tier_label} 과제 (자기주도 학습용)

[학습 정보]
- 교과목: {subject_name}
- 주제: {module}
- 일정: Day {day:02d} / {slot}교시
- 난이도: {level}

[이번 과제 목표]
- {goal_text}
- 초등학생도 혼자 따라갈 수 있도록, 작은 단계로 나눠서 완성하기

[환경 구성 - Windows PowerShell]
1) cd C:\\DevOps\\Python-AI_Agent-Class
2) python -m venv .venv
3) .\\.venv\\Scripts\\Activate.ps1
4) python -m pip install --upgrade pip
5) pip install -r requirements.txt

[환경 구성 - Linux/macOS (bash)]
1) cd /path/to/Python-AI_Agent-Class
2) python3 -m venv .venv
3) source .venv/bin/activate
4) python -m pip install --upgrade pip
5) pip install -r requirements.txt

[실행 방법]
- python {class_id}/{class_id}_assignment_{tier}.py

[쉬운 학습 포인트]
- {tips["kid_point"]}
- {tips["core_hint"]}

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- {tips["debug_hint"]}
- {process_tip}
"""
'''
    return dedent(doc).strip() + "\n"


def replace_leading_docstring(path: Path, new_docstring: str) -> bool:
    original = path.read_text(encoding="utf-8")
    bom = "\ufeff" if original.startswith("\ufeff") else ""
    text = original[len(bom) :]
    notice_line = f"# {COPYRIGHT_TEXT}"

    body = text
    # Clean any repeated notice/docstring blocks at file head.
    while True:
        changed = False
        if body.startswith(notice_line):
            body = body[len(notice_line) :].lstrip("\r\n")
            changed = True
        if body.startswith('"""') or body.startswith("'''"):
            quote = body[:3]
            end = body.find(quote, 3)
            if end != -1:
                body = body[end + 3 :].lstrip("\r\n")
                changed = True
        if not changed:
            break

    updated = bom + notice_line + "\n" + new_docstring + "\n\n" + body
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return rows


def rebuild_assignment_guides() -> None:
    rows = read_rows()
    updated_count = 0
    missing_count = 0

    for row in rows:
        class_id = row["class"]
        track = choose_track(row["subject_name"], row["module"])
        class_dir = ROOT / class_id

        for tier in TIERS:
            path = class_dir / f"{class_id}_assignment_{tier}.py"
            if not path.exists():
                missing_count += 1
                continue
            new_doc = build_docstring(row=row, tier=tier, track=track)
            replace_leading_docstring(path, new_doc)
            updated_count += 1

    print(f"Updated assignment guides: {updated_count}")
    print(f"Missing files: {missing_count}")


if __name__ == "__main__":
    rebuild_assignment_guides()
