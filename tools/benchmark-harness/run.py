#!/usr/bin/env python3
"""Sequential fixed-context benchmark. Python 3.10+, standard library only."""
import argparse
import hashlib
import json
import platform
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from evaluation import evaluate
from providers import PROVIDERS, endpoint, generate, make_request, request_json

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "benchmarks/datasets/smb-v1"


def command(*args):
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def snapshot(provider, model):
    paths = {"ollama": ["/api/version", "/api/tags"],
        "lemonade": ["/models"], "nvidia-nim": ["/models"]}[provider]
    result = {}
    for path in paths:
        try:
            result[path] = request_json(provider, path, timeout=30)
        except Exception as error:
            result[path] = {"error_type": type(error).__name__}
    if provider == "ollama":
        try:
            result["/api/show"] = request_json(provider, "/api/show", {"model": model}, 30)
        except Exception as error:
            result["/api/show"] = {"error_type": type(error).__name__}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, choices=PROVIDERS)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-family", required=True)
    parser.add_argument("--parameter-count", default=None)
    parser.add_argument("--quantization", default=None)
    parser.add_argument("--runtime-version", default=None)
    parser.add_argument("--backend", default=None)
    parser.add_argument("--context", type=int, default=4096, help="Ollama request context; for others configure server separately")
    parser.add_argument("--configured-context", type=int, default=None, help="Verified server context for OpenAI-compatible providers")
    parser.add_argument("--context-limit", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--seed", type=int, default=None, help="Only set after verifying provider/model support")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--only", default=None, help="Comma-separated test IDs; default all")
    parser.add_argument("--execution", choices=("local", "remote"), required=True)
    args = parser.parse_args()
    if min(args.context, args.max_tokens, args.timeout, args.repetitions) <= 0:
        parser.error("Context, token budget, timeout and repetitions must be positive")
    if args.provider == "nvidia-nim" and args.execution != "remote":
        parser.error("This NIM adapter represents the hosted service")
    if args.provider == "nvidia-nim":
        import os
        if not os.environ.get("NVIDIA_API_KEY"):
            parser.error("Export NVIDIA_API_KEY before running")
    endpoint(args.provider)
    corpus = json.loads((DATASET / "corpus.json").read_text())
    cases = json.loads((DATASET / "cases.json").read_text())
    if args.only:
        selected = set(args.only.split(","))
        if not selected <= {case["test_id"] for case in cases}:
            parser.error("Unknown test ID")
        cases = [case for case in cases if case["test_id"] in selected]
    timestamp = datetime.now(timezone.utc)
    run_id = timestamp.strftime("%Y%m%dT%H%M%SZ") + "-" + args.provider + "-" + uuid.uuid4().hex[:8]
    output = ROOT / "benchmarks/results" / run_id
    output.mkdir(parents=True, exist_ok=False)
    inputs = {name: (DATASET / name).read_text() for name in ("corpus.json", "cases.json", "system.txt")}
    write_json(output / "inputs.json", inputs)
    source_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(Path(__file__).parent.glob("*.py"))}
    for path in Path(__file__).parent.glob("*.py"):
        archive = ROOT / "benchmarks/source-snapshots"
        archive.mkdir(parents=True, exist_ok=True)
        target = archive / (source_hashes[path.name] + ".py")
        if not target.exists():
            target.write_bytes(path.read_bytes())
    data_hashes = {name: hashlib.sha256(text.encode()).hexdigest() for name, text in inputs.items()}
    inventory = snapshot(args.provider, args.model)
    write_json(output / "provider-snapshot.json", inventory)
    details = inventory.get("/api/show", {}).get("details", {})
    model_version = next((item.get("digest") for item in inventory.get("/api/tags", {}).get("models", []) if item.get("name") == args.model), None)
    status = command("git", "status", "--porcelain", "--untracked-files=all")
    host = {"host_os": platform.platform(), "host_architecture": platform.machine(),
        "host_memory": command("sysctl", "-n", "hw.memsize") if platform.system() == "Darwin" else None,
        "hardware": command("sysctl", "-n", "machdep.cpu.brand_string") if platform.system() == "Darwin" else platform.processor() or None}
    manifest = {"run_id": run_id, "timestamp": timestamp.isoformat(), "git_commit": command("git", "rev-parse", "HEAD"),
        "git_dirty": bool(status) if status is not None else None, "source_sha256": source_hashes,
        "provider": args.provider, "runtime": args.provider, "runtime_version": args.runtime_version,
        "model": args.model, "model_family": args.model_family, "parameter_count": args.parameter_count or details.get("parameter_size"),
        "model_version": model_version, "quantization": args.quantization or details.get("quantization_level"),
        "context_limit": args.context_limit, "configured_context": args.context if args.provider == "ollama" else args.configured_context,
        "temperature": args.temperature, "max_tokens": args.max_tokens, "seed_if_supported": args.seed,
        "streaming": False, "client_environment": host,
        "inference_environment": host if args.execution == "local" else {key: None for key in host},
        "backend": args.backend, "local_or_remote": args.execution, "benchmark_version": "0.1.0",
        "dataset_version": corpus["version"], "dataset_sha256": data_hashes, "endpoint": endpoint(args.provider),
        "test_ids": [case["test_id"] for case in cases], "repetitions": args.repetitions,
        "warmup": "none; residency uncontrolled; first call may include load", "retrieval": "none; full fixed corpus in original order",
        "status": "running", "measurement_units": {"total_time": "seconds", "time_to_first_token": "seconds", "native_metrics": "Ollama nanoseconds"}}
    write_json(output / "manifest.json", manifest)
    documents = corpus["documents"]
    context = "\n\n".join("[" + document["id"] + "] " + document["title"] + "\n" + document["text"] for document in documents)
    document_ids = {document["id"] for document in documents}
    results = []
    with (output / "results.jsonl").open("x") as stream:
        for repetition in range(args.repetitions):
            for case in cases:
                messages = [{"role": "system", "content": inputs["system.txt"]},
                    {"role": "user", "content": "Documents:\n" + context + "\n\nQuestion: " + case["question"]}]
                path, body = make_request(args.provider, args.model, messages, args.temperature, args.max_tokens, args.context, args.seed)
                result = generate(args.provider, path, body, args.timeout)
                result.update(run_id=run_id, test_id=case["test_id"], repetition=repetition,
                    request_metadata={"path": path, "body": body},
                    evaluation=evaluate(result["response"], case, document_ids),
                    notes=["Nonstreaming: TTFT unavailable. Throughput only reported from native generation timing."])
                stream.write(json.dumps(result, ensure_ascii=False) + "\n")
                stream.flush()
                results.append(result)
                print(case["test_id"], result["error"] or "response received", round(result["total_time"], 3), flush=True)
    failures = sum(result["error"] is not None for result in results)
    manifest.update(status="completed", request_count=len(results), failure_count=failures)
    write_json(output / "manifest.json", manifest)
    print(output)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
