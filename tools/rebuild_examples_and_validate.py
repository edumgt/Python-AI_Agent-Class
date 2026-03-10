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
    if "rag(retrieval-augmented generation)" in subject_text:
        return "rag"
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
        import json

        LEARNING_GOALS = [
            "원하는 결과를 얻기 위한 프롬프트 설계 능력 습득",
            "프롬프트 패턴과 전략 이해",
            "출력 품질·형식·안정성 개선 방법 습득",
            "LLM 응답 제어 기술 확보",
        ]
        BANNED_RULES = ["무조건 정답", "100% 보장", "절대 틀리지 않음"]

        def resolve_mode():
            if "프롬프트 엔지니어링 개요" in TOPIC:
                return "overview"
            if "질문 구조화" in TOPIC:
                return "structure"
            if "역할/맥락 설정" in TOPIC:
                return "role_context"
            if "출력 포맷 제어" in TOPIC:
                return "output_control"
            if "예시 기반 학습" in TOPIC:
                return "shot_learning"
            if "단계적 추론 유도" in TOPIC:
                return "reasoning"
            if "평가와 개선" in TOPIC:
                return "evaluation"
            if "자동화 프롬프트 패턴" in TOPIC:
                return "automation"
            if "도메인 템플릿 작성" in TOPIC:
                return "domain_template"
            if "실전 프롬프트 튜닝" in TOPIC:
                return "practical_tuning"
            return "prompt_general"

        def template_version():
            return f"prompt-v{EXAMPLE_VARIANT}.0"

        def build_cases():
            cases = [
                {
                    "id": "support",
                    "domain": "고객상담",
                    "role": "고객상담 매니저",
                    "goal": "환불 문의에 정책 기반 답변 제공",
                    "input_text": "배송이 8일 지연됐는데 환불 가능한가요?",
                    "tone": "친절",
                }
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    {
                        "id": "summary",
                        "domain": "문서요약",
                        "role": "문서 요약 비서",
                        "goal": "회의록 핵심 3가지 요약",
                        "input_text": "회의 내용: 비용 절감, 응답 지연 개선, 보안 점검 일정 확정",
                        "tone": "간결",
                    }
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    {
                        "id": "code",
                        "domain": "코드생성",
                        "role": "Python 튜터",
                        "goal": "문자열 길이 계산 함수 생성",
                        "input_text": "입력 문자열 길이를 반환하는 함수를 만들어줘",
                        "tone": "정확",
                    }
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    {
                        "id": "report",
                        "domain": "보고서 작성",
                        "role": "기획 리포트 작성자",
                        "goal": "주간 보고서 초안 작성",
                        "input_text": "이번 주 이슈: API 장애 2회, 복구시간 개선, 다음주 위험요소 정리",
                        "tone": "공식",
                    }
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    {
                        "id": "edu",
                        "domain": "교육 콘텐츠 생성",
                        "role": "교육 콘텐츠 설계자",
                        "goal": "초급 학습자용 퀴즈 3문항 생성",
                        "input_text": "프롬프트 엔지니어링 입문 내용을 바탕으로 퀴즈를 만들어줘",
                        "tone": "친절",
                    }
                )
            return cases

        def build_constraints(case):
            max_chars = 120 + EXAMPLE_VARIANT * 30
            constraints = [
                f"MAX_CHARS={max_chars}",
                "사실 단정 표현 최소화",
                "근거가 없으면 '확인 필요' 표기",
            ]
            if case["domain"] in {"코드생성", "보고서 작성"}:
                constraints.append("출력 항목 누락 금지")
            if EXAMPLE_VARIANT >= 4:
                constraints.append("금지 규칙 위반 문장 제거")
            return constraints

        def split_system_user_prompts(case, output_format, constraints):
            system_prompt = (
                "당신은 출력 형식을 지키는 프롬프트 실행 도우미다. "
                "금지 규칙을 위반하면 경고를 반환한다."
            )
            user_prompt = (
                f"역할={case['role']}\\n"
                f"목표={case['goal']}\\n"
                f"입력={case['input_text']}\\n"
                f"출력형식={output_format}\\n"
                f"제약={', '.join(constraints)}"
            )
            return {"system": system_prompt, "user": user_prompt}

        def build_prompt(role, goal, input_text, output_format, constraints, examples=None, style=None):
            lines = [
                f"[ROLE] {role}",
                f"[GOAL] {goal}",
                f"[INPUT] {input_text}",
                f"[FORMAT] {output_format}",
                f"[CONSTRAINTS] {'; '.join(constraints)}",
            ]
            if style:
                lines.append(f"[STYLE] {style}")
            if examples:
                lines.append("[EXAMPLES]")
                for idx, item in enumerate(examples, start=1):
                    lines.append(f"{idx}) {item}")
            return "\\n".join(lines)

        def lint_prompt(prompt_text):
            required = ["[ROLE]", "[GOAL]", "[INPUT]", "[FORMAT]", "[CONSTRAINTS]"]
            missing = [tag for tag in required if tag not in prompt_text]
            return {"is_valid": len(missing) == 0, "missing": missing}

        def build_zero_one_few_prompts(case, output_format, constraints):
            zero = build_prompt(
                role=case["role"],
                goal=case["goal"],
                input_text=case["input_text"],
                output_format=output_format,
                constraints=constraints,
                style=case["tone"],
            )
            one = build_prompt(
                role=case["role"],
                goal=case["goal"],
                input_text=case["input_text"],
                output_format=output_format,
                constraints=constraints,
                examples=["입력: 환불 문의 / 출력: 정책 조건 2개 + 안내 문장"],
                style=case["tone"],
            )
            few = build_prompt(
                role=case["role"],
                goal=case["goal"],
                input_text=case["input_text"],
                output_format=output_format,
                constraints=constraints,
                examples=[
                    "입력: 배송 지연 / 출력: 요약 + 조치",
                    "입력: 결제 오류 / 출력: 원인 + 재시도 절차",
                    "입력: 계정 문의 / 출력: 확인 정보 + 안내",
                ],
                style=case["tone"],
            )
            return [
                {"strategy": "zero-shot", "prompt": zero},
                {"strategy": "one-shot", "prompt": one},
                {"strategy": "few-shot", "prompt": few},
            ]

        def build_reasoning_prompts(case, output_format, constraints):
            baseline = build_prompt(
                role=case["role"],
                goal=case["goal"],
                input_text=case["input_text"],
                output_format=output_format,
                constraints=constraints,
                style=case["tone"],
            )
            step = baseline + "\\n[REASONING] Step-by-step으로 핵심 단계를 3개로 나눠 작성"
            cot = baseline + "\\n[REASONING] Chain-of-thought 개념에 따라 단계 요약 후 최종 답만 출력"
            return [
                {"strategy": "baseline", "prompt": baseline},
                {"strategy": "step-by-step", "prompt": step},
                {"strategy": "cot-concept", "prompt": cot},
            ]

        def parse_max_chars(constraints):
            for item in constraints:
                if item.startswith("MAX_CHARS="):
                    try:
                        return int(item.split("=", maxsplit=1)[1])
                    except ValueError:
                        return 200
            return 200

        def enforce_length(text, limit):
            if len(text) <= limit:
                return text
            if limit <= 3:
                return text[:limit]
            return text[: limit - 3] + "..."

        def enforce_banned_rules(text):
            cleaned = text
            for bad in BANNED_RULES:
                cleaned = cleaned.replace(bad, "확인 필요")
            return cleaned

        def apply_tone(text, tone):
            prefix_map = {
                "친절": "안내: ",
                "간결": "요약: ",
                "정확": "정의: ",
                "공식": "보고: ",
            }
            return prefix_map.get(tone, "") + text

        def render_output(output_format, case):
            if output_format == "JSON":
                payload = {
                    "domain": case["domain"],
                    "goal": case["goal"],
                    "answer": "핵심 항목을 조건에 맞춰 생성했습니다.",
                }
                return json.dumps(payload, ensure_ascii=False)
            if output_format == "TABLE":
                return (
                    "| 항목 | 내용 |\\n"
                    "| --- | --- |\\n"
                    f"| domain | {case['domain']} |\\n"
                    f"| goal | {case['goal']} |\\n"
                    "| answer | 조건 기반 응답 |"
                )
            return f"{case['goal']} -> {case['input_text']} 기반으로 응답을 생성했습니다."

        def simulate_response(prompt_text, case, output_format, constraints):
            lint = lint_prompt(prompt_text)
            base = render_output(output_format, case)
            if "[REASONING]" in prompt_text:
                base += " 단계1 문제정의/단계2 정보정리/단계3 출력검증."
            if "[EXAMPLES]" in prompt_text:
                base += " 예시 패턴을 반영했습니다."
            if not lint["is_valid"]:
                base = "필수 블록 누락으로 품질 저하 가능: " + ", ".join(lint["missing"])
            toned = apply_tone(base, case["tone"])
            safe = enforce_banned_rules(toned)
            limited = enforce_length(safe, parse_max_chars(constraints))
            return {"text": limited, "lint": lint}

        def check_format(response_text, output_format):
            if output_format == "JSON":
                try:
                    json.loads(response_text)
                    return True
                except json.JSONDecodeError:
                    return False
            if output_format == "TABLE":
                return "| 항목 | 내용 |" in response_text
            return len(response_text.strip()) > 0

        def evaluate_response(case, strategy, output_format, result):
            text = result["text"]
            format_ok = check_format(text, output_format)
            goal_ok = case["goal"].split()[0] in text or case["domain"] in text
            safe = all(bad not in text for bad in BANNED_RULES)
            score = int(format_ok) + int(goal_ok) + int(safe)
            return {
                "case_id": case["id"],
                "strategy": strategy,
                "format": output_format,
                "score": score,
                "format_ok": format_ok,
                "goal_ok": goal_ok,
                "safe": safe,
                "lint_ok": result["lint"]["is_valid"],
                "response": text,
            }

        def choose_output_formats(mode):
            if mode == "output_control":
                return ["TABLE", "JSON", "TEXT"]
            if EXAMPLE_VARIANT >= 4:
                return ["JSON", "TEXT"]
            return ["TEXT"]

        def build_prompt_variants(mode, case, output_format, constraints):
            if mode == "shot_learning":
                return build_zero_one_few_prompts(case, output_format, constraints)
            if mode == "reasoning":
                return build_reasoning_prompts(case, output_format, constraints)

            base_prompt = build_prompt(
                role=case["role"],
                goal=case["goal"],
                input_text=case["input_text"],
                output_format=output_format,
                constraints=constraints,
                style=case["tone"],
            )
            tuned_prompt = build_prompt(
                role=case["role"],
                goal=case["goal"],
                input_text=case["input_text"],
                output_format=output_format,
                constraints=constraints + ["불확실하면 확인 필요 표기"],
                examples=["입력과 같은 도메인의 예시를 반영"],
                style=case["tone"],
            )
            prompts = [{"strategy": "baseline", "prompt": base_prompt}]
            if EXAMPLE_VARIANT >= 2:
                prompts.append({"strategy": "tuned", "prompt": tuned_prompt})
            return prompts

        def analyze_failure_patterns(rows):
            failures = {"format": 0, "goal": 0, "safety": 0, "lint": 0}
            for row in rows:
                if not row["format_ok"]:
                    failures["format"] += 1
                if not row["goal_ok"]:
                    failures["goal"] += 1
                if not row["safe"]:
                    failures["safety"] += 1
                if not row["lint_ok"]:
                    failures["lint"] += 1
            return failures

        def summarize_mode(mode, rows, cases):
            avg_score = round(sum(row["score"] for row in rows) / max(1, len(rows)), 2)
            failures = analyze_failure_patterns(rows)
            domains = sorted({case["domain"] for case in cases})

            if mode == "overview":
                return {"learning_goals": LEARNING_GOALS, "avg_score": avg_score, "domains": domains}
            if mode == "structure":
                return {
                    "prompt_structure": ["ROLE", "GOAL", "INPUT", "FORMAT", "CONSTRAINTS"],
                    "avg_score": avg_score,
                    "failures": failures,
                }
            if mode == "role_context":
                split_sample = split_system_user_prompts(
                    cases[0], output_format="TEXT", constraints=build_constraints(cases[0])
                )
                return {
                    "system_user_split": split_sample,
                    "avg_score": avg_score,
                    "failures": failures,
                }
            if mode == "output_control":
                return {
                    "output_controls": ["표 형식", "JSON 형식", "길이 제한", "어조/문체", "금지 규칙"],
                    "format_success": sum(1 for row in rows if row["format_ok"]),
                    "total": len(rows),
                }
            if mode == "shot_learning":
                by_strategy = {}
                for row in rows:
                    by_strategy.setdefault(row["strategy"], []).append(row["score"])
                comparison = {
                    key: round(sum(vals) / len(vals), 2) for key, vals in by_strategy.items() if vals
                }
                return {"shot_comparison": comparison, "failures": failures}
            if mode == "reasoning":
                return {
                    "reasoning_methods": ["baseline", "step-by-step", "cot-concept"],
                    "avg_score": avg_score,
                    "failures": failures,
                }
            if mode == "evaluation":
                return {
                    "improvement_loop": ["실패 수집", "원인 분류", "지시 수정", "재평가"],
                    "failure_patterns": failures,
                    "avg_score": avg_score,
                }
            if mode == "automation":
                return {
                    "template_version": template_version(),
                    "automation_items": ["버전 관리", "재사용 템플릿", "테스트 케이스 자동 평가"],
                    "case_count": len(cases),
                }
            if mode == "domain_template":
                return {
                    "domains": domains,
                    "domain_tasks": ["고객상담", "문서요약", "코드생성", "보고서 작성", "교육 콘텐츠 생성"],
                    "avg_score": avg_score,
                }
            if mode == "practical_tuning":
                baseline_scores = [row["score"] for row in rows if row["strategy"] == "baseline"]
                tuned_scores = [row["score"] for row in rows if row["strategy"] != "baseline"]
                return {
                    "tuning_compare": {
                        "baseline_avg": round(sum(baseline_scores) / max(1, len(baseline_scores)), 2),
                        "improved_avg": round(sum(tuned_scores) / max(1, len(tuned_scores)), 2),
                    },
                    "production_checks": [
                        "프롬프트 버전 관리",
                        "시스템/사용자 프롬프트 분리",
                        "테스트 케이스 기반 평가",
                        "오류 응답 처리",
                    ],
                }
            return {"avg_score": avg_score, "failure_patterns": failures}

        def main():
            print("오늘 주제:", TOPIC)
            mode = resolve_mode()
            cases = build_cases()
            rows = []

            for case in cases:
                constraints = build_constraints(case)
                for output_format in choose_output_formats(mode):
                    for item in build_prompt_variants(mode, case, output_format, constraints):
                        result = simulate_response(item["prompt"], case, output_format, constraints)
                        row = evaluate_response(
                            case=case,
                            strategy=item["strategy"],
                            output_format=output_format,
                            result=result,
                        )
                        rows.append(row)

            summary = summarize_mode(mode, rows, cases)
            print("모드:", mode)
            print("요약:", summary)
            return {
                "variant": EXAMPLE_VARIANT,
                "mode": mode,
                "sample_count": len(cases),
                "result_count": len(rows),
                "template_version": template_version(),
                "summary": summary,
            }
        """

    if template == "langchain":
        return """
        import json

        CORE_COMPONENTS = [
            {"name": "Model", "role": "LLM 호출/추론 수행"},
            {"name": "PromptTemplate", "role": "변수 주입형 프롬프트 구성"},
            {"name": "Chain", "role": "단계 실행 흐름 오케스트레이션"},
            {"name": "Output Parser", "role": "문자열/JSON 구조화"},
            {"name": "Memory", "role": "대화 이력/컨텍스트 유지"},
            {"name": "Retriever", "role": "관련 문서 검색"},
            {"name": "Tool", "role": "검색/계산/API 등 외부 기능 호출"},
            {"name": "Agent", "role": "작업별 도구 선택/실행 판단"},
        ]

        def resolve_mode():
            if "LangChain 개요" in TOPIC:
                return "overview"
            if "PromptTemplate" in TOPIC:
                return "prompt_template"
            if "Model/LLM 연결" in TOPIC:
                return "components"
            if "OutputParser" in TOPIC:
                return "output_parser"
            if "Chain 구성" in TOPIC:
                return "chain_design"
            if "Memory 활용" in TOPIC:
                return "memory_chat"
            if "Tool/Agent 기초" in TOPIC:
                return "tool_agent"
            if "문서 로딩과 분할" in TOPIC:
                return "retriever_base"
            if "VectorStore 연동" in TOPIC:
                return "rag_link"
            if "실전 체인 애플리케이션" in TOPIC:
                return "practice"
            return "langchain_general"

        def build_cases():
            cases = [
                {
                    "id": "doc_summary",
                    "task": "문서 요약 체인",
                    "input": "LangChain은 체인 기반으로 LLM 앱을 구성하며 Prompt, Parser, Memory, Tool, Retriever를 연결한다.",
                    "session_id": "s1",
                    "output_format": "TEXT",
                }
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    {
                        "id": "qa_chain",
                        "task": "질의응답 체인",
                        "input": "PromptTemplate는 왜 재사용성이 중요한가?",
                        "session_id": "s2",
                        "output_format": "TEXT",
                    }
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    {
                        "id": "chatbot",
                        "task": "간단한 챗봇",
                        "input": "이전 대화 맥락을 기억하면서 답해줘",
                        "session_id": "chat-1",
                        "output_format": "TEXT",
                    }
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    {
                        "id": "external_data",
                        "task": "외부 데이터 연동",
                        "input": "환율 API를 호출해 요약해줘",
                        "session_id": "api-1",
                        "output_format": "JSON",
                    }
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    {
                        "id": "rag_flow",
                        "task": "RAG 연계",
                        "input": "Retriever와 VectorStore를 왜 함께 쓰나?",
                        "session_id": "rag-1",
                        "output_format": "JSON",
                    }
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    {
                        "id": "langgraph_flow",
                        "task": "LangGraph 상태 흐름",
                        "input": "질문 유형에 따라 분기/재시도를 적용해줘",
                        "session_id": "graph-1",
                        "output_format": "JSON",
                    }
                )
            if EXAMPLE_VARIANT >= 5:
                cases.append(
                    {
                        "id": "langsmith_trace",
                        "task": "LangSmith 추적",
                        "input": "실행 로그와 품질 지표를 추적해줘",
                        "session_id": "trace-1",
                        "output_format": "JSON",
                    }
                )
            return cases

        def tokenize(text):
            cleaned = str(text).replace(",", " ").replace(".", " ").replace("/", " ").replace("?", " ").lower()
            return [tok for tok in cleaned.split() if tok]

        def build_prompt_template(mode):
            if mode == "prompt_template":
                return (
                    "역할: {role}\\n"
                    "목표: {goal}\\n"
                    "입력: {user_input}\\n"
                    "출력형식: {output_format}\\n"
                    "제약: 핵심 3줄, 근거 없으면 '확인 필요' 표기"
                )
            return (
                "task={task}\\n"
                "input={user_input}\\n"
                "context={context}\\n"
                "format={output_format}"
            )

        def render_prompt(case, mode, context):
            template = build_prompt_template(mode)
            role = "LangChain 엔지니어"
            goal = "체인 기반으로 안정적인 LLM 응답 생성"
            return template.format(
                role=role,
                goal=goal,
                task=case["task"],
                user_input=case["input"],
                context=context,
                output_format=case["output_format"],
            )

        def model_stub(prompt, temperature=0.35):
            head = " ".join(tokenize(prompt)[:12])
            stability = "stable" if temperature < 0.5 else "diverse"
            return f"{stability} output: {head}"

        def transform_input(text):
            tokens = tokenize(text)
            return " ".join(tokens[: min(14, len(tokens))])

        def single_chain(case, mode):
            prompt = render_prompt(case, mode, context="none")
            raw = model_stub(prompt, temperature=0.25)
            return {"pattern": "single", "prompt": prompt, "raw": raw}

        def sequential_chain(case, mode):
            normalized = transform_input(case["input"])
            prompt = render_prompt({**case, "input": normalized}, mode, context="normalized")
            raw = model_stub(prompt, temperature=0.4)
            return {"pattern": "sequential", "normalized": normalized, "prompt": prompt, "raw": raw}

        def parse_output(raw_text, output_format):
            if output_format == "JSON":
                try:
                    return {"ok": True, "data": json.loads(raw_text)}
                except json.JSONDecodeError:
                    return {"ok": False, "data": {"message": raw_text, "fallback": True}}
            return {"ok": True, "data": {"text": raw_text}}

        def to_json_text(case, raw):
            payload = {
                "task": case["task"],
                "summary": raw,
                "session": case["session_id"],
            }
            return json.dumps(payload, ensure_ascii=False)

        def append_memory(store, session_id, user_msg, assistant_msg):
            history = store.setdefault(session_id, [])
            history.append({"user": user_msg, "assistant": assistant_msg})
            if len(history) > 4:
                del history[:-4]
            return history

        def memory_chat(case, memory_store):
            history = memory_store.get(case["session_id"], [])
            recent = " / ".join(item["user"] for item in history[-2:]) if history else "none"
            prompt = render_prompt(case, mode="memory_chat", context=recent)
            raw = model_stub(prompt, temperature=0.3)
            append_memory(memory_store, case["session_id"], case["input"], raw)
            return {"history_size": len(memory_store.get(case["session_id"], [])), "raw": raw, "context": recent}

        def split_documents(text, chunk_size):
            tokens = tokenize(text)
            if not tokens:
                return []
            chunks = []
            step = max(4, chunk_size)
            for idx in range(0, len(tokens), step):
                chunks.append(" ".join(tokens[idx : idx + step]))
            return chunks

        def retrieve_chunks(query, chunks, top_k=2):
            query_tokens = set(tokenize(query))
            scored = []
            for chunk in chunks:
                overlap = len(query_tokens & set(tokenize(chunk)))
                if overlap > 0:
                    scored.append({"chunk": chunk, "score": overlap})
            scored.sort(key=lambda item: item["score"], reverse=True)
            if not scored and chunks:
                scored.append({"chunk": chunks[0], "score": 0})
            return scored[:top_k]

        def rag_chain(query, source_text):
            chunks = split_documents(source_text, chunk_size=10 + EXAMPLE_VARIANT)
            hits = retrieve_chunks(query, chunks, top_k=2)
            evidence = " | ".join(item["chunk"] for item in hits)
            prompt = f"question={query}\\nevidence={evidence}\\nanswer in json"
            raw = model_stub(prompt, temperature=0.22)
            return {"chunks": len(chunks), "hits": hits, "raw": raw}

        def tool_search(query, knowledge_base):
            q = set(tokenize(query))
            hits = []
            for doc in knowledge_base:
                score = len(q & set(tokenize(doc)))
                if score > 0:
                    hits.append({"doc": doc, "score": score})
            hits.sort(key=lambda item: item["score"], reverse=True)
            return hits[:2]

        def tool_calculate(expression):
            expr = expression.replace(" ", "")
            if "+" in expr:
                left, right = expr.split("+", maxsplit=1)
                if left.isdigit() and right.isdigit():
                    return int(left) + int(right)
            if "*" in expr:
                left, right = expr.split("*", maxsplit=1)
                if left.isdigit() and right.isdigit():
                    return int(left) * int(right)
            return "unsupported_expression"

        def tool_api(endpoint, payload):
            return {
                "endpoint": endpoint,
                "status": 200,
                "latency_ms": 35 + len(str(payload)),
                "payload": payload,
            }

        def run_agent(task, knowledge_base):
            if "검색" in task or "찾아" in task:
                result = {"tool": "search", "data": tool_search(task, knowledge_base)}
            elif "계산" in task or "+" in task or "*" in task:
                result = {"tool": "calculator", "data": tool_calculate(task.replace("계산", "").strip())}
            else:
                result = {"tool": "api", "data": tool_api("/v1/mock", {"task": task})}

            cautions = []
            if EXAMPLE_VARIANT >= 4:
                cautions.append("단순 질문은 Agent 대신 고정 체인으로 처리 가능")
            if EXAMPLE_VARIANT >= 5:
                cautions.append("Tool 호출 실패 시 fallback 경로를 먼저 정의")
            return {"result": result, "cautions": cautions}

        def langgraph_workflow(case):
            # 상태 기반 그래프 흐름을 간단한 규칙형으로 시뮬레이션
            state = {"intent": "general", "retry": 0, "route": "direct", "status": "ok"}
            text = case["input"]
            if "분기" in text or "유형" in text:
                state["intent"] = "routing"
                state["route"] = "classifier -> worker"
            if "재시도" in text or "retry" in text.lower():
                state["retry"] = 1 if EXAMPLE_VARIANT < 5 else 2
                state["status"] = "recovered"
            return state

        def langsmith_observe(case, bundle):
            # LangSmith 추적 항목과 유사한 구조(입력/출력/지연/오류)를 생성
            latency_ms = 42 + len(case["input"]) + EXAMPLE_VARIANT * 3
            error_count = 0
            if bundle.get("external_status", 200) != 200:
                error_count += 1
            return {
                "trace_name": f"trace-{case['id']}",
                "inputs_logged": True,
                "outputs_logged": True,
                "latency_ms": latency_ms,
                "error_count": error_count,
            }

        def practice_bundle(case, memory_store, knowledge_base):
            summary_case = {**case, "task": "문서 요약 체인"}
            qa_case = {**case, "task": "질의응답 체인"}
            chat_case = {**case, "task": "간단한 챗봇"}
            api_case = {**case, "task": "외부 데이터 연동"}

            summary_result = sequential_chain(summary_case, mode="practice")
            qa_result = rag_chain(qa_case["input"], "LangChain 체인은 단계 실행과 검색 근거 결합을 지원한다.")
            chat_result = memory_chat(chat_case, memory_store)
            api_result = tool_api("/v1/external", {"query": api_case["input"]})
            graph_result = langgraph_workflow(case)
            trace_result = langsmith_observe(case, {"external_status": api_result["status"]})
            return {
                "summary_chain": summary_result["pattern"],
                "qa_hits": len(qa_result["hits"]),
                "chat_history": chat_result["history_size"],
                "external_status": api_result["status"],
                "graph_route": graph_result["route"],
                "graph_retry": graph_result["retry"],
                "trace_latency_ms": trace_result["latency_ms"],
                "trace_errors": trace_result["error_count"],
            }

        def execute_case(case, mode, memory_store, knowledge_base):
            if mode == "overview":
                single = single_chain(case, mode)
                return {"case": case["id"], "mode": mode, "raw": single["raw"], "steps": ["입력", "모델", "출력"]}

            if mode == "prompt_template":
                prompt = render_prompt(case, mode, context="user_context")
                return {
                    "case": case["id"],
                    "mode": mode,
                    "prompt_preview": prompt.split("\\n")[:4],
                    "variable_injection": True,
                }

            if mode == "components":
                single = single_chain(case, mode)
                return {
                    "case": case["id"],
                    "mode": mode,
                    "component_count": len(CORE_COMPONENTS),
                    "raw": single["raw"],
                }

            if mode == "output_parser":
                single = single_chain(case, mode)
                raw = to_json_text(case, single["raw"]) if case["output_format"] == "JSON" else single["raw"]
                parsed = parse_output(raw, case["output_format"])
                return {"case": case["id"], "mode": mode, "parsed_ok": parsed["ok"], "parsed": parsed["data"]}

            if mode == "chain_design":
                s = single_chain(case, mode)
                seq = sequential_chain(case, mode)
                return {
                    "case": case["id"],
                    "mode": mode,
                    "single_len": len(tokenize(s["raw"])),
                    "sequential_len": len(tokenize(seq["raw"])),
                    "flow": ["입력", "변환", "생성"],
                }

            if mode == "memory_chat":
                chat = memory_chat(case, memory_store)
                return {"case": case["id"], "mode": mode, "history_size": chat["history_size"], "context": chat["context"]}

            if mode == "tool_agent":
                agent = run_agent(case["input"], knowledge_base)
                return {"case": case["id"], "mode": mode, "tool": agent["result"]["tool"], "cautions": agent["cautions"]}

            if mode == "retriever_base":
                chunks = split_documents(case["input"], chunk_size=8 + EXAMPLE_VARIANT)
                hits = retrieve_chunks("langchain chain", chunks, top_k=2)
                return {"case": case["id"], "mode": mode, "chunk_count": len(chunks), "hit_count": len(hits)}

            if mode == "rag_link":
                rag = rag_chain(case["input"], "VectorStore와 Retriever는 RAG의 검색 품질을 결정한다.")
                return {"case": case["id"], "mode": mode, "hits": len(rag["hits"]), "chunks": rag["chunks"]}

            if mode == "practice":
                bundle = practice_bundle(case, memory_store, knowledge_base)
                return {"case": case["id"], "mode": mode, **bundle}

            default_single = single_chain(case, mode)
            return {"case": case["id"], "mode": mode, "raw": default_single["raw"]}

        def summarize_mode(mode, rows, memory_store):
            if mode == "overview":
                return {
                    "goals": [
                        "LangChain 구성요소 이해",
                        "체인 기반 LLM 앱 설계",
                        "프롬프트·메모리·도구·에이전트 연결 이해",
                        "RAG 연계 기반 확보",
                    ],
                    "architecture": ["Model", "PromptTemplate", "Chain", "OutputParser", "Memory", "Retriever", "Tool", "Agent"],
                }
            if mode == "components":
                return {"components": CORE_COMPONENTS, "count": len(CORE_COMPONENTS)}
            if mode == "prompt_template":
                return {
                    "prompt_template_usage": ["변수 주입", "템플릿 재사용", "사용자 입력 연결", "구조화 프롬프트 관리"],
                    "sample_count": len(rows),
                }
            if mode == "chain_design":
                return {
                    "chain_patterns": ["단일 체인", "순차 체인", "다단계 처리"],
                    "flow": "입력 -> 변환 -> 생성",
                }
            if mode == "output_parser":
                success = sum(1 for row in rows if row.get("parsed_ok", False))
                return {
                    "output_parser": ["문자열 파싱", "JSON 처리", "구조화 저장", "후처리 자동화"],
                    "parsed_success": success,
                    "total": len(rows),
                }
            if mode == "memory_chat":
                return {
                    "memory_points": ["대화 이력 저장", "컨텍스트 유지", "세션별 응답 관리", "챗봇 흐름 구성"],
                    "sessions": len(memory_store),
                }
            if mode == "tool_agent":
                tool_usage = {}
                for row in rows:
                    tool = row.get("tool", "none")
                    tool_usage[tool] = tool_usage.get(tool, 0) + 1
                return {
                    "tool_agent": ["검색", "계산", "API 호출", "Agent 동작/주의사항"],
                    "tool_usage": tool_usage,
                }
            if mode == "retriever_base":
                return {
                    "retriever_base": ["문서 로딩", "청크 분할", "검색"],
                    "avg_chunks": round(sum(row.get("chunk_count", 0) for row in rows) / max(1, len(rows)), 2),
                }
            if mode == "rag_link":
                return {
                    "rag_link": ["Retriever", "VectorStore", "검색근거 결합", "생성 응답"],
                    "avg_hits": round(sum(row.get("hits", 0) for row in rows) / max(1, len(rows)), 2),
                }
            if mode == "practice":
                return {
                    "practice_items": [
                        "문서 요약 체인",
                        "질의응답 체인",
                        "간단한 챗봇",
                        "외부 데이터 연동 기본 예제",
                        "LangGraph 상태 흐름 제어",
                        "LangSmith 실행 추적",
                    ],
                    "avg_trace_latency_ms": round(
                        sum(row.get("trace_latency_ms", 0) for row in rows) / max(1, len(rows)),
                        2,
                    ),
                    "result_count": len(rows),
                }
            return {"result_count": len(rows)}

        def main():
            print("오늘 주제:", TOPIC)
            mode = resolve_mode()
            cases = build_cases()
            memory_store = {}
            knowledge_base = [
                "LangChain은 체인 기반 LLM 애플리케이션 프레임워크다.",
                "Retriever는 질문과 관련된 문서를 검색한다.",
                "Agent는 Tool을 선택해 외부 기능을 호출한다.",
                "OutputParser는 JSON 구조화를 도와준다.",
            ]

            rows = []
            for case in cases:
                row = execute_case(case, mode, memory_store, knowledge_base)
                rows.append(row)

            summary = summarize_mode(mode, rows, memory_store)
            print("모드:", mode)
            print("요약:", summary)
            return {
                "variant": EXAMPLE_VARIANT,
                "mode": mode,
                "sample_count": len(cases),
                "result_count": len(rows),
                "summary": summary,
            }
        """

    if template == "rag":
        return """
        DOCUMENTS = [
            {
                "id": "D1",
                "title": "사내 보안 정책",
                "type": "PDF",
                "section": "보안",
                "text": "사내 보안 정책은 민감 데이터 조회 시 다중인증을 요구한다. 정책 위반은 보안팀 승인 절차로 처리한다.",
            },
            {
                "id": "D2",
                "title": "RAG 운영 가이드",
                "type": "TXT",
                "section": "운영",
                "text": "RAG 파이프라인은 문서 수집, 청크 분할, 임베딩 생성, 벡터 저장, 검색, 프롬프트 주입, 답변 생성 순서로 운영한다.",
            },
            {
                "id": "D3",
                "title": "고객지원 FAQ",
                "type": "HTML",
                "section": "FAQ",
                "text": "FAQ 챗봇은 환불 기준, 배송 일정, 계정 복구 질문을 자주 처리한다. 답변에는 출처 링크를 포함해야 한다.",
            },
            {
                "id": "D4",
                "title": "제품 안내 데이터",
                "type": "CSV",
                "section": "제품",
                "text": "CSV 문서에는 제품명, 가격, 업데이트일, 담당팀 메타데이터가 저장된다. 최신 컬럼 기준으로 검색 정확도를 관리한다.",
            },
            {
                "id": "D5",
                "title": "내부 회의록",
                "type": "PDF",
                "section": "회의록",
                "text": "검색 실패 사례는 query rewrite와 reranking으로 개선한다. 하이브리드 검색은 키워드와 벡터를 결합한다.",
            },
        ]

        EMBEDDING_MODELS = [
            {"name": "ko-sbert", "strength": "한국어 의미 유사도", "cost": "중"},
            {"name": "multilingual-e5", "strength": "다국어 범용성", "cost": "중상"},
            {"name": "bge-m3", "strength": "검색/재정렬 균형", "cost": "중상"},
        ]

        def resolve_mode():
            if "RAG 개요" in TOPIC:
                return "overview"
            if "문서 수집 전략" in TOPIC:
                return "pipeline"
            if "문서 청크 설계" in TOPIC:
                return "chunking"
            if "임베딩 생성" in TOPIC:
                return "embedding"
            if "벡터DB 기초" in TOPIC:
                return "vector_db"
            if "검색 품질 개선" in TOPIC:
                return "retrieval_tuning"
            if "프롬프트 결합" in TOPIC:
                return "langchain_rag"
            if "응답 검증/출처화" in TOPIC:
                return "grounding"
            if "평가 지표 설계" in TOPIC:
                return "evaluation"
            if "Agent 시스템 통합 구현" in TOPIC:
                return "practice"
            return "rag_general"

        def tokenize(text):
            cleaned = str(text).lower()
            for ch in [",", ".", "(", ")", "/", ":", ";", "-", "_", "\\n"]:
                cleaned = cleaned.replace(ch, " ")
            return [tok for tok in cleaned.split() if tok]

        def load_documents():
            docs = list(DOCUMENTS)
            if EXAMPLE_VARIANT >= 4:
                docs.append(
                    {
                        "id": "D6",
                        "title": "사내 위키 업데이트",
                        "type": "TXT",
                        "section": "위키",
                        "text": "사내 문서 Q&A 시스템은 source 반환을 기본으로 하고 근거 없는 문장은 확인 필요로 표시한다.",
                    }
                )
            if EXAMPLE_VARIANT >= 5:
                docs.append(
                    {
                        "id": "D7",
                        "title": "릴리즈 노트",
                        "type": "HTML",
                        "section": "릴리즈",
                        "text": "신규 버전은 PDF 검색과 FAQ 챗봇을 통합했고 검색 지연을 20퍼센트 줄였다.",
                    }
                )
            return docs

        def split_text_tokens(tokens, chunk_size, overlap):
            step = max(1, chunk_size - overlap)
            groups = []
            for start in range(0, len(tokens), step):
                part = tokens[start : start + chunk_size]
                if not part:
                    continue
                groups.append(part)
                if start + chunk_size >= len(tokens):
                    break
            return groups

        def build_chunks(docs, chunk_size, overlap):
            chunks = []
            for doc in docs:
                token_groups = split_text_tokens(tokenize(doc["text"]), chunk_size, overlap)
                for idx, group in enumerate(token_groups, start=1):
                    chunks.append(
                        {
                            "chunk_id": f"{doc['id']}-c{idx}",
                            "source_id": doc["id"],
                            "source_type": doc["type"],
                            "title": doc["title"],
                            "section": doc["section"],
                            "text": " ".join(group),
                            "metadata": {
                                "doc_id": doc["id"],
                                "title": doc["title"],
                                "section": doc["section"],
                                "source_type": doc["type"],
                            },
                        }
                    )
            return chunks

        def embed_text(text):
            vec = {}
            for tok in tokenize(text):
                vec[tok] = vec.get(tok, 0.0) + 1.0
            return vec

        def cosine_similarity(vec_a, vec_b):
            keys = set(vec_a) | set(vec_b)
            dot = sum(vec_a.get(k, 0.0) * vec_b.get(k, 0.0) for k in keys)
            norm_a = sum(v * v for v in vec_a.values()) ** 0.5
            norm_b = sum(v * v for v in vec_b.values()) ** 0.5
            if norm_a == 0.0 or norm_b == 0.0:
                return 0.0
            return dot / (norm_a * norm_b)

        def select_embedding_model(mode):
            if mode == "embedding":
                return EMBEDDING_MODELS[min(len(EMBEDDING_MODELS) - 1, EXAMPLE_VARIANT - 1)]
            if mode == "vector_db":
                return EMBEDDING_MODELS[2 if EXAMPLE_VARIANT >= 3 else 1]
            return EMBEDDING_MODELS[0 if EXAMPLE_VARIANT <= 2 else 1]

        def build_index(chunks, model_name):
            index = []
            for chunk in chunks:
                row = dict(chunk)
                row["embedding_model"] = model_name
                row["vector"] = embed_text(chunk["text"])
                index.append(row)
            return index

        def lexical_score(query, text):
            q_tokens = set(tokenize(query))
            if not q_tokens:
                return 0.0
            overlap = len(q_tokens & set(tokenize(text)))
            return overlap / len(q_tokens)

        def vector_search(query, index, top_k=3):
            q_vec = embed_text(query)
            scored = []
            for row in index:
                vec_score = cosine_similarity(q_vec, row["vector"])
                key_score = lexical_score(query, row["text"])
                scored.append(
                    {
                        "chunk_id": row["chunk_id"],
                        "source_id": row["source_id"],
                        "source_type": row["source_type"],
                        "title": row["title"],
                        "section": row["section"],
                        "text": row["text"],
                        "vector_score": round(vec_score, 4),
                        "keyword_score": round(key_score, 4),
                    }
                )
            scored.sort(key=lambda x: x["vector_score"], reverse=True)
            return scored[:top_k]

        def rerank_hits(query, hits):
            q_tokens = set(tokenize(query))
            reranked = []
            for item in hits:
                boost = 0.0
                if "사내" in q_tokens and item["source_id"] in {"D1", "D2", "D6"}:
                    boost += 0.08
                if "faq" in q_tokens and item["source_type"] in {"HTML", "CSV"}:
                    boost += 0.06
                if "pdf" in q_tokens and item["source_type"] == "PDF":
                    boost += 0.06
                final = item["vector_score"] + 0.2 * item["keyword_score"] + boost
                row = dict(item)
                row["rerank_score"] = round(final, 4)
                reranked.append(row)
            reranked.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
            return reranked

        def hybrid_search(query, index, top_k=3, use_rerank=False):
            candidates = vector_search(query, index, top_k=max(top_k, 6))
            merged = []
            for item in candidates:
                hybrid = 0.65 * item["vector_score"] + 0.35 * item["keyword_score"]
                row = dict(item)
                row["hybrid_score"] = round(hybrid, 4)
                merged.append(row)
            merged.sort(key=lambda x: x["hybrid_score"], reverse=True)
            if use_rerank:
                merged = rerank_hits(query, merged)
            return merged[:top_k]

        def build_prompt(query, hits):
            contexts = []
            for h in hits:
                contexts.append(f"[{h['source_id']}|{h['chunk_id']}] {h['text']}")
            context_block = "\\n".join(contexts) if contexts else "근거 문서 없음"
            return (
                "너는 사내 문서 Q&A 도우미다.\\n"
                "규칙: 근거 없는 내용은 추측하지 말고 '확인 필요'라고 답해라.\\n"
                f"질문: {query}\\n"
                f"근거:\\n{context_block}\\n"
                "출력: 핵심 답변 + 출처 목록"
            )

        def generate_answer(query, hits):
            prompt = build_prompt(query, hits)
            if not hits:
                return {
                    "answer": "검색된 근거가 부족해 확인이 필요합니다.",
                    "sources": [],
                    "source_count": 0,
                    "needs_review": True,
                    "prompt_preview": prompt.splitlines()[0],
                }
            top_titles = ", ".join(dict.fromkeys(h["title"] for h in hits[:2]))
            sources = [f"{h['source_id']}:{h['title']}" for h in hits]
            answer = f"{query}에 대한 근거 문서는 {top_titles}입니다. 주요 정책/절차를 근거로 답변했습니다."
            return {
                "answer": answer,
                "sources": sources,
                "source_count": len(sources),
                "needs_review": False,
                "prompt_preview": prompt.splitlines()[0],
            }

        def grounded_ratio(answer_text, hits):
            evidence_tokens = set()
            for h in hits:
                evidence_tokens.update(tokenize(h["text"]))
            ans_tokens = tokenize(answer_text)
            if not ans_tokens:
                return 0.0
            matched = sum(1 for tok in ans_tokens if tok in evidence_tokens)
            return round(matched / len(ans_tokens), 4)

        def eval_retrieval(expected_sources, hits):
            expected = set(expected_sources)
            found = {h["source_id"] for h in hits}
            if not expected:
                return {
                    "precision": round(1.0 if not found else 0.0, 4),
                    "recall": 1.0,
                    "matched": 0,
                }
            matched = len(expected & found)
            precision = matched / max(1, len(found))
            recall = matched / len(expected)
            return {"precision": round(precision, 4), "recall": round(recall, 4), "matched": matched}

        def eval_answer(expected_keywords, report):
            answer = report.get("answer", "").lower()
            total = max(1, len(expected_keywords))
            matched = sum(1 for kw in expected_keywords if kw.lower() in answer)
            return {
                "keyword_accuracy": round(matched / total, 4),
                "with_source": report.get("source_count", 0) > 0,
            }

        def build_cases(mode):
            cases = [
                {
                    "name": "사내QnA",
                    "query": "사내 보안 정책에서 다중인증은 언제 적용하나요?",
                    "expected_sources": ["D1"],
                    "expected_keywords": ["사내", "근거"],
                },
                {
                    "name": "FAQ봇",
                    "query": "FAQ 챗봇은 어떤 질문을 처리하나요?",
                    "expected_sources": ["D3"],
                    "expected_keywords": ["FAQ", "질문"],
                },
                {
                    "name": "PDF검색",
                    "query": "PDF 문서 기반 검색 품질을 어떻게 높이나요?",
                    "expected_sources": ["D1", "D5"],
                    "expected_keywords": ["검색", "품질"],
                },
            ]
            if EXAMPLE_VARIANT >= 2:
                cases.append(
                    {
                        "name": "파이프라인",
                        "query": "RAG 전체 파이프라인 순서를 알려줘",
                        "expected_sources": ["D2"],
                        "expected_keywords": ["파이프라인", "근거"],
                    }
                )
            if EXAMPLE_VARIANT >= 3:
                cases.append(
                    {
                        "name": "rerank",
                        "query": "검색 실패 사례를 reranking으로 개선하는 방법은?",
                        "expected_sources": ["D5"],
                        "expected_keywords": ["검색", "개선"],
                    }
                )
            if EXAMPLE_VARIANT >= 4:
                cases.append(
                    {
                        "name": "출처검증",
                        "query": "출처 없는 답변을 줄이려면 무엇이 필요한가요?",
                        "expected_sources": ["D6"],
                        "expected_keywords": ["출처", "확인"],
                    }
                )
            if mode == "overview":
                return cases[:2]
            if mode in {"embedding", "vector_db"}:
                return cases[:4]
            return cases

        def run_case(case, mode, index):
            top_k = 2 + min(2, EXAMPLE_VARIANT // 2)
            use_hybrid = mode in {"retrieval_tuning", "evaluation", "practice"}
            use_rerank = mode in {"vector_db", "retrieval_tuning", "evaluation", "practice"}
            if use_hybrid:
                hits = hybrid_search(case["query"], index, top_k=top_k, use_rerank=use_rerank)
            else:
                hits = vector_search(case["query"], index, top_k=top_k)
                if use_rerank:
                    hits = rerank_hits(case["query"], hits)[:top_k]
            report = generate_answer(case["query"], hits)
            retrieval_metrics = eval_retrieval(case["expected_sources"], hits)
            answer_metrics = eval_answer(case["expected_keywords"], report)
            ground = grounded_ratio(report.get("answer", ""), hits)
            return {
                "name": case["name"],
                "query": case["query"],
                "hit_sources": [h["source_id"] for h in hits],
                "report": report,
                "retrieval": retrieval_metrics,
                "answer": answer_metrics,
                "grounded_ratio": ground,
                "hallucination_risk": ground < 0.2 and report.get("source_count", 0) == 0,
            }

        def summarize_mode(mode, docs, chunks, rows, model_name, chunk_size, overlap):
            avg_recall = round(sum(r["retrieval"]["recall"] for r in rows) / max(1, len(rows)), 4)
            avg_answer = round(sum(r["answer"]["keyword_accuracy"] for r in rows) / max(1, len(rows)), 4)
            avg_grounded = round(sum(r["grounded_ratio"] for r in rows) / max(1, len(rows)), 4)
            with_source_count = sum(1 for r in rows if r["report"]["source_count"] > 0)

            if mode == "overview":
                return {
                    "goals": [
                        "RAG 필요성과 구조 이해",
                        "외부 문서 검색으로 답변 품질 개선",
                        "벡터DB·임베딩·검색 파이프라인 습득",
                        "사내 문서 Q&A 구현 역량 확보",
                    ],
                    "llm_limitations": ["최신 정보 반영 한계", "사내 정보 접근 한계", "근거 없는 환각 위험"],
                    "architecture": ["검색", "문맥 주입", "생성", "출처 반환"],
                }
            if mode == "pipeline":
                return {
                    "pipeline_steps": ["문서 수집", "chunking", "임베딩", "벡터 저장", "검색", "프롬프트 주입", "답변 생성"],
                    "document_count": len(docs),
                    "chunk_count": len(chunks),
                }
            if mode == "chunking":
                return {
                    "formats": ["PDF", "TXT", "HTML", "CSV"],
                    "chunking": {"chunk_size": chunk_size, "overlap": overlap},
                    "metadata": ["doc_id", "title", "section", "source_type"],
                }
            if mode == "embedding":
                return {
                    "embedding": ["임베딩 개념", "문장 의미 벡터", "cosine similarity", "모델 선택 기준"],
                    "selected_model": model_name,
                    "avg_recall": avg_recall,
                }
            if mode == "vector_db":
                return {
                    "vector_db": ["Chroma", "FAISS", "Qdrant"],
                    "indexing": "벡터 upsert + Top-K 검색",
                    "reranking": "후보 재정렬로 정답률 향상",
                    "avg_recall": avg_recall,
                }
            if mode == "retrieval_tuning":
                return {
                    "improvements": ["Top-K 조정", "reranking", "검색 실패 사례 분석"],
                    "hybrid_search": "키워드 + 벡터 결합",
                    "avg_recall": avg_recall,
                    "avg_answer_accuracy": avg_answer,
                }
            if mode == "langchain_rag":
                return {
                    "langchain_rag": ["Retriever 구성", "Prompt 문맥 주입", "검색 기반 생성", "source 반환", "hallucination 감소"],
                    "with_source_count": with_source_count,
                }
            if mode == "grounding":
                return {
                    "source_return": "doc_id:title 형식",
                    "avg_grounded_ratio": avg_grounded,
                    "hallucination_flags": sum(1 for r in rows if r["hallucination_risk"]),
                }
            if mode == "evaluation":
                return {
                    "evaluation_points": ["검색 정확도", "답변 정확도", "chunking 개선", "프롬프트 튜닝", "하이브리드 검색"],
                    "avg_recall": avg_recall,
                    "avg_answer_accuracy": avg_answer,
                    "avg_grounded_ratio": avg_grounded,
                }
            if mode == "practice":
                return {
                    "practice": ["사내 문서 질의응답", "FAQ 챗봇", "PDF 기반 검색 시스템", "출처 포함 답변 생성"],
                    "result_count": len(rows),
                    "with_source_count": with_source_count,
                }
            return {"result_count": len(rows), "avg_recall": avg_recall, "avg_answer_accuracy": avg_answer}

        def main():
            print("오늘 주제:", TOPIC)
            mode = resolve_mode()
            docs = load_documents()
            chunk_size = 8 + EXAMPLE_VARIANT
            overlap = min(3, 1 + EXAMPLE_VARIANT // 2)
            chunks = build_chunks(docs, chunk_size=chunk_size, overlap=overlap)
            model = select_embedding_model(mode)
            index = build_index(chunks, model_name=model["name"])
            cases = build_cases(mode)

            rows = []
            for case in cases:
                rows.append(run_case(case, mode, index))

            summary = summarize_mode(mode, docs, chunks, rows, model["name"], chunk_size, overlap)
            print("모드:", mode)
            print("선택 임베딩 모델:", model)
            print("요약:", summary)
            return {
                "variant": EXAMPLE_VARIANT,
                "mode": mode,
                "documents": len(docs),
                "chunks": len(chunks),
                "cases": len(cases),
                "summary": summary,
            }
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
