from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from backend.app.core import build_custom_answer, bootstrap_knowledge, retrieve_knowledge


class CustomCoreTests(unittest.TestCase):
    def test_bootstrap_and_retrieve(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "knowledge.json"
            bootstrap_knowledge(path)
            rows = retrieve_knowledge(path, "RAG 검색 품질 어떻게 올리나요", 3)
            self.assertGreaterEqual(len(rows), 1)

    def test_build_answer(self) -> None:
        answer = build_custom_answer(
            persona_name="PERSO",
            style="친절",
            question="개인정보 정책이 뭐야?",
            matched=[{"item_id": "kb1", "title": "정책", "content": "동의가 필요함", "score": 0.8}],
        )
        self.assertIn("PERSO", answer)


if __name__ == "__main__":
    unittest.main()
