# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class048 example1: NumPy 기초"""

TOPIC = "NumPy 기초"
EXAMPLE_TEMPLATE = "numpy"

import numpy as np

def stats(values):
    arr = np.array(values, dtype=float)
    return float(arr.mean()), float(arr.std())

def main():
    print("오늘 주제:", TOPIC)
    mean, std = stats([10, 20, 30, 40])
    print("평균:", round(mean, 2), "표준편차:", round(std, 2))


if __name__ == "__main__":
    main()
