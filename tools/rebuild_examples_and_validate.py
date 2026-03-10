# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

import argparse
import csv
import py_compile
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
COPYRIGHT_TEXT = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(k).lstrip("\ufeff"): v for k, v in raw.items()})
    return rows


def class_dir_from_row(row: dict[str, str]) -> Path:
    md_rel = (row.get("md_file") or "").strip()
    if md_rel:
        md_path = ROOT / Path(md_rel)
        if md_path.name:
            return md_path.parent
    return ROOT / row["class"]


def subject_root(class_dir: Path) -> str:
    try:
        rel = class_dir.resolve().relative_to(ROOT.resolve())
        return rel.parts[0] if rel.parts else ""
    except Exception:
        return class_dir.parts[-2] if len(class_dir.parts) >= 2 else class_dir.name


def filter_rows_by_subject_roots(rows: list[dict[str, str]], roots: set[str]) -> list[dict[str, str]]:
    if not roots:
        return rows
    kept: list[dict[str, str]] = []
    for row in rows:
        class_dir = class_dir_from_row(row)
        if subject_root(class_dir) in roots:
            kept.append(row)
    return kept


def is_python_basics(row: dict[str, str], class_dir: Path | None = None) -> bool:
    class_dir = class_dir or class_dir_from_row(row)
    root_name = subject_root(class_dir)
    subject = (row.get("subject_name") or "").lower()
    return root_name == "pyBasics" or "파이썬" in subject


def variants_for_row(row: dict[str, str], class_dir: Path | None = None) -> list[int]:
    if is_python_basics(row, class_dir=class_dir):
        return [1, 2, 3, 4, 5]
    return [1, 2, 3, 4, 5]


def example_path(class_dir: Path, class_id: str, variant: int) -> Path:
    suffix = f"example{variant}"
    return class_dir / f"{class_id}_{suffix}.py"


def pick_template(module: str, subject: str) -> str:
    module_text = module.lower()
    subject_text = subject.lower()
    text = f"{subject_text} {module_text}"

    if "음성 데이터 활용한 tts와 stt 모델 개발" in subject_text:
        return "speech"
    if "거대 언어 모델을 활용한 자연어 생성" in subject:
        return "llm_gen"

    if "mlops" in text or "모델 레지스트리" in module or "배포 자동화" in module:
        return "ml"
    if "aiops" in text or "관측 데이터" in module or "이상탐지" in module or "runbook" in text:
        return "data_preprocess"

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
    if "python 외부 라이브러리 활용" in module_text:
        return "module_package"
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
    if any(
        k in module_text
        for k in [
            "오리엔테이션",
            "개발환경 준비",
            "환경 구성",
            "수업 준비",
            "개발환경 검증",
            "소프트웨어 설치",
            "플랫폼 가입",
        ]
    ):
        return "dev_setup"
    if "변수와 출력 첫 실행" in module_text:
        return "variables"

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


def q(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', "\\\"")


def wrap_code(class_id: str, module: str, template: str, variant: int, body: str) -> str:
    doc = f'"""{class_id} example{variant}: {module}"""'
    header = dedent(
        f"""\
        # {COPYRIGHT_TEXT}

        {doc}

        TOPIC = "{q(module)}"
        EXAMPLE_TEMPLATE = "{template}"
        EXAMPLE_VARIANT = {variant}
        """
    )
    return header + "\n" + body.strip() + "\n"


def build_body(template: str, class_id: str) -> str:
    if template == "dev_setup":
        return f"""
        from pathlib import Path
        import platform

        def build_setup_plan():
            plan = [
                ("venv", "python -m venv .venv"),
                ("activate", "source .venv/bin/activate"),
                ("deps", "pip install -r requirements.txt"),
                ("run", "python {class_id}_example1.py"),
            ]
            if EXAMPLE_VARIANT >= 3:
                plan.append(("freeze", "pip freeze > requirements.lock.txt"))
            if EXAMPLE_VARIANT >= 4:
                plan.append(("smoke", "python -c \\"import numpy, pandas\\""))
            if EXAMPLE_VARIANT >= 5:
                plan.append(("check", "python -m pip check"))
            return plan

        def build_path_checks():
            checks = ["README.md", "requirements.txt"]
            if EXAMPLE_VARIANT >= 2:
                checks.append("curriculum_index.csv")
            if EXAMPLE_VARIANT >= 3:
                checks.extend(["dataVizPrep", "tools/rebuild_examples_and_validate.py"])
            if EXAMPLE_VARIANT >= 4:
                checks.append("run_class.sh")
            if EXAMPLE_VARIANT >= 5:
                checks.append("run_day.sh")
            return checks

        def scan_workspace():
            root = Path(__file__).resolve().parents[2]
            checks = build_path_checks()
            existing = {{rel: (root / rel).exists() for rel in checks}}
            return {{
                "platform": platform.system(),
                "variant": EXAMPLE_VARIANT,
                "requirements_exists": (root / "requirements.txt").exists(),
                "readme_exists": (root / "README.md").exists(),
                "checks": existing,
            }}

        def main():
            print("오늘 주제:", TOPIC)
            plan = build_setup_plan()
            for idx, (name, cmd) in enumerate(plan, start=1):
                print(f"{{idx}}. {{name}} -> {{cmd}}")
            status = scan_workspace()
            print("환경 점검:", status)
            return {{"step_count": len(plan), **status}}
        """

    if template == "variables":
        return """
        def infer_schema(record):
            return {k: type(v).__name__ for k, v in record.items()}

        def parse_bool(value):
            text = str(value).strip().lower()
            return text in {"1", "true", "yes", "y"}

        def normalize_record(record):
            name = str(record["name"]).strip()
            age = int(record["age"])
            score = float(record["score"])
            active = parse_bool(record["active"])
            level = "pass" if score >= 80 else "retry"
            return {
                "name": name,
                "age": age,
                "score": score,
                "active": active,
                "level": level,
            }

        def format_report(row):
            return (
                f"{row['name']}({row['age']}) "
                f"score={row['score']:.1f} active={row['active']} level={row['level']}"
            )

        def build_test_cases():
            cases = [
                {
                    "case": "baseline",
                    "name": "  민수  ",
                    "age": "19",
                    "score": "91.5",
                    "active": "1",
                }
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    {
                        "case": "string_bool",
                        "name": "지연",
                        "age": "20",
                        "score": "79.9",
                        "active": "yes",
                    }
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    {
                        "case": "boundary",
                        "name": "하늘",
                        "age": "18",
                        "score": "80",
                        "active": "false",
                    }
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    {
                        "case": "high_score",
                        "name": "도윤",
                        "age": "22",
                        "score": "99.4",
                        "active": "True",
                    }
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    {
                        "case": "invalid_age",
                        "name": "오류케이스",
                        "age": "N/A",
                        "score": "60",
                        "active": "0",
                    }
                )
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            errors = []
            for raw in build_test_cases():
                case_name = raw["case"]
                try:
                    normalized = normalize_record(raw)
                    normalized["case"] = case_name
                    normalized["schema"] = infer_schema(normalized)
                    normalized["summary"] = format_report(normalized)
                    reports.append(normalized)
                    print(f"[{case_name}] 정규화:", normalized["summary"])
                except (TypeError, ValueError) as exc:
                    error = {"case": case_name, "error": str(exc)}
                    errors.append(error)
                    print(f"[{case_name}] 오류:", error)
            return {"variant": EXAMPLE_VARIANT, "success": len(reports), "errors": errors}
        """

    if template == "condition":
        return """
        def classify_price(amount):
            if amount >= 100000:
                return "premium"
            if amount >= 50000:
                return "standard"
            return "starter"

        def discount_policy(order):
            base = classify_price(order["amount"])
            if order["member"] and order["coupon"]:
                rate = 0.18
            elif order["member"] or order["coupon"]:
                rate = 0.1
            else:
                rate = 0.0
            if order["amount"] < 0:
                return {"status": "invalid", "rate": 0.0, "final": 0}
            final = int(order["amount"] * (1 - rate))
            return {"status": base, "rate": rate, "final": final}

        def build_test_cases():
            cases = [{"name": "A", "amount": 120000, "member": True, "coupon": False}]
            if EXAMPLE_VARIANT >= 2:
                cases.append({"name": "B", "amount": 85000, "member": False, "coupon": True})
            if EXAMPLE_VARIANT >= 3:
                cases.append({"name": "C", "amount": 42000, "member": False, "coupon": False})
            if EXAMPLE_VARIANT >= 4:
                cases.append({"name": "D", "amount": 50000, "member": True, "coupon": True})
            if EXAMPLE_VARIANT >= 5:
                cases.append({"name": "E", "amount": -1000, "member": True, "coupon": True})
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            outputs = []
            for case in build_test_cases():
                result = discount_policy(case)
                row = {**case, **result}
                outputs.append(row)
                print("판정:", row)
            invalid_count = sum(1 for row in outputs if row["status"] == "invalid")
            return {"variant": EXAMPLE_VARIANT, "case_count": len(outputs), "invalid_count": invalid_count}
        """

    if template == "loop":
        return """
        def rolling_average(values, window):
            result = []
            for idx in range(len(values)):
                start = max(0, idx - window + 1)
                chunk = values[start : idx + 1]
                result.append(round(sum(chunk) / len(chunk), 2))
            return result

        def bounded_scan(values, stop_at):
            accepted = []
            idx = 0
            while idx < len(values):
                current = values[idx]
                idx += 1
                if current < 0:
                    continue
                if current >= stop_at:
                    break
                accepted.append(current)
            return accepted

        def multiplication_grid(size):
            grid = []
            for i in range(1, size + 1):
                row = []
                for j in range(1, size + 1):
                    row.append(i * j)
                grid.append(row)
            return grid

        def build_test_cases():
            cases = [("baseline", [12, 15, 13, 20, 19, 23])]
            if EXAMPLE_VARIANT >= 2:
                cases.append(("with_zero", [5, 0, 7, 9, 0, 11]))
            if EXAMPLE_VARIANT >= 3:
                cases.append(("with_negative", [8, -1, 6, 4, -3, 9]))
            if EXAMPLE_VARIANT >= 4:
                cases.append(("longer_seq", [3, 6, 9, 12, 15, 18, 21, 24]))
            if EXAMPLE_VARIANT >= 5:
                cases.append(("high_values", [25, 33, 41, 58, 72, 91]))
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            for case_name, values in build_test_cases():
                trend = rolling_average(values, window=3)
                accepted = bounded_scan(values, stop_at=50)
                grid = multiplication_grid(2 + min(EXAMPLE_VARIANT, 3))
                report = {
                    "case": case_name,
                    "points": len(values),
                    "last_avg": trend[-1],
                    "accepted_count": len(accepted),
                    "grid_last": grid[-1][-1],
                }
                reports.append(report)
                print(f"[{case_name}] 리포트:", report)
            return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "reports": reports}
        """

    if template == "function_module":
        return """
        def grade(score, pass_line=70):
            return "PASS" if score >= pass_line else "RETRY"

        def summarize_scores(*scores):
            if not scores:
                return {"avg": 0.0, "max": 0.0, "min": 0.0}
            return {
                "avg": round(sum(scores) / len(scores), 2),
                "max": max(scores),
                "min": min(scores),
            }

        def build_profile(name, **kwargs):
            profile = {"name": name}
            profile.update(kwargs)
            return profile

        def apply_pipeline(values, *funcs):
            result = list(values)
            for fn in funcs:
                result = [fn(v) for v in result]
            return result

        def build_test_cases():
            cases = [("baseline", [72, 88, 91])]
            if EXAMPLE_VARIANT >= 2:
                cases.append(("mixed", [61, 77, 84, 95]))
            if EXAMPLE_VARIANT >= 3:
                cases.append(("boundary", [70, 70, 69]))
            if EXAMPLE_VARIANT >= 4:
                cases.append(("short", [100]))
            if EXAMPLE_VARIANT >= 5:
                cases.append(("wide", [32, 58, 74, 81, 93]))
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            for case_name, scores in build_test_cases():
                stats = summarize_scores(*scores)
                labels = [grade(score, pass_line=75) for score in scores]
                curved = apply_pipeline(
                    scores,
                    lambda v: v + 3,
                    lambda v: min(v, 100),
                )
                profile = build_profile(
                    case_name,
                    count=len(scores),
                    avg=stats["avg"],
                    pass_count=sum(1 for label in labels if label == "PASS"),
                )
                report = {
                    "case": case_name,
                    "stats": stats,
                    "labels": labels,
                    "curved": curved,
                    "profile": profile,
                }
                reports.append(report)
                print(f"[{case_name}] 함수 리포트:", report)
            return {"variant": EXAMPLE_VARIANT, "case_count": len(reports)}
        """

    if template == "module_package":
        return f"""
        import importlib.util
        import math
        import os
        import random
        from datetime import datetime
        from pathlib import Path

        def ensure_user_module():
            module_path = Path(__file__).with_name("{class_id}_user_module.py")
            if not module_path.exists():
                module_path.write_text(
                    "def build_message(name):\\n"
                    "    return f'hello, {{name}}'\\n",
                    encoding="utf-8",
                )
            spec = importlib.util.spec_from_file_location("user_module", module_path)
            module = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(module)
            return module, module_path

        def stdlib_snapshot(seed):
            random.seed(seed)
            return {{
                "randint": random.randint(1, 100),
                "sqrt_81": int(math.sqrt(81)),
                "today": datetime.now().strftime("%Y-%m-%d"),
                "cwd_name": os.path.basename(os.getcwd()),
            }}

        def build_test_cases():
            cases = [("baseline", 7)]
            if EXAMPLE_VARIANT >= 2:
                cases.append(("alt_seed", 21))
            if EXAMPLE_VARIANT >= 3:
                cases.append(("seed_42", 42))
            if EXAMPLE_VARIANT >= 4:
                cases.append(("seed_99", 99))
            if EXAMPLE_VARIANT >= 5:
                cases.append(("seed_123", 123))
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            user_module, module_path = ensure_user_module()
            reports = []
            for case_name, seed in build_test_cases():
                snap = stdlib_snapshot(seed)
                snap["case"] = case_name
                snap["message"] = user_module.build_message(case_name)
                snap["module_file"] = module_path.name
                reports.append(snap)
                print(f"[{{case_name}}] 모듈 리포트:", snap)
            return {{"variant": EXAMPLE_VARIANT, "case_count": len(reports), "module": module_path.name}}
        """

    if template == "collection":
        return """
        def summarize_orders(orders):
            teams_list = [row["team"] for row in orders]
            unique_teams_set = set(teams_list)
            top_slice = teams_list[: min(3, len(teams_list))]
            by_team_dict = {}
            for row in orders:
                by_team_dict[row["team"]] = by_team_dict.get(row["team"], 0) + row["amount"]
            ranking_tuple = tuple(sorted(by_team_dict.items(), key=lambda x: x[1], reverse=True))
            high_orders = [row for row in orders if row["amount"] >= 100]
            return {
                "team_list": teams_list,
                "unique_teams": unique_teams_set,
                "top_slice": top_slice,
                "by_team": by_team_dict,
                "ranking": ranking_tuple,
                "high_orders": high_orders,
            }

        def choose_structure(use_case):
            if use_case == "ordered":
                return "list"
            if use_case == "immutable":
                return "tuple"
            if use_case == "lookup":
                return "dict"
            return "set"

        def build_test_cases():
            cases = [
                (
                    "baseline",
                    [
                        {"team": "A", "amount": 120},
                        {"team": "B", "amount": 90},
                        {"team": "A", "amount": 60},
                        {"team": "C", "amount": 200},
                    ],
                )
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    (
                        "with_duplicate",
                        [
                            {"team": "A", "amount": 10},
                            {"team": "A", "amount": 15},
                            {"team": "B", "amount": 40},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    (
                        "many_teams",
                        [
                            {"team": "D", "amount": 130},
                            {"team": "E", "amount": 70},
                            {"team": "F", "amount": 95},
                            {"team": "G", "amount": 160},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    (
                        "small_values",
                        [
                            {"team": "X", "amount": 8},
                            {"team": "Y", "amount": 12},
                            {"team": "Z", "amount": 18},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    (
                        "mixed_values",
                        [
                            {"team": "A", "amount": 300},
                            {"team": "B", "amount": 110},
                            {"team": "C", "amount": 75},
                            {"team": "B", "amount": 25},
                        ],
                    )
                )
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            for case_name, orders in build_test_cases():
                stats = summarize_orders(orders)
                structure = choose_structure("lookup" if len(stats["by_team"]) >= 3 else "ordered")
                report = {
                    "case": case_name,
                    "team_count": len(stats["unique_teams"]),
                    "winner": stats["ranking"][0][0],
                    "selected_structure": structure,
                    "top_slice": stats["top_slice"],
                    "high_order_count": len(stats["high_orders"]),
                }
                reports.append(report)
                print(f"[{case_name}] 컬렉션 리포트:", report)
            return {"variant": EXAMPLE_VARIANT, "case_count": len(reports)}
        """

    if template == "file_io":
        return f"""
        import csv
        from pathlib import Path

        def write_text_summary(rows, out_path):
            lines = [f"{{row['name']}},{{row['score']}}" for row in rows]
            out_path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
            return out_path

        def write_csv_rows(rows, out_path):
            with out_path.open("w", encoding="utf-8", newline="") as fp:
                writer = csv.DictWriter(fp, fieldnames=["name", "score"])
                writer.writeheader()
                writer.writerows(rows)
            return out_path

        def read_csv_rows(path):
            with path.open("r", encoding="utf-8", newline="") as fp:
                reader = csv.DictReader(fp)
                return [{{"name": row["name"], "score": int(row["score"])}} for row in reader]

        def build_rows():
            rows = [
                {{"name": "A", "score": 72}},
                {{"name": "B", "score": 88}},
                {{"name": "C", "score": 91}},
            ]
            if EXAMPLE_VARIANT >= 2:
                rows.append({{"name": "D", "score": 67}})
            if EXAMPLE_VARIANT >= 3:
                rows.append({{"name": "E", "score": 95}})
            if EXAMPLE_VARIANT >= 4:
                rows.append({{"name": "F", "score": 84}})
            if EXAMPLE_VARIANT >= 5:
                rows.append({{"name": "G", "score": 78}})
            return rows

        def run_automation(base_dir):
            text_path = base_dir / "{class_id}_summary.txt"
            csv_path = base_dir / "{class_id}_scores.csv"
            rows = build_rows()
            write_text_summary(rows, text_path)
            write_csv_rows(rows, csv_path)
            loaded = read_csv_rows(csv_path)
            passed = [row for row in loaded if row["score"] >= 80]
            return {{
                "text_file": text_path.name,
                "csv_file": csv_path.name,
                "row_count": len(loaded),
                "pass_count": len(passed),
            }}

        def main():
            print("오늘 주제:", TOPIC)
            out_dir = Path(__file__).parent
            report = run_automation(out_dir)
            print("파일 리포트:", report)
            return {{"variant": EXAMPLE_VARIANT, **report}}
        """

    if template == "exception":
        return """
        import traceback

        def safe_to_float(value):
            try:
                return float(value)
            except (TypeError, ValueError) as exc:
                return {"ok": False, "value": value, "error": str(exc), "kind": type(exc).__name__}
            finally:
                pass

        def parse_batch(values):
            parsed = []
            valid = []
            errors = []
            for value in values:
                item = safe_to_float(value)
                if isinstance(item, dict):
                    errors.append(item)
                else:
                    parsed.append(item)
                    valid.append(item)
            return {
                "parsed": parsed,
                "valid_count": len(valid),
                "invalid_count": len(errors),
                "errors": errors,
            }

        def divide(a, b):
            if b == 0:
                raise ZeroDivisionError("분모는 0이 될 수 없습니다.")
            return a / b

        def build_inputs():
            cases = [["10.5", "err", None, "3"]]
            if EXAMPLE_VARIANT >= 2:
                cases.append(["7", "4.2", "x", "11"])
            if EXAMPLE_VARIANT >= 3:
                cases.append(["0", "-3", "6.5", "bad"])
            if EXAMPLE_VARIANT >= 4:
                cases.append(["100", "25", "5", "zero"])
            if EXAMPLE_VARIANT >= 5:
                cases.append(["1e2", "", "NaN", "15"])
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            for idx, values in enumerate(build_inputs(), start=1):
                report = parse_batch(values)
                try:
                    division = divide(100, idx - 2)
                    report["division"] = round(division, 2)
                except ZeroDivisionError as exc:
                    report["division_error"] = str(exc)
                    report["trace_hint"] = traceback.format_exc().splitlines()[-1]
                reports.append(report)
                print(f"[case-{idx}] 예외 리포트:", report)
            return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "invalid_total": sum(r["invalid_count"] for r in reports)}
        """

    if template == "oop":
        return """
        class Experiment:
            def __init__(self, name, score):
                self.name = name
                self.score = score

            def is_pass(self, threshold=80):
                return self.score >= threshold

            def to_dict(self):
                return {"name": self.name, "score": self.score, "pass": self.is_pass()}

        def main():
            print("오늘 주제:", TOPIC)
            runs = [Experiment("baseline", 76), Experiment("tuned", 84)]
            report = [r.to_dict() for r in runs]
            print("실험 리포트:", report)
            return {"best": max(report, key=lambda x: x["score"])["name"], "count": len(report)}
        """

    if template == "numpy":
        return """
        try:
            import numpy as np
        except ImportError:
            np = None

        def compute_stats(values):
            if not values:
                raise ValueError("values must not be empty")
            if np is None:
                avg = sum(values) / len(values)
                var = sum((v - avg) ** 2 for v in values) / len(values)
                return {"mean": round(avg, 4), "std": round(var ** 0.5, 4), "backend": "python"}
            arr = np.array(values, dtype=float)
            return {
                "mean": round(float(arr.mean()), 4),
                "std": round(float(arr.std()), 4),
                "backend": "numpy",
            }

        def build_test_cases():
            cases = [("baseline", [0.3, 0.4, 0.45, 0.5, 0.65])]
            if EXAMPLE_VARIANT >= 2:
                cases.append(("signed_values", [-1.2, -0.2, 0.0, 0.5, 1.1]))
            if EXAMPLE_VARIANT >= 3:
                cases.append(("with_outlier", [10, 10.2, 9.9, 10.1, 45]))
            if EXAMPLE_VARIANT >= 4:
                cases.append(("wide_range", [0.001, 1, 10, 100, 250]))
            if EXAMPLE_VARIANT >= 5:
                cases.append(("tiny_decimals", [0.1001, 0.1002, 0.1004, 0.1003, 0.1002]))
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            for name, values in build_test_cases():
                stats = compute_stats(values)
                stats["case"] = name
                stats["size"] = len(values)
                reports.append(stats)
                print(f"[{name}] 통계:", stats)

            largest = max(reports, key=lambda x: x["std"])
            return {
                "variant": EXAMPLE_VARIANT,
                "case_count": len(reports),
                "largest_std_case": largest["case"],
                "backend": reports[0]["backend"] if reports else "unknown",
            }
        """

    if template == "pandas":
        return """
        try:
            import pandas as pd
        except ImportError:
            pd = None

        def safe_float(value):
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        def normalize_rows(rows):
            cleaned = []
            dropped = []
            for idx, row in enumerate(rows, start=1):
                score = safe_float(row.get("score"))
                name = str(row.get("name", "")).strip() or f"unknown-{idx}"
                if score is None:
                    dropped.append({"row": idx, "reason": "invalid_score", "raw": row.get("score")})
                    continue
                cleaned.append({"name": name, "score": score})
            return cleaned, dropped

        def summarize_scores(rows):
            cleaned, dropped = normalize_rows(rows)
            if not cleaned:
                return {"backend": "python", "avg": 0.0, "pass_count": 0, "row_count": 0, "dropped_count": len(dropped)}

            if pd is None:
                avg = sum(r["score"] for r in cleaned) / len(cleaned)
                passed = sum(1 for r in cleaned if r["score"] >= 80)
                return {
                    "backend": "python",
                    "avg": round(avg, 2),
                    "pass_count": passed,
                    "row_count": len(cleaned),
                    "dropped_count": len(dropped),
                }

            df = pd.DataFrame(cleaned)
            return {
                "backend": "pandas",
                "avg": round(float(df["score"].mean()), 2),
                "pass_count": int((df["score"] >= 80).sum()),
                "row_count": int(len(df)),
                "dropped_count": len(dropped),
            }

        def build_test_cases():
            cases = [
                (
                    "baseline",
                    [
                        {"name": "A", "score": 72},
                        {"name": "B", "score": 88},
                        {"name": "C", "score": 91},
                    ],
                ),
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    (
                        "string_scores",
                        [
                            {"name": "D", "score": "84"},
                            {"name": "E", "score": "79.5"},
                            {"name": "F", "score": "92"},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    (
                        "missing_values",
                        [
                            {"name": "G", "score": 81},
                            {"name": "H", "score": None},
                            {"name": "I", "score": "err"},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    (
                        "edge_threshold",
                        [
                            {"name": "J", "score": 79.99},
                            {"name": "K", "score": 80},
                            {"name": "L", "score": 80.01},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    (
                        "mixed_inputs",
                        [
                            {"name": "M", "score": "100"},
                            {"name": "N", "score": "-5"},
                            {"name": " ", "score": 87.2},
                            {"name": "P", "score": "not-a-number"},
                        ],
                    )
                )
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            reports = []
            for name, rows in build_test_cases():
                summary = summarize_scores(rows)
                summary["case"] = name
                reports.append(summary)
                print(f"[{name}] 요약:", summary)
            return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "reports": reports}
        """

    if template == "visualization":
        return f"""
        from pathlib import Path
        import re

        def sanitize_case_name(name):
            return re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_") or "case"

        def save_chart(points, case_name):
            token = sanitize_case_name(case_name)
            out = Path(__file__).with_name(f"{class_id}_plot_{{token}}.png")
            try:
                import matplotlib.pyplot as plt

                x = [idx + 1 for idx, _ in enumerate(points)]
                y = [v for _, v in points]
                plt.figure(figsize=(5, 3))
                plt.plot(x, y, marker="o")
                plt.title(f"{{TOPIC}} | {{case_name}}")
                plt.xlabel("step")
                plt.ylabel("value")
                plt.tight_layout()
                plt.savefig(out)
                plt.close()
                mode = "matplotlib"
            except ImportError:
                text_out = out.with_suffix(".txt")
                text_out.write_text("\\n".join(f"{{k}}: {{v}}" for k, v in points), encoding="utf-8")
                out = text_out
                mode = "text-fallback"
            return out, mode

        def summarize_points(points):
            values = [float(v) for _, v in points]
            return {{
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "delta": round(values[-1] - values[0], 2),
            }}

        def build_test_cases():
            cases = [
                ("baseline_uptrend", [("week1", 61), ("week2", 67), ("week3", 73), ("week4", 78)]),
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(("with_dip", [("w1", 80), ("w2", 72), ("w3", 76), ("w4", 88)]))
            if EXAMPLE_VARIANT >= 3:
                cases.append(("negative_values", [("q1", -4), ("q2", 2), ("q3", 5), ("q4", -1)]))
            if EXAMPLE_VARIANT >= 4:
                cases.append(("flat_signal", [("h1", 5), ("h2", 5), ("h3", 5), ("h4", 5)]))
            if EXAMPLE_VARIANT >= 5:
                cases.append(("with_outlier", [("d1", 11), ("d2", 10), ("d3", 40), ("d4", 12)]))
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            outputs = []
            for case_name, points in build_test_cases():
                out, mode = save_chart(points, case_name=case_name)
                summary = summarize_points(points)
                outputs.append({{"case": case_name, "output": out.name, "mode": mode, "summary": summary}})
                print(f"[{{case_name}}] 출력 파일:", out.name, "| 요약:", summary)
            return {{"variant": EXAMPLE_VARIANT, "case_count": len(outputs), "outputs": outputs}}
        """

    if template == "data_preprocess":
        return """
        from datetime import datetime

        def parse_amount(raw):
            if raw is None:
                return None
            text = str(raw).strip().replace(",", "")
            if not text:
                return None
            try:
                return float(text)
            except ValueError:
                return None

        def parse_date(raw):
            text = str(raw).strip()
            if not text:
                return None
            try:
                return datetime.strptime(text, "%Y-%m-%d")
            except ValueError:
                return None

        def clean_rows(rows):
            cleaned = []
            rejected = []
            for idx, row in enumerate(rows, start=1):
                text = str(row.get("text", "")).strip().lower()
                amount = parse_amount(row.get("amount"))
                when = parse_date(row.get("date"))
                if not text or amount is None or when is None:
                    rejected.append(
                        {
                            "row": idx,
                            "text": row.get("text"),
                            "amount": row.get("amount"),
                            "date": row.get("date"),
                        }
                    )
                    continue
                cleaned.append({"text": text, "amount": amount, "month": when.month})
            return cleaned, rejected

        def summarize(rows):
            if not rows:
                return {"rows": 0, "total": 0.0, "avg": 0.0, "min": None, "max": None}
            total = round(sum(r["amount"] for r in rows), 2)
            avg = round(total / len(rows), 2)
            min_amount = round(min(r["amount"] for r in rows), 2)
            max_amount = round(max(r["amount"] for r in rows), 2)
            return {"rows": len(rows), "total": total, "avg": avg, "min": min_amount, "max": max_amount}

        def build_test_cases():
            cases = [
                (
                    "baseline",
                    [
                        {"text": "  GPU Server  ", "amount": "1200", "date": "2026-03-01"},
                        {"text": "Monitoring  ", "amount": "450", "date": "2026-03-12"},
                    ],
                ),
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    (
                        "zero_and_spaces",
                        [
                            {"text": "  cache  ", "amount": "0", "date": "2026-03-20"},
                            {"text": "  API Gateway ", "amount": "99.5", "date": "2026-03-21"},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    (
                        "invalid_rows",
                        [
                            {"text": "STT", "amount": "300", "date": "2026-03-10"},
                            {"text": "", "amount": "180", "date": "2026-03-11"},
                            {"text": "TTS", "amount": "not-number", "date": "2026-03-12"},
                            {"text": "Batch", "amount": "200", "date": "2026/03/13"},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    (
                        "signed_amounts",
                        [
                            {"text": "refund", "amount": "-120", "date": "2026-02-01"},
                            {"text": "usage", "amount": "320", "date": "2026-02-02"},
                            {"text": "credit", "amount": "-40", "date": "2026-02-03"},
                        ],
                    )
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    (
                        "mixed_months",
                        [
                            {"text": "alpha", "amount": "1,200", "date": "2026-01-05"},
                            {"text": "beta", "amount": "860.75", "date": "2026-02-11"},
                            {"text": "gamma", "amount": "420", "date": "2026-02-17"},
                            {"text": "delta", "amount": "1040", "date": "2026-03-09"},
                        ],
                    )
                )
            return cases

        def main():
            print("오늘 주제:", TOPIC)
            results = []
            for case_name, raw in build_test_cases():
                cleaned, rejected = clean_rows(raw)
                report = summarize(cleaned)
                report.update(
                    {
                        "case": case_name,
                        "rejected_rows": len(rejected),
                        "months": sorted({row["month"] for row in cleaned}),
                    }
                )
                results.append(report)
                print(f"[{case_name}] 정제 데이터:", cleaned)
                print(f"[{case_name}] 제외 데이터:", rejected)
                print(f"[{case_name}] 요약:", report)

            total_valid = sum(item["rows"] for item in results)
            total_rejected = sum(item["rejected_rows"] for item in results)
            return {"variant": EXAMPLE_VARIANT, "case_count": len(results), "valid_rows": total_valid, "rejected_rows": total_rejected}
        """

    if template == "ml":
        return """
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
        """

    if template == "deep_learning":
        return """
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
        """

    if template == "nlp":
        return """
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
            text = re.sub(r"\\s+", " ", str(text)).strip().lower()
            text = re.sub(r"[^0-9a-zA-Z가-힣\\s.!?]", " ", text)
            text = re.sub(r"\\s+", " ", text).strip()
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
        """

    if template == "speech":
        return """
        import math

        def resolve_mode():
            if any(k in TOPIC for k in ["NLP/STT/TTS 개요", "음성 AI 개요"]):
                return "overview"
            if any(k in TOPIC for k in ["STT 파이프라인", "STT 데이터 라벨링", "발화/화자 특성 이해", "음성 데이터 구조 이해"]):
                return "data_prep"
            if any(k in TOPIC for k in ["오디오 전처리", "STT 전처리/학습"]):
                return "preprocess"
            if any(k in TOPIC for k in ["특징 추출", "음성 품질 평가"]):
                return "feature_model"
            if any(k in TOPIC for k in ["TTS 파이프라인", "TTS 전처리/학습"]):
                return "tts_model"
            if "모델 추론 및 튜닝" in TOPIC:
                return "tuning"
            if "실전 음성 모델 데모" in TOPIC:
                return "practice_demo"
            return "speech_general"

        def build_test_cases():
            rows = [
                {
                    "id": "utt1",
                    "format": "wav",
                    "sample_rate": 16000,
                    "seconds": 1.2,
                    "freq_hz": 220,
                    "amplitude": 0.8,
                    "snr_db": 22.4,
                    "label": "hello ai",
                    "speaker": "spk_a",
                },
                {
                    "id": "utt2",
                    "format": "mp3",
                    "sample_rate": 22050,
                    "seconds": 1.8,
                    "freq_hz": 330,
                    "amplitude": 0.6,
                    "snr_db": 14.1,
                    "label": "speech demo",
                    "speaker": "spk_b",
                },
            ]
            if EXAMPLE_VARIANT >= 2:
                rows.append(
                    {
                        "id": "utt3",
                        "format": "wav",
                        "sample_rate": 8000,
                        "seconds": 2.2,
                        "freq_hz": 180,
                        "amplitude": 0.7,
                        "snr_db": 10.2,
                        "label": "noisy sample",
                        "speaker": "spk_a",
                    }
                )
            if EXAMPLE_VARIANT >= 3:
                rows.append(
                    {
                        "id": "utt4",
                        "format": "wav",
                        "sample_rate": 44100,
                        "seconds": 0.7,
                        "freq_hz": 410,
                        "amplitude": 0.9,
                        "snr_db": 18.0,
                        "label": "short clip",
                        "speaker": "spk_c",
                    }
                )
            if EXAMPLE_VARIANT >= 4:
                rows.append(
                    {
                        "id": "utt5",
                        "format": "flac",
                        "sample_rate": 16000,
                        "seconds": 2.6,
                        "freq_hz": 260,
                        "amplitude": 0.5,
                        "snr_db": 12.5,
                        "label": "tts target",
                        "speaker": "spk_d",
                    }
                )
            if EXAMPLE_VARIANT >= 5:
                rows.append(
                    {
                        "id": "utt6",
                        "format": "wav",
                        "sample_rate": 12000,
                        "seconds": 3.1,
                        "freq_hz": 140,
                        "amplitude": 0.4,
                        "snr_db": 8.8,
                        "label": "edge noisy",
                        "speaker": "spk_e",
                    }
                )
            return rows

        def generate_wave(sample_rate, seconds, freq_hz, amplitude):
            size = max(16, int(sample_rate * min(seconds, 0.2)))
            signal = []
            for i in range(size):
                t = i / sample_rate
                v = amplitude * math.sin(2 * math.pi * freq_hz * t)
                signal.append(v)
            return signal

        def segment_signal(signal, segment_size):
            chunks = []
            i = 0
            while i < len(signal):
                chunks.append(signal[i : i + segment_size])
                i += segment_size
            return chunks

        def moving_average_denoise(signal, radius=1):
            out = []
            for i in range(len(signal)):
                start = max(0, i - radius)
                end = min(len(signal), i + radius + 1)
                win = signal[start:end]
                out.append(sum(win) / len(win))
            return out

        def resample_linear(signal, src_rate, dst_rate):
            if src_rate == dst_rate or not signal:
                return list(signal)
            out_len = max(1, int(len(signal) * dst_rate / src_rate))
            out = []
            for i in range(out_len):
                pos = i * (len(signal) - 1) / max(1, out_len - 1)
                left = int(math.floor(pos))
                right = min(len(signal) - 1, left + 1)
                alpha = pos - left
                out.append(signal[left] * (1 - alpha) + signal[right] * alpha)
            return out

        def spectrum_energy(signal, bins=16):
            if not signal:
                return [0.0] * bins
            chunk = max(1, len(signal) // bins)
            out = []
            for i in range(bins):
                seg = signal[i * chunk : (i + 1) * chunk]
                if not seg:
                    out.append(0.0)
                else:
                    out.append(sum(abs(v) for v in seg) / len(seg))
            return out

        def mel_scale(freq_hz):
            return 2595.0 * math.log10(1.0 + freq_hz / 700.0)

        def mel_bins(sample_rate, bins=8):
            nyq = sample_rate / 2.0
            step = nyq / bins
            return [round(mel_scale((i + 1) * step), 2) for i in range(bins)]

        def mfcc_like(energies):
            if not energies:
                return []
            return [round(math.log(e + 1e-6), 4) for e in energies[:13]]

        def classify_speech_quality(snr_db):
            if snr_db >= 20:
                return "clean"
            if snr_db >= 12:
                return "mid"
            return "noisy"

        def asr_stub(text):
            return text.upper()

        def tts_stub(text, sample_rate):
            return {"chars": len(text), "target_sr": sample_rate, "voice": "korean-neutral"}

        def ctc_align_stub(text):
            # CTC 개념 데모: 반복 문자 병합 + blank 제거를 단순화해 표현
            collapsed = []
            prev = None
            for ch in text:
                if ch == "_":
                    prev = ch
                    continue
                if ch != prev:
                    collapsed.append(ch)
                prev = ch
            return "".join(collapsed)

        def whisper_stub(text):
            # Whisper 계열 동작 개념 데모(실제 모델 추론 아님)
            return {"transcript": text.lower(), "confidence": round(0.78 + EXAMPLE_VARIANT * 0.03, 3)}

        def g2p_stub(text):
            # 한국어 발음열 변환의 축약 데모
            normalized = text.replace(" ", "")
            return [ch for ch in normalized if ch.strip()]

        def tts_model_cards():
            return [
                {"name": "Tacotron", "strength": "자연스러운 멜 예측", "weakness": "추론 속도"},
                {"name": "FastSpeech", "strength": "빠른 추론", "weakness": "프로소디 제어 난이도"},
                {"name": "VITS", "strength": "고품질 end-to-end", "weakness": "학습 안정성 관리"},
            ]

        def service_blueprint():
            return {
                "ingest": "audio upload / stream",
                "preprocess": "resample + denoise + segment",
                "features": "spectrogram + mel + mfcc",
                "model": "ASR or TTS or classification",
                "serving": "API + monitoring + metadata logging",
            }

        def analyze_rows():
            rows = build_test_cases()
            analyzed = []
            format_count = {}
            speaker_count = {}
            for row in rows:
                signal = generate_wave(row["sample_rate"], row["seconds"], row["freq_hz"], row["amplitude"])
                seg_size = max(8, len(signal) // 4)
                segments = segment_signal(signal, seg_size)
                denoised = moving_average_denoise(signal, radius=1)
                resampled = resample_linear(denoised, row["sample_rate"], 16000)
                spec = spectrum_energy(resampled, bins=16)
                mel = mel_bins(16000, bins=8)
                mfcc = mfcc_like(spec)
                quality = classify_speech_quality(row["snr_db"])
                analyzed_row = {
                    "id": row["id"],
                    "format": row["format"],
                    "sample_rate": row["sample_rate"],
                    "seconds": row["seconds"],
                    "label": row["label"],
                    "speaker": row["speaker"],
                    "segments": len(segments),
                    "quality": quality,
                    "spectrogram_bins": len(spec),
                    "mel_bins": mel[:4],
                    "mfcc_head": mfcc[:5],
                    "asr_text": asr_stub(row["label"]),
                    "tts_meta": tts_stub(row["label"], 16000),
                }
                analyzed.append(analyzed_row)
                format_count[row["format"]] = format_count.get(row["format"], 0) + 1
                speaker_count[row["speaker"]] = speaker_count.get(row["speaker"], 0) + 1
            return {
                "rows": analyzed,
                "format_count": format_count,
                "speaker_count": speaker_count,
                "avg_seconds": round(sum(r["seconds"] for r in rows) / len(rows), 3),
                "avg_sample_rate": int(sum(r["sample_rate"] for r in rows) / len(rows)),
            }

        def build_mode_summary(mode, report):
            if mode == "overview":
                return {
                    "stt_tts_concepts": ["STT(음성→텍스트)", "TTS(텍스트→음성)", "음성비서/콜센터/자막/낭독"],
                    "service": service_blueprint(),
                    "sample_count": len(report["rows"]),
                }
            if mode == "data_prep":
                return {
                    "data_prep": ["음성 수집", "스크립트 정렬", "발화 단위 관리", "화자 정보 관리", "데이터 증강"],
                    "format_count": report["format_count"],
                    "speaker_count": report["speaker_count"],
                }
            if mode == "preprocess":
                return {
                    "pipeline": ["파일 로딩", "구간 분할", "잡음 제거", "샘플레이트 변환", "Spectrogram/Mel"],
                    "avg_sample_rate": report["avg_sample_rate"],
                    "avg_seconds": report["avg_seconds"],
                }
            if mode == "feature_model":
                return {
                    "feature_stack": ["waveform", "STFT", "Mel-Spectrogram", "MFCC", "발음-음향 특징 관계"],
                    "quality_distribution": {
                        "clean": sum(1 for r in report["rows"] if r["quality"] == "clean"),
                        "mid": sum(1 for r in report["rows"] if r["quality"] == "mid"),
                        "noisy": sum(1 for r in report["rows"] if r["quality"] == "noisy"),
                    },
                    "service": service_blueprint(),
                }
            if mode == "tts_model":
                return {
                    "tts_flow": ["텍스트→발음열", "음향모델", "보코더"],
                    "g2p_preview": g2p_stub("한국어 tts 실습"),
                    "models": tts_model_cards(),
                }
            if mode == "tuning":
                ctc_preview = ctc_align_stub("hh__ee_ll_ll_oo")
                whisper_preview = whisper_stub("안녕하세요 STT 모델 테스트")
                return {
                    "stt_model_concepts": ["음성→텍스트 구조", "음향모델/언어모델", "CTC", "Whisper", "한국어 STT 고려사항"],
                    "ctc_demo": ctc_preview,
                    "whisper_demo": whisper_preview,
                    "korean_stt_checks": ["받침/연음", "외래어", "숫자/기호 읽기"],
                }
            if mode == "practice_demo":
                return {
                    "stt_practice": ["오픈소스 STT 사용", "음성→텍스트 추출", "구간별 자막 생성", "STT 성능 확인"],
                    "tts_practice": ["텍스트→음성 변환", "톤/속도 조절", "샘플 문장 낭독", "한국어 TTS 실습"],
                    "service": service_blueprint(),
                }
            return {"avg_seconds": report["avg_seconds"], "formats": report["format_count"]}

        def main():
            print("오늘 주제:", TOPIC)
            mode = resolve_mode()
            report = analyze_rows()
            summary = build_mode_summary(mode, report)
            print("모드:", mode)
            print("요약:", summary)
            return {
                "variant": EXAMPLE_VARIANT,
                "mode": mode,
                "sample_count": len(report["rows"]),
                "summary": summary,
            }
        """

    if template == "prompt":
        return """
        def build_prompt(role, task, output_format):
            return (
                f"[ROLE] {role}\\n"
                f"[TASK] {task}\\n"
                f"[FORMAT] {output_format}\\n"
                "[RULE] 근거 없는 내용은 '확인 필요'라고 표시"
            )

        def lint_prompt(prompt):
            required = ["[ROLE]", "[TASK]", "[FORMAT]", "[RULE]"]
            missing = [tag for tag in required if tag not in prompt]
            return {"missing": missing, "is_valid": len(missing) == 0}

        def main():
            print("오늘 주제:", TOPIC)
            prompt = build_prompt("IT 튜터", "RAG를 3줄로 설명", "번호 목록")
            lint = lint_prompt(prompt)
            print(prompt)
            print("프롬프트 검사:", lint)
            return lint
        """

    if template == "langchain":
        return """
        def step_collect(question):
            return {"question": question, "context": []}

        def step_retrieve(state):
            state["context"] = [
                "체인은 여러 단계를 연결한다",
                "도구 호출 전 입력 검증이 중요하다",
            ]
            return state

        def step_answer(state):
            context = " / ".join(state["context"])
            return {"answer": f"질문: {state['question']} | 근거: {context}", "steps": 3}

        def main():
            print("오늘 주제:", TOPIC)
            s1 = step_collect("체인 설계의 핵심이 뭐야?")
            s2 = step_retrieve(s1)
            report = step_answer(s2)
            print("체인 실행 결과:", report)
            return report
        """

    if template == "rag":
        return """
        def tokenize(text):
            return [t.lower() for t in text.replace(",", " ").replace(".", " ").split() if t]

        def retrieve(question, docs, top_k=2):
            q = set(tokenize(question))
            scored = []
            for doc in docs:
                overlap = len(q & set(tokenize(doc["text"])))
                if overlap > 0:
                    scored.append({"id": doc["id"], "text": doc["text"], "score": overlap})
            scored.sort(key=lambda x: x["score"], reverse=True)
            return scored[:top_k]

        def answer(question, hits):
            if not hits:
                return {"answer": "관련 문서를 찾지 못했습니다.", "citations": []}
            citations = [f"doc{h['id']}" for h in hits]
            evidence = " | ".join(h["text"] for h in hits)
            return {"answer": f"질문: {question} -> {evidence}", "citations": citations}

        def main():
            print("오늘 주제:", TOPIC)
            docs = [
                {"id": 1, "text": "RAG는 검색 결과를 근거로 답한다"},
                {"id": 2, "text": "벡터 인덱스는 유사도 검색 속도를 높인다"},
                {"id": 3, "text": "프롬프트 템플릿은 출력 형식을 고정한다"},
            ]
            question = "RAG 답변 근거를 어떻게 확보하나요"
            hits = retrieve(question, docs)
            report = answer(question, hits)
            print("검색 히트:", [h["id"] for h in hits])
            print("응답:", report)
            return report
        """

    if template == "llm_gen":
        return """
        VOCAB = ["정확성", "요약", "근거", "응답", "검증", "안전", "JSON", "맥락", "추론", "서비스"]
        KNOWLEDGE_TERMS = {
            "llm", "transformer", "token", "context", "temperature", "topk", "topp",
            "요약", "질의응답", "번역", "문서", "코드", "분류", "추출", "json",
            "api", "cloud", "local", "security", "cost", "performance"
        }

        def resolve_mode():
            if "LLM 개요" in TOPIC:
                return "overview"
            if "토큰/컨텍스트 이해" in TOPIC:
                return "token_context"
            if "생성 파라미터" in TOPIC:
                return "generation_params"
            if "프롬프트 기반 생성" in TOPIC:
                return "prompting"
            if "요약/분류/추출" in TOPIC:
                return "task_types"
            if "대화형 응답 설계" in TOPIC:
                return "chatbot"
            if "안전성/환각 관리" in TOPIC:
                return "safety"
            if "도메인 적용 시나리오" in TOPIC:
                return "deployment_modes"
            if "API 연동 실습" in TOPIC:
                return "api_practice"
            if "Agent 시스템 통합 구현" in TOPIC:
                return "agent_integration"
            return "llm_general"

        def build_prompt_cases():
            cases = [
                "LLM의 정의를 2문장으로 설명해줘",
                "고객 문의 답변 초안을 3문장으로 작성해줘",
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append("다음 회의록을 요약해줘: 모델 비용, 지연, 보안 이슈를 논의했다.")
            if EXAMPLE_VARIANT >= 3:
                cases.append("환불 정책을 묻는 사용자에게 챗봇 응답을 작성해줘")
            if EXAMPLE_VARIANT >= 4:
                cases.append("문서에서 날짜, 담당자, 우선순위를 JSON으로 추출해줘")
            if EXAMPLE_VARIANT >= 5:
                cases.append("입력 문자열 길이를 계산하는 Python 함수를 생성해줘")
            return cases

        def build_generation_config():
            return {
                "temperature": round(0.35 + EXAMPLE_VARIANT * 0.15, 2),
                "top_k": 3 + EXAMPLE_VARIANT,
                "top_p": min(0.98, round(0.72 + EXAMPLE_VARIANT * 0.05, 2)),
                "max_tokens": 120 + EXAMPLE_VARIANT * 20,
                "context_limit": 6 + EXAMPLE_VARIANT,
            }

        def tokenize(text):
            cleaned = str(text).replace(",", " ").replace(".", " ").replace("/", " ").lower()
            return [tok for tok in cleaned.split() if tok]

        def context_window(tokens, limit):
            if limit <= 0:
                return []
            return tokens[-limit:]

        def next_token_probs(vocab, temperature):
            weighted = []
            t = max(0.1, float(temperature))
            for idx, token in enumerate(vocab):
                base = 1.0 / (idx + 2)
                weighted.append((token, base ** (1.0 / t)))
            total = sum(score for _, score in weighted) or 1.0
            return [(token, round(score / total, 4)) for token, score in weighted]

        def apply_top_k_top_p(items, top_k, top_p):
            ranked = sorted(items, key=lambda x: x[1], reverse=True)
            if top_k > 0:
                ranked = ranked[:top_k]
            selected = []
            cumulative = 0.0
            for token, prob in ranked:
                selected.append((token, prob))
                cumulative += prob
                if cumulative >= top_p:
                    break
            return selected

        def choose_next_token(filtered):
            if not filtered:
                return "응답"
            return filtered[0][0]

        def simulate_generation(prompt, cfg):
            prompt_tokens = tokenize(prompt)
            ctx = context_window(prompt_tokens, cfg["context_limit"])
            probs = next_token_probs(VOCAB, cfg["temperature"])
            filtered = apply_top_k_top_p(probs, cfg["top_k"], cfg["top_p"])
            token = choose_next_token(filtered)
            prefix = " ".join(ctx[:4]) if ctx else "입력없음"
            text = f"[SIM] {prefix} -> {token} 중심으로 답변을 생성합니다."
            if cfg["temperature"] >= 1.0 and len(prompt_tokens) > 8:
                text += " 일부 내용은 확인이 필요합니다."
            return text

        def hallucination_guard(text):
            risky_markers = ["항상", "100%", "보장", "확실히"]
            found = [m for m in risky_markers if m in text]
            unknown = []
            for tok in tokenize(text):
                if len(tok) >= 5 and tok not in KNOWLEDGE_TERMS and tok.isalpha():
                    unknown.append(tok)
                if len(unknown) >= 4:
                    break
            return {
                "risk": bool(found) or len(unknown) >= 3,
                "markers": found,
                "unknown_terms": unknown,
            }

        def build_task_outputs(prompt):
            words = tokenize(prompt)
            summary = " ".join(words[: min(8, len(words))])
            category = "고객지원" if "환불" in prompt else "일반"
            return {
                "summary": summary,
                "qa": f"Q: {prompt} / A: 핵심은 요구사항 명확화와 검증입니다.",
                "translation": f"[KR->EN] {summary}",
                "draft": f"안녕하세요. 요청하신 내용({summary})을 반영해 초안을 작성했습니다.",
                "code": "def length_of_text(text):\\n    return len(text)",
                "classification": category,
                "extraction": {"keyword_count": len(words), "first_token": words[0] if words else ""},
            }

        def deployment_options():
            return [
                {"mode": "api", "cost": "중", "latency": "낮음", "security": "중"},
                {"mode": "open_model", "cost": "중", "latency": "중", "security": "중"},
                {"mode": "cloud", "cost": "중상", "latency": "중", "security": "상"},
                {"mode": "local", "cost": "초기고", "latency": "중상", "security": "상"},
            ]

        def to_json_schema_payload(task, content):
            return {
                "task": task,
                "response": {
                    "format": "json",
                    "content": content,
                },
            }

        def handle_error(status_code):
            if status_code == 429:
                return "rate_limit_retry"
            if status_code >= 500:
                return "server_fallback"
            return "ok"

        def rule_based_reply(user_text):
            if "환불" in user_text:
                return "환불 정책 링크를 안내합니다."
            if "요약" in user_text:
                return "입력 문서의 앞부분을 기준으로 요약합니다."
            return "사전 정의된 규칙 응답입니다."

        def llm_based_reply(user_text, cfg):
            return simulate_generation(user_text, cfg)

        def build_mode_summary(mode, prompt_outputs, cfg):
            if mode == "overview":
                return {
                    "llm_core": ["LLM 정의", "Transformer", "토큰/컨텍스트", "사전학습/파인튜닝"],
                    "difference_from_nlp": ["범용 생성", "few-shot 적응", "긴 문맥 처리"],
                }
            if mode == "token_context":
                token_lengths = [len(tokenize(item["prompt"])) for item in prompt_outputs]
                return {
                    "next_token": "컨텍스트 기반 확률 예측",
                    "context_window": cfg["context_limit"],
                    "token_lengths": token_lengths,
                }
            if mode == "generation_params":
                risk_count = sum(1 for item in prompt_outputs if item["guard"]["risk"])
                return {
                    "params": {"temperature": cfg["temperature"], "top_k": cfg["top_k"], "top_p": cfg["top_p"]},
                    "hallucination_risk_count": risk_count,
                }
            if mode == "prompting":
                sample = build_task_outputs(prompt_outputs[0]["prompt"]) if prompt_outputs else {}
                return {
                    "practice": ["기본 프롬프트 생성", "문서 요약", "이메일/보고서 초안", "챗봇 응답"],
                    "sample_outputs": {"summary": sample.get("summary"), "draft": sample.get("draft")},
                }
            if mode == "task_types":
                sample = build_task_outputs(prompt_outputs[-1]["prompt"]) if prompt_outputs else {}
                return {
                    "task_types": ["요약", "질의응답", "번역", "문서 작성", "코드 생성", "분류/정보추출"],
                    "structured_output": to_json_schema_payload("extract", sample.get("extraction", {})),
                }
            if mode == "chatbot":
                user_text = prompt_outputs[-1]["prompt"] if prompt_outputs else "환불 정책을 알려줘"
                return {
                    "rule_based": rule_based_reply(user_text),
                    "llm_based": llm_based_reply(user_text, cfg),
                    "controls": ["길이", "톤", "스타일", "오류 응답 처리"],
                }
            if mode == "safety":
                risk_count = sum(1 for item in prompt_outputs if item["guard"]["risk"])
                return {
                    "limits": ["사실성 문제", "최신성 한계", "보안/개인정보", "프롬프트 민감성"],
                    "risk_count": risk_count,
                    "validation_need": "실무 적용 전 검증 필수",
                }
            if mode == "deployment_modes":
                return {
                    "modes": deployment_options(),
                    "considerations": ["비용", "성능", "보안"],
                }
            if mode == "api_practice":
                payload = to_json_schema_payload("summary", {"text": "샘플 문서"})
                return {
                    "api_flow": ["요청 구성", "응답 생성", "JSON 검증", "오류 처리"],
                    "payload_sample": payload,
                    "error_policy": {"429": handle_error(429), "500": handle_error(500)},
                }
            if mode == "agent_integration":
                user_text = prompt_outputs[0]["prompt"] if prompt_outputs else "요약 요청"
                return {
                    "workflow": ["입력 라우팅", "생성", "검증", "응답", "로그"],
                    "comparison": {
                        "rule_based": rule_based_reply(user_text),
                        "llm_based": llm_based_reply(user_text, cfg),
                    },
                }
            return {"prompt_count": len(prompt_outputs), "config": cfg}

        def main():
            print("오늘 주제:", TOPIC)
            mode = resolve_mode()
            cfg = build_generation_config()
            prompts = build_prompt_cases()

            prompt_outputs = []
            for prompt in prompts:
                text = simulate_generation(prompt, cfg)
                guard = hallucination_guard(text)
                prompt_outputs.append({"prompt": prompt, "text": text, "guard": guard})

            summary = build_mode_summary(mode, prompt_outputs, cfg)
            print("모드:", mode)
            print("요약:", summary)
            return {
                "variant": EXAMPLE_VARIANT,
                "mode": mode,
                "sample_count": len(prompts),
                "summary": summary,
            }
        """

    return """
    def solve_in_steps(task):
        return [
            f"1단계: {task} 요구사항 정리",
            "2단계: 입력 검증과 핵심 로직 분리",
            "3단계: 테스트 입력을 단계별로 확장",
        ]

    def build_test_cases():
        cases = [
            {"name": "baseline", "latency_ms": 380, "error_rate": 0.01, "coverage": 0.82},
        ]
        if EXAMPLE_VARIANT >= 2:
            cases.append({"name": "high_latency", "latency_ms": 820, "error_rate": 0.02, "coverage": 0.84})
        if EXAMPLE_VARIANT >= 3:
            cases.append({"name": "high_error", "latency_ms": 410, "error_rate": 0.09, "coverage": 0.81})
        if EXAMPLE_VARIANT >= 4:
            cases.append({"name": "low_coverage", "latency_ms": 360, "error_rate": 0.015, "coverage": 0.62})
        if EXAMPLE_VARIANT >= 5:
            cases.append({"name": "balanced", "latency_ms": 295, "error_rate": 0.008, "coverage": 0.9})
        return cases

    def evaluate_case(case):
        score = 0
        if case["latency_ms"] <= 500:
            score += 1
        if case["error_rate"] <= 0.03:
            score += 1
        if case["coverage"] >= 0.8:
            score += 1
        return {
            "name": case["name"],
            "score": score,
            "pass": score >= 2,
            "latency_ms": case["latency_ms"],
            "error_rate": case["error_rate"],
            "coverage": case["coverage"],
        }

    def main():
        print("오늘 주제:", TOPIC)
        for line in solve_in_steps(TOPIC):
            print(line)

        reports = [evaluate_case(case) for case in build_test_cases()]
        for report in reports:
            print("케이스 결과:", report)

        pass_count = sum(1 for report in reports if report["pass"])
        return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "pass_count": pass_count}
    """


def variant_brief(template: str) -> dict[str, str]:
    table: dict[str, dict[str, str]] = {
        "dev_setup": {
            "mission": "Python 인터프리터 경로와 .venv 경로를 비교해 환경 분리를 증명하세요.",
            "check": "pip 설치 로그에서 설치 경로가 .venv인지 확인하세요.",
            "challenge": "requirements.lock.txt 생성 자동화 스크립트를 추가하세요.",
            "mini": "Windows/WSL 실행 절차를 체크리스트로 통합하세요.",
            "ops": "패키지 충돌 발생 시 재설치/복구 절차를 문서화하세요.",
        },
        "variables": {
            "mission": "문자열 입력 3세트를 숫자/불리언으로 형변환해 비교하세요.",
            "check": "형변환 실패 케이스를 잡아 오류 메시지를 명확히 출력하세요.",
            "challenge": "입력/출력 문자열 포맷을 f-string으로 통일하세요.",
            "mini": "기본 문법 검증기(타입/연산자/포맷) 함수를 작성하세요.",
            "ops": "입력 검증 실패 시 기본값/재입력 정책을 정의하세요.",
        },
        "condition": {
            "mission": "if/elif/else 경계값을 5개 이상 테스트하세요.",
            "check": "잘못된 조건식 우선순위를 괄호로 바로잡아 비교하세요.",
            "challenge": "중첩 조건을 함수 분리로 리팩터링하세요.",
            "mini": "조건 분기별 실행 횟수 집계를 출력하세요.",
            "ops": "분기 규칙 변경 시 회귀 테스트 항목을 정리하세요.",
        },
        "loop": {
            "mission": "for/while 결과를 같은 입력에서 비교하세요.",
            "check": "break/continue 유무에 따른 결과 차이를 기록하세요.",
            "challenge": "중첩 반복문을 함수로 분리해 가독성을 개선하세요.",
            "mini": "실습형 문제 2개를 반복문 패턴으로 자동 채점하세요.",
            "ops": "무한루프 방지 타임아웃/카운터 정책을 정의하세요.",
        },
        "collection": {
            "mission": "list/tuple/dict/set 표현을 같은 데이터로 비교하세요.",
            "check": "슬라이싱과 컴프리헨션 결과를 테스트 케이스로 검증하세요.",
            "challenge": "자료구조 선택 기준을 함수 주석으로 명시하세요.",
            "mini": "자료구조별 성능/가독성 비교 리포트를 만드세요.",
            "ops": "데이터 구조 변경 시 역호환 체크리스트를 정의하세요.",
        },
        "function_module": {
            "mission": "기본값 인자, 가변 인자, lambda를 각각 1회 이상 사용하세요.",
            "check": "함수 입력/출력 계약을 테스트로 검증하세요.",
            "challenge": "함수형 파이프라인(map/filter 또는 lambda)을 확장하세요.",
            "mini": "작은 기능 3개를 함수 모듈로 분리해 재사용하세요.",
            "ops": "함수 변경 시 영향 범위를 문서화하고 회귀 테스트하세요.",
        },
        "module_package": {
            "mission": "random/math/datetime/os 호출 결과를 한 리포트로 묶으세요.",
            "check": "사용자 정의 모듈 import 실패/성공 케이스를 모두 확인하세요.",
            "challenge": "pip 패키지 설치 여부 점검 코드를 추가하세요.",
            "mini": "표준 라이브러리+사용자 모듈 조합 유틸리티를 완성하세요.",
            "ops": "의존성 버전 충돌 시 복구 절차를 문서화하세요.",
        },
        "file_io": {
            "mission": "텍스트/CSV 저장 후 재로드 결과를 비교하세요.",
            "check": "경로 오류와 파일 미존재 예외를 재현해 처리하세요.",
            "challenge": "파일 자동화 스크립트에 백업 단계를 추가하세요.",
            "mini": "입출력 자동화 파이프라인(읽기-가공-쓰기)을 완성하세요.",
            "ops": "파일 손상/권한 오류 시 복구 정책을 정의하세요.",
        },
        "exception": {
            "mission": "try/except/finally 동작을 케이스별로 비교하세요.",
            "check": "에러 메시지에서 원인 라인과 타입을 정확히 해석하세요.",
            "challenge": "사용자 정의 예외를 만들어 분기 처리하세요.",
            "mini": "디버깅 로그 포맷을 통일한 오류 처리기를 작성하세요.",
            "ops": "운영 장애 발생 시 에러 분류/알림 기준을 문서화하세요.",
        },
        "ml": {
            "mission": "학습 데이터에 이상치 1개를 추가하고 MAE 변화를 비교하세요.",
            "check": "baseline 대비 개선/악화 원인을 2줄로 설명하세요.",
            "challenge": "검증 데이터를 따로 두고 과적합 징후를 기록하세요.",
            "mini": "모델 버전 2개를 비교하고 채택 규칙을 코드로 만드세요.",
            "ops": "성능 저하 임계치와 롤백 조건을 정의하세요.",
        },
        "deep_learning": {
            "mission": "가중치와 bias를 2세트로 바꿔 출력 분포를 비교하세요.",
            "check": "활성화 함수 전/후 값을 표로 정리하세요.",
            "challenge": "입력 스케일 변화가 출력 안정성에 미치는 영향을 측정하세요.",
            "mini": "간단한 배치 추론 로그(입력/출력/latency)를 저장하세요.",
            "ops": "추론 실패 시 fallback 모델 호출 절차를 정의하세요.",
        },
        "rag": {
            "mission": "top_k 값을 바꿔 인용(citation) 품질 변화를 확인하세요.",
            "check": "근거 없는 문장이 섞이는 경우를 재현하고 차단 규칙을 추가하세요.",
            "challenge": "질문 재작성(query rewrite) 전/후 검색 결과를 비교하세요.",
            "mini": "검색 점수 임계치 기반 필터를 적용해 응답 품질을 높이세요.",
            "ops": "인덱스 갱신 주기와 실패 시 재시도 정책을 정하세요.",
        },
        "langchain": {
            "mission": "체인 단계 하나를 추가해 입력 검증을 자동화하세요.",
            "check": "각 단계 입력/출력을 로그로 남기고 병목을 찾으세요.",
            "challenge": "도구 호출 실패를 예외 처리해 회복 가능한 체인을 만드세요.",
            "mini": "state 객체에 trace_id를 넣고 단계별 추적 기능을 추가하세요.",
            "ops": "실패 단계 알림과 재실행 정책을 정의하세요.",
        },
        "llm_gen": {
            "mission": "temperature/top_p 조합 3개를 비교해 응답 품질을 점수화하세요.",
            "check": "환각 가능 문장에 '확인 필요' 태그를 붙이세요.",
            "challenge": "금칙어/민감어 필터를 커스터마이징하세요.",
            "mini": "입력 토큰 길이별 비용 추정기를 추가하세요.",
            "ops": "모델 장애 시 대체 모델 라우팅 규칙을 작성하세요.",
        },
        "nlp": {
            "mission": "문장 분리-토큰화-불용어 제거-벡터화(BOW/TF-IDF)를 한 파이프라인으로 실행하세요.",
            "check": "형태소/품사/개체명 결과와 텍스트 품질 이슈(빈 문장/잡음)를 함께 점검하세요.",
            "challenge": "텍스트 분류(감성/문서분류)와 유사도 계산을 동시에 리포트로 출력하세요.",
            "mini": "뉴스/리뷰 2종 데이터를 추가해 전처리/분류 성능 변화를 비교하세요.",
            "ops": "데이터 드리프트(어휘 변화) 감지 기준과 재학습 트리거를 정의하세요.",
        },
        "speech": {
            "mission": "파일 로딩-세그먼트 분할-노이즈 제거-샘플레이트 변환을 단계별로 실행하세요.",
            "check": "Spectrogram/Mel/MFCC 특징과 라벨·메타데이터 정합성을 함께 검증하세요.",
            "challenge": "ASR/TTS/음성분류 서비스 구조를 그려 입력부터 추론까지 연결하세요.",
            "mini": "오디오 포맷(wav/mp3/flac)별 품질 리포트를 CSV로 내보내세요.",
            "ops": "지연/오인식 임계치와 재시도·알림 정책을 운영 기준으로 정의하세요.",
        },
    }
    default = {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "challenge": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "mini": "미니 프로젝트 형태로 실행 로그를 구조화하세요.",
        "ops": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
    }
    return table.get(template, default)


def add_variant_tail(template: str, variant: int) -> str:
    brief = variant_brief(template)

    if variant == 1:
        return """
        if __name__ == "__main__":
            main()
        """

    if variant == 2:
        return f"""
        def extension_mission():
            return {{
                "mission": "{q(brief['mission'])}",
                "check": "{q(brief['check'])}",
                "topic": TOPIC,
            }}

        if __name__ == "__main__":
            summary = main()
            print("요약:", summary)
            print("확장 미션:", extension_mission())
        """

    if variant == 3:
        return f"""
        def self_check():
            return [
                "입력/출력 스키마를 문장으로 설명할 수 있는가?",
                "예외 입력을 최소 1개 이상 테스트했는가?",
                "결과를 재현 가능한 형태로 로그에 남겼는가?",
            ]

        def challenge_case():
            return {{
                "task": "{q(brief['challenge'])}",
                "goal": "핵심 변화 포인트를 3줄 요약",
            }}

        if __name__ == "__main__":
            summary = main()
            print("요약:", summary)
            print("자가 점검:", self_check())
            print("챌린지:", challenge_case())
        """

    if variant == 4:
        return f"""
        def mini_project_plan():
            return {{
                "scenario": "{q(brief['mini'])}",
                "steps": [
                    "1) baseline 실행",
                    "2) 개선안 적용",
                    "3) 지표/로그 비교",
                ],
                "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
            }}

        if __name__ == "__main__":
            summary = main()
            print("요약:", summary)
            print("미니 프로젝트:", mini_project_plan())
        """

    return f"""
    def ops_readiness_check():
        return {{
            "risk": "{q(brief['ops'])}",
            "monitoring": "핵심 지표를 1분 주기로 기록",
            "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
        }}

    if __name__ == "__main__":
        summary = main()
        print("요약:", summary)
        print("운영 준비 점검:", ops_readiness_check())
    """


def render_example_code(class_id: str, module: str, template: str, variant: int) -> str:
    base = dedent(build_body(template, class_id)).strip()
    tail = dedent(add_variant_tail(template, variant)).strip()
    return wrap_code(class_id, module, template, variant, base + "\n\n" + tail)


def rebuild_examples(rows: list[dict[str, str]]) -> int:
    written = 0
    for row in rows:
        class_id = row["class"]
        module = row["module"]
        subject = row["subject_name"]
        template = pick_template(module, subject)

        class_dir = class_dir_from_row(row)
        class_dir.mkdir(parents=True, exist_ok=True)

        variants = variants_for_row(row, class_dir=class_dir)
        for variant in variants:
            path = example_path(class_dir, class_id, variant)
            path.write_text(
                render_example_code(class_id, module, template, variant),
                encoding="utf-8",
                newline="\n",
            )
            written += 1

        # 레거시 기본 예제 파일명(classXXX_example.py) 정리
        legacy_example = class_dir / f"{class_id}_example.py"
        if legacy_example.exists():
            legacy_example.unlink()

    return written


def validate_examples(rows: list[dict[str, str]]) -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0

    for row in rows:
        class_id = row["class"]
        module = row["module"]
        subject = row["subject_name"]
        expected = pick_template(module, subject)
        class_dir = class_dir_from_row(row)

        for variant in variants_for_row(row, class_dir=class_dir):
            path = example_path(class_dir, class_id, variant)
            checked += 1
            if not path.exists():
                errors.append(f"{path}: missing")
                continue

            text = path.read_text(encoding="utf-8")
            if f'TOPIC = "{q(module)}"' not in text:
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
    parser = argparse.ArgumentParser(description="Rebuild example files from curriculum index.")
    parser.add_argument(
        "--subject-root",
        action="append",
        default=[],
        help="Rebuild only classes under this root folder (e.g. dataVizPrep). Can be repeated.",
    )
    args = parser.parse_args()

    roots = {item.strip() for item in args.subject_root if item.strip()}
    rows = filter_rows_by_subject_roots(read_rows(), roots)
    written = rebuild_examples(rows)
    checked, errors = validate_examples(rows)

    print(f"Rows: {len(rows)}")
    if roots:
        print(f"Subject roots: {', '.join(sorted(roots))}")
    print(f"Examples rebuilt: {written}")
    print(f"Validation checked: {checked}")
    print(f"Validation errors: {len(errors)}")
    if errors:
        print("--- errors (first 30) ---")
        for err in errors[:30]:
            print(err)


if __name__ == "__main__":
    main()
