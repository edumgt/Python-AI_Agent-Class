# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

import csv
import py_compile
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(k).lstrip("\ufeff"): v for k, v in raw.items()})
    return rows


def class_dir_from_row(row: dict[str, str]) -> Path:
    md_rel = (row.get("md_file") or "").strip()
    if md_rel:
        md_path = ROOT / Path(md_rel)
        if md_path.name:
            return md_path.parent
    return ROOT / row["class"]


def subject_root(class_dir: Path) -> str:
    try:
        rel = class_dir.resolve().relative_to(ROOT.resolve())
        return rel.parts[0] if rel.parts else ""
    except Exception:
        return class_dir.parts[-2] if len(class_dir.parts) >= 2 else class_dir.name


def is_python_basics(row: dict[str, str], class_dir: Path | None = None) -> bool:
    class_dir = class_dir or class_dir_from_row(row)
    root_name = subject_root(class_dir)
    subject = (row.get("subject_name") or "").lower()
    return root_name == "pyBasics" or "파이썬" in subject


def variants_for_row(row: dict[str, str], class_dir: Path | None = None) -> list[int]:
    if is_python_basics(row, class_dir=class_dir):
        return [1, 2, 3]
    return [1, 2, 3, 4, 5]


def example_path(class_dir: Path, class_id: str, variant: int) -> Path:
    suffix = "example" if variant == 1 else f"example{variant}"
    return class_dir / f"{class_id}_{suffix}.py"


def pick_template(module: str, subject: str) -> str:
    module_text = module.lower()
    subject_text = subject.lower()
    text = f"{subject_text} {module_text}"

    if "mlops" in text or "모델 레지스트리" in module or "배포 자동화" in module:
        return "ml"
    if "aiops" in text or "관측 데이터" in module or "이상탐지" in module or "runbook" in text:
        return "data_preprocess"

    if any(k in module_text for k in ["rag", "retrieval-augmented generation", "벡터db", "vectorstore", "문서 로딩", "문서 분할", "문서 청크", "검색 품질", "출처화"]):
        return "rag"
    if any(k in module_text for k in ["langchain", "prompttemplate", "outputparser", "memory 활용", "chain 구성", "tool/agent", "model/llm 연결", "체인 애플리케이션"]):
        return "langchain"
    if any(k in module_text for k in ["프롬프트", "질문 구조화", "역할/맥락", "출력 포맷", "예시 기반", "단계적 추론", "자동화 프롬프트", "평가 지표 설계", "프롬프트 결합", "실전 프롬프트 튜닝"]):
        return "prompt"
    if any(k in module_text for k in ["음성", "stt", "tts", "오디오", "mfcc", "발화/화자"]):
        return "speech"
    if any(k in module_text for k in ["텍스트", "토큰", "임베딩", "자연어", "nlp", "요약/분류/추출", "언어모델 입력 구조"]):
        return "nlp"
    if any(k in module_text for k in ["llm 개요", "생성 파라미터", "대화형 응답 설계", "안전성/환각 관리", "도메인 적용 시나리오", "프롬프트 기반 생성", "생성형 서비스"]):
        return "llm_gen"
    if any(k in module_text for k in ["딥러닝", "신경망"]):
        return "deep_learning"
    if any(k in module_text for k in ["회귀 모델", "분류 모델", "지도학습", "과적합", "평가와 개선", "모델 평가 지표", "특성공학", "실전 예측", "ml/dl 개요", "모델 추론 및 튜닝"]):
        return "ml"
    if any(k in module_text for k in ["문자열/날짜 전처리", "결측치/이상치 처리", "데이터 병합과 변환", "그룹화와 집계", "전처리"]):
        return "data_preprocess"
    if any(k in module_text for k in ["matplotlib", "seaborn", "시각화"]):
        return "visualization"
    if any(k in module_text for k in ["pandas", "데이터프레임"]):
        return "pandas"
    if "numpy" in module_text:
        return "numpy"
    if "파일 입출력" in module_text:
        return "file_io"
    if "예외처리" in module_text or "디버깅" in module_text:
        return "exception"
    if "객체지향" in module_text:
        return "oop"
    if "컬렉션" in module_text:
        return "collection"
    if "함수와 모듈" in module_text:
        return "function_module"
    if "반복문" in module_text:
        return "loop"
    if "연산자와 조건문" in module_text:
        return "condition"
    if "변수와 자료형" in module_text:
        return "variables"
    if any(k in module_text for k in ["오리엔테이션", "개발환경 준비", "환경 구성"]):
        return "dev_setup"

    if "langchain" in subject_text:
        return "langchain"
    if "rag" in subject_text:
        return "rag"
    if "프롬프트" in subject_text:
        return "prompt"
    if any(k in subject_text for k in ["자연어", "음성"]):
        return "nlp"
    if any(k in subject_text for k in ["머신러닝", "딥러닝"]):
        return "ml"
    return "generic"


def q(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', "\\\"")


def wrap_code(class_id: str, module: str, template: str, variant: int, body: str) -> str:
    doc = f'"""{class_id} example{variant}: {module}"""'
    header = dedent(
        f"""\
        # {COPYRIGHT_TEXT}

        {doc}

        TOPIC = "{q(module)}"
        EXAMPLE_TEMPLATE = "{template}"
        """
    )
    return header + "\n" + body.strip() + "\n"


def build_body(template: str, class_id: str) -> str:
    if template == "dev_setup":
        return f"""
        from pathlib import Path
        import platform

        def build_setup_plan():
            return [
                ("venv", "python -m venv .venv"),
                ("activate", "source .venv/bin/activate"),
                ("deps", "pip install -r requirements.txt"),
                ("run", "python {class_id}_example.py"),
            ]

        def scan_workspace():
            root = Path(__file__).resolve().parents[2]
            return {{
                "platform": platform.system(),
                "requirements_exists": (root / "requirements.txt").exists(),
                "readme_exists": (root / "README.md").exists(),
            }}

        def main():
            print("오늘 주제:", TOPIC)
            plan = build_setup_plan()
            for idx, (name, cmd) in enumerate(plan, start=1):
                print(f"{{idx}}. {{name}} -> {{cmd}}")
            status = scan_workspace()
            print("환경 점검:", status)
            return {{"step_count": len(plan), **status}}
        """

    if template == "variables":
        return """
        def infer_schema(record):
            return {k: type(v).__name__ for k, v in record.items()}

        def normalize_record(record):
            return {
                "name": str(record["name"]).strip(),
                "score": float(record["score"]),
                "active": bool(record["active"]),
            }

        def main():
            print("오늘 주제:", TOPIC)
            raw = {"name": "  민수  ", "score": "91.5", "active": 1}
            normalized = normalize_record(raw)
            print("원본 스키마:", infer_schema(raw))
            print("정규화 스키마:", infer_schema(normalized))
            return normalized
        """

    if template == "condition":
        return """
        def route_incident(score):
            if score >= 90:
                return "critical"
            if score >= 70:
                return "warning"
            if score >= 50:
                return "observe"
            return "ok"

        def main():
            print("오늘 주제:", TOPIC)
            sample_scores = [35, 58, 77, 94]
            routed = {score: route_incident(score) for score in sample_scores}
            print("라우팅:", routed)
            return {"max_level": route_incident(max(sample_scores)), "count": len(sample_scores)}
        """

    if template == "loop":
        return """
        def rolling_average(values, window):
            result = []
            for idx in range(len(values)):
                start = max(0, idx - window + 1)
                chunk = values[start : idx + 1]
                result.append(round(sum(chunk) / len(chunk), 2))
            return result

        def main():
            print("오늘 주제:", TOPIC)
            values = [12, 15, 13, 20, 19, 23]
            trend = rolling_average(values, window=3)
            print("원본:", values)
            print("이동평균:", trend)
            return {"last_avg": trend[-1], "points": len(values)}
        """

    if template == "function_module":
        return """
        import math

        def area_circle(radius):
            return round(math.pi * radius * radius, 3)

        def perimeter_rectangle(width, height):
            return 2 * (width + height)

        def main():
            print("오늘 주제:", TOPIC)
            c_area = area_circle(3)
            r_perimeter = perimeter_rectangle(4, 7)
            print("원 넓이:", c_area)
            print("직사각형 둘레:", r_perimeter)
            return {"circle_area": c_area, "rect_perimeter": r_perimeter}
        """

    if template == "collection":
        return """
        def summarize_orders(orders):
            by_team = {}
            for row in orders:
                by_team[row["team"]] = by_team.get(row["team"], 0) + row["amount"]
            ranking = sorted(by_team.items(), key=lambda x: x[1], reverse=True)
            return by_team, ranking

        def main():
            print("오늘 주제:", TOPIC)
            orders = [
                {"team": "A", "amount": 120},
                {"team": "B", "amount": 90},
                {"team": "A", "amount": 60},
                {"team": "C", "amount": 200},
            ]
            by_team, ranking = summarize_orders(orders)
            print("팀별 합계:", by_team)
            print("랭킹:", ranking)
            return {"winner": ranking[0][0], "team_count": len(by_team)}
        """

    if template == "file_io":
        return f"""
        import json
        from pathlib import Path

        def write_rows(rows):
            out = Path(__file__).with_name("{class_id}_logs.jsonl")
            payload = "\\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
            out.write_text(payload + "\\n", encoding="utf-8")
            return out

        def read_rows(path):
            rows = []
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(json.loads(line))
            return rows

        def main():
            print("오늘 주제:", TOPIC)
            source = [
                {{"step": "extract", "ok": True}},
                {{"step": "transform", "ok": True}},
                {{"step": "load", "ok": False}},
            ]
            path = write_rows(source)
            loaded = read_rows(path)
            print("저장 파일:", path.name)
            print("복원 행 수:", len(loaded))
            return {{"file": path.name, "loaded": len(loaded)}}
        """

    if template == "exception":
        return """
        def safe_to_float(value):
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        def parse_batch(values):
            parsed = [safe_to_float(v) for v in values]
            valid = [v for v in parsed if v is not None]
            return {
                "parsed": parsed,
                "valid_count": len(valid),
                "invalid_count": len(parsed) - len(valid),
            }

        def main():
            print("오늘 주제:", TOPIC)
            report = parse_batch(["10.5", "err", None, "3"])
            print("파싱 결과:", report)
            return report
        """

    if template == "oop":
        return """
        class Experiment:
            def __init__(self, name, score):
                self.name = name
                self.score = score

            def is_pass(self, threshold=80):
                return self.score >= threshold

            def to_dict(self):
                return {"name": self.name, "score": self.score, "pass": self.is_pass()}

        def main():
            print("오늘 주제:", TOPIC)
            runs = [Experiment("baseline", 76), Experiment("tuned", 84)]
            report = [r.to_dict() for r in runs]
            print("실험 리포트:", report)
            return {"best": max(report, key=lambda x: x["score"])["name"], "count": len(report)}
        """

    if template == "numpy":
        return """
        try:
            import numpy as np
        except ImportError:
            np = None

        def compute_stats(values):
            if np is None:
                avg = sum(values) / len(values)
                var = sum((v - avg) ** 2 for v in values) / len(values)
                return {"mean": round(avg, 4), "std": round(var ** 0.5, 4), "backend": "python"}
            arr = np.array(values, dtype=float)
            return {
                "mean": round(float(arr.mean()), 4),
                "std": round(float(arr.std()), 4),
                "backend": "numpy",
            }

        def main():
            print("오늘 주제:", TOPIC)
            result = compute_stats([0.3, 0.4, 0.45, 0.5, 0.65])
            print("통계:", result)
            return result
        """

    if template == "pandas":
        return """
        try:
            import pandas as pd
        except ImportError:
            pd = None

        def summarize_scores(rows):
            if pd is None:
                avg = sum(r["score"] for r in rows) / len(rows)
                passed = sum(1 for r in rows if r["score"] >= 80)
                return {"backend": "python", "avg": round(avg, 2), "pass_count": passed}

            df = pd.DataFrame(rows)
            return {
                "backend": "pandas",
                "avg": round(float(df["score"].mean()), 2),
                "pass_count": int((df["score"] >= 80).sum()),
            }

        def main():
            print("오늘 주제:", TOPIC)
            rows = [{"name": "A", "score": 72}, {"name": "B", "score": 88}, {"name": "C", "score": 91}]
            summary = summarize_scores(rows)
            print("요약:", summary)
            return summary
        """

    if template == "visualization":
        return f"""
        from pathlib import Path

        def save_chart(points):
            out = Path(__file__).with_name("{class_id}_plot.png")
            try:
                import matplotlib.pyplot as plt

                x = [idx + 1 for idx, _ in enumerate(points)]
                y = [v for _, v in points]
                plt.figure(figsize=(5, 3))
                plt.plot(x, y, marker="o")
                plt.title(TOPIC)
                plt.xlabel("step")
                plt.ylabel("value")
                plt.tight_layout()
                plt.savefig(out)
                plt.close()
                mode = "matplotlib"
            except ImportError:
                text_out = out.with_suffix(".txt")
                text_out.write_text("\\n".join(f"{{k}}: {{v}}" for k, v in points), encoding="utf-8")
                out = text_out
                mode = "text-fallback"
            return out, mode

        def main():
            print("오늘 주제:", TOPIC)
            points = [("week1", 61), ("week2", 67), ("week3", 73), ("week4", 78)]
            out, mode = save_chart(points)
            print("출력 파일:", out.name)
            return {{"output": out.name, "mode": mode}}
        """

    if template == "data_preprocess":
        return """
        from datetime import datetime

        def clean_rows(rows):
            cleaned = []
            for row in rows:
                text = row["text"].strip().lower()
                amount = float(row["amount"])
                when = datetime.strptime(row["date"], "%Y-%m-%d")
                cleaned.append({"text": text, "amount": amount, "month": when.month})
            return cleaned

        def summarize(rows):
            total = round(sum(r["amount"] for r in rows), 2)
            avg = round(total / len(rows), 2)
            return {"rows": len(rows), "total": total, "avg": avg}

        def main():
            print("오늘 주제:", TOPIC)
            raw = [
                {"text": "  GPU Server  ", "amount": "1200", "date": "2026-03-01"},
                {"text": "Monitoring  ", "amount": "450", "date": "2026-03-12"},
            ]
            cleaned = clean_rows(raw)
            report = summarize(cleaned)
            print("정제 데이터:", cleaned)
            print("요약:", report)
            return report
        """

    if template == "ml":
        return """
        def make_dataset():
            return [(1, 52), (2, 61), (3, 70), (4, 82), (5, 91)]

        def fit_linear(points):
            xs = [x for x, _ in points]
            ys = [y for _, y in points]
            mean_x = sum(xs) / len(xs)
            mean_y = sum(ys) / len(ys)
            num = sum((x - mean_x) * (y - mean_y) for x, y in points)
            den = sum((x - mean_x) ** 2 for x in xs)
            slope = num / den
            bias = mean_y - slope * mean_x
            return slope, bias

        def mae(points, slope, bias):
            errors = [abs(y - (slope * x + bias)) for x, y in points]
            return sum(errors) / len(errors)

        def main():
            print("오늘 주제:", TOPIC)
            points = make_dataset()
            slope, bias = fit_linear(points)
            metric = round(mae(points, slope, bias), 3)
            report = {"slope": round(slope, 3), "bias": round(bias, 3), "mae": metric}
            print("평가 리포트:", report)
            return report
        """

    if template == "deep_learning":
        return """
        def relu(x):
            return x if x > 0 else 0.0

        def dense_forward(inputs, weights, bias):
            z = sum(i * w for i, w in zip(inputs, weights)) + bias
            return relu(z)

        def predict_batch(batch, weights, bias):
            return [round(dense_forward(x, weights, bias), 4) for x in batch]

        def main():
            print("오늘 주제:", TOPIC)
            batch = [[0.2, 0.5, 0.1], [0.4, 0.4, 0.2], [0.9, 0.1, 0.3]]
            weights = [0.6, 0.3, 0.8]
            bias = -0.2
            preds = predict_batch(batch, weights, bias)
            report = {"predictions": preds, "max_pred": max(preds)}
            print("추론 결과:", report)
            return report
        """

    if template == "nlp":
        return """
        def tokenize(text):
            cleaned = text.replace(",", " ").replace(".", " ").replace("/", " ")
            return [tok.lower() for tok in cleaned.split() if tok]

        def top_k(tokens, k=5):
            freq = {}
            for tok in tokens:
                freq[tok] = freq.get(tok, 0) + 1
            return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:k]

        def main():
            print("오늘 주제:", TOPIC)
            text = "LLM 응답 품질은 프롬프트 구조와 검증 절차에 따라 달라진다. 응답 품질을 점검하자."
            tokens = tokenize(text)
            ranking = top_k(tokens)
            report = {"token_count": len(tokens), "top_terms": ranking}
            print("분석 리포트:", report)
            return report
        """

    if template == "speech":
        return """
        def summarize_utterances(rows):
            avg_seconds = sum(r["seconds"] for r in rows) / len(rows)
            noise_flags = [r["id"] for r in rows if r["snr_db"] < 12]
            return {
                "count": len(rows),
                "avg_seconds": round(avg_seconds, 2),
                "noisy_ids": noise_flags,
            }

        def main():
            print("오늘 주제:", TOPIC)
            rows = [
                {"id": "utt1", "seconds": 1.8, "snr_db": 15.2},
                {"id": "utt2", "seconds": 2.9, "snr_db": 10.5},
                {"id": "utt3", "seconds": 1.1, "snr_db": 18.7},
            ]
            report = summarize_utterances(rows)
            print("음성 품질 요약:", report)
            return report
        """

    if template == "prompt":
        return """
        def build_prompt(role, task, output_format):
            return (
                f"[ROLE] {role}\\n"
                f"[TASK] {task}\\n"
                f"[FORMAT] {output_format}\\n"
                "[RULE] 근거 없는 내용은 '확인 필요'라고 표시"
            )

        def lint_prompt(prompt):
            required = ["[ROLE]", "[TASK]", "[FORMAT]", "[RULE]"]
            missing = [tag for tag in required if tag not in prompt]
            return {"missing": missing, "is_valid": len(missing) == 0}

        def main():
            print("오늘 주제:", TOPIC)
            prompt = build_prompt("IT 튜터", "RAG를 3줄로 설명", "번호 목록")
            lint = lint_prompt(prompt)
            print(prompt)
            print("프롬프트 검사:", lint)
            return lint
        """

    if template == "langchain":
        return """
        def step_collect(question):
            return {"question": question, "context": []}

        def step_retrieve(state):
            state["context"] = [
                "체인은 여러 단계를 연결한다",
                "도구 호출 전 입력 검증이 중요하다",
            ]
            return state

        def step_answer(state):
            context = " / ".join(state["context"])
            return {"answer": f"질문: {state['question']} | 근거: {context}", "steps": 3}

        def main():
            print("오늘 주제:", TOPIC)
            s1 = step_collect("체인 설계의 핵심이 뭐야?")
            s2 = step_retrieve(s1)
            report = step_answer(s2)
            print("체인 실행 결과:", report)
            return report
        """

    if template == "rag":
        return """
        def tokenize(text):
            return [t.lower() for t in text.replace(",", " ").replace(".", " ").split() if t]

        def retrieve(question, docs, top_k=2):
            q = set(tokenize(question))
            scored = []
            for doc in docs:
                overlap = len(q & set(tokenize(doc["text"])))
                if overlap > 0:
                    scored.append({"id": doc["id"], "text": doc["text"], "score": overlap})
            scored.sort(key=lambda x: x["score"], reverse=True)
            return scored[:top_k]

        def answer(question, hits):
            if not hits:
                return {"answer": "관련 문서를 찾지 못했습니다.", "citations": []}
            citations = [f"doc{h['id']}" for h in hits]
            evidence = " | ".join(h["text"] for h in hits)
            return {"answer": f"질문: {question} -> {evidence}", "citations": citations}

        def main():
            print("오늘 주제:", TOPIC)
            docs = [
                {"id": 1, "text": "RAG는 검색 결과를 근거로 답한다"},
                {"id": 2, "text": "벡터 인덱스는 유사도 검색 속도를 높인다"},
                {"id": 3, "text": "프롬프트 템플릿은 출력 형식을 고정한다"},
            ]
            question = "RAG 답변 근거를 어떻게 확보하나요"
            hits = retrieve(question, docs)
            report = answer(question, hits)
            print("검색 히트:", [h["id"] for h in hits])
            print("응답:", report)
            return report
        """

    if template == "llm_gen":
        return """
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
        """

    return """
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
    """


def variant_brief(template: str) -> dict[str, str]:
    table: dict[str, dict[str, str]] = {
        "ml": {
            "mission": "학습 데이터에 이상치 1개를 추가하고 MAE 변화를 비교하세요.",
            "check": "baseline 대비 개선/악화 원인을 2줄로 설명하세요.",
            "challenge": "검증 데이터를 따로 두고 과적합 징후를 기록하세요.",
            "mini": "모델 버전 2개를 비교하고 채택 규칙을 코드로 만드세요.",
            "ops": "성능 저하 임계치와 롤백 조건을 정의하세요.",
        },
        "deep_learning": {
            "mission": "가중치와 bias를 2세트로 바꿔 출력 분포를 비교하세요.",
            "check": "활성화 함수 전/후 값을 표로 정리하세요.",
            "challenge": "입력 스케일 변화가 출력 안정성에 미치는 영향을 측정하세요.",
            "mini": "간단한 배치 추론 로그(입력/출력/latency)를 저장하세요.",
            "ops": "추론 실패 시 fallback 모델 호출 절차를 정의하세요.",
        },
        "rag": {
            "mission": "top_k 값을 바꿔 인용(citation) 품질 변화를 확인하세요.",
            "check": "근거 없는 문장이 섞이는 경우를 재현하고 차단 규칙을 추가하세요.",
            "challenge": "질문 재작성(query rewrite) 전/후 검색 결과를 비교하세요.",
            "mini": "검색 점수 임계치 기반 필터를 적용해 응답 품질을 높이세요.",
            "ops": "인덱스 갱신 주기와 실패 시 재시도 정책을 정하세요.",
        },
        "langchain": {
            "mission": "체인 단계 하나를 추가해 입력 검증을 자동화하세요.",
            "check": "각 단계 입력/출력을 로그로 남기고 병목을 찾으세요.",
            "challenge": "도구 호출 실패를 예외 처리해 회복 가능한 체인을 만드세요.",
            "mini": "state 객체에 trace_id를 넣고 단계별 추적 기능을 추가하세요.",
            "ops": "실패 단계 알림과 재실행 정책을 정의하세요.",
        },
        "llm_gen": {
            "mission": "temperature/top_p 조합 3개를 비교해 응답 품질을 점수화하세요.",
            "check": "환각 가능 문장에 '확인 필요' 태그를 붙이세요.",
            "challenge": "금칙어/민감어 필터를 커스터마이징하세요.",
            "mini": "입력 토큰 길이별 비용 추정기를 추가하세요.",
            "ops": "모델 장애 시 대체 모델 라우팅 규칙을 작성하세요.",
        },
        "speech": {
            "mission": "snr 임계값을 조정해 noisy 판정 변화를 비교하세요.",
            "check": "짧은 발화/긴 발화를 분리해 전처리 전략을 달리 적용하세요.",
            "challenge": "STT 오류가 많은 구간을 규칙 기반으로 탐지하세요.",
            "mini": "발화 단위 품질 리포트를 CSV로 내보내세요.",
            "ops": "실시간 처리 지연 임계치와 경보 조건을 정의하세요.",
        },
    }
    default = {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "challenge": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "mini": "미니 프로젝트 형태로 실행 로그를 구조화하세요.",
        "ops": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
    }
    return table.get(template, default)


def add_variant_tail(template: str, variant: int) -> str:
    brief = variant_brief(template)

    if variant == 1:
        return """
        if __name__ == "__main__":
            main()
        """

    if variant == 2:
        return f"""
        def extension_mission():
            return {{
                "mission": "{q(brief['mission'])}",
                "check": "{q(brief['check'])}",
                "topic": TOPIC,
            }}

        if __name__ == "__main__":
            summary = main()
            print("요약:", summary)
            print("확장 미션:", extension_mission())
        """

    if variant == 3:
        return f"""
        def self_check():
            return [
                "입력/출력 스키마를 문장으로 설명할 수 있는가?",
                "예외 입력을 최소 1개 이상 테스트했는가?",
                "결과를 재현 가능한 형태로 로그에 남겼는가?",
            ]

        def challenge_case():
            return {{
                "task": "{q(brief['challenge'])}",
                "goal": "핵심 변화 포인트를 3줄 요약",
            }}

        if __name__ == "__main__":
            summary = main()
            print("요약:", summary)
            print("자가 점검:", self_check())
            print("챌린지:", challenge_case())
        """

    if variant == 4:
        return f"""
        def mini_project_plan():
            return {{
                "scenario": "{q(brief['mini'])}",
                "steps": [
                    "1) baseline 실행",
                    "2) 개선안 적용",
                    "3) 지표/로그 비교",
                ],
                "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
            }}

        if __name__ == "__main__":
            summary = main()
            print("요약:", summary)
            print("미니 프로젝트:", mini_project_plan())
        """

    return f"""
    def ops_readiness_check():
        return {{
            "risk": "{q(brief['ops'])}",
            "monitoring": "핵심 지표를 1분 주기로 기록",
            "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
        }}

    if __name__ == "__main__":
        summary = main()
        print("요약:", summary)
        print("운영 준비 점검:", ops_readiness_check())
    """


def render_example_code(class_id: str, module: str, template: str, variant: int) -> str:
    base = dedent(build_body(template, class_id)).strip()
    tail = dedent(add_variant_tail(template, variant)).strip()
    return wrap_code(class_id, module, template, variant, base + "\n\n" + tail)


def rebuild_examples(rows: list[dict[str, str]]) -> int:
    written = 0
    for row in rows:
        class_id = row["class"]
        module = row["module"]
        subject = row["subject_name"]
        template = pick_template(module, subject)

        class_dir = class_dir_from_row(row)
        class_dir.mkdir(parents=True, exist_ok=True)

        variants = variants_for_row(row, class_dir=class_dir)
        for variant in variants:
            path = example_path(class_dir, class_id, variant)
            path.write_text(
                render_example_code(class_id, module, template, variant),
                encoding="utf-8",
                newline="\n",
            )
            written += 1

        # pyBasics는 기존 정책대로 example1~3만 유지
        if is_python_basics(row, class_dir=class_dir):
            for stale in (4, 5):
                stale_path = example_path(class_dir, class_id, stale)
                if stale_path.exists():
                    stale_path.unlink()

    return written


def validate_examples(rows: list[dict[str, str]]) -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0

    for row in rows:
        class_id = row["class"]
        module = row["module"]
        subject = row["subject_name"]
        expected = pick_template(module, subject)
        class_dir = class_dir_from_row(row)

        for variant in variants_for_row(row, class_dir=class_dir):
            path = example_path(class_dir, class_id, variant)
            checked += 1
            if not path.exists():
                errors.append(f"{path}: missing")
                continue

            text = path.read_text(encoding="utf-8")
            if f'TOPIC = "{q(module)}"' not in text:
                errors.append(f"{path}: TOPIC mismatch")
            if f'EXAMPLE_TEMPLATE = "{expected}"' not in text:
                errors.append(f"{path}: template mismatch")
            if COPYRIGHT_TEXT not in text:
                errors.append(f"{path}: copyright notice missing")

            try:
                py_compile.compile(str(path), doraise=True)
            except Exception as exc:
                errors.append(f"{path}: compile error: {exc}")

    return checked, errors


def main() -> None:
    rows = read_rows()
    written = rebuild_examples(rows)
    checked, errors = validate_examples(rows)

    print(f"Rows: {len(rows)}")
    print(f"Examples rebuilt: {written}")
    print(f"Validation checked: {checked}")
    print(f"Validation errors: {len(errors)}")
    if errors:
        print("--- errors (first 30) ---")
        for err in errors[:30]:
            print(err)


if __name__ == "__main__":
    main()
