# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class040 example2: 미니 실습 프로젝트"""

TOPIC = "미니 실습 프로젝트"
EXAMPLE_TEMPLATE = "generic"

def solve_in_steps(task):
    return [f"1단계: {task} 이해", "2단계: 작은 예제 작성", "3단계: 결과 확인"]

def main():
    print("오늘 주제:", TOPIC)
    for line in solve_in_steps(TOPIC):
        print(line)


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
