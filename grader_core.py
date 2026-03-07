# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
import importlib.util
import json
import math
import traceback
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import: {module_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_index_rows(index_file: Path) -> list[dict[str, str]]:
    with index_file.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    rows: list[dict[str, str]] = []
    for raw in raw_rows:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return rows


@lru_cache(maxsize=4)
def load_class_dir_map(index_file_str: str) -> dict[str, str]:
    index_file = Path(index_file_str)
    if not index_file.exists():
        return {}

    mapping: dict[str, str] = {}
    for row in read_index_rows(index_file):
        class_id = row.get("class", "").strip()
        md_rel = (row.get("md_file") or "").strip()
        if not class_id:
            continue
        if md_rel:
            mapping[class_id] = Path(md_rel).parent.as_posix()
        else:
            mapping[class_id] = class_id
    return mapping


def class_dir_from_id(root: Path, class_id: str) -> Path:
    index_file = root / "curriculum_index.csv"
    mapping = load_class_dir_map(str(index_file))
    rel_dir = mapping.get(class_id)
    if rel_dir:
        return root / rel_dir
    return root / class_id


def assignment_path(class_dir: Path, class_id: str, tier: str) -> Path:
    mapping = {
        'basic': class_dir / f'{class_id}_assignment_basic.py',
        'advanced': class_dir / f'{class_id}_assignment_advanced.py',
        'challenge': class_dir / f'{class_id}_assignment_challenge.py',
    }
    return mapping[tier]


def solution_path(class_dir: Path, class_id: str) -> Path:
    return class_dir / f'{class_id}_solution.py'


def detect_profile(module: Any) -> str:
    names = {name for name in dir(module) if callable(getattr(module, name, None))}
    if {'even_squares', 'divide', 'save_result'} <= names:
        return 'python_fundamentals'
    if {'make_plot'} <= names:
        return 'plot_generation'
    if {'make_data', 'train_and_eval'} <= names:
        return 'ml_regression'
    if {'build_df', 'save_and_load'} <= names:
        return 'dataframe_io'
    if {'build_prompt'} <= names:
        return 'prompt_template'
    return 'unknown'


def _ok(name: str, detail: str) -> CheckResult:
    return CheckResult(name, True, detail)


def _fail(name: str, detail: str) -> CheckResult:
    return CheckResult(name, False, detail)


def _safe_call(name: str, fn, *args, **kwargs):
    try:
        return True, fn(*args, **kwargs)
    except Exception as e:
        return False, f'{type(e).__name__}: {e}'


def check_python_fundamentals(module: Any, class_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    try:
        out_json = class_dir / 'outputs' / 'result.json'
        if out_json.exists():
            out_json.unlink()
    except Exception:
        pass

    ok, value = _safe_call('even_squares', module.even_squares, [1,2,3,4,5,6])
    if not ok:
        results.append(_fail('even_squares', value))
    elif value != [4, 16, 36]:
        results.append(_fail('even_squares', f'expected [4, 16, 36], got {value!r}'))
    else:
        results.append(_ok('even_squares', '짝수 필터링 + 제곱 결과가 정확합니다.'))

    ok, value = _safe_call('divide', module.divide, 10, 2)
    if not ok:
        results.append(_fail('divide', value))
    elif abs(float(value) - 5.0) > 1e-9:
        results.append(_fail('divide', f'expected 5.0, got {value!r}'))
    else:
        try:
            module.divide(10, 0)
        except ValueError:
            results.append(_ok('divide_zero', '0으로 나누기 예외 처리가 정확합니다.'))
        except Exception as e:
            results.append(_fail('divide_zero', f'ValueError expected, got {type(e).__name__}: {e}'))
        else:
            results.append(_fail('divide_zero', 'ValueError expected, but no exception was raised.'))

    payload = {'even_squares': [4, 16, 36], 'mean': 3.5}
    ok, value = _safe_call('save_result', module.save_result, payload)
    if not ok:
        results.append(_fail('save_result', value))
    else:
        out_path = Path(value)
        if not out_path.exists():
            results.append(_fail('save_result_file', f'file not found: {out_path}'))
        else:
            try:
                data = json.loads(out_path.read_text(encoding='utf-8'))
                if data != payload:
                    results.append(_fail('save_result_content', f'JSON mismatch: {data!r}'))
                else:
                    results.append(_ok('save_result', f'JSON 저장 검증 완료: {out_path.name}'))
            except Exception as e:
                results.append(_fail('save_result_content', f'JSON read failed: {type(e).__name__}: {e}'))
    return results


def check_plot_generation(module: Any, class_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    out_png = class_dir / 'outputs' / 'plot.png'
    try:
        if out_png.exists():
            out_png.unlink()
    except Exception:
        pass

    x = list(range(1, 11))
    y = [v * v for v in x]
    ok, value = _safe_call('make_plot', module.make_plot, x, y)
    if not ok:
        return [_fail('make_plot', value)]

    out_path = Path(value)
    if not out_path.exists():
        results.append(_fail('plot_file', f'file not found: {out_path}'))
        return results
    raw = out_path.read_bytes()
    if len(raw) < 16:
        results.append(_fail('plot_file', f'file too small: {len(raw)} bytes'))
    elif not raw.startswith(bytes([137,80,78,71,13,10,26,10])):
        results.append(_fail('plot_file', 'output is not a PNG signature'))
    else:
        results.append(_ok('make_plot', f'PNG 파일 생성 검증 완료: {out_path.name} ({len(raw)} bytes)'))
    return results


def check_ml_regression(module: Any, class_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    ok, value = _safe_call('make_data', module.make_data, 50, 42)
    if not ok:
        return [_fail('make_data', value)]
    try:
        X, y = value
    except Exception:
        return [_fail('make_data', f'expected tuple (X, y), got {type(value).__name__}: {value!r}')]

    shape_x = getattr(X, 'shape', None)
    shape_y = getattr(y, 'shape', None)
    if shape_x is None:
        try:
            shape_x = (len(X), len(X[0]) if len(X) else 0)
        except Exception:
            shape_x = None
    if shape_y is None:
        try:
            shape_y = (len(y),)
        except Exception:
            shape_y = None

    if not shape_x or int(shape_x[0]) != 50:
        results.append(_fail('make_data_shape', f'X row count must be 50, got {shape_x!r}'))
    else:
        results.append(_ok('make_data_shape', f'X shape={shape_x}, y shape={shape_y}'))

    ok, mse = _safe_call('train_and_eval', module.train_and_eval, X, y)
    if not ok:
        results.append(_fail('train_and_eval', mse))
        return results

    try:
        mse_value = float(mse)
    except Exception:
        results.append(_fail('train_and_eval', f'MSE must be numeric, got {mse!r}'))
        return results

    if not math.isfinite(mse_value):
        results.append(_fail('mse_value', f'MSE must be finite, got {mse_value}'))
    elif mse_value < 0:
        results.append(_fail('mse_value', f'MSE must be >= 0, got {mse_value}'))
    elif mse_value > 30:
        results.append(_fail('mse_value', f'MSE too large for sample task: {mse_value:.6f}'))
    else:
        results.append(_ok('mse_value', f'MSE 검증 통과: {mse_value:.6f}'))
    return results


def check_dataframe_io(module: Any, class_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    out_csv = class_dir / 'outputs' / 'data.csv'
    try:
        if out_csv.exists():
            out_csv.unlink()
    except Exception:
        pass

    rows = [
        {'name': 'A', 'score1': 80, 'score2': 90},
        {'name': 'B', 'score1': 75, 'score2': 60},
        {'name': 'C', 'score1': 92, 'score2': 88},
    ]
    ok, df = _safe_call('build_df', module.build_df, rows)
    if not ok:
        return [_fail('build_df', df)]

    columns = set(getattr(df, 'columns', []))
    if not {'name', 'score1', 'score2', 'total', 'average'} <= columns:
        results.append(_fail('build_df_columns', f'missing columns: expected total/average, got {sorted(columns)!r}'))
    else:
        try:
            totals = list(df['total'])
            avgs = list(df['average'])
            if totals != [170, 135, 180]:
                results.append(_fail('build_df_total', f'expected [170, 135, 180], got {totals!r}'))
            elif [round(float(v), 2) for v in avgs] != [85.0, 67.5, 90.0]:
                results.append(_fail('build_df_average', f'unexpected averages: {avgs!r}'))
            else:
                results.append(_ok('build_df', 'DataFrame 컬럼/계산 결과가 정확합니다.'))
        except Exception as e:
            results.append(_fail('build_df_values', f'{type(e).__name__}: {e}'))

    ok, df2 = _safe_call('save_and_load', module.save_and_load, df)
    if not ok:
        results.append(_fail('save_and_load', df2))
        return results

    if not out_csv.exists():
        results.append(_fail('data_csv', f'file not found: {out_csv}'))
    else:
        results.append(_ok('data_csv', f'CSV 저장 검증 완료: {out_csv.name}'))

    shape = getattr(df2, 'shape', None)
    if shape != (3, 5):
        results.append(_fail('loaded_shape', f'expected (3, 5), got {shape!r}'))
    else:
        results.append(_ok('loaded_shape', f'재로딩 shape 검증 완료: {shape}'))
    return results


def check_prompt_template(module: Any, class_dir: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    ok, prompt = _safe_call('build_prompt', module.build_prompt)
    if not ok:
        return [_fail('build_prompt', prompt)]

    variables = set(getattr(prompt, 'input_variables', []))
    if not {'role', 'question'} <= variables:
        results.append(_fail('prompt_variables', f'expected role/question, got {sorted(variables)!r}'))
    else:
        results.append(_ok('prompt_variables', f'입력 변수 검증 완료: {sorted(variables)!r}'))

    ok, rendered = _safe_call('prompt_render', prompt.format, role='친절한 튜터', question='RAG가 뭐야?')
    if not ok:
        results.append(_fail('prompt_render', rendered))
    else:
        text = str(rendered)
        if '친절한 튜터' not in text or 'RAG가 뭐야?' not in text:
            results.append(_fail('prompt_render', f'rendered text missing variables: {text!r}'))
        elif '{role}' in text or '{question}' in text:
            results.append(_fail('prompt_render', f'unresolved template markers remain: {text!r}'))
        else:
            results.append(_ok('prompt_render', 'PromptTemplate 렌더링 검증 완료.'))
    return results


def grade_class(root: Path, class_id: str, tier: str) -> dict[str, Any]:
    class_dir = class_dir_from_id(root, class_id)
    if not class_dir.exists():
        raise FileNotFoundError(f'Not found: {class_dir}')

    apath = assignment_path(class_dir, class_id, tier)
    spath = solution_path(class_dir, class_id)
    if not apath.exists():
        raise FileNotFoundError(f'Assignment not found: {apath}')
    if not spath.exists():
        raise FileNotFoundError(f'Solution not found: {spath}')

    try:
        amod = load_module(apath, f'{class_id}_{tier}_assignment')
    except Exception as e:
        return {
            'class_id': class_id,
            'tier': tier,
            'profile': 'unknown',
            'passed': False,
            'checks': [CheckResult('import_assignment', False, ''.join(traceback.format_exception_only(type(e), e)).strip())],
        }

    # solution import is optional but confirms reference code is present
    try:
        load_module(spath, f'{class_id}_solution')
        solution_status = CheckResult('import_solution', True, '정답 코드 import 확인 완료.')
    except Exception as e:
        solution_status = CheckResult('import_solution', False, ''.join(traceback.format_exception_only(type(e), e)).strip())

    profile = detect_profile(amod)
    checks = [solution_status]
    if profile == 'python_fundamentals':
        checks.extend(check_python_fundamentals(amod, class_dir))
    elif profile == 'plot_generation':
        checks.extend(check_plot_generation(amod, class_dir))
    elif profile == 'ml_regression':
        checks.extend(check_ml_regression(amod, class_dir))
    elif profile == 'dataframe_io':
        checks.extend(check_dataframe_io(amod, class_dir))
    elif profile == 'prompt_template':
        checks.extend(check_prompt_template(amod, class_dir))
    else:
        checks.append(CheckResult('profile_detection', False, '지원하지 않는 과제 패턴입니다.'))

    passed = all(c.ok for c in checks)
    return {'class_id': class_id, 'tier': tier, 'profile': profile, 'passed': passed, 'checks': checks}
