# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


TRACK_QUIZ_BANK = {
    "python": {
        "concept": "입력값을 조건문과 반복문으로 처리해 원하는 출력으로 만든다.",
        "action": "작은 입력부터 실행하고 print()로 중간 값을 확인한다.",
        "outcome": "함수로 코드를 분리해 재사용성과 가독성을 높인다.",
    },
    "data": {
        "concept": "데이터 전처리로 열 구조를 정리한 뒤 통계를 계산한다.",
        "action": "columns와 shape를 먼저 확인하고 계산 순서를 정한다.",
        "outcome": "정리된 표 데이터로 의미 있는 패턴을 설명할 수 있다.",
    },
    "ml": {
        "concept": "입력(X)과 정답(y)을 사용해 예측 규칙(모델)을 학습한다.",
        "action": "X/y 형태를 점검하고 오차를 계산해 품질을 확인한다.",
        "outcome": "예측 결과와 오차를 해석해 개선 아이디어를 낼 수 있다.",
    },
    "nlp": {
        "concept": "문장을 정제하고 토큰으로 나눠 패턴을 분석한다.",
        "action": "전처리 후 토큰 리스트를 먼저 출력해 결과를 점검한다.",
        "outcome": "주요 단어 빈도를 계산해 핵심 내용을 찾을 수 있다.",
    },
    "speech": {
        "concept": "음성 데이터는 길이, 텍스트 라벨, 품질 정보를 함께 다룬다.",
        "action": "샘플 발화를 몇 개 확인하고 길이/라벨 기준으로 필터링한다.",
        "outcome": "음성 데이터 품질 지표를 계산하고 해석할 수 있다.",
    },
    "prompt": {
        "concept": "역할(role), 목표(goal), 형식(format)을 분명히 써야 답변 품질이 오른다.",
        "action": "템플릿 변수(role, question)를 분리해 프롬프트를 구성한다.",
        "outcome": "좋은 프롬프트와 나쁜 프롬프트의 차이를 설명할 수 있다.",
    },
    "langchain": {
        "concept": "작업을 단계별 체인으로 분리하면 재사용과 디버깅이 쉬워진다.",
        "action": "각 단계의 입력/출력을 출력해 흐름을 먼저 검증한다.",
        "outcome": "단계 함수를 조합해 반복 가능한 워크플로우를 만들 수 있다.",
    },
    "rag": {
        "concept": "질문과 관련 문서를 검색하고 근거를 바탕으로 답변을 만든다.",
        "action": "검색 결과와 최종 답변을 분리해서 출력한다.",
        "outcome": "답변에 출처를 포함해 신뢰도를 높일 수 있다.",
    },
    "generic": {
        "concept": "복잡한 문제를 작은 단계로 나누면 해결이 쉬워진다.",
        "action": "TODO를 1개씩 구현하고 매 단계마다 실행 확인한다.",
        "outcome": "문제를 구조화해 스스로 학습 흐름을 만들 수 있다.",
    },
}


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))

    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return rows


def choose_track(subject_name: str, module: str) -> str:
    text = f"{subject_name} {module}"
    lowered = text.lower()
    if "rag" in lowered or "retrieval-augmented generation" in lowered:
        return "rag"
    if "langchain" in lowered:
        return "langchain"
    if any(keyword in text for keyword in ["프롬프트", "LLM", "언어모델", "생성 파라미터", "응답 설계"]):
        return "prompt"
    if any(keyword in text for keyword in ["음성", "TTS", "STT", "오디오", "발화", "화자"]):
        return "speech"
    if any(keyword in text for keyword in ["자연어", "NLP", "텍스트", "토큰", "임베딩", "시퀀스"]):
        return "nlp"
    if any(keyword in text for keyword in ["머신러닝", "딥러닝", "회귀", "분류", "모델", "학습", "MSE"]):
        return "ml"
    if any(keyword in text for keyword in ["전처리", "시각화", "데이터프레임", "pandas", "numpy"]):
        return "data"
    if "python" in lowered:
        return "python"
    return "generic"


def stable_sample(pool: list[str], k: int, seed: str) -> list[str]:
    unique = list(dict.fromkeys(pool))
    if len(unique) < k:
        return unique
    rng = random.Random(seed)
    return rng.sample(unique, k)


def build_question(
    question: str,
    correct: str,
    candidates: list[str],
    seed: str,
    explanation: str,
) -> dict:
    distractors = stable_sample([x for x in candidates if x != correct], 3, seed)
    options = [correct] + distractors
    rng = random.Random(seed + "-shuffle")
    rng.shuffle(options)
    return {
        "question": question,
        "options": options,
        "answer_index": options.index(correct),
        "explanation": explanation,
    }


def build_quiz_payload(row: dict[str, str], rows: list[dict[str, str]]) -> dict:
    class_id = row["class"]
    subject_name = row["subject_name"]
    module = row["module"]
    level = row["level"]
    day = int(row["day"])
    slot = int(row["slot"])
    session = row["subject_session"]
    track = choose_track(subject_name, module)
    bank = TRACK_QUIZ_BANK[track]

    same_subject_modules = [r["module"] for r in rows if r["subject_name"] == subject_name]
    all_concepts = [TRACK_QUIZ_BANK[t]["concept"] for t in TRACK_QUIZ_BANK]
    all_actions = [TRACK_QUIZ_BANK[t]["action"] for t in TRACK_QUIZ_BANK]

    questions = [
        build_question(
            question="이번 차시의 핵심 학습 주제로 가장 알맞은 것은 무엇인가요?",
            correct=module,
            candidates=same_subject_modules if len(same_subject_modules) >= 4 else [r["module"] for r in rows],
            seed=f"{class_id}-q1-module",
            explanation=f"정답은 '{module}' 입니다.",
        ),
        build_question(
            question=f"'{module}'를 학습할 때 핵심 개념으로 가장 적절한 설명은 무엇인가요?",
            correct=bank["concept"],
            candidates=all_concepts,
            seed=f"{class_id}-q2-concept",
            explanation="핵심 개념은 수업 주제의 기본 원리를 정확히 설명해야 합니다.",
        ),
        build_question(
            question=f"'{module}' 실습을 시작할 때 가장 좋은 방법은 무엇인가요?",
            correct=bank["action"],
            candidates=all_actions,
            seed=f"{class_id}-q3-action",
            explanation="정답은 실제 실습 성공률을 높이는 시작 루틴입니다.",
        ),
    ]

    return {
        "class_id": class_id,
        "subject_name": subject_name,
        "module": module,
        "level": level,
        "session": session,
        "track_outcome": bank["outcome"],
        "questions": questions,
        "day": day,
        "slot": slot,
    }


def build_quiz_html(row: dict[str, str], rows: list[dict[str, str]]) -> str:
    payload = build_quiz_payload(row, rows)
    quiz_json = json.dumps(payload, ensure_ascii=False, indent=2)
    class_id = payload["class_id"]
    module = payload["module"]
    subject_name = payload["subject_name"]
    session = payload["session"]
    level = payload["level"]
    day = payload["day"]
    slot = payload["slot"]

    html = f"""<!doctype html>
<!-- {COPYRIGHT_TEXT} -->
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{class_id} 3문항 퀴즈</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-slate-100 text-slate-900">
  <main class="mx-auto max-w-3xl px-4 py-10">
    <section class="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <p class="text-sm font-semibold text-sky-700">{class_id} SELF QUIZ</p>
      <h1 class="mt-2 text-2xl font-bold">{module}</h1>
      <p class="mt-2 text-sm text-slate-600">
        교과목: {subject_name} · 세부 시퀀스: {session} · 난이도: {level} · Day {day:02d} / {slot}교시
      </p>
      <p class="mt-4 rounded-lg bg-slate-50 p-3 text-sm text-slate-700">
        학습 내용 기반 3문항 퀴즈입니다. 정답을 고른 뒤 채점 버튼을 누르세요.
      </p>
    </section>

    <section id="quiz-root" class="mt-6 space-y-4"></section>

    <div class="mt-6 flex items-center gap-3">
      <button id="grade-btn" class="rounded-lg bg-sky-600 px-5 py-2 text-sm font-semibold text-white hover:bg-sky-700">
        채점하기
      </button>
      <button id="reset-btn" class="rounded-lg bg-slate-200 px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-300">
        다시풀기
      </button>
    </div>

    <section id="result-root" class="mt-6 hidden rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200"></section>
  </main>

  <script>
    const QUIZ_DATA = {quiz_json};

    function renderQuiz() {{
      const root = document.getElementById("quiz-root");
      root.innerHTML = "";

      QUIZ_DATA.questions.forEach((q, qIndex) => {{
        const wrap = document.createElement("article");
        wrap.className = "rounded-xl bg-white p-5 shadow-sm ring-1 ring-slate-200";

        const title = document.createElement("h2");
        title.className = "text-base font-semibold";
        title.textContent = `${{qIndex + 1}}번. ${{q.question}}`;
        wrap.appendChild(title);

        const list = document.createElement("div");
        list.className = "mt-3 space-y-2";

        q.options.forEach((opt, optIndex) => {{
          const label = document.createElement("label");
          label.className = "flex cursor-pointer items-start gap-2 rounded-lg border border-slate-200 p-3 hover:bg-slate-50";

          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = `q-${{qIndex}}`;
          radio.value = String(optIndex);
          radio.className = "mt-1";

          const text = document.createElement("span");
          text.className = "text-sm";
          text.textContent = opt;

          label.appendChild(radio);
          label.appendChild(text);
          list.appendChild(label);
        }});

        wrap.appendChild(list);
        root.appendChild(wrap);
      }});
    }}

    function gradeQuiz() {{
      let score = 0;
      const details = [];

      QUIZ_DATA.questions.forEach((q, qIndex) => {{
        const selected = document.querySelector(`input[name="q-${{qIndex}}"]:checked`);
        const selectedIndex = selected ? Number(selected.value) : -1;
        const isCorrect = selectedIndex === q.answer_index;
        if (isCorrect) score += 1;

        details.push({{
          number: qIndex + 1,
          isCorrect,
          correct: q.options[q.answer_index],
          chosen: selectedIndex >= 0 ? q.options[selectedIndex] : "미선택",
          explanation: q.explanation
        }});
      }});

      const resultRoot = document.getElementById("result-root");
      resultRoot.classList.remove("hidden");

      const headerClass = score === 3 ? "text-emerald-700" : "text-amber-700";
      const summary = `
        <h3 class="text-lg font-bold ${{headerClass}}">점수: ${{score}} / 3</h3>
        <p class="mt-1 text-sm text-slate-600">틀린 문제는 해설을 확인하고 다시 풀어보세요.</p>
        <p class="mt-1 text-sm text-slate-600">학습 성과 힌트: ${{QUIZ_DATA.track_outcome}}</p>
      `;

      const rows = details.map((d) => `
        <li class="rounded-lg border border-slate-200 p-3">
          <p class="text-sm font-semibold">${{d.number}}번 - ${{d.isCorrect ? "정답" : "오답"}}</p>
          <p class="mt-1 text-sm">내 답: ${{d.chosen}}</p>
          <p class="text-sm">정답: ${{d.correct}}</p>
          <p class="mt-1 text-xs text-slate-500">${{d.explanation}}</p>
        </li>
      `).join("");

      resultRoot.innerHTML = `
        ${{summary}}
        <ul class="mt-4 space-y-2">${{rows}}</ul>
      `;
    }}

    function resetQuiz() {{
      document.querySelectorAll('input[type="radio"]').forEach((el) => {{
        el.checked = false;
      }});
      const resultRoot = document.getElementById("result-root");
      resultRoot.classList.add("hidden");
      resultRoot.innerHTML = "";
    }}

    document.getElementById("grade-btn").addEventListener("click", gradeQuiz);
    document.getElementById("reset-btn").addEventListener("click", resetQuiz);
    renderQuiz();
  </script>
</body>
</html>
"""
    return dedent(html)


def build_launcher_py(class_id: str) -> str:
    return dedent(
        f'''\
        # {COPYRIGHT_TEXT}
        """
        {class_id} launcher
        - 기본 실행: {class_id}_example.py
        - 과제 실행: {class_id}_assignment.py
        - 정답 실행: {class_id}_solution.py
        """
        from __future__ import annotations

        import os
        import runpy
        from pathlib import Path

        HERE = Path(__file__).resolve().parent
        CLASS_ID = Path(__file__).resolve().stem

        if __name__ == "__main__":
            target = (os.getenv("CLASS_RUN_TARGET") or "example").strip().lower()
            mapping = {{
                "example": f"{{CLASS_ID}}_example.py",
                "assignment": f"{{CLASS_ID}}_assignment.py",
                "solution": f"{{CLASS_ID}}_solution.py",
            }}
            file_name = mapping.get(target)
            if file_name is None:
                raise SystemExit("Unknown CLASS_RUN_TARGET (use example/assignment/solution)")

            py_file = HERE / file_name
            if not py_file.exists() and target == "example":
                # 예제 파일이 없으면 기존 과제 실행으로 안전하게 폴백
                py_file = HERE / f"{{CLASS_ID}}_assignment.py"

            if not py_file.exists():
                raise SystemExit(f"Run target not found: {{py_file}}")

            runpy.run_path(str(py_file), run_name="__main__")
        '''
    )


def rebuild_launchers_and_quizzes() -> None:
    rows = read_rows()
    launcher_count = 0
    quiz_count = 0

    for row in rows:
        class_id = row["class"]
        class_dir = ROOT / class_id

        launcher_path = class_dir / f"{class_id}.py"
        launcher_path.write_text(build_launcher_py(class_id), encoding="utf-8", newline="\n")
        launcher_count += 1

        quiz_path = class_dir / f"{class_id}_quiz.html"
        quiz_path.write_text(build_quiz_html(row, rows), encoding="utf-8", newline="\n")
        quiz_count += 1

    print(f"Updated launchers: {launcher_count}")
    print(f"Created quiz html files: {quiz_count}")


if __name__ == "__main__":
    rebuild_launchers_and_quizzes()
