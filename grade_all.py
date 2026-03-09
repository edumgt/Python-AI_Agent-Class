# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from grader_core import grade_class

ROOT = Path(__file__).resolve().parent


def load_class_ids_from_index(root: Path) -> list[str]:
    index_file = root / "curriculum_index.csv"
    if not index_file.exists():
        return []

    with index_file.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))

    class_ids: list[str] = []
    for raw in raw_rows:
        row = {str(key).lstrip("\ufeff"): value for key, value in raw.items()}
        class_id = (row.get("class") or "").strip()
        if class_id and class_id not in class_ids:
            class_ids.append(class_id)
    return sorted(class_ids)


def main() -> int:
    ap = argparse.ArgumentParser(description='전체 차시 일괄 채점기')
    ap.add_argument('--tier', default='basic', choices=['basic', 'advanced', 'challenge'])
    ap.add_argument('--start', default='class001', help='시작 id (예: class001)')
    ap.add_argument('--end', default='project020', help='끝 id (예: class500 또는 project020)')
    ap.add_argument('--fail-fast', action='store_true', help='실패 시 즉시 중단')
    args = ap.parse_args()

    class_ids = load_class_ids_from_index(ROOT)
    if not class_ids:
        class_ids = sorted(
            [
                p.name
                for p in ROOT.iterdir()
                if p.is_dir() and (p.name.startswith('class') or p.name.startswith('project'))
            ]
        )
    target = [cid for cid in class_ids if args.start <= cid <= args.end]

    total = len(target)
    passed = 0
    failed = []

    for cid in target:
        result = grade_class(ROOT, cid, args.tier)
        if result['passed']:
            passed += 1
            print(f'[PASS] {cid} ({result["profile"]})')
        else:
            failed.append(cid)
            failed_checks = ', '.join([c.name for c in result['checks'] if not c.ok][:5])
            print(f'[FAIL] {cid} ({result["profile"]}) -> {failed_checks}')
            if args.fail_fast:
                break

    print('-' * 72)
    print(f'Total: {total}')
    print(f'Pass : {passed}')
    print(f'Fail : {len(failed)}')
    if failed:
        print('Failed classes:', ', '.join(failed[:50]))
        if len(failed) > 50:
            print(f'... and {len(failed)-50} more')
    return 0 if not failed else 1


if __name__ == '__main__':
    raise SystemExit(main())
