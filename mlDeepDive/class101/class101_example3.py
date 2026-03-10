# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class101 example3: 모델 평가 지표 · 단계 1/4 입문 이해 [class101]"""

TOPIC = "모델 평가 지표 · 단계 1/4 입문 이해 [class101]"
EXAMPLE_TEMPLATE = "ml"
EXAMPLE_VARIANT = 3

from math import sqrt
import random

try:
    from sklearn.datasets import make_classification, make_regression, make_blobs
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.cluster import KMeans
    from sklearn.metrics import (
        mean_absolute_error,
        mean_squared_error,
        r2_score,
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix,
        roc_auc_score,
    )
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

def resolve_mode():
    if "ML/DL 개요" in TOPIC or "문제정의" in TOPIC:
        return "overview"
    if "지도학습" in TOPIC:
        return "supervised"
    if "회귀" in TOPIC:
        return "regression"
    if "분류" in TOPIC:
        return "classification"
    if "평가 지표" in TOPIC:
        return "evaluation"
    if "특성공학" in TOPIC:
        return "feature"
    if "과적합" in TOPIC or "일반화" in TOPIC:
        return "generalization"
    return "ml_general"

def classifier_names_for_variant():
    names = ["logistic"]
    if EXAMPLE_VARIANT >= 2:
        names.append("knn")
    if EXAMPLE_VARIANT >= 3:
        names.append("decision_tree")
    if EXAMPLE_VARIANT >= 4:
        names.append("random_forest")
    if EXAMPLE_VARIANT >= 5:
        names.append("svm")
    return names

def build_regression_case(seed):
    if not SKLEARN_OK:
        points = [(1, 52), (2, 61), (3, 70), (4, 82), (5, 91), (6, 103)]
        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        num = sum((x - mean_x) * (y - mean_y) for x, y in points)
        den = sum((x - mean_x) ** 2 for x in xs)
        slope = num / den
        bias = mean_y - slope * mean_x
        preds = [slope * x + bias for x in xs]
        errors = [abs(y - p) for y, p in zip(ys, preds)]
        mae = sum(errors) / len(errors)
        return {
            "backend": "python",
            "model": "manual_linear",
            "mae": round(mae, 4),
            "mse": round(sum((y - p) ** 2 for y, p in zip(ys, preds)) / len(ys), 4),
            "rmse": round(sqrt(sum((y - p) ** 2 for y, p in zip(ys, preds)) / len(ys)), 4),
            "r2": 0.0,
        }

    x, y = make_regression(
        n_samples=180 + EXAMPLE_VARIANT * 20,
        n_features=4,
        noise=12 + EXAMPLE_VARIANT * 2,
        random_state=seed,
    )
    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=seed
    )
    x_train, x_valid, y_train, y_valid = train_test_split(
        x_train_full, y_train_full, test_size=0.25, random_state=seed
    )
    pipe = Pipeline(
        [
            ("scale", StandardScaler()),
            ("model", LinearRegression()),
        ]
    )
    pipe.fit(x_train, y_train)
    y_pred = pipe.predict(x_test)
    y_valid_pred = pipe.predict(x_valid)
    report = {
        "backend": "sklearn",
        "model": "LinearRegression",
        "train_size": len(x_train),
        "valid_size": len(x_valid),
        "test_size": len(x_test),
        "mae": round(float(mean_absolute_error(y_test, y_pred)), 4),
        "mse": round(float(mean_squared_error(y_test, y_pred)), 4),
        "rmse": round(float(sqrt(mean_squared_error(y_test, y_pred))), 4),
        "r2": round(float(r2_score(y_test, y_pred)), 4),
        "valid_mae": round(float(mean_absolute_error(y_valid, y_valid_pred)), 4),
        "pipeline": "StandardScaler + LinearRegression",
    }
    if EXAMPLE_VARIANT >= 5:
        cv = cross_val_score(pipe, x, y, cv=4, scoring="neg_mean_squared_error")
        report["cv_rmse_mean"] = round(float(sqrt(abs(cv.mean()))), 4)
    return report

def make_classifier(name):
    if name == "logistic":
        return LogisticRegression(max_iter=400), True
    if name == "knn":
        return KNeighborsClassifier(n_neighbors=5), True
    if name == "decision_tree":
        return DecisionTreeClassifier(max_depth=5, random_state=7), False
    if name == "random_forest":
        return RandomForestClassifier(n_estimators=120, random_state=7), False
    return SVC(kernel="rbf", probability=True, random_state=7), True

def build_classification_case(seed, model_name):
    if not SKLEARN_OK:
        raw = [
            {"x1": 0.1, "x2": 0.2, "y": 0},
            {"x1": 0.3, "x2": 0.8, "y": 1},
            {"x1": 0.2, "x2": 0.1, "y": 0},
            {"x1": 0.8, "x2": 0.9, "y": 1},
        ]
        pred = [1 if item["x2"] >= 0.5 else 0 for item in raw]
        true = [item["y"] for item in raw]
        acc = sum(1 for t, p in zip(true, pred) if t == p) / len(true)
        return {
            "backend": "python",
            "model": "rule_threshold",
            "accuracy": round(acc, 4),
            "precision": round(acc, 4),
            "recall": round(acc, 4),
            "f1": round(acc, 4),
            "confusion_matrix": [[2, 0], [0, 2]],
            "roc_auc": 1.0,
        }

    x, y = make_classification(
        n_samples=320 + EXAMPLE_VARIANT * 30,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        class_sep=1.0 + EXAMPLE_VARIANT * 0.05,
        random_state=seed,
    )
    if "특성공학" in TOPIC:
        # feature engineering: interaction-like column
        extra = (x[:, 0] * x[:, 1]).reshape(-1, 1)
        x = __import__("numpy").concatenate([x, extra], axis=1)

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x, y, test_size=0.2, random_state=seed, stratify=y
    )
    x_train, x_valid, y_train, y_valid = train_test_split(
        x_train_full, y_train_full, test_size=0.25, random_state=seed, stratify=y_train_full
    )
    model, need_scale = make_classifier(model_name)
    steps = []
    if need_scale:
        scaler = MinMaxScaler() if "특성공학" in TOPIC else StandardScaler()
        steps.append(("scale", scaler))
    steps.append(("model", model))
    pipe = Pipeline(steps)
    pipe.fit(x_train, y_train)
    y_pred = pipe.predict(x_test)
    y_valid_pred = pipe.predict(x_valid)

    y_score = None
    if hasattr(pipe, "predict_proba"):
        y_score = pipe.predict_proba(x_test)[:, 1]
    elif hasattr(pipe, "decision_function"):
        y_score = pipe.decision_function(x_test)

    report = {
        "backend": "sklearn",
        "model": model_name,
        "train_size": len(x_train),
        "valid_size": len(x_valid),
        "test_size": len(x_test),
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "valid_f1": round(float(f1_score(y_valid, y_valid_pred, zero_division=0)), 4),
        "pipeline": " -> ".join(name for name, _ in steps),
    }
    if y_score is not None:
        report["roc_auc"] = round(float(roc_auc_score(y_test, y_score)), 4)
    if EXAMPLE_VARIANT >= 5:
        search = GridSearchCV(
            pipe,
            param_grid={"model__C": [0.1, 1.0, 3.0]} if model_name == "logistic" else {},
            cv=3,
            scoring="f1",
        )
        if search.param_grid:
            search.fit(x_train, y_train)
            report["grid_search_best_score"] = round(float(search.best_score_), 4)
            report["grid_search_best_params"] = dict(search.best_params_)
    return report

def build_unsupervised_case(seed):
    if not SKLEARN_OK:
        return {"backend": "python", "algorithm": "manual_grouping", "clusters": 2}
    x, _ = make_blobs(n_samples=180, centers=3, cluster_std=1.2, random_state=seed)
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=seed)
    labels = kmeans.fit_predict(x)
    return {
        "backend": "sklearn",
        "algorithm": "KMeans",
        "clusters": int(len(set(labels))),
        "inertia": round(float(kmeans.inertia_), 4),
    }

def main():
    print("오늘 주제:", TOPIC)
    mode = resolve_mode()
    seed = 40 + EXAMPLE_VARIANT * 7
    reports = {"mode": mode, "variant": EXAMPLE_VARIANT, "sklearn_available": SKLEARN_OK}

    if mode in {"overview", "supervised", "ml_general"}:
        reports["regression"] = build_regression_case(seed)
        reports["classification"] = [
            build_classification_case(seed + idx, name)
            for idx, name in enumerate(classifier_names_for_variant()[:2], start=1)
        ]
        if mode == "supervised" and EXAMPLE_VARIANT >= 3:
            reports["unsupervised"] = build_unsupervised_case(seed + 99)
    elif mode == "regression":
        reports["regression"] = build_regression_case(seed)
    elif mode in {"classification", "feature", "evaluation", "generalization"}:
        reports["classification"] = [
            build_classification_case(seed + idx, name)
            for idx, name in enumerate(classifier_names_for_variant(), start=1)
        ]
        if mode in {"evaluation", "generalization"}:
            reports["regression"] = build_regression_case(seed + 77)
        if mode == "supervised":
            reports["unsupervised"] = build_unsupervised_case(seed + 99)
    else:
        reports["regression"] = build_regression_case(seed)

    print("리포트:", reports)
    return reports

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "검증 데이터를 따로 두고 과적합 징후를 기록하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
