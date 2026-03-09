# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import argparse
from pathlib import Path

from grader_core import grade_class

ROOT = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser(description='함수 단위 + 결과 파일 검증 기반 단일 차시 채점기')
    ap.add_argument('class_id', help='예: class001 또는 project001')
    ap.add_argument('--tier', default='basic', choices=['basic', 'advanced', 'challenge'])
    args = ap.parse_args()

    result = grade_class(ROOT, args.class_id, args.tier)

    print(f"[CLASS]   {result['class_id']}")
    print(f"[TIER]    {result['tier']}")
    print(f"[PROFILE] {result['profile']}")
    print('-' * 72)
    for check in result['checks']:
        prefix = 'PASS' if check.ok else 'FAIL'
        print(f"[{prefix}] {check.name}: {check.detail}")
    print('-' * 72)
    print('[RESULT] PASS' if result['passed'] else '[RESULT] FAIL')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
