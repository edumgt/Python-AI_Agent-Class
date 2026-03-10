<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class476 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **RAG(Retrieval-Augmented Generation)**
- 학습 주제: **검색 품질 개선 · 단계 2/6 기초 구현 [class476]**
- 세부 시퀀스: **28/52**
- 일정: **Day 60 / 4교시**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `RAG(Retrieval-Augmented Generation)`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 검색 근거를 결합해 신뢰도 높은 답변을 만드는 RAG 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `RAG` | 약어명사 | RAG (한자 없음) | Retrieval-Augmented Generation | 검색 결과를 근거로 생성 품질과 신뢰도를 높이는 구조입니다. |
| `Retrieval-Augmented` | 복합 형용어 | Retrieval-Augmented (한자 없음) | retrieval-augmented | 검색 결과를 생성 과정에 보강한다는 RAG 핵심 속성입니다. |
| `Generation` | 명사(영어) | Generation (한자 없음) | generation | 모델이 새 출력 텍스트를 만들어내는 단계입니다. |

#### 학습주제 표현 분석: `검색 품질 개선 · 단계 2/6 기초 구현 [class476]`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `검색 품질 개선 · 단계 2/6 기초 구현 [class476]` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `검색` | 명사 | 검색 (搜索) | retrieval/search | 질문과 유사한 문서를 찾는 단계로 RAG 품질을 좌우합니다. |
| `품질` | 명사(기술 개념어) | 품질 (한자 없음) | (context-specific) | 용어 `품질`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `개선` | 명사(기술 개념어) | 개선 (한자 없음) | (context-specific) | 용어 `개선`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `단계` | 명사(기술 개념어) | 단계 (한자 없음) | (context-specific) | 용어 `단계`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `기초` | 명사(기술 개념어) | 기초 (한자 없음) | (context-specific) | 용어 `기초`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `구현` | 명사 | 구현 (具現) | implementation | 설계를 실제 코드와 시스템 동작으로 구체화하는 과정입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class475 / 검색 품질 개선 · 단계 1/6 입문 이해 [class475]** (Day 60 / 3교시)
- 복습 연결: 이전에 배운 **검색 품질 개선 · 단계 1/6 입문 이해 [class475]** 를 떠올리며, 오늘 **검색 품질 개선 · 단계 2/6 기초 구현 [class476]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 검색 실패 사례를 분석하고 query rewrite, threshold, hybrid 검색으로 성능을 개선하는 차시입니다.
- 왜 배우나요?: RAG 품질 저하는 대부분 검색 단계에서 시작되므로 검색 전략 개선이 가장 큰 효과를 냅니다.

### 핵심 개념 3가지
1. `검색 품질 개선`은 query rewrite, score threshold, reranking 조합으로 수행합니다.
2. `하이브리드 검색`은 키워드 검색과 벡터 검색을 결합해 재현율/정밀도를 균형 있게 맞춥니다.
3. `실패 사례 분석`은 질의 의도 불일치, 청크 품질 문제, 메타데이터 누락으로 분류합니다.

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
- 예제 파일: `class476_example1.py`
- 실행 명령:
```bash
python ragPipeline/class476/class476_example1.py
```

### example1~example5 단계별 테스트 확장
1. example1: 검색 실패 사례를 분류하고 baseline을 실행한다.
2. example2: score threshold/top_k 조정 효과를 비교한다.
3. example3: query rewrite와 reranking 적용을 점검한다.
4. example4: 하이브리드 검색 적용 전후를 비교한다.
5. example5: 검색 품질 개선 체크리스트를 완성한다.

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python ragPipeline/class476/class476_example1.py`)
- 주요 문법: `query rewrite`, `score threshold`, `hybrid search`, `failure log`
- 학습 포커스: `검색 품질 개선 · 단계 2/6 기초 구현 [class476]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class476 (28/52, 기초응용)"]
N2["학습 주제 파악: 검색 품질 개선 · 단계 2/6 기초 구현 [class476]"]
N3["1단계: 실패 질의를 수집해 유형을 분류한다"]
N4["2단계: 검색 전략(벡터/하이브리드)을 비교 실행한다"]
N5["3단계: reranking/threshold를 조정한다"]
N6["4단계: 개선 결과를 지표로 검증한다"]
N7["예제 실행: python ragPipeline/class476/class476_example1.py"]
N8["다음 준비: 검색 품질 개선 · 단계 3/6 응용 확장 [class477] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class476 flow](class476_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 개선 실험이 동일 데이터·동일 질문 조건인지 확인하기
2. 재현율과 정밀도 중 우선순위 기준을 점검하기
3. 실패 케이스가 운영 모니터링에 누적되는지 확인하기

## 6) 퀴즈로 복습하기 (10문항)
- 퀴즈 파일: `class476_quiz.html`
- 브라우저에서 열기:
```bash
ragPipeline/class476/class476_quiz.html
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
1. 검색 실패 케이스를 유형별로 분류해 원인을 기록하세요.
2. 벡터 검색과 하이브리드 검색 결과를 같은 질의에서 비교하세요.
3. score threshold와 reranking 규칙을 조정해 개선 폭을 측정하세요.

## 8) 스스로 점검 체크리스트
- [ ] 검색 실패 유형과 원인을 정리했다.
- [ ] 하이브리드 검색 적용 전/후 성능을 비교했다.
- [ ] 검색 개선 규칙을 운영 설정으로 문서화했다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class477 / 검색 품질 개선 · 단계 3/6 응용 확장 [class477]** (Day 60 / 5교시)
- 미리보기: 다음 차시 전에 **검색 품질 개선 · 단계 2/6 기초 구현 [class476]** 핵심 코드 1개를 다시 실행해 두면 검색 품질 개선 · 단계 3/6 응용 확장 [class477] 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 LangChain Retriever와 프롬프트 문맥 주입을 연결합니다.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
