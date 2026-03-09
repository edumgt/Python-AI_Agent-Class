# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class365 example4: 출력 포맷 제어 · 단계 1/4 입문 이해 [class365]"""

TOPIC = "출력 포맷 제어 · 단계 1/4 입문 이해 [class365]"
EXAMPLE_TEMPLATE = "prompt"

def build_prompt(role, task, output_format):
    return (
        f"[ROLE] {role}\n"
        f"[TASK] {task}\n"
        f"[FORMAT] {output_format}\n"
        "[RULE] 근거 없는 내용은 '확인 필요'라고 표시"
    )

def lint_prompt(prompt):
    required = ["[ROLE]", "[TASK]", "[FORMAT]", "[RULE]"]
    missing = [tag for tag in required if tag not in prompt]
    return {"missing": missing, "is_valid": len(missing) == 0}

def main():
    print("오늘 주제:", TOPIC)
    prompt = build_prompt("IT 튜터", "RAG를 3줄로 설명", "번호 목록")
    lint = lint_prompt(prompt)
    print(prompt)
    print("프롬프트 검사:", lint)
    return lint

def mini_project_plan():
    return {
        "scenario": "미니 프로젝트 형태로 실행 로그를 구조화하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
