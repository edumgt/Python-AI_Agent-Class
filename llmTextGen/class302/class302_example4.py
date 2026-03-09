# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class302 example4: 생성 파라미터 · 단계 1/7 입문 이해 [class302]"""

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

def mini_project_plan():
    return {
        "scenario": "입력 토큰 길이별 비용 추정기를 추가하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
