# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import argparse
from pathlib import Path

from grader_core import grade_class

ROOT = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser(description='전체 차시 일괄 채점기')
    ap.add_argument('--tier', default='basic', choices=['basic', 'advanced', 'challenge'])
    ap.add_argument('--start', default='class001', help='시작 class id (예: class001)')
    ap.add_argument('--end', default='class500', help='끝 class id (예: class500)')
    ap.add_argument('--fail-fast', action='store_true', help='실패 시 즉시 중단')
    args = ap.parse_args()

    class_dirs = sorted([p.name for p in ROOT.glob('class*') if p.is_dir() and p.name.startswith('class')])
    target = [cid for cid in class_dirs if args.start <= cid <= args.end]

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
