# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
import re
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont


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
    "llm": {
        "kid_summary": "거대 언어 모델에게 목적과 조건을 정확히 지시해 원하는 답을 얻는 방법을 배워요.",
        "why": "같은 모델이라도 지시문, 검증 기준, 도메인 맥락을 어떻게 주느냐에 따라 결과 품질이 크게 달라져요.",
        "concepts": [
            "요구사항을 프롬프트 조건(역할/출력형식/제약)으로 구조화해요.",
            "안전성·환각 점검 기준을 함께 넣어 결과의 신뢰도를 높여요.",
            "도메인 문맥과 예시를 연결해 실무형 답변 품질을 높여요.",
        ],
        "analogy": "똑똑한 조교에게 과제를 맡길 때, 목표·형식·검수 기준을 먼저 주면 결과가 정확해지는 것과 같아요.",
        "practice_steps": [
            "같은 질문을 조건 없는 프롬프트와 조건 있는 프롬프트로 각각 실행해 비교해요.",
            "답변에 근거/제약/출처 항목을 넣어 품질 기준을 점검해요.",
            "도메인 예시 1개를 추가하고 답변 정확도가 어떻게 달라지는지 확인해요.",
        ],
        "checklist": [
            "프롬프트의 역할/목표/출력형식을 구분해 설명할 수 있다.",
            "환각 가능 문장을 식별하고 검증 절차를 적용했다.",
            "도메인 문맥을 넣은 버전과 넣지 않은 버전을 비교했다.",
        ],
        "next_tip": "다음 차시에서는 도메인 시나리오를 API나 서비스 흐름과 연결해 실전형으로 확장해 볼 거예요.",
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


TRACK_MAIN_SYNTAX = {
    "python": ["함수", "조건문", "반복문", "출력(print)"],
    "data": ["함수", "리스트/딕셔너리", "집계 로직", "출력(print)"],
    "ml": ["함수", "리스트 컴프리헨션", "오차 계산", "출력(print)"],
    "nlp": ["문자열 처리", "토큰화", "딕셔너리 집계", "출력(print)"],
    "llm": ["함수", "프롬프트 구성", "검증 조건", "출력(print)"],
    "speech": ["리스트/딕셔너리", "조건 필터링", "통계 계산", "출력(print)"],
    "prompt": ["문자열 템플릿", "함수", "변수 치환", "출력(print)"],
    "langchain": ["단계 함수", "체인 구성", "중간 상태 점검", "출력(print)"],
    "rag": ["검색 함수", "유사도 계산", "근거 결합", "출력(print)"],
    "generic": ["함수", "조건문", "반복문", "출력(print)"],
}

TRACK_FLOW_STEPS = {
    "python": [
        "입력값과 요구사항을 확인한다",
        "조건문/반복문으로 핵심 로직을 구현한다",
        "함수 단위로 코드를 분리한다",
        "출력 결과를 테스트 케이스로 검증한다",
    ],
    "data": [
        "원본 데이터를 로딩하고 구조를 확인한다",
        "결측치/이상치를 전처리한다",
        "집계·변환으로 분석용 데이터를 만든다",
        "요약 결과를 표/리포트로 검증한다",
    ],
    "ml": [
        "학습 데이터(X,y)를 준비한다",
        "예측 규칙(모델)을 학습/계산한다",
        "오차 지표를 계산해 성능을 확인한다",
        "오차 원인을 분석해 개선 포인트를 정리한다",
    ],
    "nlp": [
        "텍스트를 정제하고 토큰 단위로 분해한다",
        "핵심 특징(빈도/패턴)을 계산한다",
        "주요 태스크를 실행해 결과를 생성한다",
        "오탐/누락 사례를 점검해 규칙을 보완한다",
    ],
    "llm": [
        "요구사항을 프롬프트 구조로 정리한다",
        "생성 파라미터와 출력 형식을 설정한다",
        "안전성/환각 기준으로 답변을 검증한다",
        "도메인 맥락을 반영해 최종 답변을 보정한다",
    ],
    "speech": [
        "음성 데이터와 라벨 품질을 점검한다",
        "특징(MFCC 등)을 추출하고 전처리한다",
        "STT/TTS 추론 또는 학습 단계를 실행한다",
        "품질 지표를 계산해 결과를 검증한다",
    ],
    "prompt": [
        "역할/목표/형식을 명확히 정의한다",
        "프롬프트 템플릿을 작성한다",
        "예시를 바꿔 응답 품질을 비교한다",
        "평가 기준에 맞게 프롬프트를 튜닝한다",
    ],
    "langchain": [
        "체인 단계(입력/처리/출력)를 설계한다",
        "모델·도구·메모리를 연결한다",
        "중간 상태 로그를 확인한다",
        "워크플로우 전체 결과를 검증한다",
    ],
    "rag": [
        "문서를 로딩하고 청크를 구성한다",
        "임베딩/벡터 검색으로 관련 문서를 찾는다",
        "검색 근거를 컨텍스트로 결합한다",
        "출처 포함 답변을 생성하고 검증한다",
    ],
    "generic": [
        "핵심 개념을 정리한다",
        "최소 실행 예제를 구현한다",
        "입력값을 바꿔 결과를 비교한다",
        "체크리스트로 학습 결과를 검증한다",
    ],
}


AUTO_TECH_STACK_START = "<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->"
AUTO_TECH_STACK_END = "<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->"
TERM_TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9+\-]*|[가-힣]+")
PARTICLE_SUFFIXES = ("은", "는", "이", "가", "을", "를", "와", "과", "의")
SKIP_TERMS = {"및", "와", "과", "등"}

TRACK_TERM_CONTEXT = {
    "python": "코드 문법을 통해 문제를 절차적으로 해결하는 역량을 기르는 교과목입니다.",
    "data": "데이터 전처리와 시각화를 통해 분석 가능한 정보로 바꾸는 교과목입니다.",
    "ml": "모델 학습과 성능 평가를 통해 예측 시스템을 설계하는 교과목입니다.",
    "nlp": "텍스트를 계산 가능한 단위로 바꿔 의미를 다루는 자연어 처리 교과목입니다.",
    "llm": "거대 언어 모델을 실무 도메인과 연결해 생성 품질을 높이는 교과목입니다.",
    "speech": "음성 신호를 정제하고 STT/TTS 모델로 연결하는 음성 AI 교과목입니다.",
    "prompt": "프롬프트 설계로 모델 응답 품질을 제어하는 생성형 AI 교과목입니다.",
    "langchain": "체인 기반 워크플로우를 구성해 서비스형 AI를 구현하는 교과목입니다.",
    "rag": "검색 근거를 결합해 신뢰도 높은 답변을 만드는 RAG 교과목입니다.",
    "generic": "핵심 용어를 기능 단위로 분해해 구현까지 연결하는 실습 중심 교과목입니다.",
}

TERM_ALIASES = {
    "langchain": "LangChain",
    "Langchain": "LangChain",
    "ml": "ML",
    "dl": "DL",
    "llm": "LLM",
    "stt": "STT",
    "tts": "TTS",
    "nlp": "NLP",
    "rag": "RAG",
    "api": "API",
    "벡터db": "벡터DB",
    "vectorstore": "VectorStore",
    "prompttemplate": "PromptTemplate",
    "outputparser": "OutputParser",
}

TERM_LEXICON: dict[str, dict[str, str]] = {
    "Python": {
        "grammar": "고유명사(언어명)",
        "hanja": "-",
        "english": "Python",
        "technical": "데이터 처리와 AI 실습에 널리 쓰이는 범용 프로그래밍 언어입니다.",
    },
    "프로그래밍": {
        "grammar": "명사",
        "hanja": "-",
        "english": "programming",
        "technical": "문제를 알고리즘으로 분해해 코드로 구현하는 활동입니다.",
    },
    "전처리": {
        "grammar": "명사",
        "hanja": "前處理",
        "english": "preprocessing",
        "technical": "원시 데이터를 모델이 다루기 쉬운 형태로 정리하는 단계입니다.",
    },
    "시각화": {
        "grammar": "명사",
        "hanja": "視覺化",
        "english": "visualization",
        "technical": "숫자 데이터를 그래프와 차트로 표현해 패턴을 해석하는 과정입니다.",
    },
    "데이터": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "data",
        "technical": "분석, 학습, 추론의 입력이 되는 관측값 집합입니다.",
    },
    "분석": {
        "grammar": "명사",
        "hanja": "分析",
        "english": "analysis",
        "technical": "데이터를 분해해 의미 있는 결론을 도출하는 과정입니다.",
    },
    "머신러닝": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "machine learning",
        "technical": "데이터에서 패턴을 학습해 예측 규칙을 만드는 기술입니다.",
    },
    "딥러닝": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "deep learning",
        "technical": "다층 신경망으로 복잡한 패턴을 학습하는 머신러닝 하위 분야입니다.",
    },
    "자연어": {
        "grammar": "명사",
        "hanja": "自然語",
        "english": "natural language",
        "technical": "사람이 일상에서 사용하는 언어 텍스트/발화를 의미합니다.",
    },
    "음성": {
        "grammar": "명사",
        "hanja": "音聲",
        "english": "speech/audio",
        "technical": "사람의 발화 신호를 디지털로 표현한 데이터입니다.",
    },
    "거대": {
        "grammar": "관형어",
        "hanja": "巨大",
        "english": "large-scale",
        "technical": "모델 파라미터와 학습 데이터 규모가 매우 큼을 나타냅니다.",
    },
    "언어": {
        "grammar": "명사",
        "hanja": "言語",
        "english": "language",
        "technical": "의미를 전달하기 위한 기호 체계로, NLP의 분석 대상입니다.",
    },
    "모델": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "model",
        "technical": "입력과 출력 관계를 수학적으로 근사한 계산 구조입니다.",
    },
    "학습": {
        "grammar": "명사",
        "hanja": "學習",
        "english": "training/learning",
        "technical": "데이터로부터 모델 파라미터를 조정하는 과정입니다.",
    },
    "생성": {
        "grammar": "명사",
        "hanja": "生成",
        "english": "generation",
        "technical": "모델이 새 텍스트/응답/콘텐츠를 출력하는 과정입니다.",
    },
    "활용": {
        "grammar": "명사/동사 어근",
        "hanja": "活用",
        "english": "utilization",
        "technical": "이론이나 도구를 실제 문제 해결 맥락에 적용하는 행위입니다.",
    },
    "개발": {
        "grammar": "명사",
        "hanja": "開發",
        "english": "development",
        "technical": "기능 기획, 구현, 검증을 통해 소프트웨어를 완성하는 과정입니다.",
    },
    "프롬프트": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "prompt",
        "technical": "모델의 응답 방향을 결정하는 입력 지시문입니다.",
    },
    "엔지니어링": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "engineering",
        "technical": "재현 가능한 품질을 목표로 설계·검증하는 공학적 접근입니다.",
    },
    "도메인": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "domain",
        "technical": "문제를 푸는 특정 업무 영역(예: 의료, 법률, 제조)을 뜻합니다.",
    },
    "적용": {
        "grammar": "명사/동사 어근",
        "hanja": "適用",
        "english": "application",
        "technical": "일반 기술을 실제 업무 요구사항에 맞게 구현하는 단계입니다.",
    },
    "시나리오": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "scenario",
        "technical": "사용자 행동, 입력, 예외를 포함한 실행 흐름 설계 문서입니다.",
    },
    "안전성": {
        "grammar": "명사",
        "hanja": "安全性",
        "english": "safety",
        "technical": "유해 출력, 오남용, 규정 위반을 줄이는 모델 운영 특성입니다.",
    },
    "환각": {
        "grammar": "명사",
        "hanja": "幻覺",
        "english": "hallucination",
        "technical": "모델이 사실 근거 없이 그럴듯한 잘못된 답을 생성하는 현상입니다.",
    },
    "관리": {
        "grammar": "명사",
        "hanja": "管理",
        "english": "management",
        "technical": "정책, 검증, 모니터링으로 품질을 지속 통제하는 활동입니다.",
    },
    "API": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Application Programming Interface",
        "technical": "서비스 간 기능을 호출하기 위한 표준 인터페이스입니다.",
    },
    "연동": {
        "grammar": "명사",
        "hanja": "連動",
        "english": "integration",
        "technical": "서로 다른 시스템을 연결해 데이터와 기능을 교환하는 과정입니다.",
    },
    "서비스": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "service",
        "technical": "사용자에게 기능을 제공하는 실행 가능한 애플리케이션 단위입니다.",
    },
    "구현": {
        "grammar": "명사",
        "hanja": "具現",
        "english": "implementation",
        "technical": "설계를 실제 코드와 시스템 동작으로 구체화하는 과정입니다.",
    },
    "요약": {
        "grammar": "명사",
        "hanja": "要約",
        "english": "summarization",
        "technical": "원문 핵심 정보를 압축해 짧은 문장으로 재구성하는 작업입니다.",
    },
    "분류": {
        "grammar": "명사",
        "hanja": "分類",
        "english": "classification",
        "technical": "입력을 사전 정의된 카테고리로 할당하는 지도학습 과제입니다.",
    },
    "추출": {
        "grammar": "명사",
        "hanja": "抽出",
        "english": "extraction",
        "technical": "원문에서 필요한 구조화 정보만 뽑아내는 작업입니다.",
    },
    "토큰": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "token",
        "technical": "모델이 처리하는 최소 단위 문자열 조각입니다.",
    },
    "컨텍스트": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "context",
        "technical": "현재 답변 생성에 사용되는 주변 정보 범위입니다.",
    },
    "파라미터": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "parameter",
        "technical": "모델 동작을 제어하거나 학습으로 조정되는 수치 변수입니다.",
    },
    "대화형": {
        "grammar": "관형어형 명사",
        "hanja": "對話型",
        "english": "conversational",
        "technical": "사용자-시스템 상호작용이 왕복 구조로 진행됨을 나타냅니다.",
    },
    "응답": {
        "grammar": "명사",
        "hanja": "應答",
        "english": "response",
        "technical": "모델이 입력 프롬프트에 대해 반환하는 출력 텍스트입니다.",
    },
    "LLM": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Large Language Model",
        "technical": "대규모 텍스트로 사전학습된 생성형 언어 모델입니다.",
    },
    "NLP": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Natural Language Processing",
        "technical": "자연어를 분석·이해·생성하는 인공지능 분야입니다.",
    },
    "STT": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Speech-to-Text",
        "technical": "음성 신호를 텍스트로 변환하는 기술입니다.",
    },
    "TTS": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Text-to-Speech",
        "technical": "텍스트를 자연스러운 음성으로 합성하는 기술입니다.",
    },
    "ML": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Machine Learning",
        "technical": "데이터 기반 학습으로 예측 규칙을 만드는 방법론입니다.",
    },
    "DL": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Deep Learning",
        "technical": "심층 신경망으로 표현학습을 수행하는 방법론입니다.",
    },
    "LangChain": {
        "grammar": "고유명사(프레임워크명)",
        "hanja": "-",
        "english": "LangChain",
        "technical": "LLM 애플리케이션을 체인/도구 기반으로 구성하는 프레임워크입니다.",
    },
    "RAG": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Retrieval-Augmented Generation",
        "technical": "검색 결과를 근거로 생성 품질과 신뢰도를 높이는 구조입니다.",
    },
    "Retrieval-Augmented": {
        "grammar": "복합 형용어",
        "hanja": "-",
        "english": "retrieval-augmented",
        "technical": "검색 결과를 생성 과정에 보강한다는 RAG 핵심 속성입니다.",
    },
    "Generation": {
        "grammar": "명사(영어)",
        "hanja": "-",
        "english": "generation",
        "technical": "모델이 새 출력 텍스트를 만들어내는 단계입니다.",
    },
    "PromptTemplate": {
        "grammar": "복합명사(클래스명)",
        "hanja": "-",
        "english": "PromptTemplate",
        "technical": "변수 기반 프롬프트를 재사용 가능하게 만드는 템플릿 구성요소입니다.",
    },
    "OutputParser": {
        "grammar": "복합명사(클래스명)",
        "hanja": "-",
        "english": "OutputParser",
        "technical": "모델 출력을 지정된 구조(JSON 등)로 파싱하는 구성요소입니다.",
    },
    "Chain": {
        "grammar": "명사(영어)",
        "hanja": "-",
        "english": "chain",
        "technical": "여러 처리 단계를 순차 연결한 실행 파이프라인입니다.",
    },
    "Memory": {
        "grammar": "명사(영어)",
        "hanja": "-",
        "english": "memory",
        "technical": "대화/상태 정보를 보존해 문맥 일관성을 높이는 저장 장치입니다.",
    },
    "Tool": {
        "grammar": "명사(영어)",
        "hanja": "-",
        "english": "tool",
        "technical": "모델이 외부 기능(API, 계산기 등)을 호출할 수 있게 한 모듈입니다.",
    },
    "Agent": {
        "grammar": "명사(영어)",
        "hanja": "-",
        "english": "agent",
        "technical": "목표 달성을 위해 도구 선택과 실행 순서를 스스로 결정하는 실행자입니다.",
    },
    "VectorStore": {
        "grammar": "복합명사(영어)",
        "hanja": "-",
        "english": "vector store",
        "technical": "임베딩 벡터를 저장하고 유사도 검색을 수행하는 저장소입니다.",
    },
    "벡터DB": {
        "grammar": "복합명사",
        "hanja": "-",
        "english": "vector database",
        "technical": "고차원 벡터 검색을 최적화한 데이터베이스입니다.",
    },
    "문서": {
        "grammar": "명사",
        "hanja": "文書",
        "english": "document",
        "technical": "RAG 검색과 근거 생성에 사용하는 텍스트 단위 데이터입니다.",
    },
    "검색": {
        "grammar": "명사",
        "hanja": "搜索",
        "english": "retrieval/search",
        "technical": "질문과 유사한 문서를 찾는 단계로 RAG 품질을 좌우합니다.",
    },
    "출처화": {
        "grammar": "명사",
        "hanja": "-",
        "english": "citation grounding",
        "technical": "답변 문장별 근거 문서를 연결해 신뢰성을 높이는 작업입니다.",
    },
    "검증": {
        "grammar": "명사",
        "hanja": "檢證",
        "english": "validation",
        "technical": "결과가 요구사항과 기준을 만족하는지 확인하는 절차입니다.",
    },
    "임베딩": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "embedding",
        "technical": "텍스트/신호를 벡터 공간에 사상해 의미 유사도를 계산하는 표현입니다.",
    },
    "파이프라인": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "pipeline",
        "technical": "여러 처리 단계를 자동으로 연결한 실행 흐름입니다.",
    },
    "오디오": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "audio",
        "technical": "디지털 음성 신호 파일/스트림 데이터를 의미합니다.",
    },
    "발화": {
        "grammar": "명사",
        "hanja": "發話",
        "english": "utterance",
        "technical": "화자가 실제로 말한 하나의 문장 단위 음성 샘플입니다.",
    },
    "화자": {
        "grammar": "명사",
        "hanja": "話者",
        "english": "speaker",
        "technical": "음성을 발화한 사람(또는 음색 정체성)을 나타냅니다.",
    },
    "특징": {
        "grammar": "명사",
        "hanja": "特徵",
        "english": "feature",
        "technical": "모델이 학습에 사용하는 입력 속성값입니다.",
    },
    "MFCC": {
        "grammar": "약어명사",
        "hanja": "-",
        "english": "Mel-Frequency Cepstral Coefficients",
        "technical": "음성 스펙트럼 특성을 요약하는 대표 음향 특징 벡터입니다.",
    },
    "변수": {
        "grammar": "명사",
        "hanja": "變數",
        "english": "variable",
        "technical": "값을 저장하고 재사용하기 위한 이름 붙은 메모리 공간입니다.",
    },
    "자료형": {
        "grammar": "명사",
        "hanja": "資料型",
        "english": "data type",
        "technical": "값의 종류와 연산 방식을 정의하는 타입 체계입니다.",
    },
    "연산자": {
        "grammar": "명사",
        "hanja": "演算子",
        "english": "operator",
        "technical": "피연산자에 연산 규칙을 적용하는 기호/키워드입니다.",
    },
    "조건문": {
        "grammar": "명사",
        "hanja": "條件文",
        "english": "conditional statement",
        "technical": "조건 평가 결과에 따라 실행 분기를 선택하는 문법입니다.",
    },
    "반복문": {
        "grammar": "명사",
        "hanja": "反復文",
        "english": "loop statement",
        "technical": "동일 로직을 조건/횟수 기준으로 반복 실행하는 문법입니다.",
    },
    "흐름제어": {
        "grammar": "명사",
        "hanja": "흐름制御",
        "english": "flow control",
        "technical": "실행 순서를 분기, 반복, 중단으로 조절하는 기술입니다.",
    },
    "함수": {
        "grammar": "명사",
        "hanja": "函數",
        "english": "function",
        "technical": "입력을 받아 결과를 반환하는 재사용 가능한 코드 블록입니다.",
    },
    "모듈": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "module",
        "technical": "관련 함수/클래스를 묶은 코드 파일 단위입니다.",
    },
    "컬렉션": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "collection",
        "technical": "리스트, 딕셔너리 등 여러 데이터를 저장하는 자료구조군입니다.",
    },
    "자료구조": {
        "grammar": "명사",
        "hanja": "資料構造",
        "english": "data structure",
        "technical": "데이터 저장 방식과 접근 효율을 결정하는 구조입니다.",
    },
    "파일": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "file",
        "technical": "디스크에 저장되는 데이터 단위입니다.",
    },
    "입출력": {
        "grammar": "명사",
        "hanja": "入出力",
        "english": "input/output",
        "technical": "외부 데이터의 읽기/쓰기 과정을 의미합니다.",
    },
    "예외처리": {
        "grammar": "명사",
        "hanja": "例外處理",
        "english": "exception handling",
        "technical": "실행 중 오류 상황을 안전하게 제어하는 기법입니다.",
    },
    "디버깅": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "debugging",
        "technical": "오류 원인을 추적하고 수정하는 개발 절차입니다.",
    },
    "객체지향": {
        "grammar": "명사",
        "hanja": "客體指向",
        "english": "object-oriented",
        "technical": "데이터와 동작을 객체 단위로 모델링하는 설계 패러다임입니다.",
    },
    "NumPy": {
        "grammar": "고유명사(라이브러리명)",
        "hanja": "-",
        "english": "NumPy",
        "technical": "배열 연산과 선형대수 계산을 위한 파이썬 핵심 라이브러리입니다.",
    },
    "Pandas": {
        "grammar": "고유명사(라이브러리명)",
        "hanja": "-",
        "english": "pandas",
        "technical": "테이블형 데이터 조작과 분석에 특화된 파이썬 라이브러리입니다.",
    },
    "데이터프레임": {
        "grammar": "명사(복합 외래어)",
        "hanja": "-",
        "english": "DataFrame",
        "technical": "행/열 기반 표 데이터를 다루는 판다스의 핵심 자료구조입니다.",
    },
    "결측치": {
        "grammar": "명사",
        "hanja": "缺測値",
        "english": "missing value",
        "technical": "값이 비어 있거나 측정되지 않은 데이터 항목입니다.",
    },
    "이상치": {
        "grammar": "명사",
        "hanja": "異常値",
        "english": "outlier",
        "technical": "분포에서 비정상적으로 벗어난 값으로 모델 품질에 영향이 큽니다.",
    },
    "문자열": {
        "grammar": "명사",
        "hanja": "文字列",
        "english": "string",
        "technical": "텍스트 데이터를 표현하는 기본 자료형입니다.",
    },
    "날짜": {
        "grammar": "명사",
        "hanja": "날짜",
        "english": "date",
        "technical": "시간 축 분석과 정렬/집계에 필요한 시계열 데이터입니다.",
    },
    "그룹화": {
        "grammar": "명사",
        "hanja": "그룹化",
        "english": "grouping",
        "technical": "공통 키 기준으로 데이터를 묶어 집계 가능한 형태로 만듭니다.",
    },
    "집계": {
        "grammar": "명사",
        "hanja": "集計",
        "english": "aggregation",
        "technical": "합계, 평균, 개수 등 통계량을 계산하는 단계입니다.",
    },
    "병합": {
        "grammar": "명사",
        "hanja": "倂合",
        "english": "merge",
        "technical": "여러 데이터 소스를 키 기준으로 결합하는 작업입니다.",
    },
    "변환": {
        "grammar": "명사",
        "hanja": "變換",
        "english": "transformation",
        "technical": "데이터 스키마, 타입, 값 표현을 목적에 맞게 바꾸는 과정입니다.",
    },
    "Matplotlib": {
        "grammar": "고유명사(라이브러리명)",
        "hanja": "-",
        "english": "Matplotlib",
        "technical": "파이썬 기본 시각화 라이브러리로 정적 그래프 생성에 강점이 있습니다.",
    },
    "Seaborn": {
        "grammar": "고유명사(라이브러리명)",
        "hanja": "-",
        "english": "Seaborn",
        "technical": "통계 시각화를 고수준 API로 제공하는 Matplotlib 기반 라이브러리입니다.",
    },
    "차트": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "chart",
        "technical": "데이터를 시각적 기호로 표현한 그래프 결과물입니다.",
    },
    "회귀": {
        "grammar": "명사",
        "hanja": "回歸",
        "english": "regression",
        "technical": "연속형 수치를 예측하는 지도학습 문제 유형입니다.",
    },
    "과적합": {
        "grammar": "명사",
        "hanja": "過適合",
        "english": "overfitting",
        "technical": "학습 데이터에 과도하게 맞춰 일반화 성능이 떨어지는 현상입니다.",
    },
    "일반화": {
        "grammar": "명사",
        "hanja": "一般化",
        "english": "generalization",
        "technical": "보지 못한 데이터에서도 성능을 유지하는 모델 능력입니다.",
    },
    "신경망": {
        "grammar": "명사",
        "hanja": "神經網",
        "english": "neural network",
        "technical": "뉴런 계층을 연결해 비선형 함수를 학습하는 모델 구조입니다.",
    },
    "특성공학": {
        "grammar": "명사",
        "hanja": "特性工學",
        "english": "feature engineering",
        "technical": "모델 성능 향상을 위해 입력 특성을 설계·가공하는 작업입니다.",
    },
    "평가": {
        "grammar": "명사",
        "hanja": "評價",
        "english": "evaluation",
        "technical": "지표 기반으로 모델이나 결과물 품질을 측정하는 단계입니다.",
    },
    "지표": {
        "grammar": "명사",
        "hanja": "指標",
        "english": "metric",
        "technical": "정확도, F1, MAE처럼 성능을 수치화하는 기준값입니다.",
    },
    "튜닝": {
        "grammar": "명사(외래어)",
        "hanja": "-",
        "english": "tuning",
        "technical": "파라미터/하이퍼파라미터 조정으로 성능을 개선하는 작업입니다.",
    },
}


def normalize_term(term: str) -> str:
    raw = term.strip().strip(".,")
    if not raw:
        return ""
    if raw in SKIP_TERMS:
        return ""

    alias = TERM_ALIASES.get(raw)
    if alias:
        return alias
    alias_lower = TERM_ALIASES.get(raw.lower())
    if alias_lower:
        return alias_lower

    if raw in TERM_LEXICON:
        return raw

    for suffix in PARTICLE_SUFFIXES:
        if raw.endswith(suffix) and len(raw) > len(suffix) + 1:
            candidate = raw[: -len(suffix)]
            if candidate in TERM_LEXICON:
                return candidate
            alias_candidate = TERM_ALIASES.get(candidate) or TERM_ALIASES.get(candidate.lower())
            if alias_candidate:
                return alias_candidate

    if raw.endswith("하기") and len(raw) > 2:
        candidate = raw[:-2]
        if candidate in TERM_LEXICON:
            return candidate
    if raw.endswith("한") and len(raw) > 1:
        candidate = raw[:-1]
        if candidate in TERM_LEXICON:
            return candidate

    return raw


def collect_key_terms(text: str, max_terms: int = 6) -> list[str]:
    normalized_text = (
        text.replace("(", " ")
        .replace(")", " ")
        .replace("/", " ")
        .replace("+", " ")
        .replace(",", " ")
    )
    tokens = TERM_TOKEN_PATTERN.findall(normalized_text)
    terms: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        base = normalize_term(token)
        if not base or base in SKIP_TERMS:
            continue
        key = base.lower()
        if key in seen:
            continue
        seen.add(key)
        terms.append(base)
        if len(terms) >= max_terms:
            break
    return terms


def lookup_term_info(term: str) -> dict[str, str]:
    if term in TERM_LEXICON:
        return TERM_LEXICON[term]
    lowered = term.lower()
    for key, value in TERM_LEXICON.items():
        if key.lower() == lowered:
            return value

    if re.fullmatch(r"[A-Za-z][A-Za-z0-9+\-]*", term):
        return {
            "grammar": "영문 기술명/약어",
            "hanja": "-",
            "english": term,
            "technical": f"용어 `{term}`: 이번 차시에서 쓰이는 핵심 기술 용어입니다.",
        }

    return {
        "grammar": "명사(기술 개념어)",
        "hanja": "-",
        "english": "(context-specific)",
        "technical": f"용어 `{term}`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다.",
    }


def describe_phrase_grammar(phrase: str) -> str:
    if "을 활용한" in phrase or "를 활용한" in phrase:
        return "목적어(…을/를) + 관형절(활용한) + 중심 명사 구조로, 적용 대상을 문법적으로 분명히 드러냅니다."
    if "및" in phrase:
        return "명사구를 연결어 '및'으로 병렬 연결한 구조입니다. 동등한 학습 범위를 함께 제시합니다."
    if "와" in phrase or "과" in phrase:
        return "명사와 명사를 대등하게 묶는 병렬 명사구 구조입니다."
    if phrase.endswith("하기"):
        return "동사 어간 + '-기' 명사형 구조입니다. 학습 행동 자체를 주제로 명사화한 표현입니다."
    return "핵심 개념 명사를 중심으로 한 명사구 구조입니다."


def format_hangul_hanja(term: str, hanja: str) -> str:
    if hanja == "-":
        return f"{term} (한자 없음)"
    return f"{term} ({hanja})"


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


def render_term_table(terms: list[str]) -> str:
    if not terms:
        return "- (추출된 핵심 용어가 없습니다.)"

    lines = [
        "| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for term in terms:
        info = lookup_term_info(term)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_table_cell(term)}`",
                    escape_table_cell(info["grammar"]),
                    escape_table_cell(format_hangul_hanja(term, info["hanja"])),
                    escape_table_cell(info["english"]),
                    escape_table_cell(info["technical"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def render_term_guide(subject_name: str, module: str, track: str) -> str:
    subject_terms = collect_key_terms(subject_name, max_terms=6)
    module_terms = collect_key_terms(module, max_terms=6)
    subject_table = render_term_table(subject_terms)
    module_table = render_term_table(module_terms)
    subject_context = TRACK_TERM_CONTEXT.get(track, TRACK_TERM_CONTEXT["generic"])
    lines = [
        f"#### 교과목 표현 분석: `{subject_name}`",
        f"- 문법 포인트: {describe_phrase_grammar(subject_name)}",
        f"- 기술 포인트: {subject_context}",
        subject_table,
        "",
        f"#### 학습주제 표현 분석: `{module}`",
        f"- 문법 포인트: {describe_phrase_grammar(module)}",
        f"- 기술 포인트: 이번 차시는 `{module}` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.",
        module_table,
    ]
    return "\n".join(lines)


def sanitize_mermaid_label(text: str) -> str:
    cleaned = text.replace('"', "'").replace("\n", " ").strip()
    return cleaned


def build_flow_steps(
    row: dict[str, str],
    track: str,
    example_file: str,
    next_row: dict[str, str] | None,
) -> list[str]:
    class_id = row["class"]
    module = row["module"]
    session = row["subject_session"]
    level = row["level"]
    track_steps = TRACK_FLOW_STEPS.get(track, TRACK_FLOW_STEPS["generic"])

    steps = [
        f"시작: {class_id} ({session}, {level})",
        f"학습 주제 파악: {module}",
        f"1단계: {track_steps[0]}",
        f"2단계: {track_steps[1]}",
        f"3단계: {track_steps[2]}",
        f"4단계: {track_steps[3]}",
        f"예제 실행: python {class_id}/{example_file}",
    ]
    if next_row is None:
        steps.append("마무리: 학습 노트 작성 및 전체 복습")
    else:
        steps.append(f"다음 준비: {next_row['module']} 연결 포인트 정리")
    return steps


def render_mermaid_flowchart(steps: list[str]) -> str:
    lines = ["flowchart TD"]
    for idx, step in enumerate(steps, start=1):
        lines.append(f'    N{idx}["{sanitize_mermaid_label(step)}"]')
    for idx in range(1, len(steps)):
        lines.append(f"    N{idx} --> N{idx + 1}")
    return "\n".join(lines)


def render_auto_tech_stack_block(
    class_id: str,
    module: str,
    example_file: str,
    track: str,
    mermaid_flow: str,
    flow_image_file: str,
) -> str:
    syntax = TRACK_MAIN_SYNTAX.get(track, TRACK_MAIN_SYNTAX["generic"])
    syntax_text = ", ".join(f"`{item}`" for item in syntax)
    block = f"""
    {AUTO_TECH_STACK_START}
    ### 기술 스택
    - 언어: `Python 3`
    - 실행: `CLI` (`python {class_id}/{example_file}`)
    - 주요 문법: {syntax_text}
    - 학습 포커스: `{module}`

    ### 실습 example.py 동작 원리 (Mermaid Flowchart)
    ```mermaid
    {mermaid_flow}
    ```

    ### Flow PNG 캡처
    ![{class_id} flow]({flow_image_file})
    {AUTO_TECH_STACK_END}
    """
    return dedent(block).strip()


def load_flow_font(size: int) -> ImageFont.ImageFont:
    for font_path in [
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/malgunbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]:
        try:
            return ImageFont.truetype(font_path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap_text_by_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        test = current + ch
        left, top, right, bottom = draw.textbbox((0, 0), test, font=font)
        if (right - left) <= max_width:
            current = test
            continue
        if current:
            lines.append(current)
            current = ch
        else:
            lines.append(ch)
            current = ""
    if current:
        lines.append(current)
    return lines or [text]


def save_flow_png(steps: list[str], out_path: Path, class_id: str, module: str) -> None:
    margin_x = 90
    margin_y = 70
    box_width = 1160
    vertical_gap = 52
    line_height = 30
    min_box_height = 62

    title_font = load_flow_font(28)
    text_font = load_flow_font(22)

    temp_image = Image.new("RGB", (box_width + margin_x * 2, 1000), "white")
    temp_draw = ImageDraw.Draw(temp_image)

    wrapped_steps: list[list[str]] = []
    box_heights: list[int] = []
    for step in steps:
        wrapped = wrap_text_by_width(temp_draw, step, text_font, box_width - 70)
        wrapped_steps.append(wrapped)
        height = max(min_box_height, 24 + line_height * len(wrapped))
        box_heights.append(height)

    title_height = 56
    content_height = sum(box_heights) + vertical_gap * (len(steps) - 1)
    canvas_height = margin_y * 2 + title_height + content_height
    canvas_width = box_width + margin_x * 2

    image = Image.new("RGB", (canvas_width, canvas_height), "#F8FAFC")
    draw = ImageDraw.Draw(image)

    title = f"{class_id} Flow - {module}"
    draw.text((margin_x, margin_y - 8), title, fill="#0F172A", font=title_font)

    colors = ["#E2E8F0", "#DBEAFE", "#DCFCE7", "#FEF3C7", "#FCE7F3", "#E0E7FF"]
    x1 = margin_x
    x2 = margin_x + box_width
    center_x = margin_x + box_width // 2
    y = margin_y + title_height

    for idx, wrapped in enumerate(wrapped_steps):
        box_h = box_heights[idx]
        y1 = y
        y2 = y + box_h
        fill_color = colors[idx % len(colors)]
        draw.rounded_rectangle((x1, y1, x2, y2), radius=20, fill=fill_color, outline="#334155", width=3)

        text_block_h = line_height * len(wrapped)
        text_y = y1 + (box_h - text_block_h) // 2
        for line in wrapped:
            left, top, right, bottom = draw.textbbox((0, 0), line, font=text_font)
            text_w = right - left
            draw.text((center_x - text_w // 2, text_y), line, fill="#0F172A", font=text_font)
            text_y += line_height

        if idx < len(wrapped_steps) - 1:
            arrow_start_y = y2
            arrow_end_y = y2 + vertical_gap - 14
            draw.line((center_x, arrow_start_y, center_x, arrow_end_y), fill="#1E293B", width=4)
            draw.polygon(
                [
                    (center_x, arrow_end_y + 12),
                    (center_x - 10, arrow_end_y - 2),
                    (center_x + 10, arrow_end_y - 2),
                ],
                fill="#1E293B",
            )

        y = y2 + vertical_gap

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, format="PNG")


def choose_track(subject_name: str, module: str) -> str:
    text = f"{subject_name} {module}"
    lowered = text.lower()
    if "rag" in lowered or "retrieval-augmented generation" in lowered:
        return "rag"
    if "langchain" in lowered:
        return "langchain"
    if any(keyword in module for keyword in ["텍스트", "토큰", "임베딩", "자연어", "요약/분류/추출", "언어모델 입력 구조"]):
        return "nlp"
    if any(keyword in module for keyword in ["음성", "STT", "TTS", "오디오", "발화", "화자", "MFCC"]):
        return "speech"
    if any(
        keyword in text
        for keyword in [
            "거대 언어 모델",
            "언어 모델",
            "LLM 개요",
            "생성 파라미터",
            "프롬프트 기반 생성",
            "대화형 응답 설계",
            "안전성/환각 관리",
            "도메인 적용 시나리오",
            "API 연동 실습",
            "생성형 서비스",
        ]
    ):
        return "llm"
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
    tech_stack_block: str,
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
    term_guide_block = render_term_guide(subject_name=subject_name, module=module, track=track)
    tech_stack_section = tech_stack_block.strip()

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

    ### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
    __TERM_GUIDE_BLOCK__

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

    __TECH_STACK_SECTION__

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
    body = body.replace("__TERM_GUIDE_BLOCK__", term_guide_block)
    if tech_stack_section:
        body = body.replace("__TECH_STACK_SECTION__", tech_stack_section)
    else:
        body = body.replace("__TECH_STACK_SECTION__\n", "")
        body = body.replace("__TECH_STACK_SECTION__", "")
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

        flow_steps = build_flow_steps(
            row=row,
            track=track,
            example_file=example_path.name,
            next_row=next_row,
        )
        flow_mermaid = render_mermaid_flowchart(flow_steps)
        flow_image_file = f"{class_id}_flow.png"
        save_flow_png(
            steps=flow_steps,
            out_path=class_dir / flow_image_file,
            class_id=class_id,
            module=module,
        )
        tech_stack_block = render_auto_tech_stack_block(
            class_id=class_id,
            module=module,
            example_file=example_path.name,
            track=track,
            mermaid_flow=flow_mermaid,
            flow_image_file=flow_image_file,
        )

        md_path.write_text(
            render_markdown(
                row=row,
                track=track,
                example_file=example_path.name,
                quiz_file=quiz_path.name,
                prev_row=prev_row,
                next_row=next_row,
                tech_stack_block=tech_stack_block,
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
