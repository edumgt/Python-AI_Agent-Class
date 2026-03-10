from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from backend.app.core import answer_without_llm, build_prompt, upsert_persona


class PersonaCoreTests(unittest.TestCase):
    def test_upsert_and_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "personas.json"
            persona = upsert_persona(
                path,
                {
                    "name": "mentor",
                    "role": "AI 코치",
                    "tone": "단호하고 친절한",
                    "speaking_rules": ["근거 먼저"],
                },
            )
            prompt = build_prompt(persona, "RAG를 어떻게 시작하나요?", "사내 문서가 있음")
            self.assertIn("RAG", prompt)

    def test_local_answer_not_empty(self) -> None:
        persona = {
            "name": "mentor",
            "tone": "친절",
            "greeting": "안녕하세요",
        }
        answer = answer_without_llm(persona=persona, question="학습 계획 추천", context="")
        self.assertTrue(answer)


if __name__ == "__main__":
    unittest.main()
