<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class489 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **RAG(Retrieval-Augmented Generation)**
- 학습 주제: **응답 검증/출처화 · 단계 4/5 실전 검증 [class489]**
- 세부 시퀀스: **41/52**
- 일정: **Day 62 / 1교시**
- 난이도: **실전심화**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `RAG(Retrieval-Augmented Generation)`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 검색 근거를 결합해 신뢰도 높은 답변을 만드는 RAG 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `RAG` | 약어명사 | RAG (한자 없음) | Retrieval-Augmented Generation | 검색 결과를 근거로 생성 품질과 신뢰도를 높이는 구조입니다. |
| `Retrieval-Augmented` | 복합 형용어 | Retrieval-Augmented (한자 없음) | retrieval-augmented | 검색 결과를 생성 과정에 보강한다는 RAG 핵심 속성입니다. |
| `Generation` | 명사(영어) | Generation (한자 없음) | generation | 모델이 새 출력 텍스트를 만들어내는 단계입니다. |

#### 학습주제 표현 분석: `응답 검증/출처화 · 단계 4/5 실전 검증 [class489]`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `응답 검증/출처화` 핵심 개념을 코드 구현, 결과 해석, 점검 기준으로 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `응답` | 명사 | 응답 (應答) | response | 모델이 입력 프롬프트에 대해 반환하는 출력 텍스트입니다. |
| `검증` | 명사 | 검증 (檢證) | validation | 결과가 요구사항과 기준을 만족하는지 확인하는 절차입니다. |
| `출처화` | 명사 | 출처화 (한자 없음) | citation grounding | 답변 문장별 근거 문서를 연결해 신뢰성을 높이는 작업입니다. |
| `source` | 영문 기술명/약어 | source (한자 없음) | source | 이번 차시 맥락: 답변 정확성을 점검하고 source를 반환해 근거 추적 가능한 RAG 응답을 만드는 차시입니다. 이를 기준으로 `source`를 코드와 결과 해석에 연결합니다. |
| `반환` | 명사(주제 핵심 용어) | 반환 (한자 없음) | (topic-specific) | 이번 차시 맥락: 답변 정확성을 점검하고 source를 반환해 근거 추적 가능한 RAG 응답을 만드는 차시입니다. 이를 기준으로 `반환`를 코드와 결과 해석에 연결합니다. |
| `hallucination` | 영문 기술명/약어 | hallucination (한자 없음) | hallucination | 이번 차시 맥락: `hallucination 감소`는 근거 매칭 실패 문장을 표시하거나 제거하는 정책으로 구현합니다. 이를 기준으로 `hallucination`를 코드와 결과 해석에 연결합니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class488 / 응답 검증/출처화 · 단계 3/5 응용 확장 [class488]** (Day 61 / 8교시)
- 복습 연결: 이전에 배운 **응답 검증/출처화 · 단계 3/5 응용 확장 [class488]** 를 떠올리며, 오늘 **응답 검증/출처화 · 단계 4/5 실전 검증 [class489]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 답변 정확성을 점검하고 source를 반환해 근거 추적 가능한 RAG 응답을 만드는 차시입니다.
- 왜 배우나요?: 출처 없는 답변은 실무에서 신뢰할 수 없고, 검증 가능한 출력 포맷이 있어야 서비스로 운영할 수 있습니다.

### 핵심 개념 3가지
1. `source 반환`은 답변 문장과 문서/페이지/섹션을 연결해 검증 가능성을 만듭니다.
2. `응답 검증`은 검색 근거 포함 여부와 근거-답변 일치도를 확인하는 단계입니다.
3. `hallucination 감소`는 근거 매칭 실패 문장을 표시하거나 제거하는 정책으로 구현합니다.

### 비유로 이해하기
- 시험 문제를 풀 때 교과서 해당 페이지를 먼저 찾고 답을 쓰는 방식과 같아요.

## 4) 실습 환경 만들기 (항상 먼저)
아래 명령은 **처음 한 번** 준비해 두면 이후 학습이 쉬워집니다.

### Windows PowerShell
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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
- 예제 파일: `class489_example1.py`
- 실행 명령:
```bash
python ragPipeline/class489/class489_example1.py
```

### example1~example5 단계별 테스트 확장
1. example1: 답변과 source를 함께 반환하는 구조를 구현한다.
2. example2: 문장-근거 매핑 검증을 확장한다.
3. example3: 출처 누락/오표기 실패 케이스를 점검한다.
4. example4: hallucination 감소 규칙 전후를 비교한다.
5. example5: 출처화 품질 기준과 감사 로그 정책을 정리한다.

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python ragPipeline/class489/class489_example1.py`)
- 주요 문법: `answer schema`, `source map`, `grounding check`, `hallucination guard`
- 학습 포커스: `응답 검증/출처화 · 단계 4/5 실전 검증 [class489]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class489 (41/52, 실전심화)"]
N2["학습 주제 파악: 응답 검증/출처화 · 단계 4/5 실전 검증 [class489]"]
N3["1단계: 답변과 근거를 매핑한다"]
N4["2단계: 문장별 근거 일치 여부를 검증한다"]
N5["3단계: 근거 부족 문장을 표시/제거한다"]
N6["4단계: 출처 포함 최종 응답을 반환한다"]
N7["예제 실행: python ragPipeline/class489/class489_example1.py"]
N8["다음 준비: 응답 검증/출처화 · 단계 5/5 운영 최적화 [class490] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class489 flow](class489_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. source ID와 문서 메타데이터가 일관적인지 확인하기
2. 검증 실패 문장 처리 정책이 명확한지 점검하기
3. 사용자에게 근거를 읽기 쉬운 형태로 제공하는지 확인하기

## 6) 퀴즈로 복습하기 (10문항)
- 퀴즈 파일: `class489_quiz.html`
- 브라우저에서 열기:
```bash
ragPipeline/class489/class489_quiz.html
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
1. 답변과 source 목록을 함께 반환하는 출력 스키마를 구현하세요.
2. 근거 없는 문장을 표시하는 검증 함수를 추가하세요.
3. 출처 누락/오표기 실패 케이스를 재현해 복구 로직을 점검하세요.

## 8) 스스로 점검 체크리스트
- [ ] 답변에 source를 포함하는 구조를 구현했다.
- [ ] 근거 일치 검증 규칙을 적용했다.
- [ ] 출처화 실패 케이스 대응 방안을 정리했다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class490 / 응답 검증/출처화 · 단계 5/5 운영 최적화 [class490]** (Day 62 / 2교시)
- 미리보기: 다음 차시 전에 **응답 검증/출처화 · 단계 4/5 실전 검증 [class489]** 핵심 코드 1개를 다시 실행해 두면 응답 검증/출처화 · 단계 5/5 운영 최적화 [class490] 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 검색 정확도와 답변 정확도를 수치로 평가하고 개선합니다.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
