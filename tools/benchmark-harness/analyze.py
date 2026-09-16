#!/usr/bin/env python3
"""Verify recorded input/source hashes and recompute mechanical summaries."""
import hashlib
import json
import statistics
from pathlib import Path
from evaluation import evaluate

ROOT = Path(__file__).resolve().parents[2]


def main():
    summaries = []
    for directory in sorted((ROOT / "benchmarks/results").iterdir()):
        if not directory.is_dir():
            continue
        manifest = json.loads((directory / "manifest.json").read_text())
        inputs = json.loads((directory / "inputs.json").read_text())
        for name, digest in manifest["dataset_sha256"].items():
            assert hashlib.sha256(inputs[name].encode()).hexdigest() == digest, (directory, name)
        for name, digest in manifest["source_sha256"].items():
            source = ROOT / "benchmarks/source-snapshots" / (digest + ".py")
            assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, (directory, name)
        rows = [json.loads(line) for line in (directory / "results.jsonl").read_text().splitlines()]
        assert manifest["status"] == "completed", directory
        assert len(rows) == manifest["request_count"] == len(manifest["test_ids"]) * manifest["repetitions"]
        assert {(row["test_id"], row["repetition"]) for row in rows} == {(test, repeat) for test in manifest["test_ids"] for repeat in range(manifest["repetitions"])}
        cases = {case["test_id"]: case for case in json.loads(inputs["cases.json"])}
        document_ids = {document["id"] for document in json.loads(inputs["corpus.json"])["documents"]}
        for row in rows:
            assert row["run_id"] == manifest["run_id"]
            assert row["evaluation"] == evaluate(row["response"], cases[row["test_id"]], document_ids)
        successful = [row for row in rows if row["error"] is None]
        summaries.append({"run_id": manifest["run_id"], "model": manifest["model"], "requests": len(rows),
            "failures": len(rows) - len(successful),
            "strict_json_valid": sum(row["evaluation"]["structured_output_valid"] for row in rows),
            "status_matches": sum(row["evaluation"]["status_matches"] for row in rows),
            "median_success_response_seconds": statistics.median(row["total_time"] for row in successful) if successful else None,
            "human_reviewed": sum(row["evaluation"]["human_review"] is not None for row in rows)})
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
