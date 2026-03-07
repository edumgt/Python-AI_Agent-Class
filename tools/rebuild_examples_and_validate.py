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
    with INDEX_FILE.open(encoding="utf-8", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(k).lstrip("\ufeff"): v for k, v in raw.items()})
    return rows


def pick_template(module: str, subject: str) -> str:
    module_text = module.lower()
    subject_text = subject.lower()
    text = f"{subject_text} {module_text}"

    # 1) module(차시 주제) 우선 매핑
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

    # 2) subject(교과목) 보조 매핑
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


def wrap_code(class_id: str, module: str, template: str, variant: int, body: str) -> str:
    doc = f'"""{class_id} example{variant}: {module}"""'
    header = dedent(
        f"""\
        # {COPYRIGHT_TEXT}

        {doc}

        TOPIC = "{module}"
        EXAMPLE_TEMPLATE = "{template}"
        """
    )
    return header + "\n" + dedent(body).strip() + "\n"


def render_example_code(class_id: str, module: str, template: str, variant: int) -> str:
    if template == "dev_setup":
        body = """
        def checklist():
            return [
                "python -m venv .venv",
                "가상환경 활성화",
                "pip install -r requirements.txt",
            ]

        def main():
            print("오늘 주제:", TOPIC)
            for idx, step in enumerate(checklist(), start=1):
                print(f"{idx}. {step}")
        """
    elif template == "variables":
        body = """
        def inspect_values():
            sample = {"name": "민수", "age": 11, "height": 140.5, "is_student": True}
            return {k: type(v).__name__ for k, v in sample.items()}

        def main():
            print("오늘 주제:", TOPIC)
            print("자료형 확인:", inspect_values())
        """
    elif template == "condition":
        body = """
        def grade(score):
            if score >= 90:
                return "A"
            if score >= 80:
                return "B"
            if score >= 70:
                return "C"
            return "D"

        def main():
            score = 86
            print("오늘 주제:", TOPIC)
            print(f"점수 {score} -> 등급 {grade(score)}")
        """
    elif template == "loop":
        body = """
        def even_sum(limit):
            total = 0
            for n in range(1, limit + 1):
                if n % 2 == 0:
                    total += n
            return total

        def main():
            print("오늘 주제:", TOPIC)
            print("1~10 짝수 합:", even_sum(10))
        """
    elif template == "function_module":
        body = """
        import math

        def area_circle(radius):
            return round(math.pi * radius * radius, 2)

        def main():
            r = 3
            print("오늘 주제:", TOPIC)
            print(f"반지름 {r} 원의 넓이:", area_circle(r))
        """
    elif template == "collection":
        body = """
        def summarize_scores(scores):
            return {
                "count": len(scores),
                "max": max(scores),
                "min": min(scores),
                "avg": round(sum(scores) / len(scores), 2),
            }

        def main():
            scores = [75, 88, 92, 81]
            print("오늘 주제:", TOPIC)
            print("요약:", summarize_scores(scores))
        """
    elif template == "file_io":
        body = f"""
        from pathlib import Path

        def save_and_read(text):
            out = Path(__file__).with_name("{class_id}_note.txt")
            out.write_text(text, encoding="utf-8")
            return out.read_text(encoding="utf-8")

        def main():
            print("오늘 주제:", TOPIC)
            msg = "파일에 저장하고 다시 읽기 성공"
            loaded = save_and_read(msg)
            print("읽은 내용:", loaded)
        """
    elif template == "exception":
        body = """
        def safe_divide(a, b):
            try:
                return a / b
            except ZeroDivisionError:
                return "0으로 나눌 수 없어요."

        def main():
            print("오늘 주제:", TOPIC)
            print("10 / 2 =", safe_divide(10, 2))
            print("10 / 0 =", safe_divide(10, 0))
        """
    elif template == "oop":
        body = """
        class Student:
            def __init__(self, name, level):
                self.name = name
                self.level = level

            def introduce(self):
                return f"안녕하세요, 저는 {self.name}이고 {self.level} 단계예요."

        def main():
            print("오늘 주제:", TOPIC)
            student = Student("지유", "기초응용")
            print(student.introduce())
        """
    elif template == "numpy":
        body = """
        import numpy as np

        def stats(values):
            arr = np.array(values, dtype=float)
            return float(arr.mean()), float(arr.std())

        def main():
            print("오늘 주제:", TOPIC)
            mean, std = stats([10, 20, 30, 40])
            print("평균:", round(mean, 2), "표준편차:", round(std, 2))
        """
    elif template == "pandas":
        body = """
        import pandas as pd

        def build_frame():
            df = pd.DataFrame(
                [
                    {"name": "민수", "score": 90},
                    {"name": "지유", "score": 85},
                ]
            )
            df["pass"] = df["score"] >= 80
            return df

        def main():
            print("오늘 주제:", TOPIC)
            print(build_frame())
        """
    elif template == "visualization":
        body = f"""
        from pathlib import Path
        import matplotlib.pyplot as plt

        def make_plot():
            x = [1, 2, 3, 4]
            y = [2, 4, 3, 5]
            plt.figure(figsize=(4, 3))
            plt.plot(x, y, marker="o")
            plt.title(TOPIC)
            out = Path(__file__).with_name("{class_id}_plot.png")
            plt.tight_layout()
            plt.savefig(out)
            plt.close()
            return out

        def main():
            print("오늘 주제:", TOPIC)
            print("그래프 저장:", make_plot())
        """
    elif template == "data_preprocess":
        body = """
        from datetime import datetime

        def clean_rows(rows):
            cleaned = []
            for row in rows:
                text = row["text"].strip().lower()
                date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
                cleaned.append({"text": text, "month": date_obj.month})
            return cleaned

        def main():
            rows = [
                {"text": "  Hello AI  ", "date": "2026-03-01"},
                {"text": "Data  Prep ", "date": "2026-04-02"},
            ]
            print("오늘 주제:", TOPIC)
            print(clean_rows(rows))
        """
    elif template == "ml":
        body = """
        def make_data():
            return [(1, 52), (2, 61), (3, 70), (4, 82)]

        def mean_predict(train):
            return sum(y for _, y in train) / len(train)

        def mae(train, pred):
            return sum(abs(y - pred) for _, y in train) / len(train)

        def main():
            data = make_data()
            pred = mean_predict(data)
            print("오늘 주제:", TOPIC)
            print("기본 예측값:", round(pred, 2))
            print("MAE:", round(mae(data, pred), 2))
        """
    elif template == "deep_learning":
        body = """
        def relu(x):
            return x if x > 0 else 0

        def dense_step(inputs, weights, bias):
            total = sum(i * w for i, w in zip(inputs, weights)) + bias
            return relu(total)

        def main():
            print("오늘 주제:", TOPIC)
            out = dense_step([0.8, -0.2, 0.5], [0.4, 0.6, 0.3], 0.1)
            print("뉴런 출력:", round(out, 3))
        """
    elif template == "nlp":
        body = """
        def tokenize(text):
            cleaned = text.replace(",", " ").replace(".", " ")
            return [tok.lower() for tok in cleaned.split() if tok]

        def top_words(tokens):
            freq = {}
            for tok in tokens:
                freq[tok] = freq.get(tok, 0) + 1
            return sorted(freq.items(), key=lambda x: x[1], reverse=True)

        def main():
            print("오늘 주제:", TOPIC)
            tokens = tokenize("AI 수업은 재미있고, AI 실습은 유익하다.")
            print("토큰:", tokens)
            print("빈도:", top_words(tokens))
        """
    elif template == "speech":
        body = """
        def summarize_clips(clips):
            avg = sum(c["seconds"] for c in clips) / len(clips)
            short = [c["id"] for c in clips if c["seconds"] <= 2.0]
            return {"avg_seconds": round(avg, 2), "short_ids": short}

        def main():
            clips = [
                {"id": "utt1", "seconds": 1.3, "text": "안녕하세요"},
                {"id": "utt2", "seconds": 2.4, "text": "오늘은 음성 실습"},
                {"id": "utt3", "seconds": 1.8, "text": "반가워요"},
            ]
            print("오늘 주제:", TOPIC)
            print(summarize_clips(clips))
        """
    elif template == "prompt":
        body = """
        def build_prompt(role, question):
            return (
                f"너는 {role}이야.\\n"
                f"질문: {question}\\n"
                "답변은 3줄 이내로 핵심만 설명해."
            )

        def main():
            print("오늘 주제:", TOPIC)
            print(build_prompt("친절한 과학 선생님", "중력이 뭐야?"))
        """
    elif template == "langchain":
        body = """
        def step_collect(question):
            return {"question": question}

        def step_plan(state):
            return {"question": state["question"], "plan": "핵심 개념 3개로 설명"}

        def step_answer(state):
            return f"[응답] {state['question']} -> {state['plan']}"

        def main():
            print("오늘 주제:", TOPIC)
            s1 = step_collect("RAG가 뭐야?")
            s2 = step_plan(s1)
            print(step_answer(s2))
        """
    elif template == "rag":
        body = """
        def retrieve(question, docs):
            q = set(question.split())
            scored = []
            for doc in docs:
                overlap = len(q & set(doc["text"].split()))
                scored.append((overlap, doc))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [doc for score, doc in scored if score > 0][:2]

        def answer(question, docs):
            if not docs:
                return "관련 문서를 찾지 못했어요."
            joined = " / ".join(d["text"] for d in docs)
            return f"질문: {question}\\n근거: {joined}"

        def main():
            docs = [
                {"id": 1, "text": "RAG는 검색 결과를 근거로 답변한다"},
                {"id": 2, "text": "벡터 검색으로 관련 문서를 찾는다"},
                {"id": 3, "text": "프롬프트 설계도 중요하다"},
            ]
            q = "RAG 답변 근거"
            picked = retrieve(q, docs)
            print("오늘 주제:", TOPIC)
            print("선택 문서:", [d["id"] for d in picked])
            print(answer(q, picked))
        """
    elif template == "llm_gen":
        body = """
        def build_generation_config():
            return {"temperature": 0.7, "max_tokens": 200, "top_p": 0.9}

        def simulate_response(prompt, cfg):
            return f"[생성 결과]\\n프롬프트: {prompt}\\n설정: {cfg}"

        def main():
            cfg = build_generation_config()
            print("오늘 주제:", TOPIC)
            print(simulate_response("한 줄 자기소개를 써줘", cfg))
        """
    else:
        body = """
        def solve_in_steps(task):
            return [f"1단계: {task} 이해", "2단계: 작은 예제 작성", "3단계: 결과 확인"]

        def main():
            print("오늘 주제:", TOPIC)
            for line in solve_in_steps(TOPIC):
                print(line)
        """

    # example2 adds extension mission and richer output while keeping topic fit.
    if variant == 2:
        body += """

        def extension_mission():
            return {
                "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
                "check": "결과 차이를 한 줄로 설명하기",
            }

        if __name__ == "__main__":
            main()
            print("확장 미션:", extension_mission())
        """
    else:
        body += """

        if __name__ == "__main__":
            main()
        """

    return wrap_code(class_id, module, template, variant, body)


def rebuild_examples(rows: list[dict[str, str]]) -> None:
    for row in rows:
        class_id = row["class"]
        module = row["module"]
        subject = row["subject_name"]
        template = pick_template(module, subject)

        class_dir = ROOT / class_id
        example1 = class_dir / f"{class_id}_example.py"
        example2 = class_dir / f"{class_id}_example2.py"

        example1.write_text(render_example_code(class_id, module, template, 1), encoding="utf-8", newline="\n")
        example2.write_text(render_example_code(class_id, module, template, 2), encoding="utf-8", newline="\n")


def validate_examples(rows: list[dict[str, str]]) -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0

    for row in rows:
        class_id = row["class"]
        module = row["module"]
        subject = row["subject_name"]
        expected = pick_template(module, subject)
        class_dir = ROOT / class_id

        for suffix in ("example", "example2"):
            path = class_dir / f"{class_id}_{suffix}.py"
            checked += 1
            if not path.exists():
                errors.append(f"{path}: missing")
                continue

            text = path.read_text(encoding="utf-8")
            if f'TOPIC = "{module}"' not in text:
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
    rebuild_examples(rows)
    checked, errors = validate_examples(rows)

    print(f"Examples rebuilt: {len(rows) * 2}")
    print(f"Validation checked: {checked}")
    print(f"Validation errors: {len(errors)}")
    if errors:
        print("--- errors (first 30) ---")
        for err in errors[:30]:
            print(err)


if __name__ == "__main__":
    main()
