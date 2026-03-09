# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class290 example1: LLM 개요 · 단계 2/7 기초 구현 [class290]"""

TOPIC = "LLM 개요 · 단계 2/7 기초 구현 [class290]"
EXAMPLE_TEMPLATE = "llm_gen"

def build_generation_config(temp=0.5, max_tokens=180):
    return {"temperature": temp, "max_tokens": max_tokens, "top_p": 0.9}

def simulate_generation(prompt, cfg):
    return f"[SIM] prompt={prompt} | temp={cfg['temperature']} | max_tokens={cfg['max_tokens']}"

def safety_guard(text):
    blocked = ["개인정보", "비밀번호"]
    found = [w for w in blocked if w in text]
    return {"ok": not found, "blocked_terms": found}

def main():
    print("오늘 주제:", TOPIC)
    cfg = build_generation_config()
    prompt = "고객문의 답변 초안을 3문장으로 작성"
    output = simulate_generation(prompt, cfg)
    guard = safety_guard(output)
    report = {"config": cfg, "guard": guard}
    print(output)
    print("안전 점검:", guard)
    return report

if __name__ == "__main__":
    main()
