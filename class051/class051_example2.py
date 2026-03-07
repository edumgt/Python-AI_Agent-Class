# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class051 example2: Pandas 데이터프레임 기초"""

TOPIC = "Pandas 데이터프레임 기초"
EXAMPLE_TEMPLATE = "pandas"

import pandas as pd

def build_frame():
    df = pd.DataFrame(
        [
            {"name": "민수", "score": 90},
            {"name": "지유", "score": 85},
        ]
    )
    df["pass"] = df["score"] >= 80
    return df

def main():
    print("오늘 주제:", TOPIC)
    print(build_frame())


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
