# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import json
import random
import re
from pathlib import Path
from textwrap import dedent
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


TRACK_QUIZ_BANK = {
    "python": {
        "concept": "입력값을 조건문과 반복문으로 처리해 원하는 출력으로 만든다.",
        "action": "작은 입력부터 실행하고 print()로 중간 값을 확인한다.",
        "pitfall": "입력 경계값(0, 빈 문자열, 음수)을 테스트하지 않고 예시 1개만 확인한다.",
        "check": "같은 로직을 최소 3개 입력으로 실행하고 조건 분기가 모두 동작하는지 확인한다.",
        "outcome": "함수로 코드를 분리해 재사용성과 가독성을 높인다.",
    },
    "data": {
        "concept": "데이터 전처리로 열 구조를 정리한 뒤 통계를 계산한다.",
        "action": "columns와 shape를 먼저 확인하고 계산 순서를 정한다.",
        "pitfall": "결측치/자료형을 확인하지 않은 채 평균과 시각화를 바로 계산한다.",
        "check": "전처리 전후 행 수, 결측치 개수, 핵심 통계를 비교표로 남긴다.",
        "outcome": "정리된 표 데이터로 의미 있는 패턴을 설명할 수 있다.",
    },
    "ml": {
        "concept": "입력(X)과 정답(y)을 사용해 예측 규칙(모델)을 학습한다.",
        "action": "X/y 형태를 점검하고 오차를 계산해 품질을 확인한다.",
        "pitfall": "학습 데이터와 평가 데이터를 섞어 과대평가된 점수를 믿는다.",
        "check": "훈련/검증 분리를 유지하고 오차 지표(MSE/정확도)를 함께 기록한다.",
        "outcome": "예측 결과와 오차를 해석해 개선 아이디어를 낼 수 있다.",
    },
    "nlp": {
        "concept": "문장을 정제하고 토큰으로 나눠 패턴을 분석한다.",
        "action": "전처리 후 토큰 리스트를 먼저 출력해 결과를 점검한다.",
        "pitfall": "불용어/특수문자 정제를 생략해 토큰 빈도 해석을 왜곡한다.",
        "check": "전처리 전후 토큰 샘플을 비교하고 빈도 변화 이유를 설명한다.",
        "outcome": "주요 단어 빈도를 계산해 핵심 내용을 찾을 수 있다.",
    },
    "speech": {
        "concept": "음성 데이터는 길이, 텍스트 라벨, 품질 정보를 함께 다룬다.",
        "action": "샘플 발화를 몇 개 확인하고 길이/라벨 기준으로 필터링한다.",
        "pitfall": "오디오 길이와 라벨 품질을 확인하지 않아 학습 데이터 잡음이 증가한다.",
        "check": "샘플 청취와 라벨 점검 후 길이/잡음 기준 필터링 로그를 남긴다.",
        "outcome": "음성 데이터 품질 지표를 계산하고 해석할 수 있다.",
    },
    "prompt": {
        "concept": "역할(role), 목표(goal), 형식(format)을 분명히 써야 답변 품질이 오른다.",
        "action": "템플릿 변수(role, question)를 분리해 프롬프트를 구성한다.",
        "pitfall": "역할, 목표, 출력형식을 섞어 써서 재현 불가능한 응답을 만든다.",
        "check": "같은 질문을 2회 이상 실행해 형식 일관성과 누락 항목을 점검한다.",
        "outcome": "좋은 프롬프트와 나쁜 프롬프트의 차이를 설명할 수 있다.",
    },
    "langchain": {
        "concept": "작업을 단계별 체인으로 분리하면 재사용과 디버깅이 쉬워진다.",
        "action": "각 단계의 입력/출력을 출력해 흐름을 먼저 검증한다.",
        "pitfall": "체인 단계를 한 번에 묶어 디버깅 지점을 확인하지 못한다.",
        "check": "각 단계 입력/출력 스냅샷을 저장해 실패 지점을 단계별로 추적한다.",
        "outcome": "단계 함수를 조합해 반복 가능한 워크플로우를 만들 수 있다.",
    },
    "rag": {
        "concept": "질문과 관련 문서를 검색하고 근거를 바탕으로 답변을 만든다.",
        "action": "검색 결과와 최종 답변을 분리해서 출력한다.",
        "pitfall": "검색 근거 없이 모델 답변만 채택해 환각을 놓친다.",
        "check": "답변 문장별로 근거 문서와 출처를 매핑해 근거 없는 문장을 표시한다.",
        "outcome": "답변에 출처를 포함해 신뢰도를 높일 수 있다.",
    },
    "generic": {
        "concept": "복잡한 문제를 작은 단계로 나누면 해결이 쉬워진다.",
        "action": "TODO를 1개씩 구현하고 매 단계마다 실행 확인한다.",
        "pitfall": "요구사항을 분해하지 않고 코드를 길게 작성해 오류 원인을 숨긴다.",
        "check": "작업을 TODO 단위로 나누고 단계별 성공 조건을 체크리스트로 검증한다.",
        "outcome": "문제를 구조화해 스스로 학습 흐름을 만들 수 있다.",
    },
}


def module_core_name(module: str) -> str:
    return module.split("·", maxsplit=1)[0].strip()


DATA_VIZ_QUIZ_BANK = {
    "데이터 분석 환경 구성": {
        "concept": "분석 프로세스와 정형/비정형, CSV/Excel/JSON 구조를 먼저 이해해야 전처리 방향이 맞아진다.",
        "action": "문제 정의 -> 수집 -> 정제 -> 분석 -> 시각화 흐름과 파일 구조를 먼저 확인한다.",
        "pitfall": "데이터 유형과 포맷 차이를 구분하지 않아 로딩/정제 단계에서 오류가 반복된다.",
        "check": "정형/비정형 예시와 CSV/Excel/JSON 차이를 표로 정리해 검증한다.",
        "outcome": "분석 시작 전에 데이터 구조와 도구 선택 기준을 설명할 수 있다.",
    },
    "NumPy 기초": {
        "concept": "배열(Array), list와 ndarray 차이, 벡터화 연산, 인덱싱/슬라이싱이 NumPy 핵심이다.",
        "action": "같은 계산을 list 반복문과 ndarray 벡터화 방식으로 비교한다.",
        "pitfall": "ndarray 특성을 이해하지 않고 list 방식으로만 처리해 성능과 정확도를 놓친다.",
        "check": "케이스별 인덱싱/슬라이싱 결과와 기초 통계를 함께 검증한다.",
        "outcome": "벡터화 기반 수치 연산을 안정적으로 적용할 수 있다.",
    },
    "Pandas 데이터프레임 기초": {
        "concept": "Series/DataFrame, 데이터 로딩/저장, 행/열 선택, 필터링, 정렬, 기초 통계가 Pandas 기본기다.",
        "action": "컬럼 선택·행 선택·조건 필터링·정렬을 순서대로 실행해 확인한다.",
        "pitfall": "행/열 선택 기준이 불명확해 의도와 다른 데이터가 분석에 포함된다.",
        "check": "필터링·정렬 전후 행 수와 핵심 통계를 비교해 기록한다.",
        "outcome": "표 데이터 조작을 재현 가능한 절차로 수행할 수 있다.",
    },
    "결측치/이상치 처리": {
        "concept": "결측치 처리, 중복 제거, 데이터 타입 변환은 데이터 정제의 핵심 축이다.",
        "action": "결측/중복/타입 변환 규칙을 분리해 단계별로 적용한다.",
        "pitfall": "정제 규칙 없이 평균/모델링을 진행해 분석 결과가 왜곡된다.",
        "check": "정제 전후 행 수·결측 수·중복 수를 비교표로 남긴다.",
        "outcome": "정제 규칙과 품질 개선 효과를 근거로 설명할 수 있다.",
    },
    "문자열/날짜 전처리": {
        "concept": "문자열 정리, 날짜형 처리, 컬럼명 정리는 후속 분석 안정성을 높인다.",
        "action": "공백/대소문자/특수문자와 날짜 포맷, 컬럼명 규칙을 표준화한다.",
        "pitfall": "컬럼명/날짜 포맷 불일치를 방치해 groupby/join 단계에서 오류가 발생한다.",
        "check": "파싱 성공/실패 건수와 컬럼명 변환 전후 스키마를 기록한다.",
        "outcome": "텍스트·날짜·스키마 정리를 자동화할 수 있다.",
    },
    "그룹화와 집계": {
        "concept": "파생변수 생성과 groupby/aggregation으로 데이터 패턴을 요약한다.",
        "action": "파생변수 추가 후 groupby와 agg 조합을 비교 실행한다.",
        "pitfall": "파생변수 정의와 그룹 키를 검증하지 않아 잘못된 집계가 발생한다.",
        "check": "원본 샘플과 그룹 집계 결과를 대조해 검증한다.",
        "outcome": "집계 지표를 근거로 의미 있는 인사이트를 제시할 수 있다.",
    },
    "데이터 병합과 변환": {
        "concept": "merge/join, pivot table, 범주형 데이터 처리는 데이터 가공의 핵심이다.",
        "action": "join 방식과 pivot table 구조를 비교해 분석용 테이블을 구성한다.",
        "pitfall": "키 누락·중복과 범주형 순서를 확인하지 않아 결과 해석이 어긋난다.",
        "check": "병합 전후 행 수, key 일치율, pivot 결과를 함께 검증한다.",
        "outcome": "다중 소스 데이터를 일관된 분석 구조로 변환할 수 있다.",
    },
    "Matplotlib 시각화 기초": {
        "concept": "시각화 원칙과 Matplotlib 기본 문법(line/bar/scatter/histogram), 한글 폰트/제목/축/범례 설정이 핵심이다.",
        "action": "동일 데이터를 line/bar/scatter/histogram으로 각각 그려 비교한다.",
        "pitfall": "한글 폰트·축·범례 설정을 생략해 그래프 해석이 왜곡된다.",
        "check": "차트 유형별 결과와 라벨/범례 설정을 체크리스트로 검증한다.",
        "outcome": "시각화 결과를 명확한 그래프 구성과 함께 전달할 수 있다.",
    },
    "Seaborn/실전 차트 해석": {
        "concept": "EDA에서 분포, 평균/중앙값/표준편차, 상관관계, 패턴, 가설 설정을 다룬다.",
        "action": "분포 지표와 상관 차트를 함께 확인해 문제 정의와 가설을 작성한다.",
        "pitfall": "요약 통계 없이 시각 패턴만 보고 성급하게 결론을 내린다.",
        "check": "EDA 결과를 근거 수치와 가설 문장으로 정리한다.",
        "outcome": "탐색 결과를 다음 분석/모델링 단계로 연결할 수 있다.",
    },
    "Agent 시스템 통합 구현": {
        "concept": "전처리-집계-시각화를 통합 파이프라인으로 연결한다.",
        "action": "정상/지연/오류 입력을 단계별로 실행해 실패 지점을 찾는다.",
        "pitfall": "정상 케이스만 테스트해 운영 장애 시나리오를 놓친다.",
        "check": "단계별 로그와 복구 절차(재시도/롤백)를 함께 점검한다.",
        "outcome": "통합 파이프라인의 안정성과 운영 준비도를 검증할 수 있다.",
    },
}


ML_DEEP_QUIZ_BANK = {
    "ML/DL 개요와 문제정의": {
        "concept": "AI/머신러닝/딥러닝 차이와 규칙기반/학습기반 접근을 구분해야 문제정의가 정확해진다.",
        "action": "학습 데이터, feature, label, 목표 지표를 먼저 정의한다.",
        "pitfall": "문제 유형을 정하지 않고 모델부터 선택해 성능 해석이 불가능해진다.",
        "check": "문제정의 문서에 입력/출력/지표/제약을 명시했는지 점검한다.",
        "outcome": "ML/DL 적용 가능성과 학습 흐름을 구조적으로 설명할 수 있다.",
    },
    "지도학습 기초": {
        "concept": "지도학습/비지도학습과 분류/회귀 구분, 훈련/검증/테스트 분할이 핵심이다.",
        "action": "train/valid/test 분할을 먼저 고정하고 baseline을 실행한다.",
        "pitfall": "데이터 분할 없이 단일 데이터 성능만 보고 일반화 성능을 오판한다.",
        "check": "훈련-검증 성능 차이와 누출 여부를 함께 검증한다.",
        "outcome": "문제 유형과 데이터 분할 전략을 일관되게 설계할 수 있다.",
    },
    "회귀 모델": {
        "concept": "scikit-learn 선형회귀와 회귀 지표(MAE/MSE/RMSE/R²) 해석이 회귀 기본기다.",
        "action": "train_test_split -> fit -> predict 순서로 baseline 회귀를 실행한다.",
        "pitfall": "R²만 보고 오차 크기(MAE/RMSE)를 확인하지 않는다.",
        "check": "MAE/MSE/RMSE/R²를 함께 기록하고 split 조건을 고정한다.",
        "outcome": "회귀 모델 결과를 오차 관점으로 해석하고 개선할 수 있다.",
    },
    "분류 모델": {
        "concept": "로지스틱 회귀, KNN, 의사결정나무, 랜덤포레스트, SVM은 대표 분류 모델군이다.",
        "action": "Pipeline으로 전처리+모델을 연결해 여러 분류기를 같은 조건에서 비교한다.",
        "pitfall": "정확도(Accuracy)만 보고 정밀도/재현율/F1을 무시한다.",
        "check": "Confusion Matrix와 F1-score를 함께 비교한다.",
        "outcome": "분류 모델별 특성을 이해하고 문제에 맞게 선택할 수 있다.",
    },
    "모델 평가 지표": {
        "concept": "회귀/분류 지표, ROC/AUC, 교차검증을 함께 봐야 신뢰 가능한 평가가 된다.",
        "action": "문제 유형에 맞는 지표를 먼저 고른 뒤 계산한다.",
        "pitfall": "단일 split 결과를 일반화 성능으로 과대해석한다.",
        "check": "교차검증 평균/편차와 ROC/AUC를 함께 보고한다.",
        "outcome": "지표 기반 모델 선택 근거를 명확히 제시할 수 있다.",
    },
    "특성공학과 전처리": {
        "concept": "feature engineering, 스케일링/정규화/인코딩, Grid Search는 성능 개선 핵심이다.",
        "action": "전처리와 모델을 Pipeline으로 연결하고 baseline 대비 개선을 측정한다.",
        "pitfall": "특성 추가만 반복하고 데이터 누출 여부를 확인하지 않는다.",
        "check": "feature 추가 전후 지표와 best params를 비교 기록한다.",
        "outcome": "전처리-모델-튜닝 흐름을 재현 가능한 실험으로 운영할 수 있다.",
    },
    "과적합과 일반화": {
        "concept": "과적합은 훈련 성능 과대, 일반화는 미지 데이터 성능 유지 능력이다.",
        "action": "훈련/검증 곡선을 비교해 과적합 신호를 먼저 점검한다.",
        "pitfall": "훈련 성능 개선을 일반화 성능 개선으로 착각한다.",
        "check": "교차검증과 규제 적용 전후를 같은 지표로 비교한다.",
        "outcome": "과적합을 탐지하고 일반화 개선 전략을 적용할 수 있다.",
    },
    "신경망 기초": {
        "concept": "TensorFlow 또는 PyTorch로 간단한 신경망과 학습 루프를 구성하는 것이 핵심이다.",
        "action": "epoch, batch, optimizer를 바꿔 손실/정확도 변화를 확인한다.",
        "pitfall": "학습 루프 개념 없이 프레임워크 코드만 복사해 원인을 해석하지 못한다.",
        "check": "epoch/batch/optimizer 설정과 결과를 함께 기록한다.",
        "outcome": "프레임워크 기반 딥러닝 기초 실습을 독립적으로 수행할 수 있다.",
    },
    "딥러닝 학습 구조": {
        "concept": "MNIST(또는 대체 digits) 분류 실습으로 예측/오분류 분석까지 연결한다.",
        "action": "기본 분류 모델 학습 후 예측값과 오분류 샘플을 확인한다.",
        "pitfall": "정확도 숫자만 보고 오분류 패턴 분석을 생략한다.",
        "check": "오분류 사례를 최소 3건 이상 분석해 개선안을 기록한다.",
        "outcome": "딥러닝 분류 실습 결과를 시각화와 함께 해석할 수 있다.",
    },
    "Agent 시스템 통합 구현": {
        "concept": "학습/평가/배포 관점을 통합해 운영 가능한 ML/DL 파이프라인을 구성한다.",
        "action": "정상/오류 입력으로 단계별 로그를 검증한다.",
        "pitfall": "모델 정확도만 보고 운영 지표(지연/복구/버전)를 점검하지 않는다.",
        "check": "모델 버전, 평가 지표, 롤백 절차를 함께 점검한다.",
        "outcome": "ML/DL 결과를 실제 서비스 운영 관점으로 연결할 수 있다.",
    },
}


PYTHON_PL_QUIZ_BANK = {
    "오리엔테이션 및 개발환경 준비": {
        "concept": "인터프리터·가상환경·의존성 고정은 실행 재현성의 기본이다.",
        "action": "`python --version`, `where python`, `.venv` 활성화 상태를 먼저 확인한다.",
        "pitfall": "전역 Python과 가상환경 Python을 섞어 패키지 설치 경로가 꼬인다.",
        "check": "`sys.executable` 경로가 프로젝트 `.venv`를 가리키는지 확인하고 샘플 import 테스트를 통과한다.",
        "outcome": "실습 환경을 스스로 재현하고 환경 이슈를 분리해 해결할 수 있다.",
    },
    "변수와 자료형": {
        "concept": "변수/상수 관례/타입/배열(list) 모델을 구분해 데이터를 안전하게 다룬다.",
        "action": "값을 할당한 뒤 `type()`과 `isinstance()`로 타입 가정을 즉시 검증한다.",
        "pitfall": "문자열 숫자를 정수로 변환하지 않아 연산 결과가 의도와 달라진다.",
        "check": "변수·상수·list를 포함한 예제를 만들고 경계 인덱스까지 테스트한다.",
        "outcome": "PL 기초 데이터 모델(바인딩·타입·배열)을 코드로 설명할 수 있다.",
    },
    "연산자와 조건문": {
        "concept": "연산자와 조건식은 불리언 평가를 통해 분기 경로를 결정한다.",
        "action": "조건식을 괄호로 명확히 하고 경계값 입력으로 각 분기 결과를 확인한다.",
        "pitfall": "연산자 우선순위를 오해해 의도와 다른 조건 분기가 실행된다.",
        "check": "`if/elif/else`의 모든 경로를 최소 1회 이상 실행해 분기 누락이 없는지 확인한다.",
        "outcome": "표현식과 분기 로직을 예측 가능하게 설계할 수 있다.",
    },
    "반복문과 흐름제어": {
        "concept": "for/while 반복과 흐름제어문은 시퀀스 처리 성능과 정확도를 좌우한다.",
        "action": "반복 변수와 누적 변수 변화를 `print()`로 추적하며 루프를 검증한다.",
        "pitfall": "종료 조건이 약해 무한 루프 또는 누락 집계가 발생한다.",
        "check": "`break/continue` 유무에 따른 결과 차이를 비교하고 종료 조건을 문서화한다.",
        "outcome": "반복 처리 로직을 안정적으로 설계하고 디버깅할 수 있다.",
    },
    "함수와 모듈": {
        "concept": "함수 시그니처와 모듈 분리는 재사용성과 테스트 가능성을 높인다.",
        "action": "중복 코드를 함수로 추출하고 입력·출력 계약을 먼저 정의한다.",
        "pitfall": "전역 상태에 의존해 함수 재사용 시 부작용이 발생한다.",
        "check": "함수별 정상/경계 테스트를 수행하고 다른 모듈에서 import 실행을 확인한다.",
        "outcome": "책임 분리된 함수·모듈 구조로 코드를 확장할 수 있다.",
    },
    "모듈과 패키지": {
        "concept": "import 체계와 표준 라이브러리(random/math/datetime/os), 사용자 모듈 분리가 핵심이다.",
        "action": "표준 라이브러리 호출과 사용자 모듈 import를 같은 실습에서 검증한다.",
        "pitfall": "패키지 설치 경로(.venv)와 인터프리터 경로가 달라 import 오류가 반복된다.",
        "check": "pip 설치 환경과 import 성공/실패 케이스를 함께 기록한다.",
        "outcome": "모듈/패키지 구조를 재현 가능하게 운영할 수 있다.",
    },
    "컬렉션 자료구조": {
        "concept": "list/tuple/dict/set 선택은 데이터 접근 패턴과 연산 효율을 결정한다.",
        "action": "동일 데이터를 여러 컬렉션으로 표현해 조회·수정 패턴을 비교한다.",
        "pitfall": "가변 객체 공유(얕은 복사)를 놓쳐 예상치 못한 동시 변경이 발생한다.",
        "check": "컬렉션별 장단점을 근거로 구조 선택 이유를 설명하고 컴프리헨션 결과를 검증한다.",
        "outcome": "문제 특성에 맞는 자료구조를 선택해 코드 품질을 높일 수 있다.",
    },
    "파일 입출력": {
        "concept": "파일 입출력은 경로·모드·인코딩·직렬화 규칙을 함께 다뤄야 안전하다.",
        "action": "`with open(..., encoding='utf-8')`으로 읽기/쓰기 후 재로드 검증을 수행한다.",
        "pitfall": "인코딩이나 파일 모드를 명시하지 않아 데이터가 깨지거나 누락된다.",
        "check": "저장 전후 데이터 동등성 확인과 파일 예외 케이스(미존재/권한)를 점검한다.",
        "outcome": "영속 데이터 처리 파이프라인을 안정적으로 구현할 수 있다.",
    },
    "예외처리와 디버깅": {
        "concept": "예외처리는 정상 경로와 실패 경로를 분리해 프로그램 복원력을 높인다.",
        "action": "오류를 재현한 뒤 traceback 라인 기준으로 원인을 좁히고 `try/except`를 적용한다.",
        "pitfall": "광범위한 `except Exception`으로 원인을 숨겨 디버깅 정보를 잃는다.",
        "check": "예외 타입별 처리 정책을 분리하고 회귀 테스트로 재발 방지를 확인한다.",
        "outcome": "디버깅 근거를 남기며 안정적인 오류 처리 코드를 작성할 수 있다.",
    },
    "객체지향 기초": {
        "concept": "클래스는 상태와 동작을 캡슐화해 복잡한 도메인을 모델링한다.",
        "action": "핵심 개체를 클래스화하고 `__init__`·메서드·상태 전이를 테스트한다.",
        "pitfall": "책임이 다른 로직을 한 클래스에 몰아 결합도가 과도해진다.",
        "check": "객체 생성/메서드 호출 전후 상태 불변식을 검증하고 필요 시 상속을 최소 적용한다.",
        "outcome": "클래스 설계 원칙으로 확장 가능한 구조를 만들 수 있다.",
    },
    "미니 실습 프로젝트": {
        "concept": "프로젝트는 변수·함수·클래스·예외처리를 통합한 PL 종합 적용 단계다.",
        "action": "요구사항을 TODO로 분해하고 최소 기능부터 구현 후 반복 개선한다.",
        "pitfall": "설계 없이 구현부터 시작해 모듈 경계와 테스트 전략이 무너진다.",
        "check": "핵심 시나리오 테스트를 통과하고 리팩터링 전후 동작 동일성을 확인한다.",
        "outcome": "작동하는 프로그램을 구조적으로 완성하고 개선 루프를 운영할 수 있다.",
    },
}

NLP_SPEECH_QUIZ_BANK = {
    "NLP/STT/TTS 개요": {
        "concept": "NLP/STT/TTS는 텍스트와 음성 데이터를 전처리-특징추출-모델-평가 흐름으로 통합하는 구조다.",
        "action": "텍스트/음성 입력과 출력 스키마를 먼저 분리해 파이프라인으로 연결한다.",
        "pitfall": "개념만 암기하고 데이터 품질 검증(라벨/잡음/누락)을 생략한다.",
        "check": "전처리-특징-모델-평가 단계가 모두 연결된 최소 실행 흐름을 검증한다.",
        "outcome": "자연어·음성 통합 모델 개발의 전체 흐름을 설명할 수 있다.",
    },
    "텍스트 데이터 수집": {
        "concept": "문장/문서/토큰, 형태소/품사/개체명, 품질 이슈를 이해해야 NLP 입력이 안정된다.",
        "action": "뉴스/리뷰/대화 데이터를 문장-토큰 단위로 분해하고 품질 이슈를 기록한다.",
        "pitfall": "텍스트 유형과 품질 문제를 구분하지 않아 이후 전처리 규칙이 흔들린다.",
        "check": "문장/문서/토큰 구조와 품질 플래그를 같은 리포트에서 검증한다.",
        "outcome": "자연어 데이터 구조와 품질 기준을 실습 코드로 제시할 수 있다.",
    },
    "텍스트 정제와 토큰화": {
        "concept": "정규화, 토큰화, 불용어 제거, 형태소 분석, 문장 분리, 벡터화 기초가 핵심이다.",
        "action": "정제 전/후 결과를 비교하고 BoW/TF-IDF 입력까지 연결한다.",
        "pitfall": "불용어/기호 정제를 생략해 토큰 빈도와 벡터화 결과가 왜곡된다.",
        "check": "전처리 단계별 출력(문장, 토큰, 벡터)을 순서대로 검증한다.",
        "outcome": "텍스트 전처리 파이프라인을 재현 가능한 코드로 구성할 수 있다.",
    },
    "임베딩 기초": {
        "concept": "BoW/TF-IDF와 Word/Sentence Embedding을 비교해 의미 기반 표현을 이해한다.",
        "action": "동일 문서셋으로 벡터화 방식을 바꿔 유사도와 분류 성능을 비교한다.",
        "pitfall": "벡터화 방식별 장단점 확인 없이 단일 표현만 사용한다.",
        "check": "유사도 상위 문장과 분류 결과를 함께 기록해 해석한다.",
        "outcome": "문장 임베딩 기반 유사도/분류 실습을 수행할 수 있다.",
    },
    "언어모델 입력 구조": {
        "concept": "토큰 인덱싱, 패딩, 시퀀스 길이 정규화는 모델 입력 안정성의 기본이다.",
        "action": "시퀀스 입력을 패딩/트렁케이션 규칙으로 통일해 테스트한다.",
        "pitfall": "입력 길이/토큰 매핑 검증 없이 모델에 바로 전달한다.",
        "check": "입력 포맷 오류(빈 토큰/길이 초과)를 사전에 검증한다.",
        "outcome": "언어모델 입력 구조를 일관되게 설계하고 점검할 수 있다.",
    },
    "음성 데이터 구조 이해": {
        "concept": "샘플링/주파수/진폭, WAV/MP3 포맷, 라벨·메타데이터 구조를 함께 다뤄야 한다.",
        "action": "오디오 메타데이터(샘플레이트·길이·화자·라벨)를 표준 스키마로 정리한다.",
        "pitfall": "포맷/샘플레이트 차이를 무시해 전처리 단계에서 품질 편차가 커진다.",
        "check": "포맷별 샘플 품질과 라벨 정합성을 동시에 검증한다.",
        "outcome": "음성 데이터셋의 구조와 메타데이터 설계를 설명할 수 있다.",
    },
    "오디오 전처리": {
        "concept": "파일 로딩, 구간 분할, 잡음 제거, 샘플레이트 변환, Spectrogram/Mel 변환이 핵심이다.",
        "action": "전처리 단계별 결과를 저장하고 전후 품질 지표를 비교한다.",
        "pitfall": "세그먼트/리샘플링 기준이 불명확해 모델 입력 규격이 흔들린다.",
        "check": "세그먼트 개수, 샘플레이트, Mel 특징 차원을 단계별로 검증한다.",
        "outcome": "음성 전처리 파이프라인을 안정적으로 구성할 수 있다.",
    },
    "특징 추출(MFCC 등)": {
        "concept": "MFCC 특징과 음성 분류 기초, ASR/TTS 서비스 구조 연결이 핵심이다.",
        "action": "MFCC를 추출하고 분류/인식 태스크 입력으로 연결한다.",
        "pitfall": "특징 차원/품질 검증 없이 모델 입력으로 바로 사용한다.",
        "check": "MFCC 값 범위와 모델 입력 차원 정합성을 점검한다.",
        "outcome": "음성 특징 추출 결과를 서비스 구조와 연결해 설명할 수 있다.",
    },
    "텍스트 분류 기초": {
        "concept": "텍스트 분류와 감성분석, 문장 유사도 계산은 NLP 기본 응용 태스크다.",
        "action": "뉴스/리뷰 데이터를 전처리해 기본 분류와 감성 결과를 비교한다.",
        "pitfall": "라벨 품질과 오분류 사례를 점검하지 않고 정확도만 확인한다.",
        "check": "분류 결과와 유사도 근거를 함께 기록해 해석한다.",
        "outcome": "문서분류/감성분석 기초 실습을 독립적으로 수행할 수 있다.",
    },
    "시퀀스 모델 기초": {
        "concept": "토큰 순서를 반영하는 시퀀스 표현은 문맥 이해 성능을 높인다.",
        "action": "시퀀스 입력과 baseline 입력을 같은 데이터에서 비교한다.",
        "pitfall": "패딩/길이 정책을 고정하지 않아 실험 재현성이 깨진다.",
        "check": "시퀀스 길이 처리 규칙과 성능 차이를 함께 검증한다.",
        "outcome": "시퀀스 기반 모델 입력/평가 흐름을 설명할 수 있다.",
    },
    "멀티모달 데이터 연결": {
        "concept": "텍스트 특징과 음성 특징을 정렬해 결합하는 멀티모달 연결이 핵심이다.",
        "action": "모달 정렬(시간/인덱스) 후 결합 특징으로 통합 추론을 수행한다.",
        "pitfall": "길이/정렬 불일치를 방치해 모달 결합 결과가 왜곡된다.",
        "check": "모달 결합 전후 성능과 오류 케이스를 비교한다.",
        "outcome": "멀티모달 데이터 연결 파이프라인을 구성할 수 있다.",
    },
    "실전 데이터셋 설계": {
        "concept": "뉴스/리뷰 전처리, 텍스트 분류, 오디오 분석, 특징 추출을 통합한 프로젝트형 데이터셋 설계가 핵심이다.",
        "action": "텍스트·음성 실습 결과를 하나의 데이터셋 버전 정책으로 문서화한다.",
        "pitfall": "품질 기준/라벨 정책 없이 데이터만 모아 재현 가능한 실험이 불가능해진다.",
        "check": "버전, 라벨, 품질 임계치, 재학습 트리거를 함께 점검한다.",
        "outcome": "실제 AI 응용 프로젝트에 바로 적용 가능한 데이터 기반 역량을 확보한다.",
    },
}

SPEECH_TTS_STT_QUIZ_BANK = {
    "음성 AI 개요": {
        "concept": "STT는 음성→텍스트, TTS는 텍스트→음성 변환으로 동작 원리와 활용 목적이 다르다.",
        "action": "음성비서·콜센터·자막·낭독 서비스 시나리오를 STT/TTS 기능에 매핑한다.",
        "pitfall": "STT/TTS를 같은 파이프라인으로만 보고 과업별 지표와 요구사항을 분리하지 않는다.",
        "check": "STT와 TTS의 입력·출력·핵심 지표를 각각 정의해 비교한다.",
        "outcome": "STT/TTS 차이와 음성 AI 서비스 구조를 설명할 수 있다.",
    },
    "STT 파이프라인": {
        "concept": "음성 수집, 텍스트 정렬, 발화 단위/화자 관리, 데이터 증강이 STT 데이터 준비 핵심이다.",
        "action": "발화 메타데이터와 스크립트 정렬 검증 규칙을 먼저 고정한다.",
        "pitfall": "정렬 품질 점검 없이 학습 데이터를 바로 사용해 인식 오류가 누적된다.",
        "check": "발화-스크립트 정합성과 증강 전후 분포를 함께 검증한다.",
        "outcome": "STT 학습 데이터 준비 과정을 재현 가능한 절차로 구성할 수 있다.",
    },
    "STT 데이터 라벨링": {
        "concept": "라벨 정규화, 정렬 검증, 메타데이터 품질이 STT 성능의 기초 체력을 결정한다.",
        "action": "라벨 오류(누락/오타/시간 불일치)와 메타데이터 누락을 자동 탐지하는 규칙을 실행한다.",
        "pitfall": "라벨 검수 루프 없이 모델만 튜닝해도 오류 원인이 사라지지 않는다.",
        "check": "라벨 정규화 전후, 정렬 오차, 메타데이터 스키마 검증 로그를 함께 비교한다.",
        "outcome": "STT 라벨/메타데이터 품질을 정량적으로 점검하고 개선할 수 있다.",
    },
    "STT 전처리/학습": {
        "concept": "파형, STFT, Mel-Spectrogram, MFCC는 STT 입력 특징 추출의 핵심 축이다.",
        "action": "동일 발화에서 STFT/Mel/MFCC를 계산해 특징 차이를 비교한다.",
        "pitfall": "특징 차원/품질 검증 없이 학습 입력으로 사용해 성능 불안정을 만든다.",
        "check": "특징 차원 정합성과 발음-음향 관계 변화를 검증한다.",
        "outcome": "STT 전처리-학습 흐름을 특징 중심으로 설명할 수 있다.",
    },
    "TTS 파이프라인": {
        "concept": "텍스트→발음열→음향모델→보코더 구조가 TTS 기본 동작 흐름이다.",
        "action": "Tacotron/FastSpeech/VITS 구조와 장단점을 비교해 기록한다.",
        "pitfall": "발음열 변환과 보코더 단계를 분리하지 않아 품질 저하 원인 추적이 어렵다.",
        "check": "발음열, 음향특징, 파형 생성 단계별 출력을 순서대로 점검한다.",
        "outcome": "TTS 모델 구조와 핵심 컴포넌트를 구체적으로 설명할 수 있다.",
    },
    "발화/화자 특성 이해": {
        "concept": "발화/화자 특성은 STT 정확도와 TTS 자연스러움 모두에 영향을 준다.",
        "action": "화자별 메타데이터와 품질 지표를 비교해 편향을 점검한다.",
        "pitfall": "화자 분포 불균형을 무시해 실전 추론 성능이 특정 화자에 편중된다.",
        "check": "화자 특성 통계와 성능 차이를 같은 기준으로 검증한다.",
        "outcome": "화자 특성을 반영한 데이터 설계와 모델 개선 방향을 제시할 수 있다.",
    },
    "TTS 전처리/학습": {
        "concept": "텍스트 정규화, 발음열 변환, 음향모델/보코더 연결이 TTS 학습 핵심이다.",
        "action": "톤/속도 조절 파라미터를 바꿔 한국어 TTS 결과를 비교한다.",
        "pitfall": "한국어 발음 규칙을 반영하지 않아 발음 오류와 부자연스러운 합성이 발생한다.",
        "check": "샘플 문장 낭독 결과에서 발음·톤·속도 품질을 함께 점검한다.",
        "outcome": "한국어 TTS 전처리와 학습 실습을 안정적으로 수행할 수 있다.",
    },
    "음성 품질 평가": {
        "concept": "STT 성능과 TTS 품질을 통합 지표로 평가해야 서비스 품질이 보장된다.",
        "action": "STT 자막 품질과 TTS 낭독 품질을 동일 시나리오에서 비교한다.",
        "pitfall": "한쪽 지표만 개선하고 다른 쪽 품질 저하를 놓친다.",
        "check": "구간별 오류와 품질 지표를 통합 리포트로 검증한다.",
        "outcome": "STT/TTS 품질 평가 체계를 설계하고 해석할 수 있다.",
    },
    "모델 추론 및 튜닝": {
        "concept": "CTC/Whisper 기반 STT와 TTS 추론 튜닝은 정확도, 지연, 안정성을 함께 최적화해야 한다.",
        "action": "CTC 디코딩/Whisper 옵션과 STT/TTS 파라미터 조합을 바꿔 결과와 지연을 비교한다.",
        "pitfall": "단일 지표만 보고 튜닝해 서비스 레벨 성능 저하를 초래한다.",
        "check": "한국어 STT 오류 유형(받침/연음/숫자/외래어)과 튜닝 전후 성능·롤백 기준을 동일 조건으로 점검한다.",
        "outcome": "CTC/Whisper를 포함한 STT/TTS 추론 튜닝 루프를 운영 기준에 맞게 실행할 수 있다.",
    },
    "실전 음성 모델 데모": {
        "concept": "오픈소스 STT/TTS 실습을 통합해 음성 AI 서비스 데모를 완성한다.",
        "action": "STT 텍스트 추출·자막 생성과 TTS 낭독을 하나의 흐름으로 구현한다.",
        "pitfall": "개별 실습만 수행하고 서비스형 통합 검증을 생략한다.",
        "check": "STT 성능, TTS 품질, 오류 처리, 운영 로그를 함께 검증한다.",
        "outcome": "음성 AI 서비스 구현을 위한 실전 기반 역량을 확보한다.",
    },
}


PYTHON_PL_MODULE_ALIASES = {
    "수업 준비 1: 필수 플랫폼 가입/계정 설정 (class001)": "오리엔테이션 및 개발환경 준비",
    "수업 준비 2: 필수 소프트웨어 설치 (class002)": "오리엔테이션 및 개발환경 준비",
    "수업 준비 3: 개발환경 검증/실행 확인 (class003)": "오리엔테이션 및 개발환경 준비",
    "Python 기초 시작: 변수와 출력 첫 실행 (class004)": "변수와 자료형",
    "Python 외부 라이브러리 활용": "모듈과 패키지",
}


def normalize_python_pl_module(module: str) -> str:
    core = module_core_name(module)
    return PYTHON_PL_MODULE_ALIASES.get(core, core)


def resolve_quiz_bank(subject_name: str, module: str, track: str) -> dict[str, str]:
    normalized_subject = subject_name.strip()
    module_core = module_core_name(module)

    if normalized_subject == "음성 데이터 활용한 TTS와 STT 모델 개발":
        module_bank = SPEECH_TTS_STT_QUIZ_BANK.get(module_core)
        if module_bank:
            return module_bank
    if normalized_subject == "자연어 및 음성 데이터 활용 및 모델 개발":
        module_bank = NLP_SPEECH_QUIZ_BANK.get(module_core)
        if module_bank:
            return module_bank
    if normalized_subject == "Python 전처리 및 시각화":
        module_bank = DATA_VIZ_QUIZ_BANK.get(module_core)
        if module_bank:
            return module_bank
    if normalized_subject == "머신러닝과 딥러닝":
        module_bank = ML_DEEP_QUIZ_BANK.get(module_core)
        if module_bank:
            return module_bank
    if normalized_subject == "Python 프로그래밍":
        module_bank = PYTHON_PL_QUIZ_BANK.get(normalize_python_pl_module(module))
        if module_bank:
            return module_bank
    return TRACK_QUIZ_BANK[track]


class LearningPoints(TypedDict):
    summary: str
    concepts: list[str]
    missions: list[str]
    checklist: list[str]


class ExampleSnippet(TypedDict):
    file: str
    code: str


class ExampleFileInsights(TypedDict):
    template: str
    imports: list[str]
    functions: list[str]
    entrypoint: str


class ExampleInsights(TypedDict):
    primary_file: str
    files: list[str]
    highest_variant: int
    template: str
    templates: list[str]
    imports: list[str]
    functions: list[str]
    entrypoint: str
    by_file: dict[str, ExampleFileInsights]
    snippets: list[ExampleSnippet]


class QuizContext(TypedDict):
    banks_by_class: dict[str, dict[str, str]]
    all_concepts: list[str]
    all_actions: list[str]
    all_pitfalls: list[str]
    all_checks: list[str]
    example_by_class: dict[str, ExampleInsights]
    all_primary_files: list[str]
    all_templates: list[str]
    all_imports: list[str]
    all_functions: list[str]
    all_entrypoints: list[str]


def parse_example_variant(class_id: str, file_name: str) -> int | None:
    pattern = re.compile(rf"^{re.escape(class_id)}_example(\d+)\.py$", re.IGNORECASE)
    match = pattern.match(file_name)
    if not match:
        return None
    return int(match.group(1))


def list_example_files(class_dir: Path, class_id: str) -> list[tuple[int, Path]]:
    variants: dict[int, Path] = {}
    for path in class_dir.glob(f"{class_id}_example*.py"):
        variant = parse_example_variant(class_id, path.name)
        if variant is None:
            continue
        variants[variant] = path

    legacy = class_dir / f"{class_id}_example.py"
    if legacy.exists() and 1 not in variants:
        variants[1] = legacy

    return sorted(variants.items(), key=lambda item: item[0])


def build_code_preview(text: str, max_lines: int = 18, max_chars: int = 1200) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    preview = "\n".join(lines[:max_lines]).strip()
    if len(preview) > max_chars:
        preview = preview[:max_chars].rstrip() + "\n..."
    if not preview:
        return "# 코드가 비어 있습니다."
    return preview


def parse_template_from_code(code: str) -> str:
    match = re.search(r'^EXAMPLE_TEMPLATE\s*=\s*"([^"]+)"', code, re.MULTILINE)
    return match.group(1).strip() if match else "generic"


def parse_imports_from_code(code: str) -> list[str]:
    import_candidates: list[str] = []
    for raw in code.splitlines():
        line = raw.strip()
        if line.startswith("import "):
            modules = line[len("import ") :].split(",")
            for module in modules:
                token = module.strip().split(" as ", maxsplit=1)[0].strip()
                token = token.split(".", maxsplit=1)[0].strip()
                if token and token not in import_candidates:
                    import_candidates.append(token)
        elif line.startswith("from "):
            token = line[len("from ") :].split(" import ", maxsplit=1)[0].strip()
            token = token.split(".", maxsplit=1)[0].strip()
            if token and token not in import_candidates:
                import_candidates.append(token)
    return import_candidates


def parse_functions_from_code(code: str) -> list[str]:
    functions = [
        fn
        for fn in re.findall(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code, flags=re.MULTILINE)
        if fn not in {"__init__"}
    ]
    return list(dict.fromkeys(functions))


def detect_entrypoint(functions: list[str]) -> str:
    if "main" in functions:
        return "main()"
    if functions:
        return f"{functions[0]}()"
    return 'if __name__ == "__main__":'


@lru_cache(maxsize=None)
def load_example_insights(class_dir_str: str, class_id: str) -> ExampleInsights:
    class_dir = Path(class_dir_str)
    variant_paths = list_example_files(class_dir, class_id)
    files = [path.name for _, path in variant_paths]
    highest_variant = max((variant for variant, _ in variant_paths), default=1)

    import_candidates: list[str] = []
    all_functions: list[str] = []
    all_templates: list[str] = []
    by_file: dict[str, ExampleFileInsights] = {}

    snippets: list[ExampleSnippet] = []
    for _, path in variant_paths:
        try:
            code = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        template = parse_template_from_code(code)
        imports = parse_imports_from_code(code)
        functions = parse_functions_from_code(code)
        entrypoint = detect_entrypoint(functions)

        by_file[path.name] = {
            "template": template,
            "imports": imports,
            "functions": functions,
            "entrypoint": entrypoint,
        }

        if template not in all_templates:
            all_templates.append(template)
        for token in imports:
            if token not in import_candidates:
                import_candidates.append(token)
        for fn in functions:
            if fn not in all_functions:
                all_functions.append(fn)
        if len(snippets) < 5:
            snippets.append({"file": path.name, "code": build_code_preview(code)})

    if not files:
        files = [f"{class_id}_example1.py"]

    primary_file = files[0]
    primary_meta = by_file.get(
        primary_file,
        {
            "template": "generic",
            "imports": [],
            "functions": [],
            "entrypoint": 'if __name__ == "__main__":',
        },
    )
    if primary_meta["template"] not in all_templates:
        all_templates.insert(0, primary_meta["template"])

    return {
        "primary_file": primary_file,
        "files": files,
        "highest_variant": max(1, highest_variant),
        "template": primary_meta["template"],
        "templates": all_templates,
        "imports": import_candidates,
        "functions": all_functions,
        "entrypoint": primary_meta["entrypoint"],
        "by_file": by_file,
        "snippets": snippets,
    }


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))

    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return rows


def class_dir_from_row(row: dict[str, str]) -> Path:
    md_rel = (row.get("md_file") or "").strip()
    if md_rel:
        md_path = ROOT / Path(md_rel)
        if md_path.name:
            return md_path.parent
    return ROOT / row["class"]


def subject_root_from_row(row: dict[str, str]) -> str:
    md_rel = (row.get("md_file") or "").strip()
    if md_rel:
        parts = Path(md_rel).parts
        if parts:
            return parts[0]
    class_dir = class_dir_from_row(row)
    try:
        rel = class_dir.resolve().relative_to(ROOT.resolve())
        return rel.parts[0] if rel.parts else ""
    except Exception:
        return class_dir.name


def filter_rows_by_subject_roots(rows: list[dict[str, str]], roots: set[str]) -> list[dict[str, str]]:
    if not roots:
        return rows
    return [row for row in rows if subject_root_from_row(row) in roots]


def choose_track(subject_name: str, module: str) -> str:
    text = f"{subject_name} {module}"
    lowered = text.lower()
    if "mlops" in lowered or "모델 레지스트리" in text or "배포 자동화" in text:
        return "ml"
    if "aiops" in lowered or "관측 데이터" in text or "이상탐지" in text or "runbook" in lowered:
        return "data"
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


def parse_session_order(subject_session: str) -> int:
    raw = subject_session.split("/", maxsplit=1)[0].strip()
    if raw.isdigit():
        return int(raw)
    return 0


def clean_learning_line(line: str) -> str:
    cleaned = line.strip()
    cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
    cleaned = re.sub(r"^- \[[ xX]\]\s*", "", cleaned)
    cleaned = re.sub(r"^-\s*", "", cleaned)
    return cleaned.strip()


@lru_cache(maxsize=None)
def load_learning_points(md_rel_path: str) -> LearningPoints:
    empty: LearningPoints = {
        "summary": "",
        "concepts": [],
        "missions": [],
        "checklist": [],
    }
    if not md_rel_path:
        return empty

    md_path = ROOT / md_rel_path
    if not md_path.exists():
        return empty

    summary = ""
    concepts: list[str] = []
    missions: list[str] = []
    checklist: list[str] = []
    section = ""

    with md_path.open(encoding="utf-8") as fp:
        for raw in fp:
            line = raw.strip()
            if not line:
                continue

            if line.startswith("- 한 줄 설명:"):
                summary = line.split(":", maxsplit=1)[1].strip()
                continue

            if line.startswith("### 핵심 개념 3가지"):
                section = "concepts"
                continue
            if line.startswith("### 실습 미션"):
                section = "missions"
                continue
            if line.startswith("## 8) 스스로 점검 체크리스트"):
                section = "checklist"
                continue
            if line.startswith("## "):
                section = ""
                continue

            if section in {"concepts", "missions"} and re.match(r"^\d+\.\s+", line):
                normalized = clean_learning_line(line)
                if normalized:
                    if section == "concepts":
                        concepts.append(normalized)
                    else:
                        missions.append(normalized)
                continue

            if section == "checklist" and line.startswith("- [ ]"):
                normalized = clean_learning_line(line)
                if normalized:
                    checklist.append(normalized)

    return {
        "summary": summary,
        "concepts": concepts,
        "missions": missions,
        "checklist": checklist,
    }


def merge_candidates(*pools: list[str]) -> list[str]:
    merged: list[str] = []
    for pool in pools:
        for item in pool:
            text = item.strip()
            if text and text not in merged:
                merged.append(text)
    return merged


def ensure_min_candidates(primary: list[str], fallback: list[str], minimum: int = 4) -> list[str]:
    candidates = merge_candidates(primary)
    if len(candidates) >= minimum:
        return candidates

    for item in fallback:
        text = item.strip()
        if text and text not in candidates:
            candidates.append(text)
            if len(candidates) >= minimum:
                break
    return candidates


def class_focus_point(row: dict[str, str]) -> str:
    points = load_learning_points(row.get("md_file", ""))
    module = row["module"]
    for text in points["missions"] + points["concepts"]:
        if text:
            return f"{module} 실습: {text}"
    if points["summary"]:
        return f"{module} 핵심: {points['summary']}"
    return f"{module} 학습 절차를 순서대로 설명할 수 있다."


def class_check_point(row: dict[str, str]) -> str:
    points = load_learning_points(row.get("md_file", ""))
    module = row["module"]
    for text in points["checklist"]:
        if text:
            return f"{module} 점검: {text}"

    track = choose_track(row["subject_name"], row["module"])
    bank = resolve_quiz_bank(subject_name=row["subject_name"], module=row["module"], track=track)
    return f"{module} 점검: {bank['check']}"


def find_prev_next_modules(current: dict[str, str], same_subject_rows: list[dict[str, str]]) -> tuple[str | None, str | None]:
    ordered = sorted(
        same_subject_rows,
        key=lambda item: (parse_session_order(item["subject_session"]), item["class"]),
    )

    current_index = next((i for i, item in enumerate(ordered) if item["class"] == current["class"]), -1)
    if current_index < 0:
        return None, None

    prev_module: str | None = None
    for i in range(current_index - 1, -1, -1):
        candidate = ordered[i]["module"]
        if candidate != current["module"]:
            prev_module = candidate
            break

    next_module: str | None = None
    for i in range(current_index + 1, len(ordered)):
        candidate = ordered[i]["module"]
        if candidate != current["module"]:
            next_module = candidate
            break

    return prev_module, next_module


def stable_sample(pool: list[str], k: int, seed: str) -> list[str]:
    unique = list(dict.fromkeys(pool))
    if len(unique) < k:
        return unique
    rng = random.Random(seed)
    return rng.sample(unique, k)


def build_quiz_context(rows: list[dict[str, str]]) -> QuizContext:
    banks_by_class: dict[str, dict[str, str]] = {}
    all_concepts: list[str] = []
    all_actions: list[str] = []
    all_pitfalls: list[str] = []
    all_checks: list[str] = []

    example_by_class: dict[str, ExampleInsights] = {}
    all_primary_files: list[str] = []
    all_templates: list[str] = []
    all_imports: list[str] = []
    all_functions: list[str] = []
    all_entrypoints: list[str] = []

    for row in rows:
        class_id = row["class"]
        track = choose_track(row["subject_name"], row["module"])
        bank = resolve_quiz_bank(subject_name=row["subject_name"], module=row["module"], track=track)
        banks_by_class[class_id] = bank

        for value, pool in (
            (bank["concept"], all_concepts),
            (bank["action"], all_actions),
            (bank["pitfall"], all_pitfalls),
            (bank["check"], all_checks),
        ):
            if value not in pool:
                pool.append(value)

        class_dir = class_dir_from_row(row)
        insights = load_example_insights(str(class_dir), class_id)
        example_by_class[class_id] = insights

        if insights["primary_file"] not in all_primary_files:
            all_primary_files.append(insights["primary_file"])
        for template in insights["templates"]:
            if template not in all_templates:
                all_templates.append(template)

        for token in insights["imports"]:
            if token not in all_imports:
                all_imports.append(token)
        for fn in insights["functions"]:
            if fn not in all_functions:
                all_functions.append(fn)
        for meta in insights["by_file"].values():
            entrypoint = meta["entrypoint"]
            if entrypoint not in all_entrypoints:
                all_entrypoints.append(entrypoint)
        if insights["entrypoint"] not in all_entrypoints:
            all_entrypoints.append(insights["entrypoint"])

    return {
        "banks_by_class": banks_by_class,
        "all_concepts": all_concepts,
        "all_actions": all_actions,
        "all_pitfalls": all_pitfalls,
        "all_checks": all_checks,
        "example_by_class": example_by_class,
        "all_primary_files": all_primary_files,
        "all_templates": all_templates,
        "all_imports": all_imports,
        "all_functions": all_functions,
        "all_entrypoints": all_entrypoints,
    }


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


def build_quiz_payload(row: dict[str, str], rows: list[dict[str, str]], context: QuizContext) -> dict:
    class_id = row["class"]
    subject_name = row["subject_name"]
    module = row["module"]
    level = row["level"]
    day = int(row["day"])
    slot = int(row["slot"])
    session = row["subject_session"]
    track = choose_track(subject_name, module)
    bank = context["banks_by_class"].get(class_id) or resolve_quiz_bank(
        subject_name=subject_name,
        module=module,
        track=track,
    )
    example = context["example_by_class"].get(class_id) or load_example_insights(str(class_dir_from_row(row)), class_id)

    same_subject_rows = [r for r in rows if r["subject_name"] == subject_name]
    same_subject_modules = [r["module"] for r in same_subject_rows]
    prev_module, next_module = find_prev_next_modules(row, same_subject_rows)

    all_concepts = context["all_concepts"]
    all_actions = context["all_actions"]
    all_pitfalls = context["all_pitfalls"]
    all_checks = context["all_checks"]

    subject_focus_points = [class_focus_point(r) for r in same_subject_rows]
    all_focus_points = [class_focus_point(r) for r in rows]
    focus_point = class_focus_point(row)
    focus_candidates = ensure_min_candidates(
        subject_focus_points,
        merge_candidates(all_focus_points, all_concepts),
        minimum=6,
    )

    subject_check_points = [class_check_point(r) for r in same_subject_rows]
    all_check_points = [class_check_point(r) for r in rows]
    check_point = class_check_point(row)
    check_candidates = ensure_min_candidates(
        subject_check_points,
        merge_candidates(all_check_points, all_checks),
        minimum=6,
    )
    module_candidates = ensure_min_candidates(same_subject_modules, [r["module"] for r in rows], minimum=6)
    file_candidates = ensure_min_candidates(
        context["all_primary_files"],
        [f"{r['class']}_example1.py" for r in rows],
        minimum=6,
    )
    template_candidates = ensure_min_candidates(
        context["all_templates"],
        ["python", "data", "ml", "nlp", "speech", "prompt", "langchain", "rag", "generic"],
        minimum=6,
    )
    function_candidates = ensure_min_candidates(
        context["all_functions"],
        ["main", "build_prompt", "retrieve", "solve_in_steps", "predict_batch", "summarize_utterances"],
        minimum=6,
    )
    import_candidates = ensure_min_candidates(
        context["all_imports"],
        ["pathlib", "json", "math", "datetime", "re", "(import 없음)"],
        minimum=6,
    )
    entrypoint_candidates = ensure_min_candidates(
        context["all_entrypoints"],
        ["main()", "run()", "invoke()", 'if __name__ == "__main__":', "process()"],
        minimum=6,
    )

    files_for_reference = example["files"] if example["files"] else [example["primary_file"]]
    by_file = example["by_file"]

    def pick_ref_file(index: int) -> str:
        if not files_for_reference:
            return example["primary_file"]
        if index < len(files_for_reference):
            return files_for_reference[index]
        return files_for_reference[-1]

    def file_meta(file_name: str) -> ExampleFileInsights:
        meta = by_file.get(file_name)
        if meta:
            return meta
        return {
            "template": example["template"],
            "imports": example["imports"],
            "functions": example["functions"],
            "entrypoint": example["entrypoint"],
        }

    template_file = pick_ref_file(1 if len(files_for_reference) > 1 else 0)
    function_file = pick_ref_file(2 if len(files_for_reference) > 2 else len(files_for_reference) - 1)
    import_file = pick_ref_file(3 if len(files_for_reference) > 3 else len(files_for_reference) - 1)
    entrypoint_file = pick_ref_file(4 if len(files_for_reference) > 4 else len(files_for_reference) - 1)

    template_meta = file_meta(template_file)
    function_meta = file_meta(function_file)
    import_meta = file_meta(import_file)
    entrypoint_meta = file_meta(entrypoint_file)

    correct_template = template_meta["template"]

    if not function_meta["functions"]:
        correct_function = "main"
    else:
        non_main = [fn for fn in function_meta["functions"] if fn != "main"]
        correct_function = non_main[0] if non_main else function_meta["functions"][0]

    if not import_meta["imports"]:
        correct_import = "(import 없음)"
    else:
        correct_import = import_meta["imports"][0]

    correct_entrypoint = entrypoint_meta["entrypoint"]

    highest_variant = max(1, min(5, int(example["highest_variant"])))
    if highest_variant == 1:
        variant_label = "example1만 제공 (총 1개)"
    else:
        variant_label = f"example1~example{highest_variant} (총 {highest_variant}개)"

    questions = [
        build_question(
            question=f"{class_id} ({subject_name} {session}) 차시의 실제 학습 주제는 무엇인가요?",
            correct=module,
            candidates=module_candidates,
            seed=f"{class_id}-q1-module",
            explanation=f"정답은 '{module}' 입니다. 이전 모듈은 '{prev_module or '없음'}', 다음 모듈은 '{next_module or '없음'}' 입니다.",
        ),
        build_question(
            question=f"'{module}' 차시의 실제 실습 목표를 가장 구체적으로 설명한 문장은 무엇인가요?",
            correct=focus_point,
            candidates=focus_candidates,
            seed=f"{class_id}-q2-focus",
            explanation="정답은 해당 차시 MD의 핵심 개념/실습 미션에서 직접 가져온 문장입니다.",
        ),
        build_question(
            question=f"'{module}' 실습에서 오류를 줄이는 시작 전략으로 가장 적절한 것은 무엇인가요?",
            correct=bank["action"],
            candidates=all_actions,
            seed=f"{class_id}-q3-action",
            explanation="정답은 실행 흐름을 먼저 검증하는 고효율 시작 루틴입니다.",
        ),
        build_question(
            question=f"'{module}' 실습 결과를 왜곡할 가능성이 가장 큰 실수는 무엇인가요?",
            correct=bank["pitfall"],
            candidates=all_pitfalls,
            seed=f"{class_id}-q4-pitfall",
            explanation="정답은 현장에서 자주 발생하는 품질 저하 패턴입니다.",
        ),
        build_question(
            question=f"'{module}'를 끝낸 직후, 다음 학습 단계로 넘어가기 전 자기 점검 항목으로 가장 적절한 것은 무엇인가요?",
            correct=check_point,
            candidates=check_candidates,
            seed=f"{class_id}-q5-check",
            explanation=f"이 차시는 '{bank['check']}' 관점으로 검증해야 다음 단계로 안정적으로 연결됩니다.",
        ),
        build_question(
            question=f"'{module}' 기본 실습에서 첫 실행 대상으로 맞는 파일명은 무엇인가요?",
            correct=example["primary_file"],
            candidates=file_candidates,
            seed=f"{class_id}-q6-file",
            explanation=f"기본 예제 파일은 {example['primary_file']} 입니다.",
        ),
        build_question(
            question=f"'{template_file}'에 선언된 EXAMPLE_TEMPLATE 값으로 맞는 것은 무엇인가요?",
            correct=correct_template,
            candidates=template_candidates,
            seed=f"{class_id}-q7-template",
            explanation=f"{template_file}의 EXAMPLE_TEMPLATE 값은 '{correct_template}' 입니다.",
        ),
        build_question(
            question=f"'{function_file}' 코드에 실제 정의된 함수 이름으로 맞는 것은 무엇인가요?",
            correct=correct_function,
            candidates=function_candidates,
            seed=f"{class_id}-q8-function",
            explanation=f"{function_file} 함수 목록: {', '.join(function_meta['functions'][:8]) if function_meta['functions'] else '확인 필요'}",
        ),
        build_question(
            question=f"'{import_file}'에서 import 또는 from으로 사용되는 모듈은 무엇인가요?",
            correct=correct_import,
            candidates=import_candidates,
            seed=f"{class_id}-q9-import",
            explanation=f"{import_file} import 목록: {', '.join(import_meta['imports']) if import_meta['imports'] else '(import 없음)'}",
        ),
        build_question(
            question=f"'{entrypoint_file}' 파일의 실행 진입점(entrypoint)으로 맞는 것은 무엇인가요?",
            correct=correct_entrypoint,
            candidates=entrypoint_candidates,
            seed=f"{class_id}-q10-entrypoint",
            explanation=f"{entrypoint_file} 엔트리는 '{correct_entrypoint}' 입니다. 현재 example 구성: {variant_label} ({', '.join(example['files'])})",
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
        "question_count": len(questions),
        "day": day,
        "slot": slot,
        "example_reference": {
            "files": example["files"],
            "template": example["template"],
            "templates": example["templates"],
            "imports": example["imports"],
            "functions": example["functions"],
            "entrypoint": example["entrypoint"],
            "by_file": example["by_file"],
        },
        "example_snippets": example["snippets"],
    }


def build_quiz_html(row: dict[str, str], rows: list[dict[str, str]], context: QuizContext) -> str:
    payload = build_quiz_payload(row, rows, context)
    quiz_json = json.dumps(payload, ensure_ascii=False, indent=2)
    class_id = payload["class_id"]
    module = payload["module"]
    subject_name = payload["subject_name"]
    session = payload["session"]
    level = payload["level"]
    day = payload["day"]
    slot = payload["slot"]
    question_count = payload["question_count"]

    html = """<!doctype html>
<!-- __COPYRIGHT__ -->
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>__CLASS_ID__ __QUESTION_COUNT__문항 퀴즈</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" />
  <style>
    :root {
      --bg: #f3f6fb;
      --panel: #ffffff;
      --ink: #0f172a;
      --sub: #475569;
      --primary: #0b5fff;
      --primary-strong: #0038c7;
      --accent: #04b7a1;
      --line: #d9e3f3;
      --danger: #e44863;
      --shadow: 0 20px 45px rgba(15, 23, 42, 0.09);
    }

    * {
      box-sizing: border-box;
    }

    html, body {
      margin: 0;
      padding: 0;
      font-family: "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 15% -10%, rgba(11, 95, 255, 0.18), transparent 36%),
        radial-gradient(circle at 90% 0%, rgba(4, 183, 161, 0.15), transparent 35%),
        var(--bg);
    }

    body.scroll-lock {
      overflow: hidden;
    }

    .container {
      width: min(1100px, 100% - 32px);
      margin: 28px auto 56px;
    }

    .hero {
      background: linear-gradient(140deg, #ffffff, #f8fbff);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 24px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 12px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 12px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      background: rgba(11, 95, 255, 0.1);
      color: var(--primary-strong);
    }

    .hero h1 {
      margin: 14px 0 8px;
      font-size: clamp(24px, 3.4vw, 34px);
      line-height: 1.22;
    }

    .meta {
      margin: 0;
      color: var(--sub);
      font-size: 14px;
      line-height: 1.6;
    }

    .notice {
      margin-top: 16px;
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }

    .notice-card {
      border-radius: 14px;
      border: 1px solid var(--line);
      background: #fbfdff;
      padding: 12px;
      font-size: 13px;
      color: var(--sub);
    }

    .btn-row {
      margin-top: 18px;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .btn {
      border: 0;
      border-radius: 12px;
      padding: 11px 16px;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
    }

    .btn.primary {
      background: linear-gradient(120deg, var(--primary), var(--primary-strong));
      color: #fff;
    }

    .btn.secondary {
      background: #e6edf9;
      color: #0b326c;
    }

    .btn.ghost {
      background: #eff9f7;
      color: #06645c;
      border: 1px solid #bee9e3;
    }

    .quiz-grid {
      margin-top: 18px;
      display: grid;
      gap: 14px;
    }

    .question {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
      padding: 16px;
    }

    .question-title {
      margin: 0;
      font-weight: 700;
      line-height: 1.52;
      font-size: 15px;
    }

    .options {
      margin-top: 12px;
      display: grid;
      gap: 8px;
    }

    .option {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      border: 1px solid #d7e0ef;
      border-radius: 12px;
      padding: 10px 12px;
      cursor: pointer;
      background: #fff;
      font-size: 14px;
    }

    .option:hover {
      background: #f5f8fd;
    }

    .option input {
      margin-top: 3px;
      accent-color: var(--primary);
    }

    .modal {
      position: fixed;
      inset: 0;
      display: grid;
      place-items: center;
      z-index: 50;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.18s ease;
      padding: 16px;
    }

    .modal.show {
      opacity: 1;
      pointer-events: auto;
    }

    .modal.hidden {
      display: none;
    }

    .modal-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(15, 23, 42, 0.52);
      backdrop-filter: blur(2px);
    }

    .modal-dialog {
      position: relative;
      z-index: 1;
      width: min(920px, 100%);
      max-height: 82vh;
      overflow: auto;
      border-radius: 20px;
      background: #ffffff;
      border: 1px solid var(--line);
      box-shadow: 0 30px 50px rgba(15, 23, 42, 0.24);
      padding: 18px;
      transform: translateY(10px) scale(0.98);
      transition: transform 0.18s ease;
    }

    .modal.show .modal-dialog {
      transform: translateY(0) scale(1);
    }

    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }

    .modal-header h2 {
      margin: 0;
      font-size: 20px;
    }

    .close-btn {
      border: 0;
      border-radius: 10px;
      padding: 7px 12px;
      background: #eaf0fb;
      font-weight: 700;
      color: #29476f;
      cursor: pointer;
    }

    .result-summary {
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px;
      background: #f8fbff;
    }

    .result-title {
      margin: 0;
      font-size: 20px;
    }

    .progress {
      margin-top: 10px;
      height: 10px;
      background: #dbe6f7;
      border-radius: 999px;
      overflow: hidden;
    }

    .progress > div {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(120deg, var(--primary), var(--accent));
    }

    .result-list {
      margin: 14px 0 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 10px;
    }

    .result-item {
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px;
      background: #fff;
      font-size: 14px;
      line-height: 1.55;
    }

    .ok {
      color: #0a7f51;
      font-weight: 700;
    }

    .bad {
      color: var(--danger);
      font-weight: 700;
    }

    .code-meta {
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #f8fbff;
      padding: 12px;
      font-size: 13px;
      color: var(--sub);
      line-height: 1.6;
    }

    .code-grid {
      margin-top: 10px;
      display: grid;
      gap: 10px;
    }

    .code-card {
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      background: #ffffff;
    }

    .code-card header {
      padding: 10px 12px;
      font-weight: 700;
      border-bottom: 1px solid var(--line);
      background: #f7faff;
      font-size: 13px;
    }

    .code-card pre {
      margin: 0;
      padding: 12px;
      overflow: auto;
      font-size: 12px;
      line-height: 1.5;
      background: #0f172a;
      color: #d7e7ff;
    }

    @media (max-width: 740px) {
      .container {
        width: min(1100px, 100% - 20px);
        margin-top: 16px;
      }
      .hero {
        padding: 18px;
      }
      .btn {
        width: 100%;
      }
      .btn-row {
        display: grid;
      }
      .modal-dialog {
        padding: 14px;
      }
    }
  </style>
</head>
<body>
  <main class="container">
    <section class="hero">
      <span class="badge">__CLASS_ID__ SELF QUIZ</span>
      <h1>__MODULE__</h1>
      <p class="meta">교과목: __SUBJECT_NAME__ · 세부 시퀀스: __SESSION__ · 난이도: __LEVEL__ · Day __DAY__ / __SLOT__교시</p>
      <div class="notice">
        <article class="notice-card">학습 내용 + example1~example5 코드 내용을 함께 반영한 __QUESTION_COUNT__문항 퀴즈입니다.</article>
        <article class="notice-card">채점 결과는 모달 팝업으로 제공되며, example 코드 스니펫도 모달에서 바로 확인할 수 있습니다.</article>
      </div>
      <div class="btn-row">
        <button id="grade-btn" class="btn primary" type="button">채점하기</button>
        <button id="reset-btn" class="btn secondary" type="button">다시 풀기</button>
        <button id="open-code-btn" class="btn ghost" type="button">example 코드 보기</button>
      </div>
    </section>

    <section id="quiz-root" class="quiz-grid"></section>
  </main>

  <div id="result-modal" class="modal hidden" aria-hidden="true">
    <div class="modal-backdrop" data-close-modal="result-modal"></div>
    <section class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="result-title">
      <header class="modal-header">
        <h2 id="result-title">채점 결과</h2>
        <button class="close-btn" type="button" data-close-modal="result-modal">닫기</button>
      </header>
      <section id="result-root"></section>
    </section>
  </div>

  <div id="code-modal" class="modal hidden" aria-hidden="true">
    <div class="modal-backdrop" data-close-modal="code-modal"></div>
    <section class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="code-title">
      <header class="modal-header">
        <h2 id="code-title">example 코드 참고</h2>
        <button class="close-btn" type="button" data-close-modal="code-modal">닫기</button>
      </header>
      <section id="code-meta" class="code-meta"></section>
      <section id="code-snippet-list" class="code-grid"></section>
    </section>
  </div>

  <script>
    const QUIZ_DATA = __QUIZ_JSON__;

    function escapeHtml(value) {
      return String(value || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function openModal(modalId) {
      const modal = document.getElementById(modalId);
      if (!modal) return;
      modal.classList.remove("hidden");
      modal.setAttribute("aria-hidden", "false");
      requestAnimationFrame(() => modal.classList.add("show"));
      document.body.classList.add("scroll-lock");
    }

    function closeModal(modalId) {
      const modal = document.getElementById(modalId);
      if (!modal) return;
      modal.classList.remove("show");
      modal.setAttribute("aria-hidden", "true");
      window.setTimeout(() => {
        modal.classList.add("hidden");
        if (!document.querySelector(".modal.show")) {
          document.body.classList.remove("scroll-lock");
        }
      }, 180);
    }

    function renderQuiz() {
      const root = document.getElementById("quiz-root");
      root.innerHTML = "";

      QUIZ_DATA.questions.forEach((q, qIndex) => {
        const wrap = document.createElement("article");
        wrap.className = "question";

        const title = document.createElement("h2");
        title.className = "question-title";
        title.textContent = `${qIndex + 1}번. ${q.question}`;
        wrap.appendChild(title);

        const list = document.createElement("div");
        list.className = "options";

        q.options.forEach((opt, optIndex) => {
          const label = document.createElement("label");
          label.className = "option";

          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = `q-${qIndex}`;
          radio.value = String(optIndex);

          const text = document.createElement("span");
          text.textContent = `${optIndex + 1}) ${opt}`;

          label.appendChild(radio);
          label.appendChild(text);
          list.appendChild(label);
        });

        wrap.appendChild(list);
        root.appendChild(wrap);
      });
    }

    function renderCodeModal() {
      const ref = QUIZ_DATA.example_reference || {};
      const files = Array.isArray(ref.files) ? ref.files : [];
      const templates = Array.isArray(ref.templates) ? ref.templates : [];
      const imports = Array.isArray(ref.imports) ? ref.imports : [];
      const functions = Array.isArray(ref.functions) ? ref.functions : [];
      const byFile = ref.by_file && typeof ref.by_file === "object" ? ref.by_file : {};
      const snippets = Array.isArray(QUIZ_DATA.example_snippets) ? QUIZ_DATA.example_snippets : [];

      const fileMeta = files.map((file) => {
        const meta = byFile[file] || {};
        const template = meta.template || ref.template || "generic";
        const imp = Array.isArray(meta.imports) ? meta.imports.join(", ") : "(import 없음)";
        const fn = Array.isArray(meta.functions) ? meta.functions.join(", ") : "정보 없음";
        const ep = meta.entrypoint || ref.entrypoint || "main()";
        return `<div><b>${escapeHtml(file)}</b> · template=${escapeHtml(template)} · entry=${escapeHtml(ep)} · imports=${escapeHtml(imp || "(import 없음)")} · functions=${escapeHtml(fn || "정보 없음")}</div>`;
      }).join("");

      const meta = `
        <div><b>파일:</b> ${escapeHtml(files.join(", ") || "정보 없음")}</div>
        <div><b>템플릿(전체):</b> ${escapeHtml(templates.join(", ") || ref.template || "generic")}</div>
        <div><b>엔트리:</b> ${escapeHtml(ref.entrypoint || "main()")}</div>
        <div><b>imports:</b> ${escapeHtml(imports.join(", ") || "(import 없음)")}</div>
        <div><b>functions:</b> ${escapeHtml(functions.join(", ") || "정보 없음")}</div>
        <div><b>파일별 메타:</b></div>
        <div>${fileMeta || "정보 없음"}</div>
      `;
      document.getElementById("code-meta").innerHTML = meta;

      const list = document.getElementById("code-snippet-list");
      if (!snippets.length) {
        list.innerHTML = `
          <article class="code-card">
            <header>example 코드 미리보기</header>
            <pre>표시할 코드 스니펫이 없습니다.</pre>
          </article>
        `;
        return;
      }

      list.innerHTML = snippets.map((item) => `
        <article class="code-card">
          <header>${escapeHtml(item.file || "example1.py")}</header>
          <pre>${escapeHtml(item.code || "")}</pre>
        </article>
      `).join("");
    }

    function gradeQuiz() {
      let score = 0;
      const details = [];
      const total = QUIZ_DATA.questions.length;

      QUIZ_DATA.questions.forEach((q, qIndex) => {
        const selected = document.querySelector(`input[name="q-${qIndex}"]:checked`);
        const selectedIndex = selected ? Number(selected.value) : -1;
        const isCorrect = selectedIndex === q.answer_index;
        if (isCorrect) score += 1;

        details.push({
          number: qIndex + 1,
          isCorrect,
          correct: q.options[q.answer_index],
          chosen: selectedIndex >= 0 ? q.options[selectedIndex] : "미선택",
          explanation: q.explanation
        });
      });

      const resultRoot = document.getElementById("result-root");
      const ratio = Math.round((score / total) * 100);
      const statusClass = score === total ? "ok" : "bad";
      const summary = `
        <article class="result-summary">
          <h3 class="result-title ${statusClass}">점수: ${score} / ${total} (${ratio}%)</h3>
          <p>학습 성과 힌트: ${escapeHtml(QUIZ_DATA.track_outcome || "")}</p>
          <div class="progress"><div style="width:${ratio}%"></div></div>
        </article>
      `;

      const rows = details.map((d) => `
        <li class="result-item">
          <div><b>${d.number}번</b> · <span class="${d.isCorrect ? "ok" : "bad"}">${d.isCorrect ? "정답" : "오답"}</span></div>
          <div>내 답: ${escapeHtml(d.chosen)}</div>
          <div>정답: ${escapeHtml(d.correct)}</div>
          <div>해설: ${escapeHtml(d.explanation)}</div>
        </li>
      `).join("");

      resultRoot.innerHTML = `
        ${summary}
        <ul class="result-list">${rows}</ul>
      `;
      openModal("result-modal");
    }

    function resetQuiz() {
      document.querySelectorAll('input[type="radio"]').forEach((el) => {
        el.checked = false;
      });
      document.getElementById("result-root").innerHTML = "";
      closeModal("result-modal");
    }

    function bindModalCloseButtons() {
      document.querySelectorAll("[data-close-modal]").forEach((el) => {
        el.addEventListener("click", () => closeModal(el.dataset.closeModal));
      });
      document.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;
        closeModal("result-modal");
        closeModal("code-modal");
      });
    }

    document.getElementById("grade-btn").addEventListener("click", () => gradeQuiz());
    document.getElementById("reset-btn").addEventListener("click", () => resetQuiz());
    document.getElementById("open-code-btn").addEventListener("click", () => openModal("code-modal"));
    bindModalCloseButtons();
    renderQuiz();
    renderCodeModal();
  </script>
</body>
</html>
"""
    return (
        dedent(html)
        .replace("__COPYRIGHT__", COPYRIGHT_TEXT)
        .replace("__CLASS_ID__", class_id)
        .replace("__MODULE__", module)
        .replace("__SUBJECT_NAME__", subject_name)
        .replace("__SESSION__", session)
        .replace("__LEVEL__", level)
        .replace("__DAY__", f"{day:02d}")
        .replace("__SLOT__", str(slot))
        .replace("__QUESTION_COUNT__", str(question_count))
        .replace("__QUIZ_JSON__", quiz_json)
    )


def build_launcher_py(class_id: str) -> str:
    return dedent(
        f'''\
        # {COPYRIGHT_TEXT}
        """
        {class_id} launcher
        - 기본 실행: {class_id}_example1.py
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
                "example": f"{{CLASS_ID}}_example1.py",
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


def rebuild_launchers_and_quizzes(roots: set[str] | None = None) -> None:
    roots = roots or set()
    rows = filter_rows_by_subject_roots(read_rows(), roots)
    if not rows:
        print("Updated launchers: 0")
        print("Created quiz html files: 0")
        return
    context = build_quiz_context(rows)
    launcher_count = 0
    quiz_count = 0

    for row in rows:
        class_id = row["class"]
        class_dir = class_dir_from_row(row)
        class_dir.mkdir(parents=True, exist_ok=True)

        launcher_path = class_dir / f"{class_id}.py"
        launcher_path.write_text(build_launcher_py(class_id), encoding="utf-8", newline="\n")
        launcher_count += 1

        quiz_path = class_dir / f"{class_id}_quiz.html"
        quiz_path.write_text(build_quiz_html(row, rows, context), encoding="utf-8", newline="\n")
        quiz_count += 1

    print(f"Updated launchers: {launcher_count}")
    print(f"Created quiz html files: {quiz_count}")
    if roots:
        print(f"Subject roots: {', '.join(sorted(roots))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild class launchers and quiz HTML files.")
    parser.add_argument(
        "--subject-root",
        action="append",
        default=[],
        help="Rebuild only rows under this root folder (e.g. dataVizPrep). Can be repeated.",
    )
    args = parser.parse_args()
    roots = {item.strip() for item in args.subject_root if item.strip()}
    rebuild_launchers_and_quizzes(roots=roots)
