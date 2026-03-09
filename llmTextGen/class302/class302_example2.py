# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class302 example2: 생성 파라미터 · 단계 1/7 입문 이해 [class302]"""

TOPIC = "생성 파라미터 · 단계 1/7 입문 이해 [class302]"
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

def extension_mission():
    return {
        "mission": "temperature/top_p 조합 3개를 비교해 응답 품질을 점수화하세요.",
        "check": "환각 가능 문장에 '확인 필요' 태그를 붙이세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
