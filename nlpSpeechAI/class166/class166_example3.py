# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class166 example3: 언어모델 입력 구조 · 단계 6/8 실전 검증 [class166]"""

TOPIC = "언어모델 입력 구조 · 단계 6/8 실전 검증 [class166]"
EXAMPLE_TEMPLATE = "nlp"
EXAMPLE_VARIANT = 3

import math
import re

STOPWORDS = {"은", "는", "이", "가", "을", "를", "에", "의", "그리고", "또한", "but", "the", "a"}
POS_RULES = [
    ("하다", "VERB"),
    ("했다", "VERB"),
    ("합니다", "VERB"),
    ("적", "NOUN"),
    ("성", "NOUN"),
    ("다", "ENDING"),
]
POSITIVE_WORDS = {"좋다", "만족", "추천", "향상", "개선", "정확", "편리", "안정"}
NEGATIVE_WORDS = {"나쁘다", "불만", "오류", "지연", "실패", "불안정", "잡음", "누락"}

def resolve_mode():
    if "텍스트 정제와 토큰화" in TOPIC:
        return "preprocess"
    if any(k in TOPIC for k in ["임베딩", "텍스트 분류", "시퀀스 모델", "언어모델 입력 구조"]):
        return "model"
    if any(k in TOPIC for k in ["멀티모달", "실전 데이터셋 설계"]):
        return "practice"
    if any(k in TOPIC for k in ["개요", "데이터 수집"]):
        return "understanding"
    return "nlp_general"

def normalize_text(text):
    text = re.sub(r"\s+", " ", str(text)).strip().lower()
    text = re.sub(r"[^0-9a-zA-Z가-힣\s.!?]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def split_sentences(text):
    raw = re.split(r"[.!?]+", text)
    return [s.strip() for s in raw if s.strip()]

def tokenize(sentence):
    return [tok for tok in sentence.split(" ") if tok]

def remove_stopwords(tokens):
    return [tok for tok in tokens if tok not in STOPWORDS and len(tok) > 1]

def infer_pos(token):
    for suffix, tag in POS_RULES:
        if token.endswith(suffix):
            return tag
    if token.isdigit():
        return "NUM"
    if token and token[0].isupper():
        return "PROPN"
    return "NOUN"

def extract_named_entities(tokens):
    entities = []
    for tok in tokens:
        if tok in {"서울", "부산", "python", "ai", "stt", "tts", "ml"}:
            entities.append({"token": tok, "label": "ENTITY"})
    return entities

def bow_vector(tokens):
    freq = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1
    return freq

def tfidf_vectors(doc_tokens_list):
    df = {}
    for tokens in doc_tokens_list:
        for tok in set(tokens):
            df[tok] = df.get(tok, 0) + 1
    total_docs = max(1, len(doc_tokens_list))
    vectors = []
    for tokens in doc_tokens_list:
        tf = bow_vector(tokens)
        vec = {}
        for tok, cnt in tf.items():
            idf = math.log((1 + total_docs) / (1 + df.get(tok, 0))) + 1.0
            vec[tok] = round((cnt / max(1, len(tokens))) * idf, 4)
        vectors.append(vec)
    return vectors

def cosine_similarity(vec_a, vec_b):
    keys = set(vec_a) | set(vec_b)
    dot = sum(vec_a.get(k, 0.0) * vec_b.get(k, 0.0) for k in keys)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return round(dot / (norm_a * norm_b), 4)

def sentiment_score(tokens):
    pos = sum(1 for tok in tokens if tok in POSITIVE_WORDS)
    neg = sum(1 for tok in tokens if tok in NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"

def quality_issues(text):
    issues = []
    if not text:
        issues.append("empty")
    if len(text) < 8:
        issues.append("too_short")
    if text.count("  ") > 0:
        issues.append("duplicate_spaces")
    return issues

def build_test_cases():
    cases = [
        {
            "id": "news-1",
            "doc_type": "news",
            "text": "서울 AI 센터는 음성 데이터 전처리 성능을 향상했다. 사용자 만족이 개선됐다.",
            "label": "tech",
        },
        {
            "id": "review-1",
            "doc_type": "review",
            "text": "앱 반응이 빠르고 추천 기능이 편리하다.",
            "label": "positive",
        },
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append(
            {
                "id": "review-2",
                "doc_type": "review",
                "text": "잡음이 많아 인식 실패가 자주 발생해서 불만이 크다.",
                "label": "negative",
            }
        )
    if EXAMPLE_VARIANT >= 3:
        cases.append(
            {
                "id": "forum-1",
                "doc_type": "forum",
                "text": "stt 결과가 가끔 누락됨... why???",
                "label": "issue",
            }
        )
    if EXAMPLE_VARIANT >= 4:
        cases.append(
            {
                "id": "news-2",
                "doc_type": "news",
                "text": "python 기반 문서분류 모델이 정확도 0.91을 기록했다! 배포 자동화도 완료.",
                "label": "tech",
            }
        )
    if EXAMPLE_VARIANT >= 5:
        cases.append(
            {
                "id": "edge-empty",
                "doc_type": "review",
                "text": "",
                "label": "unknown",
            }
        )
    return cases

def build_query():
    if EXAMPLE_VARIANT >= 4:
        return "음성 인식 성능과 잡음 문제"
    if EXAMPLE_VARIANT >= 2:
        return "리뷰 만족과 오류"
    return "ai 음성 전처리"

def analyze_documents():
    cases = build_test_cases()
    rows = []
    all_tokens = []
    doc_tokens_list = []
    type_count = {}
    for case in cases:
        norm = normalize_text(case["text"])
        sentences = split_sentences(norm)
        tokens_raw = []
        for sent in sentences:
            tokens_raw.extend(tokenize(sent))
        tokens = remove_stopwords(tokens_raw)
        pos_tags = [infer_pos(tok) for tok in tokens]
        entities = extract_named_entities(tokens)
        issues = quality_issues(norm)
        sentiment = sentiment_score(tokens)
        row = {
            "id": case["id"],
            "doc_type": case["doc_type"],
            "label": case["label"],
            "sentence_count": len(sentences),
            "token_count": len(tokens),
            "tokens": tokens,
            "pos_tags": pos_tags,
            "entities": entities,
            "issues": issues,
            "sentiment": sentiment,
        }
        rows.append(row)
        all_tokens.extend(tokens)
        doc_tokens_list.append(tokens)
        type_count[case["doc_type"]] = type_count.get(case["doc_type"], 0) + 1

    bows = [bow_vector(row["tokens"]) for row in rows]
    tfidf = tfidf_vectors(doc_tokens_list)
    query_tokens = remove_stopwords(tokenize(normalize_text(build_query())))
    query_vec = bow_vector(query_tokens)
    similarities = []
    for row, vec in zip(rows, tfidf):
        sim = cosine_similarity(query_vec, vec)
        similarities.append((row["id"], sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    pos_dist = {}
    for row in rows:
        pos_dist[row["sentiment"]] = pos_dist.get(row["sentiment"], 0) + 1

    return {
        "rows": rows,
        "type_count": type_count,
        "token_total": len(all_tokens),
        "unique_tokens": len(set(all_tokens)),
        "top_terms": sorted(bow_vector(all_tokens).items(), key=lambda x: (-x[1], x[0]))[:7],
        "bow_vocab_size": len(set().union(*(set(v.keys()) for v in bows))) if bows else 0,
        "tfidf_doc_count": len(tfidf),
        "similarity_top": similarities[:3],
        "sentiment_distribution": pos_dist,
        "query_tokens": query_tokens,
    }

def build_mode_summary(mode, report):
    if mode == "understanding":
        return {
            "nlp_concepts": ["문장/문서/토큰", "형태소·품사·개체명", "텍스트 품질 이슈"],
            "doc_types": report["type_count"],
            "quality_flags": sum(len(row["issues"]) for row in report["rows"]),
        }
    if mode == "preprocess":
        return {
            "pipeline": ["정제", "문장분리", "토큰화", "불용어 제거", "벡터화"],
            "token_total": report["token_total"],
            "vocab": report["bow_vocab_size"],
        }
    if mode == "model":
        return {
            "model_keywords": ["BoW", "TF-IDF", "문장 임베딩(유사도)", "텍스트 분류(감성)"],
            "similarity_top": report["similarity_top"],
            "sentiment_distribution": report["sentiment_distribution"],
        }
    if mode == "practice":
        return {
            "practice_examples": ["뉴스/리뷰 전처리", "간단 분류", "멀티모달 확장 준비"],
            "query_tokens": report["query_tokens"],
            "top_terms": report["top_terms"],
        }
    return {"token_total": report["token_total"], "top_terms": report["top_terms"]}

def main():
    print("오늘 주제:", TOPIC)
    mode = resolve_mode()
    report = analyze_documents()
    summary = build_mode_summary(mode, report)
    print("모드:", mode)
    print("요약:", summary)
    return {
        "variant": EXAMPLE_VARIANT,
        "mode": mode,
        "doc_count": len(report["rows"]),
        "summary": summary,
    }

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "텍스트 분류(감성/문서분류)와 유사도 계산을 동시에 리포트로 출력하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
