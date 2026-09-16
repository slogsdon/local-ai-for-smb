# Reproducing Phase 0

Requirements: Python 3.10+, a configured inference provider, Git for revision metadata. Run commands from repository root. No Python packages are required.

```sh
python3 -B -m unittest discover -s tools/benchmark-harness -p 'test_*.py'
python3 -B tools/benchmark-harness/run.py --help
```

Configure using exported variables in `.env.example`; the harness deliberately does not execute or load `.env` files. See individual [provider instructions](../../providers). Never put credentials in endpoint URLs or command arguments. NIM requires `NVIDIA_API_KEY`. Only synthetic corpus content is sent remotely. Authentication headers and HTTP error bodies are never recorded; error status/type is retained.

## Inputs and procedure

`benchmarks/datasets/smb-v1/` contains five CC0 synthetic documents, eight test cases and the common system prompt. Each case fixes category, question, evidence, expected behavior/status, difficulty and notes before generation. Both repetitions use the same ordered cases, temperature zero and 512 output-token budget. Seed is omitted by default because support is not assumed. Temperature zero is not a determinism guarantee.

No provider-specific JSON enforcement or prompt tuning is used. Markdown-fenced JSON fails strict structured-output compliance; it is not silently repaired. Semantics can still be reviewed independently. Maximum tokens may include model reasoning; inspect raw reasoning and finish reasons for truncation.

Runs are sequential per provider. No automatic retries hide service failures. No timed warmup is imposed; residency and prompt-cache effects are uncontrolled and must be described alongside timings. Local runtimes should not generate concurrently. Close unrelated workloads for controlled performance studies; this Phase 0 desktop session is not such a study.

## Artifacts

Each unique `benchmarks/results/<run_id>/` holds:

- `manifest.json`: timestamps, Git revision/dirty state, source and input SHA256, provider/model/configuration, client vs inference environment, measurement definitions and final run status.
- `inputs.json`: exact full dataset and prompt snapshot.
- `provider-snapshot.json`: live catalog and, for Ollama, version/model details.
- `results.jsonl`: exact request bodies, untruncated response and raw provider body, usage, finish reason, timing, errors and mechanical checks. Each request flushes immediately; an interrupted manifest remains `running`.

`benchmarks/source-snapshots/<sha256>.py` preserves executed code even for precommit runs. Restore each filename according to `source_sha256` in a manifest. Git commit alone is insufficient when `git_dirty` is true. Client hardware is distinct from remote hardware, which remains null. Manual runtime/backend claims must be supported by environment evidence.

## Measurements and limits

- `total_time`: monotonic seconds around HTTP request and response parsing; excludes local evaluation and result writing. This is application/API latency, not pure inference.
- `time_to_first_token`: null in this nonstreaming increment. No fabricated TTFT.
- `input_tokens`, `output_tokens`: provider-reported; tokenizers and reasoning accounting differ.
- `tokens_per_second`: native Ollama generation count/duration only. Not output tokens divided by request latency. Lemonade native fields remain in raw response if exposed, but are not promoted without attribution validation.
- Native Ollama durations are nanoseconds. Missing memory/utilization/power/load measurements remain absent or null; no process memory estimate substitutes for GPU memory.
- HTTP success, JSON validity, recognized citations, expected citation coverage and status matching are separate dimensions. None proves factual grounding or practical task success. Invalid structured output makes subsequent mechanical fields false, not independent semantic judgments.

## Human rubric, fixed before review

Score each dimension separately: grounding, completeness, instruction following, hallucination avoidance and practical usefulness. 0 = incorrect/unusable; 1 = partly correct; 2 = correct with meaningful deficiencies; 3 = correct and practically useful. For hallucination avoidance, 3 means no unsupported assertions and appropriate uncertainty; 0 means material fabrication. Record reviewer identity/type, run/test/repetition, scores and rationale. No composite winner score.

Human reviewers compare answers with `expected_behavior` and cited documents, including missing conditions, conflated plans and accepted false premises. AI-assisted annotations must be labeled as such and never presented as human judgments. `human_review` stays null until a human reviews. A completed review should be a separate analysis artifact, leaving raw results untouched.

## Immediate next experiment

Introduce deterministic lexical retrieval; evaluate expected-document recall before generation. Add question variants and blind human review, then streaming TTFT, measured warmup and more repetitions. Rate-limit, disconnect, timeout and context-overflow studies are future experiments, not conclusions from successful calls.
