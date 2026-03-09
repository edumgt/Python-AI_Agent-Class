# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""project004 example1: DevOps 프로젝트 착수와 요구사항 정의 · 단계 4/5 실전 검증 [project004]"""

TOPIC = "DevOps 프로젝트 착수와 요구사항 정의 · 단계 4/5 실전 검증 [project004]"
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
