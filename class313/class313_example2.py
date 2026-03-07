# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class313 example2: 프롬프트 기반 생성"""

TOPIC = "프롬프트 기반 생성"
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


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
