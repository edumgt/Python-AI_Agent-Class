# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class071 Advanced(심화) 과제 (자기주도 학습용)

[학습 정보]
- 교과목: Python 전처리 및 시각화
- 주제: Matplotlib 시각화 기초
- 일정: Day 09 / 7교시
- 난이도: 실전심화

[이번 과제 목표]
- 입력 검증/구조화/결과 저장까지 포함한 실무형 코드로 확장하기
- 초등학생도 혼자 따라갈 수 있도록, 작은 단계로 나눠서 완성하기

[환경 구성 - Windows PowerShell]
1) cd C:\DevOps\Python-AI_Agent-Class
2) python -m venv .venv
3) .\.venv\Scripts\Activate.ps1
4) python -m pip install --upgrade pip
5) pip install -r requirements.txt

[환경 구성 - Linux/macOS (bash)]
1) cd /path/to/Python-AI_Agent-Class
2) python3 -m venv .venv
3) source .venv/bin/activate
4) python -m pip install --upgrade pip
5) pip install -r requirements.txt

[실행 방법]
- python class071/class071_assignment_advanced.py

[쉬운 학습 포인트]
- 표 데이터를 정리해서 의미를 찾는 연습을 해요.
- 열 이름을 먼저 확인하고, 어떤 숫자를 계산할지 순서를 정하세요.

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- shape/columns를 출력하면 데이터 구조 오류를 빠르게 찾을 수 있어요.
- 기본 동작을 유지하면서 예외 처리와 결과 구조를 추가하세요.
"""


from __future__ import annotations

from pathlib import Path
import math
import statistics
import json
import random


import pandas as pd
import matplotlib.pyplot as plt

# =========================
# TODO 1) 간단 데이터 준비
# =========================
x = list(range(1, 11))
y = [v * v for v in x]

# =========================
# TODO 2) 라인 차트 그리기
# - 제목/축라벨 포함
# - outputs/plot.png 로 저장
# =========================
def make_plot(x: list[int], y: list[int]) -> Path:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "plot.png"
    # TODO: plot + savefig
    raise NotImplementedError

def main():
    out = make_plot(x, y)
    print("saved:", out)

if __name__ == "__main__":
    main()


# =========================
# ADVANCED 확장 과제
# =========================
def advanced_extension():
    """심화 과제: 기본 과제를 '조금 더 실무형'으로 확장합니다.

    TODO(심화):
    1) 입력값 검증을 강화하고, 실패 케이스를 예외로 처리하세요.
    2) 결과를 dict로 정리해 JSON 파일로 저장하세요. (파일명: class071_advanced_result.json)
    3) 표준 라이브러리만 사용해서 간단한 리포트(텍스트)를 출력하세요.
    """
    # TODO: 아래는 예시 스켈레톤입니다. 필요한 로직을 채우세요.
    result = {
        "class_id": "class071",
        "tier": "advanced",
        "summary": "TODO: 실습 결과 요약",
    }
    # TODO: JSON 저장
    # from pathlib import Path
    # import json
    # Path(__file__).with_name("class071_advanced_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    # 기존 main 흐름을 유지하고, 마지막에 심화 확장 실행
    try:
        # 파일 내에 main()이 있다면 호출
        main  # type: ignore[name-defined]
    except Exception:
        pass
    else:
        try:
            main()  # type: ignore[misc]
        except TypeError:
            # main이 인자를 요구하면 스킵
            pass

    print("\n[ADVANCED] extension running...")
    out = advanced_extension()
    print(out)
