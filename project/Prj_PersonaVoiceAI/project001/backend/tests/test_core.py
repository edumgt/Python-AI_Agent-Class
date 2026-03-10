from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from backend.app.core import create_profile, get_profile, synthesize_preview, train_profile


class VoiceCoreTests(unittest.TestCase):
    def test_profile_create_and_get(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "profiles.json"
            profile = create_profile(path, {"name": "coach-kim", "style_tags": ["calm"]})
            loaded = get_profile(path, profile["profile_id"])
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["name"], "coach-kim")

    def test_train_profile_status(self) -> None:
        profile = {
            "profile_id": "vp_test001",
            "name": "tester",
            "style_tags": ["clear"],
            "speaking_rate": 1.0,
            "pitch_shift": 0.0,
        }
        result = train_profile(
            profile,
            {
                "recordings_count": 300,
                "total_minutes": 120,
                "noise_level": 0.1,
                "pronunciation_score": 0.92,
                "emotion_score": 0.8,
            },
        )
        self.assertIn(result["status"], {"ready", "tuning", "collect_more_data"})

    def test_synthesize_preview(self) -> None:
        profile = {
            "profile_id": "vp_test001",
            "name": "tester",
            "base_voice": "warm",
            "style_tags": ["friendly"],
            "speaking_rate": 1.1,
            "pitch_shift": 1.2,
        }
        out = synthesize_preview(profile, "안녕하세요", 0.7)
        self.assertIn("ssml_preview", out)


if __name__ == "__main__":
    unittest.main()
