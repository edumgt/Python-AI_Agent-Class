# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""
class512 example5: LLM 평가와 품질 · 운영 최적화 [class512]
"""

TOPIC = "LLM 평가와 품질 · 운영 최적화 [class512]"
EXAMPLE_VARIANT = 5

import json


LLMOPS_COMPONENTS = [
    {"name": "프롬프트 관리",  "role": "프롬프트 버전/템플릿 관리"},
    {"name": "평가 파이프라인","role": "응답 품질 자동 측정"},
    {"name": "모니터링",       "role": "토큰·지연·오류율 추적"},
    {"name": "배포 자동화",    "role": "CI/CD 기반 안전 배포"},
    {"name": "가드레일",       "role": "유해·부정확 응답 차단"},
]


def resolve_mode(topic):
    if "LLMOps 개요"     in topic: return "overview"
    if "프롬프트 관리"   in topic: return "prompt_mgmt"
    if "LLM 평가"        in topic: return "evaluation"
    if "LLM 모니터링"    in topic: return "monitoring"
    if "LLM 배포"        in topic: return "deployment"
    return "general"


def build_cases(variant):
    cases = [
        {
            "id": "case_1",
            "task": "LLM 평가와 품질 기본 동작 확인",
            "input": "LLMOps 핵심 흐름을 설명해줘.",
            "output_format": "TEXT",
        }
    ]
    if variant >= 2:
        cases.append({"id": "case_2", "task": "구성요소 매핑", "input": "핵심 컴포넌트를 역할별로 나열해.", "output_format": "TEXT"})
    if variant >= 3:
        cases.append({"id": "case_3", "task": "실패 케이스 재현", "input": "모니터링 누락 시 발생하는 문제는?", "output_format": "TEXT"})
    if variant >= 4:
        cases.append({"id": "case_4", "task": "개선 비교", "input": "배포 자동화 전후 차이를 설명해.", "output_format": "JSON"})
    if variant >= 5:
        cases.append({"id": "case_5", "task": "운영 체크리스트", "input": "LLMOps 운영 점검 항목을 정리해.", "output_format": "JSON"})
    return cases


def model_stub(prompt: str, temperature: float = 0.3) -> str:
    tokens = prompt.replace(",", " ").split()[:10]
    stability = "stable" if temperature < 0.5 else "diverse"
    return f"{stability} output: {chr(32).join(tokens)}"


def parse_output(raw: str, fmt: str) -> dict:
    if fmt == "JSON":
        try:
            return {"ok": True, "data": json.loads(raw)}
        except json.JSONDecodeError:
            return {"ok": False, "data": {"message": raw, "fallback": True}}
    return {"ok": True, "data": {"text": raw}}


def execute_case(case: dict, mode: str) -> dict:
    task_val = case['task']
    input_val = case['input']
    prompt = f"mode={mode} task={task_val} input={input_val}"
    raw = model_stub(prompt, temperature=0.3)
    parsed = parse_output(raw, case["output_format"])
    return {"case": case["id"], "mode": mode, "parsed_ok": parsed["ok"], "raw": raw}


def summarize(mode: str, rows: list) -> dict:
    success = sum(1 for r in rows if r.get("parsed_ok", False))
    return {
        "mode": mode,
        "components": [c["name"] for c in LLMOPS_COMPONENTS],
        "total": len(rows),
        "success": success,
    }


def main():
    print("오늘 주제:", TOPIC)
    mode = resolve_mode(TOPIC)
    cases = build_cases(EXAMPLE_VARIANT)
    rows = [execute_case(c, mode) for c in cases]
    summary = summarize(mode, rows)
    print("모드:", mode)
    print("요약:", summary)
    return {"variant": EXAMPLE_VARIANT, "mode": mode, "summary": summary}


if __name__ == "__main__":
    main()
