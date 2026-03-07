# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class043 example1: 데이터 분석 환경 구성"""

TOPIC = "데이터 분석 환경 구성"
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


if __name__ == "__main__":
    main()
