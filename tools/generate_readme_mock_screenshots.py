# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "screenshots"


@dataclass(frozen=True)
class ScreenSpec:
    filename: str
    title: str
    subtitle: str
    fake_id: str
    menu: list[str]
    steps: list[str]


SCREENS = [
    ScreenSpec(
        filename="01_chatgpt_signup_mock.png",
        title="ChatGPT 가입/로그인 화면 (모의 캡처)",
        subtitle="https://chatgpt.com",
        fake_id="demo.chatgpt.001@virtual.local",
        menu=["Home", "Pricing", "Sign up", "Log in"],
        steps=[
            "1) Email 입력",
            "2) 비밀번호 설정",
            "3) 이메일 인증 완료",
            "4) 프로필 이름 설정",
        ],
    ),
    ScreenSpec(
        filename="02_codex_integration_mock.png",
        title="Codex 연동 설정 화면 (모의 캡처)",
        subtitle="VS Code / Codex Extension Settings",
        fake_id="demo.codex.user01",
        menu=["Extension", "Authentication", "Model", "Workspace"],
        steps=[
            "1) OpenAI 계정 로그인",
            "2) Workspace 선택",
            "3) 모델/권한 확인",
            "4) 테스트 프롬프트 실행",
        ],
    ),
    ScreenSpec(
        filename="03_github_mock.png",
        title="GitHub 로그인 화면 (모의 캡처)",
        subtitle="https://github.com/login",
        fake_id="demo-github-user01",
        menu=["Sign in", "Repository", "Branch", "Pull Request"],
        steps=[
            "1) 사용자명 입력",
            "2) 비밀번호 입력",
            "3) 2FA 인증",
            "4) 저장소 접근 확인",
        ],
    ),
    ScreenSpec(
        filename="04_vscode_extensions_mock.png",
        title="VS Code 확장팩 설치 화면 (모의 캡처)",
        subtitle="Extensions: Python / Pylance / Markdown Mermaid",
        fake_id="demo.vscode.user01",
        menu=["Python", "Pylance", "Markdown All in One", "Markdown Mermaid"],
        steps=[
            "1) Ctrl+Shift+X",
            "2) 확장 검색",
            "3) Install 클릭",
            "4) Reload/활성화",
        ],
    ),
    ScreenSpec(
        filename="05_mermaid_preview_mock.png",
        title="Markdown Mermaid 미리보기 (모의 캡처)",
        subtitle="README.md Preview",
        fake_id="demo.docs.viewer01",
        menu=["README.md", "Split View", "Preview", "Mermaid Rendered"],
        steps=[
            "1) README.md 열기",
            "2) Ctrl+K, V",
            "3) Mermaid 렌더 확인",
            "4) 흐름도 이미지 비교",
        ],
    ),
    ScreenSpec(
        filename="06_python_env_mock.png",
        title="Python 가상환경/패키지 설치 (모의 캡처)",
        subtitle="Terminal: venv + pip install -r requirements.txt",
        fake_id="demo.python.user01",
        menu=["python -m venv .venv", "activate", "pip install", "python --version"],
        steps=[
            "1) 가상환경 생성",
            "2) 가상환경 활성화",
            "3) requirements 설치",
            "4) 실행/버전 확인",
        ],
    ),
    ScreenSpec(
        filename="07_docker_rag_mock.png",
        title="Docker RAG/LLM 실습 구성 (모의 캡처)",
        subtitle="docker compose: ollama + qdrant",
        fake_id="demo.docker.user01",
        menu=["compose up -d", "ollama", "qdrant", "health check"],
        steps=[
            "1) docker compose up -d",
            "2) ollama 모델 pull",
            "3) qdrant dashboard 확인",
            "4) RAG 파이프라인 연결 테스트",
        ],
    ),
]


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str) -> None:
    draw.rounded_rectangle(xy, radius=16, fill=fill, outline=outline, width=2)


def render_screen(spec: ScreenSpec) -> Image.Image:
    w, h = 1440, 900
    image = Image.new("RGB", (w, h), "#F1F5F9")
    draw = ImageDraw.Draw(image)

    font_title = load_font(34, bold=True)
    font_sub = load_font(20)
    font_body = load_font(22)
    font_small = load_font(18)
    font_code = load_font(20)

    # browser top bar
    draw.rectangle((0, 0, w, 72), fill="#0F172A")
    draw.text((24, 18), "Virtual Capture", font=font_sub, fill="#E2E8F0")
    draw.rounded_rectangle((220, 14, 980, 58), radius=12, fill="#1E293B", outline="#334155", width=2)
    draw.text((242, 26), spec.subtitle, font=font_small, fill="#CBD5E1")
    draw.rounded_rectangle((1040, 16, 1410, 56), radius=12, fill="#1D4ED8", outline="#1E40AF", width=2)
    draw.text((1060, 26), f"ID: {spec.fake_id}", font=font_small, fill="white")

    # title
    draw.text((32, 96), spec.title, font=font_title, fill="#0F172A")

    # left nav
    draw_card(draw, (32, 156, 360, 860), fill="#E2E8F0", outline="#94A3B8")
    draw.text((54, 182), "메뉴", font=font_body, fill="#0F172A")
    y = 230
    for item in spec.menu:
        draw.rounded_rectangle((52, y, 338, y + 54), radius=10, fill="#F8FAFC", outline="#94A3B8", width=1)
        draw.text((66, y + 15), item, font=font_small, fill="#1E293B")
        y += 70

    # main panel
    draw_card(draw, (390, 156, 1408, 860), fill="#FFFFFF", outline="#CBD5E1")
    draw.text((420, 184), "실행 단계", font=font_body, fill="#0F172A")

    y = 238
    for idx, step in enumerate(spec.steps, start=1):
        draw.rounded_rectangle((420, y, 1368, y + 78), radius=14, fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((442, y + 24), f"STEP {idx}", font=font_code, fill="#1D4ED8")
        draw.text((572, y + 24), step, font=font_body, fill="#0F172A")
        y += 94

    # footer
    draw.rounded_rectangle((420, 760, 1368, 836), radius=14, fill="#DBEAFE", outline="#93C5FD", width=1)
    draw.text(
        (442, 788),
        "주의: 본 이미지는 문서용 가상 계정 모의 캡처입니다.",
        font=font_small,
        fill="#1E3A8A",
    )

    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in SCREENS:
        image = render_screen(spec)
        out_path = OUT_DIR / spec.filename
        image.save(out_path, format="PNG")
        print(f"saved: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

