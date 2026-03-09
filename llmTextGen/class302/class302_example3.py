# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class302 example3: 생성 파라미터 · 단계 1/7 입문 이해 [class302]"""

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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "금칙어/민감어 필터를 커스터마이징하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
