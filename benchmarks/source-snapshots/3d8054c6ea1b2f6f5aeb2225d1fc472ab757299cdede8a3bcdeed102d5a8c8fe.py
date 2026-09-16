"""Run: python3 -B -m unittest discover -s tools/benchmark-harness -p 'test_*.py'."""
import json
import unittest
from unittest.mock import patch
import urllib.error
from evaluation import evaluate
from providers import generate, make_request, normalize


class HarnessChecks(unittest.TestCase):
    def test_metrics_and_request(self):
        path, body = make_request("ollama", "test", [], 0, 64, 4096, 7)
        self.assertEqual(path, "/api/chat")
        self.assertEqual(body["options"]["num_ctx"], 4096)
        self.assertEqual(body["options"]["seed"], 7)
        native = normalize("ollama", {"message": {"content": "x"}, "eval_count": 10, "eval_duration": 2e9})
        self.assertEqual(native["tokens_per_second"], 5)
        remote = normalize("nvidia-nim", {"choices": [{"message": {"content": "x"}}]})
        self.assertIsNone(remote["output_tokens"])
        self.assertIsNone(remote["tokens_per_second"])

    def test_evaluation_rejects_invalid_and_unknown_evidence(self):
        case = {"expected_status": "answered", "expected_evidence": ["P1"]}
        for text in ("not json", "[]", '{"answer": "x"}'):
            self.assertFalse(evaluate(text, case, {"P1"})["structured_output_valid"])
        text = json.dumps({"answer": "x", "citations": ["invented"], "status": "answered"})
        result = evaluate(text, case, {"P1"})
        self.assertTrue(result["structured_output_valid"])
        self.assertFalse(result["citations_known"])
        self.assertFalse(result["expected_evidence_covered"])
        self.assertIsNone(result["human_review"])

    def test_failure_does_not_leak_error_body(self):
        with patch("providers.request_json", side_effect=urllib.error.HTTPError("url", 429, "secret", {}, None)):
            result = generate("nvidia-nim", "/chat/completions", {}, 1)
        self.assertEqual(result["error"], {"type": "http", "status": 429})
        self.assertNotIn("secret", json.dumps(result))
        self.assertIsNone(result["output_tokens"])
        self.assertGreaterEqual(result["total_time"], 0)

    def test_success_preserves_raw(self):
        raw = {"choices": [{"message": {"content": "answer"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2}}
        with patch("providers.request_json", return_value=raw):
            result = generate("lemonade", "/chat/completions", {}, 1)
        self.assertEqual(result["raw_response"], raw)
        self.assertEqual(result["output_tokens"], 2)
        self.assertIsNone(result["time_to_first_token"])


if __name__ == "__main__":
    unittest.main()
