# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class008 example1: 변수와 자료형"""

TOPIC = "변수와 자료형"
EXAMPLE_TEMPLATE = "variables"

def inspect_values():
    sample = {"name": "민수", "age": 11, "height": 140.5, "is_student": True}
    return {k: type(v).__name__ for k, v in sample.items()}

def main():
    print("오늘 주제:", TOPIC)
    print("자료형 확인:", inspect_values())


if __name__ == "__main__":
    main()
