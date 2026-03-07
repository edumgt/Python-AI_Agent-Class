# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class002 example2: 오리엔테이션 및 개발환경 준비"""

TOPIC = "오리엔테이션 및 개발환경 준비"
EXAMPLE_TEMPLATE = "dev_setup"

def checklist():
    return [
        "python -m venv .venv",
        "가상환경 활성화",
        "pip install -r requirements.txt",
    ]

def main():
    print("오늘 주제:", TOPIC)
    for idx, step in enumerate(checklist(), start=1):
        print(f"{idx}. {step}")


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
