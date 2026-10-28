"""Offline fault-injection tests only, not model-quality/inference tests.

Fresh model/moderation and registered UI callback runs are in notebook 11.
These tests replace stage boundaries to exercise deterministic failure paths.
Any unexpected HTTP request fails before transmission.
"""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

os.environ.setdefault("OPENAI_API_KEY", "offline-tests-do-not-send")
import customer_service as service


class PipelineContractTests(unittest.TestCase):
    def test_failure_paths_preserve_history(self):
        prior = [{"role": "user", "content": "old"},
                 {"role": "assistant", "content": "reply"}]
        selected = '[{"category":"Smartphones and Accessories","products":["SmartX ProPhone"]}]'
        cases = [
            {"moderation": [True], "expected": "Sorry, I cannot process this request."},
            {"raw": "not JSON"},
            {"raw": '[{"category":"Smartphones and Accessories","products":["fake"]}]'},
            {"moderation": [False, True]},
            {"decision": "N"},
            {"judge_error": ValueError("Malformed judge result")},
            {"generate_error": RuntimeError("Incomplete completion")},
            {"extract_error": RuntimeError("Request failed")},
        ]
        for case in cases:
            with self.subTest(case=case):
                flags = iter(case.get("moderation", [False, False]))
                with patch("httpx.Client.send", side_effect=AssertionError("No HTTP permitted")), \
                     patch.object(service, "moderate", side_effect=lambda _: SimpleNamespace(flagged=next(flags))), \
                     patch.object(service, "find_category_and_product_only", return_value=case.get("raw", selected), side_effect=case.get("extract_error")), \
                     patch.object(service, "generate_answer", return_value="candidate", side_effect=case.get("generate_error")), \
                     patch.object(service, "evaluate_answer", return_value=case.get("decision", "Y"), side_effect=case.get("judge_error")):
                    answer, updated = service.process_user_message("query", prior)
                self.assertEqual(answer, case.get("expected", service.FALLBACK))
                self.assertEqual(updated, prior)
                self.assertIsNot(updated, prior)
                self.assertEqual(len(prior), 2)

    def test_success_appends_complete_turn_without_mutating_caller(self):
        prior = [{"role": "user", "content": "old"}, {"role": "assistant", "content": "reply"}]
        selected = '[{"category":"Smartphones and Accessories","products":["SmartX ProPhone"]}]'
        with patch("httpx.Client.send", side_effect=AssertionError("No HTTP permitted")), \
             patch.object(service, "moderate", return_value=SimpleNamespace(flagged=False)), \
             patch.object(service, "find_category_and_product_only", return_value=selected), \
             patch.object(service, "generate_answer", return_value="candidate"), \
             patch.object(service, "evaluate_answer", return_value="Y"):
            answer, updated = service.process_user_message("query", prior)
        self.assertEqual(answer, "candidate")
        self.assertEqual(len(prior), 2)
        self.assertEqual(updated[-2:], [{"role": "user", "content": "query"},
                                       {"role": "assistant", "content": "candidate"}])


if __name__ == "__main__":
    unittest.main()
