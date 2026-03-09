# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class366 example1: 출력 포맷 제어 · 단계 2/4 기초 구현 [class366]"""

TOPIC = "출력 포맷 제어 · 단계 2/4 기초 구현 [class366]"
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

if __name__ == "__main__":
    main()
