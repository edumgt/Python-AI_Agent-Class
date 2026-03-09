# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class363 example1: 역할/맥락 설정 · 단계 3/4 실전 검증 [class363]"""

TOPIC = "역할/맥락 설정 · 단계 3/4 실전 검증 [class363]"
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
