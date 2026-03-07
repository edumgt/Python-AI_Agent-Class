# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class047 쉬운 예제: NumPy 기초"""

TOPIC = "NumPy 기초"

def add_average(rows):
    for row in rows:
        row["avg"] = round((row["math"] + row["science"]) / 2, 1)
    return rows

def print_report(rows):
    print("오늘 주제:", TOPIC)
    for row in rows:
        print(f"{row['name']} -> 평균 {row['avg']}")

def main():
    students = [
        {"name": "민수", "math": 90, "science": 80},
        {"name": "지유", "math": 75, "science": 95},
    ]
    result = add_average(students)
    print_report(result)

if __name__ == "__main__":
    main()
