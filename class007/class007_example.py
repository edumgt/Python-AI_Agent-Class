# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class007 쉬운 예제: 변수와 자료형"""

TOPIC = "변수와 자료형"

def even_double(numbers):
    return [n * 2 for n in numbers if n % 2 == 0]

def make_message(values):
    if not values:
        return "조건을 만족하는 숫자가 없어요."
    return f"짝수만 2배: {values}"

def main():
    data = [1, 2, 3, 4, 5, 6]
    result = even_double(data)
    print("오늘 주제:", TOPIC)
    print(make_message(result))

if __name__ == "__main__":
    main()
