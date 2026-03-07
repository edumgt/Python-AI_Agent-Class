# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class026 example1: 파일 입출력"""

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


if __name__ == "__main__":
    main()
