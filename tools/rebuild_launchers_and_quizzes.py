# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

import csv
from functools import lru_cache
import json
import random
import re
from pathlib import Path
from textwrap import dedent
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


TRACK_QUIZ_BANK = {
    "python": {
        "concept": "입력값을 조건문과 반복문으로 처리해 원하는 출력으로 만든다.",
        "action": "작은 입력부터 실행하고 print()로 중간 값을 확인한다.",
        "pitfall": "입력 경계값(0, 빈 문자열, 음수)을 테스트하지 않고 예시 1개만 확인한다.",
        "check": "같은 로직을 최소 3개 입력으로 실행하고 조건 분기가 모두 동작하는지 확인한다.",
        "outcome": "함수로 코드를 분리해 재사용성과 가독성을 높인다.",
    },
    "data": {
        "concept": "데이터 전처리로 열 구조를 정리한 뒤 통계를 계산한다.",
        "action": "columns와 shape를 먼저 확인하고 계산 순서를 정한다.",
        "pitfall": "결측치/자료형을 확인하지 않은 채 평균과 시각화를 바로 계산한다.",
        "check": "전처리 전후 행 수, 결측치 개수, 핵심 통계를 비교표로 남긴다.",
        "outcome": "정리된 표 데이터로 의미 있는 패턴을 설명할 수 있다.",
    },
    "ml": {
        "concept": "입력(X)과 정답(y)을 사용해 예측 규칙(모델)을 학습한다.",
        "action": "X/y 형태를 점검하고 오차를 계산해 품질을 확인한다.",
        "pitfall": "학습 데이터와 평가 데이터를 섞어 과대평가된 점수를 믿는다.",
        "check": "훈련/검증 분리를 유지하고 오차 지표(MSE/정확도)를 함께 기록한다.",
        "outcome": "예측 결과와 오차를 해석해 개선 아이디어를 낼 수 있다.",
    },
    "nlp": {
        "concept": "문장을 정제하고 토큰으로 나눠 패턴을 분석한다.",
        "action": "전처리 후 토큰 리스트를 먼저 출력해 결과를 점검한다.",
        "pitfall": "불용어/특수문자 정제를 생략해 토큰 빈도 해석을 왜곡한다.",
        "check": "전처리 전후 토큰 샘플을 비교하고 빈도 변화 이유를 설명한다.",
        "outcome": "주요 단어 빈도를 계산해 핵심 내용을 찾을 수 있다.",
    },
    "speech": {
        "concept": "음성 데이터는 길이, 텍스트 라벨, 품질 정보를 함께 다룬다.",
        "action": "샘플 발화를 몇 개 확인하고 길이/라벨 기준으로 필터링한다.",
        "pitfall": "오디오 길이와 라벨 품질을 확인하지 않아 학습 데이터 잡음이 증가한다.",
        "check": "샘플 청취와 라벨 점검 후 길이/잡음 기준 필터링 로그를 남긴다.",
        "outcome": "음성 데이터 품질 지표를 계산하고 해석할 수 있다.",
    },
    "prompt": {
        "concept": "역할(role), 목표(goal), 형식(format)을 분명히 써야 답변 품질이 오른다.",
        "action": "템플릿 변수(role, question)를 분리해 프롬프트를 구성한다.",
        "pitfall": "역할, 목표, 출력형식을 섞어 써서 재현 불가능한 응답을 만든다.",
        "check": "같은 질문을 2회 이상 실행해 형식 일관성과 누락 항목을 점검한다.",
        "outcome": "좋은 프롬프트와 나쁜 프롬프트의 차이를 설명할 수 있다.",
    },
    "langchain": {
        "concept": "작업을 단계별 체인으로 분리하면 재사용과 디버깅이 쉬워진다.",
        "action": "각 단계의 입력/출력을 출력해 흐름을 먼저 검증한다.",
        "pitfall": "체인 단계를 한 번에 묶어 디버깅 지점을 확인하지 못한다.",
        "check": "각 단계 입력/출력 스냅샷을 저장해 실패 지점을 단계별로 추적한다.",
        "outcome": "단계 함수를 조합해 반복 가능한 워크플로우를 만들 수 있다.",
    },
    "rag": {
        "concept": "질문과 관련 문서를 검색하고 근거를 바탕으로 답변을 만든다.",
        "action": "검색 결과와 최종 답변을 분리해서 출력한다.",
        "pitfall": "검색 근거 없이 모델 답변만 채택해 환각을 놓친다.",
        "check": "답변 문장별로 근거 문서와 출처를 매핑해 근거 없는 문장을 표시한다.",
        "outcome": "답변에 출처를 포함해 신뢰도를 높일 수 있다.",
    },
    "generic": {
        "concept": "복잡한 문제를 작은 단계로 나누면 해결이 쉬워진다.",
        "action": "TODO를 1개씩 구현하고 매 단계마다 실행 확인한다.",
        "pitfall": "요구사항을 분해하지 않고 코드를 길게 작성해 오류 원인을 숨긴다.",
        "check": "작업을 TODO 단위로 나누고 단계별 성공 조건을 체크리스트로 검증한다.",
        "outcome": "문제를 구조화해 스스로 학습 흐름을 만들 수 있다.",
    },
}


PYTHON_PL_QUIZ_BANK = {
    "오리엔테이션 및 개발환경 준비": {
        "concept": "인터프리터·가상환경·의존성 고정은 실행 재현성의 기본이다.",
        "action": "`python --version`, `where python`, `.venv` 활성화 상태를 먼저 확인한다.",
        "pitfall": "전역 Python과 가상환경 Python을 섞어 패키지 설치 경로가 꼬인다.",
        "check": "`sys.executable` 경로가 프로젝트 `.venv`를 가리키는지 확인하고 샘플 import 테스트를 통과한다.",
        "outcome": "실습 환경을 스스로 재현하고 환경 이슈를 분리해 해결할 수 있다.",
    },
    "변수와 자료형": {
        "concept": "변수/상수 관례/타입/배열(list) 모델을 구분해 데이터를 안전하게 다룬다.",
        "action": "값을 할당한 뒤 `type()`과 `isinstance()`로 타입 가정을 즉시 검증한다.",
        "pitfall": "문자열 숫자를 정수로 변환하지 않아 연산 결과가 의도와 달라진다.",
        "check": "변수·상수·list를 포함한 예제를 만들고 경계 인덱스까지 테스트한다.",
        "outcome": "PL 기초 데이터 모델(바인딩·타입·배열)을 코드로 설명할 수 있다.",
    },
    "연산자와 조건문": {
        "concept": "연산자와 조건식은 불리언 평가를 통해 분기 경로를 결정한다.",
        "action": "조건식을 괄호로 명확히 하고 경계값 입력으로 각 분기 결과를 확인한다.",
        "pitfall": "연산자 우선순위를 오해해 의도와 다른 조건 분기가 실행된다.",
        "check": "`if/elif/else`의 모든 경로를 최소 1회 이상 실행해 분기 누락이 없는지 확인한다.",
        "outcome": "표현식과 분기 로직을 예측 가능하게 설계할 수 있다.",
    },
    "반복문과 흐름제어": {
        "concept": "for/while 반복과 흐름제어문은 시퀀스 처리 성능과 정확도를 좌우한다.",
        "action": "반복 변수와 누적 변수 변화를 `print()`로 추적하며 루프를 검증한다.",
        "pitfall": "종료 조건이 약해 무한 루프 또는 누락 집계가 발생한다.",
        "check": "`break/continue` 유무에 따른 결과 차이를 비교하고 종료 조건을 문서화한다.",
        "outcome": "반복 처리 로직을 안정적으로 설계하고 디버깅할 수 있다.",
    },
    "함수와 모듈": {
        "concept": "함수 시그니처와 모듈 분리는 재사용성과 테스트 가능성을 높인다.",
        "action": "중복 코드를 함수로 추출하고 입력·출력 계약을 먼저 정의한다.",
        "pitfall": "전역 상태에 의존해 함수 재사용 시 부작용이 발생한다.",
        "check": "함수별 정상/경계 테스트를 수행하고 다른 모듈에서 import 실행을 확인한다.",
        "outcome": "책임 분리된 함수·모듈 구조로 코드를 확장할 수 있다.",
    },
    "컬렉션 자료구조": {
        "concept": "list/tuple/dict/set 선택은 데이터 접근 패턴과 연산 효율을 결정한다.",
        "action": "동일 데이터를 여러 컬렉션으로 표현해 조회·수정 패턴을 비교한다.",
        "pitfall": "가변 객체 공유(얕은 복사)를 놓쳐 예상치 못한 동시 변경이 발생한다.",
        "check": "컬렉션별 장단점을 근거로 구조 선택 이유를 설명하고 컴프리헨션 결과를 검증한다.",
        "outcome": "문제 특성에 맞는 자료구조를 선택해 코드 품질을 높일 수 있다.",
    },
    "파일 입출력": {
        "concept": "파일 입출력은 경로·모드·인코딩·직렬화 규칙을 함께 다뤄야 안전하다.",
        "action": "`with open(..., encoding='utf-8')`으로 읽기/쓰기 후 재로드 검증을 수행한다.",
        "pitfall": "인코딩이나 파일 모드를 명시하지 않아 데이터가 깨지거나 누락된다.",
        "check": "저장 전후 데이터 동등성 확인과 파일 예외 케이스(미존재/권한)를 점검한다.",
        "outcome": "영속 데이터 처리 파이프라인을 안정적으로 구현할 수 있다.",
    },
    "예외처리와 디버깅": {
        "concept": "예외처리는 정상 경로와 실패 경로를 분리해 프로그램 복원력을 높인다.",
        "action": "오류를 재현한 뒤 traceback 라인 기준으로 원인을 좁히고 `try/except`를 적용한다.",
        "pitfall": "광범위한 `except Exception`으로 원인을 숨겨 디버깅 정보를 잃는다.",
        "check": "예외 타입별 처리 정책을 분리하고 회귀 테스트로 재발 방지를 확인한다.",
        "outcome": "디버깅 근거를 남기며 안정적인 오류 처리 코드를 작성할 수 있다.",
    },
    "객체지향 기초": {
        "concept": "클래스는 상태와 동작을 캡슐화해 복잡한 도메인을 모델링한다.",
        "action": "핵심 개체를 클래스화하고 `__init__`·메서드·상태 전이를 테스트한다.",
        "pitfall": "책임이 다른 로직을 한 클래스에 몰아 결합도가 과도해진다.",
        "check": "객체 생성/메서드 호출 전후 상태 불변식을 검증하고 필요 시 상속을 최소 적용한다.",
        "outcome": "클래스 설계 원칙으로 확장 가능한 구조를 만들 수 있다.",
    },
    "미니 실습 프로젝트": {
        "concept": "프로젝트는 변수·함수·클래스·예외처리를 통합한 PL 종합 적용 단계다.",
        "action": "요구사항을 TODO로 분해하고 최소 기능부터 구현 후 반복 개선한다.",
        "pitfall": "설계 없이 구현부터 시작해 모듈 경계와 테스트 전략이 무너진다.",
        "check": "핵심 시나리오 테스트를 통과하고 리팩터링 전후 동작 동일성을 확인한다.",
        "outcome": "작동하는 프로그램을 구조적으로 완성하고 개선 루프를 운영할 수 있다.",
    },
}


def resolve_quiz_bank(subject_name: str, module: str, track: str) -> dict[str, str]:
    if subject_name.strip() == "Python 프로그래밍":
        module_bank = PYTHON_PL_QUIZ_BANK.get(module)
        if module_bank:
            return module_bank
    return TRACK_QUIZ_BANK[track]


class LearningPoints(TypedDict):
    summary: str
    concepts: list[str]
    missions: list[str]
    checklist: list[str]


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))

    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return rows


def class_dir_from_row(row: dict[str, str]) -> Path:
    md_rel = (row.get("md_file") or "").strip()
    if md_rel:
        md_path = ROOT / Path(md_rel)
        if md_path.name:
            return md_path.parent
    return ROOT / row["class"]


def choose_track(subject_name: str, module: str) -> str:
    text = f"{subject_name} {module}"
    lowered = text.lower()
    if "mlops" in lowered or "모델 레지스트리" in text or "배포 자동화" in text:
        return "ml"
    if "aiops" in lowered or "관측 데이터" in text or "이상탐지" in text or "runbook" in lowered:
        return "data"
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


def parse_session_order(subject_session: str) -> int:
    raw = subject_session.split("/", maxsplit=1)[0].strip()
    if raw.isdigit():
        return int(raw)
    return 0


def clean_learning_line(line: str) -> str:
    cleaned = line.strip()
    cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
    cleaned = re.sub(r"^- \[[ xX]\]\s*", "", cleaned)
    cleaned = re.sub(r"^-\s*", "", cleaned)
    return cleaned.strip()


@lru_cache(maxsize=None)
def load_learning_points(md_rel_path: str) -> LearningPoints:
    empty: LearningPoints = {
        "summary": "",
        "concepts": [],
        "missions": [],
        "checklist": [],
    }
    if not md_rel_path:
        return empty

    md_path = ROOT / md_rel_path
    if not md_path.exists():
        return empty

    summary = ""
    concepts: list[str] = []
    missions: list[str] = []
    checklist: list[str] = []
    section = ""

    with md_path.open(encoding="utf-8") as fp:
        for raw in fp:
            line = raw.strip()
            if not line:
                continue

            if line.startswith("- 한 줄 설명:"):
                summary = line.split(":", maxsplit=1)[1].strip()
                continue

            if line.startswith("### 핵심 개념 3가지"):
                section = "concepts"
                continue
            if line.startswith("### 실습 미션"):
                section = "missions"
                continue
            if line.startswith("## 8) 스스로 점검 체크리스트"):
                section = "checklist"
                continue
            if line.startswith("## "):
                section = ""
                continue

            if section in {"concepts", "missions"} and re.match(r"^\d+\.\s+", line):
                normalized = clean_learning_line(line)
                if normalized:
                    if section == "concepts":
                        concepts.append(normalized)
                    else:
                        missions.append(normalized)
                continue

            if section == "checklist" and line.startswith("- [ ]"):
                normalized = clean_learning_line(line)
                if normalized:
                    checklist.append(normalized)

    return {
        "summary": summary,
        "concepts": concepts,
        "missions": missions,
        "checklist": checklist,
    }


def merge_candidates(*pools: list[str]) -> list[str]:
    merged: list[str] = []
    for pool in pools:
        for item in pool:
            text = item.strip()
            if text and text not in merged:
                merged.append(text)
    return merged


def ensure_min_candidates(primary: list[str], fallback: list[str], minimum: int = 4) -> list[str]:
    candidates = merge_candidates(primary)
    if len(candidates) >= minimum:
        return candidates

    for item in fallback:
        text = item.strip()
        if text and text not in candidates:
            candidates.append(text)
            if len(candidates) >= minimum:
                break
    return candidates


def class_focus_point(row: dict[str, str]) -> str:
    points = load_learning_points(row.get("md_file", ""))
    module = row["module"]
    for text in points["missions"] + points["concepts"]:
        if text:
            return f"{module} 실습: {text}"
    if points["summary"]:
        return f"{module} 핵심: {points['summary']}"
    return f"{module} 학습 절차를 순서대로 설명할 수 있다."


def class_check_point(row: dict[str, str]) -> str:
    points = load_learning_points(row.get("md_file", ""))
    module = row["module"]
    for text in points["checklist"]:
        if text:
            return f"{module} 점검: {text}"

    track = choose_track(row["subject_name"], row["module"])
    bank = resolve_quiz_bank(subject_name=row["subject_name"], module=row["module"], track=track)
    return f"{module} 점검: {bank['check']}"


def find_prev_next_modules(current: dict[str, str], same_subject_rows: list[dict[str, str]]) -> tuple[str | None, str | None]:
    ordered = sorted(
        same_subject_rows,
        key=lambda item: (parse_session_order(item["subject_session"]), item["class"]),
    )

    current_index = next((i for i, item in enumerate(ordered) if item["class"] == current["class"]), -1)
    if current_index < 0:
        return None, None

    prev_module: str | None = None
    for i in range(current_index - 1, -1, -1):
        candidate = ordered[i]["module"]
        if candidate != current["module"]:
            prev_module = candidate
            break

    next_module: str | None = None
    for i in range(current_index + 1, len(ordered)):
        candidate = ordered[i]["module"]
        if candidate != current["module"]:
            next_module = candidate
            break

    return prev_module, next_module


def stable_sample(pool: list[str], k: int, seed: str) -> list[str]:
    unique = list(dict.fromkeys(pool))
    if len(unique) < k:
        return unique
    rng = random.Random(seed)
    return rng.sample(unique, k)


def build_question(
    question: str,
    correct: str,
    candidates: list[str],
    seed: str,
    explanation: str,
) -> dict:
    distractors = stable_sample([x for x in candidates if x != correct], 3, seed)
    options = [correct] + distractors
    rng = random.Random(seed + "-shuffle")
    rng.shuffle(options)
    return {
        "question": question,
        "options": options,
        "answer_index": options.index(correct),
        "explanation": explanation,
    }


def build_quiz_payload(row: dict[str, str], rows: list[dict[str, str]]) -> dict:
    class_id = row["class"]
    subject_name = row["subject_name"]
    module = row["module"]
    level = row["level"]
    day = int(row["day"])
    slot = int(row["slot"])
    session = row["subject_session"]
    track = choose_track(subject_name, module)
    bank = resolve_quiz_bank(subject_name=subject_name, module=module, track=track)

    same_subject_rows = [r for r in rows if r["subject_name"] == subject_name]
    same_subject_modules = [r["module"] for r in same_subject_rows]
    prev_module, next_module = find_prev_next_modules(row, same_subject_rows)

    all_banks = [
        resolve_quiz_bank(
            subject_name=candidate["subject_name"],
            module=candidate["module"],
            track=choose_track(candidate["subject_name"], candidate["module"]),
        )
        for candidate in rows
    ]
    all_concepts = [candidate_bank["concept"] for candidate_bank in all_banks]
    all_actions = [candidate_bank["action"] for candidate_bank in all_banks]
    all_pitfalls = [candidate_bank["pitfall"] for candidate_bank in all_banks]
    all_checks = [candidate_bank["check"] for candidate_bank in all_banks]

    subject_focus_points = [class_focus_point(r) for r in same_subject_rows]
    all_focus_points = [class_focus_point(r) for r in rows]
    focus_point = class_focus_point(row)
    focus_candidates = ensure_min_candidates(
        subject_focus_points,
        merge_candidates(all_focus_points, all_concepts),
        minimum=6,
    )

    subject_check_points = [class_check_point(r) for r in same_subject_rows]
    all_check_points = [class_check_point(r) for r in rows]
    check_point = class_check_point(row)
    check_candidates = ensure_min_candidates(
        subject_check_points,
        merge_candidates(all_check_points, all_checks),
        minimum=6,
    )
    module_candidates = ensure_min_candidates(same_subject_modules, [r["module"] for r in rows], minimum=6)

    questions = [
        build_question(
            question=f"{class_id} ({subject_name} {session}) 차시의 실제 학습 주제는 무엇인가요?",
            correct=module,
            candidates=module_candidates,
            seed=f"{class_id}-q1-module",
            explanation=f"정답은 '{module}' 입니다. 이전 모듈은 '{prev_module or '없음'}', 다음 모듈은 '{next_module or '없음'}' 입니다.",
        ),
        build_question(
            question=f"'{module}' 차시의 실제 실습 목표를 가장 구체적으로 설명한 문장은 무엇인가요?",
            correct=focus_point,
            candidates=focus_candidates,
            seed=f"{class_id}-q2-focus",
            explanation="정답은 해당 차시 MD의 핵심 개념/실습 미션에서 직접 가져온 문장입니다.",
        ),
        build_question(
            question=f"'{module}' 실습에서 오류를 줄이는 시작 전략으로 가장 적절한 것은 무엇인가요?",
            correct=bank["action"],
            candidates=all_actions,
            seed=f"{class_id}-q3-action",
            explanation="정답은 실행 흐름을 먼저 검증하는 고효율 시작 루틴입니다.",
        ),
        build_question(
            question=f"'{module}' 실습 결과를 왜곡할 가능성이 가장 큰 실수는 무엇인가요?",
            correct=bank["pitfall"],
            candidates=all_pitfalls,
            seed=f"{class_id}-q4-pitfall",
            explanation="정답은 현장에서 자주 발생하는 품질 저하 패턴입니다.",
        ),
        build_question(
            question=f"'{module}'를 끝낸 직후, 다음 학습 단계로 넘어가기 전 자기 점검 항목으로 가장 적절한 것은 무엇인가요?",
            correct=check_point,
            candidates=check_candidates,
            seed=f"{class_id}-q5-check",
            explanation=f"이 차시는 '{bank['check']}' 관점으로 검증해야 다음 단계로 안정적으로 연결됩니다.",
        ),
    ]

    return {
        "class_id": class_id,
        "subject_name": subject_name,
        "module": module,
        "level": level,
        "session": session,
        "track_outcome": bank["outcome"],
        "questions": questions,
        "question_count": len(questions),
        "day": day,
        "slot": slot,
    }


def build_quiz_html(row: dict[str, str], rows: list[dict[str, str]]) -> str:
    payload = build_quiz_payload(row, rows)
    quiz_json = json.dumps(payload, ensure_ascii=False, indent=2)
    class_id = payload["class_id"]
    module = payload["module"]
    subject_name = payload["subject_name"]
    session = payload["session"]
    level = payload["level"]
    day = payload["day"]
    slot = payload["slot"]

    html = f"""<!doctype html>
<!-- {COPYRIGHT_TEXT} -->
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{class_id} 5문항 퀴즈</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-slate-100 text-slate-900">
  <main class="mx-auto max-w-3xl px-4 py-10">
    <section class="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <p class="text-sm font-semibold text-sky-700">{class_id} SELF QUIZ</p>
      <h1 class="mt-2 text-2xl font-bold">{module}</h1>
      <p class="mt-2 text-sm text-slate-600">
        교과목: {subject_name} · 세부 시퀀스: {session} · 난이도: {level} · Day {day:02d} / {slot}교시
      </p>
      <p class="mt-4 rounded-lg bg-slate-50 p-3 text-sm text-slate-700">
        학습 내용 기반 심화 5문항 퀴즈입니다. 정답을 고른 뒤 채점 버튼을 누르세요.
      </p>
    </section>

    <section id="quiz-root" class="mt-6 space-y-4"></section>

    <div class="mt-6 flex items-center gap-3">
      <button id="grade-btn" class="rounded-lg bg-sky-600 px-5 py-2 text-sm font-semibold text-white hover:bg-sky-700">
        채점하기
      </button>
      <button id="reset-btn" class="rounded-lg bg-slate-200 px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-300">
        다시풀기
      </button>
    </div>

    <section id="result-root" class="mt-6 hidden rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200"></section>
  </main>

  <script>
    const QUIZ_DATA = {quiz_json};

    function renderQuiz() {{
      const root = document.getElementById("quiz-root");
      root.innerHTML = "";

      QUIZ_DATA.questions.forEach((q, qIndex) => {{
        const wrap = document.createElement("article");
        wrap.className = "rounded-xl bg-white p-5 shadow-sm ring-1 ring-slate-200";

        const title = document.createElement("h2");
        title.className = "text-base font-semibold";
        title.textContent = `${{qIndex + 1}}번. ${{q.question}}`;
        wrap.appendChild(title);

        const list = document.createElement("div");
        list.className = "mt-3 space-y-2";

        q.options.forEach((opt, optIndex) => {{
          const label = document.createElement("label");
          label.className = "flex cursor-pointer items-start gap-2 rounded-lg border border-slate-200 p-3 hover:bg-slate-50";

          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = `q-${{qIndex}}`;
          radio.value = String(optIndex);
          radio.className = "mt-1";

          const text = document.createElement("span");
          text.className = "text-sm";
          text.textContent = opt;

          label.appendChild(radio);
          label.appendChild(text);
          list.appendChild(label);
        }});

        wrap.appendChild(list);
        root.appendChild(wrap);
      }});
    }}

    function gradeQuiz() {{
      let score = 0;
      const details = [];
      const total = QUIZ_DATA.questions.length;

      QUIZ_DATA.questions.forEach((q, qIndex) => {{
        const selected = document.querySelector(`input[name="q-${{qIndex}}"]:checked`);
        const selectedIndex = selected ? Number(selected.value) : -1;
        const isCorrect = selectedIndex === q.answer_index;
        if (isCorrect) score += 1;

        details.push({{
          number: qIndex + 1,
          isCorrect,
          correct: q.options[q.answer_index],
          chosen: selectedIndex >= 0 ? q.options[selectedIndex] : "미선택",
          explanation: q.explanation
        }});
      }});

      const resultRoot = document.getElementById("result-root");
      resultRoot.classList.remove("hidden");

      const headerClass = score === total ? "text-emerald-700" : "text-amber-700";
      const summary = `
        <h3 class="text-lg font-bold ${{headerClass}}">점수: ${{score}} / ${{total}}</h3>
        <p class="mt-1 text-sm text-slate-600">틀린 문제는 해설을 확인하고 다시 풀어보세요.</p>
        <p class="mt-1 text-sm text-slate-600">학습 성과 힌트: ${{QUIZ_DATA.track_outcome}}</p>
      `;

      const rows = details.map((d) => `
        <li class="rounded-lg border border-slate-200 p-3">
          <p class="text-sm font-semibold">${{d.number}}번 - ${{d.isCorrect ? "정답" : "오답"}}</p>
          <p class="mt-1 text-sm">내 답: ${{d.chosen}}</p>
          <p class="text-sm">정답: ${{d.correct}}</p>
          <p class="mt-1 text-xs text-slate-500">${{d.explanation}}</p>
        </li>
      `).join("");

      resultRoot.innerHTML = `
        ${{summary}}
        <ul class="mt-4 space-y-2">${{rows}}</ul>
      `;
    }}

    function resetQuiz() {{
      document.querySelectorAll('input[type="radio"]').forEach((el) => {{
        el.checked = false;
      }});
      const resultRoot = document.getElementById("result-root");
      resultRoot.classList.add("hidden");
      resultRoot.innerHTML = "";
    }}

    document.getElementById("grade-btn").addEventListener("click", gradeQuiz);
    document.getElementById("reset-btn").addEventListener("click", resetQuiz);
    renderQuiz();
  </script>
</body>
</html>
"""
    return dedent(html)


def build_launcher_py(class_id: str) -> str:
    return dedent(
        f'''\
        # {COPYRIGHT_TEXT}
        """
        {class_id} launcher
        - 기본 실행: {class_id}_example.py
        - 과제 실행: {class_id}_assignment.py
        - 정답 실행: {class_id}_solution.py
        """
        from __future__ import annotations

        import os
        import runpy
        from pathlib import Path

        HERE = Path(__file__).resolve().parent
        CLASS_ID = Path(__file__).resolve().stem

        if __name__ == "__main__":
            target = (os.getenv("CLASS_RUN_TARGET") or "example").strip().lower()
            mapping = {{
                "example": f"{{CLASS_ID}}_example.py",
                "assignment": f"{{CLASS_ID}}_assignment.py",
                "solution": f"{{CLASS_ID}}_solution.py",
            }}
            file_name = mapping.get(target)
            if file_name is None:
                raise SystemExit("Unknown CLASS_RUN_TARGET (use example/assignment/solution)")

            py_file = HERE / file_name
            if not py_file.exists() and target == "example":
                # 예제 파일이 없으면 기존 과제 실행으로 안전하게 폴백
                py_file = HERE / f"{{CLASS_ID}}_assignment.py"

            if not py_file.exists():
                raise SystemExit(f"Run target not found: {{py_file}}")

            runpy.run_path(str(py_file), run_name="__main__")
        '''
    )


def rebuild_launchers_and_quizzes() -> None:
    rows = read_rows()
    launcher_count = 0
    quiz_count = 0

    for row in rows:
        class_id = row["class"]
        class_dir = class_dir_from_row(row)
        class_dir.mkdir(parents=True, exist_ok=True)

        launcher_path = class_dir / f"{class_id}.py"
        launcher_path.write_text(build_launcher_py(class_id), encoding="utf-8", newline="\n")
        launcher_count += 1

        quiz_path = class_dir / f"{class_id}_quiz.html"
        quiz_path.write_text(build_quiz_html(row, rows), encoding="utf-8", newline="\n")
        quiz_count += 1

    print(f"Updated launchers: {launcher_count}")
    print(f"Created quiz html files: {quiz_count}")


if __name__ == "__main__":
    rebuild_launchers_and_quizzes()
