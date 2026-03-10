from __future__ import annotations

import unittest

from backend.app.core import evaluate


class CoreScenarioTests(unittest.TestCase):
    def test_evaluate_returns_status(self) -> None:
        result = evaluate(track_code="프로젝트-1", values=[0.1, 0.2, 0.3], note="unit-test")
        self.assertIn(result.status, {"ready", "design"})
        self.assertIsInstance(result.summary, dict)

    def test_continual_track_has_drift_score(self) -> None:
        result = evaluate(track_code="프로젝트-4", values=[0.8, 0.9, 0.7], note="aiops")
        self.assertIn("drift_score", result.summary)


if __name__ == "__main__":
    unittest.main()
