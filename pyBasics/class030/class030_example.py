# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class030 example1: 웹 프론트엔드 기초 (HTML/CSS/JS) · 단계 2/2 운영 최적화 [class030]"""

TOPIC = "웹 프론트엔드 기초 (HTML/CSS/JS) · 단계 2/2 운영 최적화 [class030]"
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
