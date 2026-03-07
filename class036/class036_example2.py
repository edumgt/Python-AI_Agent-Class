# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class036 example2: 객체지향 기초"""

TOPIC = "객체지향 기초"
EXAMPLE_TEMPLATE = "oop"

class Student:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def introduce(self):
        return f"안녕하세요, 저는 {self.name}이고 {self.level} 단계예요."

def main():
    print("오늘 주제:", TOPIC)
    student = Student("지유", "기초응용")
    print(student.introduce())


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
