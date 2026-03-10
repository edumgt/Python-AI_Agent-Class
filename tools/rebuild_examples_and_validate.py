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
        def tokenize(text):
            cleaned = text.replace(",", " ").replace(".", " ").replace("/", " ")
            return [tok.lower() for tok in cleaned.split() if tok]

        def top_k(tokens, k=5):
            freq = {}
            for tok in tokens:
                freq[tok] = freq.get(tok, 0) + 1
            return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:k]

        def main():
            print("오늘 주제:", TOPIC)
            text = "LLM 응답 품질은 프롬프트 구조와 검증 절차에 따라 달라진다. 응답 품질을 점검하자."
            tokens = tokenize(text)
            ranking = top_k(tokens)
            report = {"token_count": len(tokens), "top_terms": ranking}
            print("분석 리포트:", report)
            return report
        """

    if template == "speech":
        return """
        def summarize_utterances(rows):
            avg_seconds = sum(r["seconds"] for r in rows) / len(rows)
            noise_flags = [r["id"] for r in rows if r["snr_db"] < 12]
            return {
                "count": len(rows),
                "avg_seconds": round(avg_seconds, 2),
                "noisy_ids": noise_flags,
            }

        def main():
            print("오늘 주제:", TOPIC)
            rows = [
                {"id": "utt1", "seconds": 1.8, "snr_db": 15.2},
                {"id": "utt2", "seconds": 2.9, "snr_db": 10.5},
                {"id": "utt3", "seconds": 1.1, "snr_db": 18.7},
            ]
            report = summarize_utterances(rows)
            print("음성 품질 요약:", report)
            return report
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
        def build_generation_config(temp=0.5, max_tokens=180):
            return {"temperature": temp, "max_tokens": max_tokens, "top_p": 0.9}

        def simulate_generation(prompt, cfg):
            return f"[SIM] prompt={prompt} | temp={cfg['temperature']} | max_tokens={cfg['max_tokens']}"

        def safety_guard(text):
            blocked = ["개인정보", "비밀번호"]
            found = [w for w in blocked if w in text]
            return {"ok": not found, "blocked_terms": found}

        def main():
            print("오늘 주제:", TOPIC)
            cfg = build_generation_config()
            prompt = "고객문의 답변 초안을 3문장으로 작성"
            output = simulate_generation(prompt, cfg)
            guard = safety_guard(output)
            report = {"config": cfg, "guard": guard}
            print(output)
            print("안전 점검:", guard)
            return report
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
        "speech": {
            "mission": "snr 임계값을 조정해 noisy 판정 변화를 비교하세요.",
            "check": "짧은 발화/긴 발화를 분리해 전처리 전략을 달리 적용하세요.",
            "challenge": "STT 오류가 많은 구간을 규칙 기반으로 탐지하세요.",
            "mini": "발화 단위 품질 리포트를 CSV로 내보내세요.",
            "ops": "실시간 처리 지연 임계치와 경보 조건을 정의하세요.",
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
