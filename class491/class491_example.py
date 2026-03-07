# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class491 example1: 평가 지표 설계"""

TOPIC = "평가 지표 설계"
EXAMPLE_TEMPLATE = "prompt"

def build_prompt(role, question):
    return (
        f"너는 {role}이야.\n"
        f"질문: {question}\n"
        "답변은 3줄 이내로 핵심만 설명해."
    )

def main():
    print("오늘 주제:", TOPIC)
    print(build_prompt("친절한 과학 선생님", "중력이 뭐야?"))


if __name__ == "__main__":
    main()
