# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class010 example1: BMI 조건 분기"""

TOPIC = "연산자와 조건문"


def bmi_status(weight, height_m):
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        label = "저체중"
    elif bmi < 23:
        label = "정상"
    elif bmi < 25:
        label = "과체중"
    else:
        label = "비만"
    return bmi, label


def main():
    bmi, label = bmi_status(68, 1.72)
    print("오늘 주제:", TOPIC)
    print(f"BMI={bmi:.1f} -> {label}")


if __name__ == "__main__":
    main()
