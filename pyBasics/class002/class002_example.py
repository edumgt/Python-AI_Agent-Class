# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class002 example1: 수업 준비 2: 필수 소프트웨어 설치 (class002) · 단계 1/1 입문 이해 [class002]"""

TOPIC = "수업 준비 2: 필수 소프트웨어 설치 (class002) · 단계 1/1 입문 이해 [class002]"
EXAMPLE_TEMPLATE = "generic"

def solve_in_steps(task):
    return [
        f"1단계: {task} 요구사항 정리",
        "2단계: 작은 함수로 분리",
        "3단계: 테스트 입력 2개 이상 실행",
    ]

def main():
    print("오늘 주제:", TOPIC)
    steps = solve_in_steps(TOPIC)
    for line in steps:
        print(line)
    return {"step_count": len(steps)}

if __name__ == "__main__":
    main()
