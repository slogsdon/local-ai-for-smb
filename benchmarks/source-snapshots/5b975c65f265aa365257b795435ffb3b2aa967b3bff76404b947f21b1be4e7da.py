"""Mechanical checks are diagnostics, never a substitute for semantic review."""
import json


def evaluate(text, case, document_ids):
    result = {"structured_output_valid": False, "status_matches": False,
        "citations_known": False, "expected_evidence_covered": False,
        "human_review": None}
    try:
        value = json.loads(text)
    except (ValueError, TypeError):
        return result
    if not isinstance(value, dict) or set(value) != {"answer", "citations", "status"}:
        return result
    if not isinstance(value["answer"], str) or not value["answer"].strip():
        return result
    citations = value["citations"]
    if not isinstance(citations, list) or not all(isinstance(item, str) for item in citations):
        return result
    if value["status"] not in ("answered", "clarify", "insufficient"):
        return result
    result.update(structured_output_valid=True,
        status_matches=value["status"] == case["expected_status"],
        citations_known=set(citations) <= document_ids,
        expected_evidence_covered=set(case["expected_evidence"]) <= set(citations))
    return result
