# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class308 example5: 생성 파라미터 · 단계 7/7 운영 최적화 [class308]"""

TOPIC = "생성 파라미터 · 단계 7/7 운영 최적화 [class308]"
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

def ops_readiness_check():
    return {
        "risk": "모델 장애 시 대체 모델 라우팅 규칙을 작성하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
