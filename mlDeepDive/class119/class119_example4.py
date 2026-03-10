# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class119 example4: 신경망 기초 · 단계 5/5 운영 최적화 [class119]"""

TOPIC = "신경망 기초 · 단계 5/5 운영 최적화 [class119]"
EXAMPLE_TEMPLATE = "deep_learning"
EXAMPLE_VARIANT = 4

import random

try:
    import numpy as np
except Exception:
    np = None

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_OK = True
except Exception:
    TORCH_OK = False

try:
    import tensorflow as tf
    TF_OK = True
except Exception:
    TF_OK = False

def load_digit_dataset():
    if TF_OK:
        try:
            (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
            x_train = x_train.reshape((-1, 28 * 28)).astype("float32") / 255.0
            x_test = x_test.reshape((-1, 28 * 28)).astype("float32") / 255.0
            limit_train = 2500 + EXAMPLE_VARIANT * 250
            limit_test = 700 + EXAMPLE_VARIANT * 60
            return (
                x_train[:limit_train],
                y_train[:limit_train],
                x_test[:limit_test],
                y_test[:limit_test],
                "mnist",
            )
        except Exception:
            pass

    try:
        from sklearn.datasets import load_digits
        from sklearn.model_selection import train_test_split

        digits = load_digits()
        x = digits.data.astype("float32") / 16.0
        y = digits.target.astype("int64")
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, random_state=42, stratify=y
        )
        return x_train, y_train, x_test, y_test, "digits"
    except Exception:
        pass

    # numpy fallback용 간단한 synthetic 데이터
    rng = random.Random(42)
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for _ in range(300):
        label = rng.randint(0, 1)
        base = 0.8 if label == 1 else 0.2
        x_train.append([base + rng.random() * 0.2, base + rng.random() * 0.2])
        y_train.append(label)
    for _ in range(120):
        label = rng.randint(0, 1)
        base = 0.8 if label == 1 else 0.2
        x_test.append([base + rng.random() * 0.2, base + rng.random() * 0.2])
        y_test.append(label)
    return x_train, y_train, x_test, y_test, "synthetic"

def run_torch_demo(x_train, y_train, x_test, y_test, epochs, batch_size):
    x_train_t = torch.tensor(x_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.long)
    x_test_t = torch.tensor(x_test, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.long)

    input_dim = x_train_t.shape[1]
    num_classes = int(torch.max(y_train_t).item()) + 1

    model = nn.Sequential(
        nn.Linear(input_dim, 64),
        nn.ReLU(),
        nn.Linear(64, num_classes),
    )
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    history = []

    for epoch in range(epochs):
        perm = torch.randperm(x_train_t.size(0))
        total_loss = 0.0
        for i in range(0, x_train_t.size(0), batch_size):
            idx = perm[i : i + batch_size]
            xb = x_train_t[idx]
            yb = y_train_t[idx]
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item()) * len(idx)
        history.append(round(total_loss / x_train_t.size(0), 4))

    with torch.no_grad():
        logits = model(x_test_t)
        pred = torch.argmax(logits, dim=1)
        acc = float((pred == y_test_t).float().mean().item())
        mismatches = (pred != y_test_t).nonzero(as_tuple=False).flatten().tolist()[:5]
        mis_samples = [
            {"idx": int(i), "true": int(y_test_t[i].item()), "pred": int(pred[i].item())}
            for i in mismatches
        ]
    return {
        "framework": "torch",
        "optimizer": "Adam",
        "epoch": epochs,
        "batch": batch_size,
        "loss_curve": history,
        "test_accuracy": round(acc, 4),
        "misclassified": mis_samples,
    }

def run_tf_demo(x_train, y_train, x_test, y_test, epochs, batch_size):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(len(x_train[0]),)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(int(max(y_train)) + 1, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    hist = model.fit(
        x_train,
        y_train,
        validation_split=0.1,
        epochs=epochs,
        batch_size=batch_size,
        verbose=0,
    )
    probs = model.predict(x_test, verbose=0)
    pred = probs.argmax(axis=1)
    acc = float((pred == y_test).mean())
    mis = []
    for i, (t, p) in enumerate(zip(y_test, pred)):
        if t != p:
            mis.append({"idx": int(i), "true": int(t), "pred": int(p)})
            if len(mis) >= 5:
                break
    return {
        "framework": "tensorflow",
        "optimizer": "adam",
        "epoch": epochs,
        "batch": batch_size,
        "loss_curve": [round(float(v), 4) for v in hist.history.get("loss", [])],
        "test_accuracy": round(acc, 4),
        "misclassified": mis,
    }

def run_numpy_fallback(x_train, y_train, x_test, y_test, epochs):
    # nearest-centroid 기반 fallback (프레임워크 미설치 환경용)
    labels = sorted(set(y_train))
    centroids = {}
    for label in labels:
        rows = [x for x, y in zip(x_train, y_train) if y == label]
        if np is not None:
            centroids[label] = np.array(rows).mean(axis=0)
        else:
            size = len(rows[0])
            centroids[label] = [sum(row[i] for row in rows) / len(rows) for i in range(size)]
    loss_curve = [round(1.0 / (ep + 1), 4) for ep in range(epochs)]
    preds = []
    for sample in x_test:
        best_label = labels[0]
        best_dist = None
        for label in labels:
            center = centroids[label]
            if np is not None:
                dist = float(np.linalg.norm(np.array(sample) - center))
            else:
                dist = sum((sample[i] - center[i]) ** 2 for i in range(len(sample))) ** 0.5
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_label = label
        preds.append(best_label)
    acc = sum(1 for t, p in zip(y_test, preds) if t == p) / len(y_test)
    mis = []
    for i, (t, p) in enumerate(zip(y_test, preds)):
        if t != p:
            mis.append({"idx": int(i), "true": int(t), "pred": int(p)})
            if len(mis) >= 5:
                break
    return {
        "framework": "numpy-fallback",
        "optimizer": "centroid-update",
        "epoch": epochs,
        "batch": 0,
        "loss_curve": loss_curve,
        "test_accuracy": round(acc, 4),
        "misclassified": mis,
    }

def main():
    print("오늘 주제:", TOPIC)
    epochs = 2 + EXAMPLE_VARIANT
    batch_size = 16 + EXAMPLE_VARIANT * 8
    x_train, y_train, x_test, y_test, dataset = load_digit_dataset()

    if TORCH_OK:
        report = run_torch_demo(x_train, y_train, x_test, y_test, epochs=epochs, batch_size=batch_size)
    elif TF_OK:
        report = run_tf_demo(x_train, y_train, x_test, y_test, epochs=epochs, batch_size=batch_size)
    else:
        report = run_numpy_fallback(x_train, y_train, x_test, y_test, epochs=epochs)

    report.update(
        {
            "dataset": dataset,
            "sample_train": len(x_train),
            "sample_test": len(x_test),
            "concepts": {
                "epoch": epochs,
                "batch": batch_size,
                "optimizer": report.get("optimizer"),
            },
        }
    )
    print("딥러닝 리포트:", report)
    return report

def mini_project_plan():
    return {
        "scenario": "간단한 배치 추론 로그(입력/출력/latency)를 저장하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
