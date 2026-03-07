# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class026 example2: 파일 입출력"""

TOPIC = "파일 입출력"
EXAMPLE_TEMPLATE = "file_io"

from pathlib import Path

def save_and_read(text):
    out = Path(__file__).with_name("class026_note.txt")
    out.write_text(text, encoding="utf-8")
    return out.read_text(encoding="utf-8")

def main():
    print("오늘 주제:", TOPIC)
    msg = "파일에 저장하고 다시 읽기 성공"
    loaded = save_and_read(msg)
    print("읽은 내용:", loaded)


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
