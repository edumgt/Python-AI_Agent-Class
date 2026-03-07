# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


TRACK_INFO = {
    "python": {
        "kid_summary": "코드를 작은 블록처럼 조립하면서 문제를 해결하는 방법을 배워요.",
        "why": "컴퓨터에게 순서대로 일을 시키는 힘을 키우면, 복잡한 문제도 차근차근 풀 수 있어요.",
        "concepts": [
            "입력값을 받아서 규칙대로 처리한 뒤 결과를 출력해요.",
            "조건문과 반복문으로 '언제/몇 번' 실행할지 정해요.",
            "함수로 코드를 나누면 읽기 쉽고 재사용하기 쉬워요.",
        ],
        "analogy": "레고를 만들 때 설명서 순서대로 블록을 끼우는 것과 같아요.",
        "practice_steps": [
            "예제 파일을 실행해서 결과 문장을 먼저 확인해요.",
            "숫자나 문자열 값을 바꿔 보며 결과가 어떻게 달라지는지 관찰해요.",
            "비슷한 기능을 함수 하나 더 만들어 스스로 확장해 봐요.",
        ],
        "checklist": [
            "코드가 오류 없이 끝까지 실행된다.",
            "변수 이름만 보고도 역할을 설명할 수 있다.",
            "같은 기능을 다른 입력으로 다시 테스트했다.",
        ],
        "next_tip": "다음 차시에서는 오늘 만든 규칙을 더 큰 문제에 연결해 볼 거예요.",
    },
    "data": {
        "kid_summary": "표 형태 데이터를 정리하고, 눈으로 이해하기 쉽게 만드는 방법을 배워요.",
        "why": "정리된 데이터는 실수를 줄여 주고, 중요한 패턴을 빨리 발견하게 도와줘요.",
        "concepts": [
            "데이터는 수집 후 바로 쓰지 않고 먼저 정리(전처리)해야 해요.",
            "열(column) 이름을 명확하게 두면 분석 과정이 쉬워져요.",
            "평균, 합계 같은 간단한 통계로도 큰 힌트를 얻을 수 있어요.",
        ],
        "analogy": "지저분한 책상을 정리하면 필요한 물건을 빨리 찾을 수 있는 것과 같아요.",
        "practice_steps": [
            "예제 데이터를 보고 어떤 열이 있는지 소리 내어 읽어 봐요.",
            "점수/길이 같은 숫자 열의 평균을 직접 계산해 봐요.",
            "출력 순서를 바꿔서 내가 보기 편한 리포트를 만들어 봐요.",
        ],
        "checklist": [
            "데이터 항목 이름을 정확히 이해했다.",
            "정리 전/정리 후 차이를 설명할 수 있다.",
            "평균/최댓값/최솟값 중 1개 이상을 계산했다.",
        ],
        "next_tip": "다음 차시에서는 더 큰 데이터에서도 같은 정리 원칙을 적용해 볼 거예요.",
    },
    "ml": {
        "kid_summary": "데이터를 보고 규칙을 찾는 '작은 모델' 사고법을 배워요.",
        "why": "정답을 외우는 대신 규칙을 찾으면 새로운 문제도 스스로 예측할 수 있어요.",
        "concepts": [
            "모델은 입력을 받아 예측값을 만들어요.",
            "예측값과 실제값의 차이(오차)를 확인해야 실력이 늘어요.",
            "작은 데이터로 원리를 이해한 뒤 큰 데이터로 확장해요.",
        ],
        "analogy": "농구 슛 연습에서 '던진 거리와 결과'를 보고 감을 조절하는 것과 비슷해요.",
        "practice_steps": [
            "예제의 입력/정답 쌍을 먼저 표처럼 정리해 봐요.",
            "평균 기반 예측처럼 가장 쉬운 모델부터 실행해 봐요.",
            "오차가 큰 항목을 찾아 이유를 한 문장으로 적어 봐요.",
        ],
        "checklist": [
            "입력값과 정답값의 의미를 설명할 수 있다.",
            "예측 결과와 오차를 직접 확인했다.",
            "오차를 줄이기 위한 아이디어를 1개 이상 말했다.",
        ],
        "next_tip": "다음 차시에서는 더 정확한 예측을 위해 특징(feature)을 늘려 볼 거예요.",
    },
    "nlp": {
        "kid_summary": "문장을 컴퓨터가 다루기 쉬운 형태(단어, 토큰)로 바꾸는 방법을 배워요.",
        "why": "문장을 숫자/토큰으로 바꾸면 검색, 분류, 요약 같은 작업을 자동화할 수 있어요.",
        "concepts": [
            "텍스트 전처리로 공백/기호를 정리해요.",
            "토큰화로 문장을 작은 단위로 나눠요.",
            "단어 빈도 계산으로 중요한 단어를 찾을 수 있어요.",
        ],
        "analogy": "긴 문장을 단어 카드로 잘라서 분류하는 놀이와 같아요.",
        "practice_steps": [
            "예제 문장을 토큰 리스트로 바꿔 결과를 확인해요.",
            "가장 자주 나온 단어를 찾아 이유를 말해요.",
            "문장을 1개 추가하고 빈도 순위가 바뀌는지 확인해요.",
        ],
        "checklist": [
            "토큰화 전/후 차이를 설명할 수 있다.",
            "불필요한 기호 제거 이유를 설명할 수 있다.",
            "빈도 상위 단어를 3개 이상 찾았다.",
        ],
        "next_tip": "다음 차시에서는 토큰을 숫자 벡터로 바꿔 모델에 넣어 볼 거예요.",
    },
    "speech": {
        "kid_summary": "사람의 목소리 데이터를 구조적으로 다루는 방법을 배워요.",
        "why": "음성 데이터를 잘 다루면 TTS/STT처럼 실제 서비스에 쓰이는 기능을 만들 수 있어요.",
        "concepts": [
            "음성 데이터는 파일 경로, 길이, 텍스트 라벨이 함께 필요해요.",
            "전처리로 잡음을 줄이고 규격을 맞추면 모델 성능이 안정돼요.",
            "평가 지표를 통해 품질을 숫자로 확인해요.",
        ],
        "analogy": "노래 경연 점수를 매길 때 음정, 박자, 발음을 항목별로 보는 것과 비슷해요.",
        "practice_steps": [
            "예제의 발화 목록을 보고 길이/텍스트를 확인해요.",
            "조건에 맞는 데이터만 골라 새 리스트를 만들어 봐요.",
            "평균 길이와 최대 길이를 계산해 품질 기준을 세워 봐요.",
        ],
        "checklist": [
            "음성 샘플 하나를 데이터 항목으로 설명할 수 있다.",
            "필터링 조건을 바꿔 결과 변화를 확인했다.",
            "품질 확인용 숫자 지표를 1개 이상 계산했다.",
        ],
        "next_tip": "다음 차시에서는 텍스트와 음성을 연결하는 파이프라인을 다뤄요.",
    },
    "prompt": {
        "kid_summary": "좋은 질문(프롬프트)을 설계해서 AI 답변 품질을 높이는 방법을 배워요.",
        "why": "같은 AI라도 질문 방식이 다르면 답변 품질이 크게 달라져요.",
        "concepts": [
            "역할(role), 목표(goal), 형식(format)을 명확히 쓰면 답이 좋아져요.",
            "입력 변수를 분리하면 재사용 가능한 템플릿이 돼요.",
            "평가 기준을 먼저 정하면 결과를 고치기 쉬워요.",
        ],
        "analogy": "친구에게 길을 물을 때 목적지와 조건을 정확히 말해야 정확한 답을 듣는 것과 같아요.",
        "practice_steps": [
            "예제 템플릿에서 역할과 질문을 바꿔 실행해 봐요.",
            "답변 형식을 3줄 요약으로 제한해 봐요.",
            "좋은 프롬프트와 나쁜 프롬프트를 한 쌍 비교해 봐요.",
        ],
        "checklist": [
            "역할/목표/형식을 각각 설명할 수 있다.",
            "템플릿 변수 2개 이상을 직접 바꿨다.",
            "출력 품질이 왜 달라졌는지 설명할 수 있다.",
        ],
        "next_tip": "다음 차시에서는 프롬프트를 체인으로 묶어 복잡한 작업을 수행해요.",
    },
    "langchain": {
        "kid_summary": "작은 작업들을 순서대로 연결해 큰 AI 작업을 만드는 방법을 배워요.",
        "why": "체인 구조를 쓰면 반복 가능한 워크플로우를 만들 수 있어요.",
        "concepts": [
            "입력 -> 처리 -> 출력의 단계를 명확히 분리해요.",
            "각 단계 함수는 한 가지 책임만 갖게 만들어요.",
            "체인 중간 결과를 기록하면 디버깅이 쉬워져요.",
        ],
        "analogy": "샌드위치를 만들 때 재료 준비, 굽기, 포장을 단계별로 나누는 것과 같아요.",
        "practice_steps": [
            "예제의 단계 함수를 하나씩 실행해 중간 결과를 확인해요.",
            "중간 단계에 로그 문장을 추가해 흐름을 추적해요.",
            "새 단계 하나를 넣어 체인을 확장해 봐요.",
        ],
        "checklist": [
            "단계별 입력/출력을 설명할 수 있다.",
            "중간 결과를 출력해 흐름을 확인했다.",
            "단계 순서를 바꿨을 때 변화도 실험했다.",
        ],
        "next_tip": "다음 차시에서는 체인에 검색과 메모리를 결합해 볼 거예요.",
    },
    "rag": {
        "kid_summary": "질문과 관련된 자료를 먼저 찾고, 그 자료를 바탕으로 답하는 방법을 배워요.",
        "why": "기억만으로 답하는 것보다 자료를 근거로 답하면 더 정확하고 믿을 수 있어요.",
        "concepts": [
            "검색 단계에서 질문과 비슷한 문서를 찾아요.",
            "찾은 문서를 컨텍스트로 넣어 답변을 생성해요.",
            "출처를 함께 보여 주면 답의 신뢰도가 올라가요.",
        ],
        "analogy": "시험 문제를 풀 때 교과서 해당 페이지를 먼저 찾고 답을 쓰는 방식과 같아요.",
        "practice_steps": [
            "예제 문서 목록에서 질문과 가장 비슷한 문서를 찾아요.",
            "검색 결과 1~2개만 사용해 요약 답변을 만드세요.",
            "출처 문장 번호를 함께 출력해 근거를 표시해요.",
        ],
        "checklist": [
            "질문과 문서의 연결 기준을 설명할 수 있다.",
            "검색 결과와 최종 답변을 구분해서 출력했다.",
            "근거(출처)를 답변에 포함했다.",
        ],
        "next_tip": "다음 차시에서는 검색 품질을 높이는 인덱싱 전략을 배워요.",
    },
    "generic": {
        "kid_summary": "복잡한 주제도 작은 단계로 나눠서 차근차근 배우는 연습을 해요.",
        "why": "문제를 작게 나누는 습관이 있으면 어떤 새 주제도 스스로 배울 수 있어요.",
        "concepts": [
            "오늘 주제의 핵심 용어를 먼저 정리해요.",
            "작동하는 최소 예제를 먼저 만든 뒤 확장해요.",
            "결과를 눈으로 확인하며 한 단계씩 수정해요.",
        ],
        "analogy": "큰 퍼즐을 색깔별로 나눠 맞추는 방법과 같아요.",
        "practice_steps": [
            "예제 코드를 실행해 기본 동작을 확인해요.",
            "입력값 한 개를 바꾸고 차이를 관찰해요.",
            "실행 결과를 한 줄로 요약해 학습 노트를 작성해요.",
        ],
        "checklist": [
            "오늘 주제를 한 문장으로 설명할 수 있다.",
            "코드를 최소 1번 수정하고 다시 실행했다.",
            "결과를 글로 정리했다.",
        ],
        "next_tip": "다음 차시에서는 오늘 만든 최소 예제를 확장해 볼 거예요.",
    },
}


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


def render_example(track: str, class_id: str, module: str) -> str:
    templates = {
        "python": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def even_double(numbers):
                return [n * 2 for n in numbers if n % 2 == 0]

            def make_message(values):
                if not values:
                    return "조건을 만족하는 숫자가 없어요."
                return f"짝수만 2배: {{values}}"

            def main():
                data = [1, 2, 3, 4, 5, 6]
                result = even_double(data)
                print("오늘 주제:", TOPIC)
                print(make_message(result))

            if __name__ == "__main__":
                main()
            """
        ),
        "data": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def add_average(rows):
                for row in rows:
                    row["avg"] = round((row["math"] + row["science"]) / 2, 1)
                return rows

            def print_report(rows):
                print("오늘 주제:", TOPIC)
                for row in rows:
                    print(f"{{row['name']}} -> 평균 {{row['avg']}}")

            def main():
                students = [
                    {{"name": "민수", "math": 90, "science": 80}},
                    {{"name": "지유", "math": 75, "science": 95}},
                ]
                result = add_average(students)
                print_report(result)

            if __name__ == "__main__":
                main()
            """
        ),
        "ml": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def average_predictor(samples):
                total = sum(score for _, score in samples)
                return total / len(samples)

            def mae(samples, prediction):
                errors = [abs(score - prediction) for _, score in samples]
                return sum(errors) / len(errors)

            def main():
                data = [(1, 50), (2, 60), (3, 70), (4, 80)]
                pred = average_predictor(data)
                error = mae(data, pred)
                print("오늘 주제:", TOPIC)
                print("예측값(평균):", round(pred, 2))
                print("평균 절대 오차:", round(error, 2))

            if __name__ == "__main__":
                main()
            """
        ),
        "nlp": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def tokenize(sentence):
                cleaned = sentence.replace(",", " ").replace(".", " ")
                return [token.lower() for token in cleaned.split() if token]

            def word_count(tokens):
                counts = {{}}
                for token in tokens:
                    counts[token] = counts.get(token, 0) + 1
                return counts

            def main():
                sentence = "AI 수업은 재미있고, AI 실습은 더 재미있다."
                tokens = tokenize(sentence)
                counts = word_count(tokens)
                print("오늘 주제:", TOPIC)
                print("토큰:", tokens)
                print("빈도:", counts)

            if __name__ == "__main__":
                main()
            """
        ),
        "speech": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def filter_short_clips(items, max_seconds):
                return [item for item in items if item["seconds"] <= max_seconds]

            def average_seconds(items):
                return sum(item["seconds"] for item in items) / len(items)

            def main():
                clips = [
                    {{"id": "utt1", "text": "안녕하세요", "seconds": 1.2}},
                    {{"id": "utt2", "text": "오늘도 화이팅", "seconds": 2.4}},
                    {{"id": "utt3", "text": "파이썬은 재밌다", "seconds": 1.8}},
                ]
                short_clips = filter_short_clips(clips, 2.0)
                print("오늘 주제:", TOPIC)
                print("짧은 발화:", [item["id"] for item in short_clips])
                print("평균 길이:", round(average_seconds(clips), 2))

            if __name__ == "__main__":
                main()
            """
        ),
        "prompt": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def build_prompt(role, question):
                template = (
                    "너는 {{role}}야.\\n"
                    "질문: {{question}}\\n"
                    "답변은 3줄 이내로 쉽게 설명해 줘."
                )
                return template.format(role=role, question=question)

            def main():
                prompt = build_prompt("친절한 과학 선생님", "중력이 뭐야?")
                print("오늘 주제:", TOPIC)
                print(prompt)

            if __name__ == "__main__":
                main()
            """
        ),
        "langchain": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def step_collect(question):
                return f"[수집] 질문 받음: {{question}}"

            def step_summarize(text):
                return f"[요약] 핵심: {{text[-10:]}}"

            def step_answer(summary):
                return f"[응답] {{summary}} 를 바탕으로 답변 생성"

            def main():
                question = "지구가 태양 주위를 도는 이유를 알려줘"
                collected = step_collect(question)
                summary = step_summarize(collected)
                answer = step_answer(summary)
                print("오늘 주제:", TOPIC)
                print(collected)
                print(summary)
                print(answer)

            if __name__ == "__main__":
                main()
            """
        ),
        "rag": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def retrieve(question, docs):
                q_tokens = set(question.split())
                scored = []
                for doc in docs:
                    d_tokens = set(doc["text"].split())
                    score = len(q_tokens & d_tokens)
                    scored.append((score, doc))
                scored.sort(key=lambda x: x[0], reverse=True)
                return [doc for score, doc in scored if score > 0][:2]

            def build_answer(question, picked_docs):
                if not picked_docs:
                    return "관련 문서를 찾지 못했어요."
                evidence = " / ".join(doc["text"] for doc in picked_docs)
                return f"질문: {{question}}\\n근거: {{evidence}}"

            def main():
                docs = [
                    {{"id": 1, "text": "지구는 태양 주위를 1년에 한 번 공전한다"}},
                    {{"id": 2, "text": "달은 지구 주위를 약 27일에 한 번 돈다"}},
                    {{"id": 3, "text": "태양은 태양계의 중심 별이다"}},
                ]
                question = "지구와 태양의 관계를 알려줘"
                picked = retrieve(question, docs)
                answer = build_answer(question, picked)
                print("오늘 주제:", TOPIC)
                print("검색 문서 id:", [doc["id"] for doc in picked])
                print(answer)

            if __name__ == "__main__":
                main()
            """
        ),
        "generic": dedent(
            f"""
            \"\"\"{class_id} 쉬운 예제: {module}\"\"\"

            TOPIC = "{module}"

            def split_steps(task):
                return [f"1단계: {{task}} 이해", f"2단계: 작은 코드 작성", f"3단계: 결과 확인"]

            def main():
                steps = split_steps(TOPIC)
                print("오늘 주제:", TOPIC)
                for step in steps:
                    print(step)

            if __name__ == "__main__":
                main()
            """
        ),
    }
    content = templates.get(track, templates["generic"]).strip() + "\n"
    return f"# {COPYRIGHT_TEXT}\n\n{content}"


def render_markdown(
    row: dict[str, str],
    track: str,
    example_file: str,
    quiz_file: str,
    prev_row: dict[str, str] | None,
    next_row: dict[str, str] | None,
) -> str:
    class_id = row["class"]
    day = int(row["day"])
    slot = int(row["slot"])
    subject_name = row["subject_name"]
    module = row["module"]
    level = row["level"]
    session = row["subject_session"]
    info = TRACK_INFO[track]
    day_text = f"Day {day:02d}"
    slot_text = f"{slot}교시"

    if prev_row is None:
        prev_block = (
            "- 이전 차시가 없습니다. 이 차시는 전체 과정의 시작점입니다.\n"
            "    - 오늘은 학습 규칙과 기본 흐름을 만드는 데 집중하세요."
        )
    else:
        prev_day = int(prev_row["day"])
        prev_slot = int(prev_row["slot"])
        prev_block = (
            f"- 이전 차시: **{prev_row['class']} / {prev_row['module']}** "
            f"(Day {prev_day:02d} / {prev_slot}교시)\n"
            f"    - 복습 연결: 이전에 배운 **{prev_row['module']}** 를 떠올리며, "
            f"오늘 **{module}** 와 어떤 점이 이어지는지 비교해 보세요."
        )

    if next_row is None:
        next_block = (
            "- 다음 차시는 없습니다. 이 차시는 전체 과정의 마지막입니다.\n"
            "    - 지금까지 학습한 내용을 한 번에 요약해 나만의 정리 노트를 만들어 보세요."
        )
        connection_tip = "과정이 끝났으니, 지금까지 만든 코드와 노트를 묶어 나만의 포트폴리오로 정리해 보세요."
    else:
        next_day = int(next_row["day"])
        next_slot = int(next_row["slot"])
        next_block = (
            f"- 다음 차시: **{next_row['class']} / {next_row['module']}** "
            f"(Day {next_day:02d} / {next_slot}교시)\n"
            f"    - 미리보기: 다음 차시 전에 **{module}** 핵심 코드 1개를 다시 실행해 두면 "
            f"{next_row['module']} 학습이 더 쉬워집니다."
        )
        connection_tip = info["next_tip"]

    content = f"""
    # {class_id} 자기주도 학습 가이드

    ## 1) 오늘의 학습 정보
    - 교과목: **{subject_name}**
    - 학습 주제: **{module}**
    - 세부 시퀀스: **{session}**
    - 일정: **{day_text} / {slot_text}**
    - 난이도: **{level}**

    ## 2) 이전에 배운 내용 (복습)
    {prev_block}

    ## 3) 주제를 아주 쉽게 이해하기
    - 한 줄 설명: {info["kid_summary"]}
    - 왜 배우나요?: {info["why"]}

    ### 핵심 개념 3가지
    1. {info["concepts"][0]}
    2. {info["concepts"][1]}
    3. {info["concepts"][2]}

    ### 비유로 이해하기
    - {info["analogy"]}

    ## 4) 실습 환경 만들기 (항상 먼저)
    아래 명령은 **처음 한 번** 준비해 두면 이후 학습이 쉬워집니다.

    ### Windows PowerShell
    ```powershell
    cd C:\\DevOps\\Python-AI_Agent-Class
    python -m venv .venv
    .\\.venv\\Scripts\\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    ### Linux/macOS (bash)
    ```bash
    cd /path/to/Python-AI_Agent-Class
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    ## 5) 오늘의 예제 코드
    - 예제 파일: `{example_file}`
    - 실행 명령:
    ```bash
    python {class_id}/{example_file}
    ```

    ### 예제 코드를 볼 때 집중할 포인트
    1. 입력이 무엇인지 먼저 찾기
    2. 처리 규칙(함수/조건/반복) 확인하기
    3. 출력 결과가 목표와 맞는지 점검하기

    ## 6) 퀴즈로 복습하기 (5문항)
    - 퀴즈 파일: `{quiz_file}`
    - 브라우저에서 열기:
    ```bash
    {class_id}/{quiz_file}
    ```
    - 버튼 설명:
    1. `채점하기`: 현재 선택한 답으로 점수를 계산해요.
    2. `다시풀기`: 선택을 모두 지우고 처음부터 다시 풀어요.

    ## 7) 혼자 실습 순서 (초등학생 버전)
    1. 코드를 한 번 그대로 실행해요.
    2. 숫자/문장 값을 1개 바꿔요.
    3. 결과가 왜 바뀌었는지 한 줄로 적어요.
    4. 함수를 1개 더 만들어 작은 기능을 추가해요.

    ### 실습 미션
    1. {info["practice_steps"][0]}
    2. {info["practice_steps"][1]}
    3. {info["practice_steps"][2]}

    ## 8) 스스로 점검 체크리스트
    - [ ] {info["checklist"][0]}
    - [ ] {info["checklist"][1]}
    - [ ] {info["checklist"][2]}

    ## 9) 막히면 이렇게 해결해요
    1. 에러 메시지 마지막 줄을 먼저 읽어요.
    2. 함수 이름과 괄호 짝을 확인해요.
    3. `print()`를 넣어 중간 값을 확인해요.
    4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

    ## 10) 학습 후 다음에 배울 내용
    {next_block}

    ## 11) 다음 차시 연결
    - {connection_tip}
    - 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
    """
    body = dedent(content).strip() + "\n"
    return f"<!-- {COPYRIGHT_TEXT} -->\n{body}"


def build_self_study_materials() -> None:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"Cannot find index file: {INDEX_FILE}")

    with INDEX_FILE.open(encoding="utf-8", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))

    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        cleaned = {str(key).lstrip("\ufeff"): value for key, value in raw.items()}
        rows.append(cleaned)

    def class_number(class_id: str) -> int:
        return int(class_id.replace("class", ""))

    ordered_rows = sorted(rows, key=lambda r: class_number(r["class"]))
    neighbors: dict[str, tuple[dict[str, str] | None, dict[str, str] | None]] = {}
    for i, current in enumerate(ordered_rows):
        prev_row = ordered_rows[i - 1] if i > 0 else None
        next_row = ordered_rows[i + 1] if i + 1 < len(ordered_rows) else None
        neighbors[current["class"]] = (prev_row, next_row)

    for row in ordered_rows:
        class_id = row["class"]
        module = row["module"]
        subject_name = row["subject_name"]
        track = choose_track(subject_name, module)
        prev_row, next_row = neighbors[class_id]

        class_dir = ROOT / class_id
        md_path = class_dir / f"{class_id}.md"
        example_path = class_dir / f"{class_id}_example.py"
        quiz_path = class_dir / f"{class_id}_quiz.html"

        md_path.write_text(
            render_markdown(
                row=row,
                track=track,
                example_file=example_path.name,
                quiz_file=quiz_path.name,
                prev_row=prev_row,
                next_row=next_row,
            ),
            encoding="utf-8",
            newline="\n",
        )
        if not example_path.exists():
            example_path.write_text(
                render_example(track=track, class_id=class_id, module=module),
                encoding="utf-8",
                newline="\n",
            )

    print(f"Updated {len(ordered_rows)} class markdown files.")


if __name__ == "__main__":
    build_self_study_materials()
