# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class335 example1: 도메인 적용 시나리오"""

TOPIC = "도메인 적용 시나리오"
EXAMPLE_TEMPLATE = "llm_gen"

def build_generation_config():
    return {"temperature": 0.7, "max_tokens": 200, "top_p": 0.9}

def simulate_response(prompt, cfg):
    return f"[생성 결과]\n프롬프트: {prompt}\n설정: {cfg}"

def main():
    cfg = build_generation_config()
    print("오늘 주제:", TOPIC)
    print(simulate_response("한 줄 자기소개를 써줘", cfg))


if __name__ == "__main__":
    main()
