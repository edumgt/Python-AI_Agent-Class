# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class332 example3: 안전성/환각 관리"""

TOPIC = "안전성/환각 관리"
EXAMPLE_TEMPLATE = "llm_gen"

def build_generation_config():
    return {"temperature": 0.7, "max_tokens": 200, "top_p": 0.9}

def simulate_response(prompt, cfg):
    return f"[생성 결과]\n프롬프트: {prompt}\n설정: {cfg}"

def main():
    cfg = build_generation_config()
    print("오늘 주제:", TOPIC)
    print(simulate_response("한 줄 자기소개를 써줘", cfg))


def self_check():
    return [
        "입력/출력 형식을 다시 설명할 수 있는가?",
        "오류 상황 1가지를 직접 만들어 테스트했는가?",
        "핵심 로직을 함수 단위로 분리했는가?",
    ]

def challenge_case():
    return {
        "task": "같은 로직을 새로운 입력 데이터로 재실행",
        "goal": "결과 차이를 한 문장으로 요약",
    }

if __name__ == "__main__":
    main()
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
