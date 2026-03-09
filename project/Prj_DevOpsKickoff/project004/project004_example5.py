# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""project004 example5: DevOps 프로젝트 착수와 요구사항 정의 · 단계 4/5 실전 검증 [project004]"""

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

def ops_readiness_check():
    return {
        "risk": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
