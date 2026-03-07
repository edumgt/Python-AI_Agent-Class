# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class378 쉬운 예제: 평가와 개선"""

TOPIC = "평가와 개선"

def build_prompt(role, question):
    template = (
        "너는 {role}야.\n"
        "질문: {question}\n"
        "답변은 3줄 이내로 쉽게 설명해 줘."
    )
    return template.format(role=role, question=question)

def main():
    prompt = build_prompt("친절한 과학 선생님", "중력이 뭐야?")
    print("오늘 주제:", TOPIC)
    print(prompt)

if __name__ == "__main__":
    main()
