# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class026 example3: 파일 입출력"""

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


def self_check():
    return [
        "입력/출력 형식을 다시 설명할 수 있는가?",
        "오류 상황 1가지를 직접 만들어 테스트했는가?",
        "핵심 로직을 함수 단위로 분리했는가?",
    ]

def challenge_case():
    return {
        "task": "같은 로직을 새로운 입력 데이터로 재실행",
        "goal": "결과 차이를 한 문장으로 요약",
    }

if __name__ == "__main__":
    main()
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
