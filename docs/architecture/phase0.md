# Phase 0 architecture

`versioned corpus + cases + common prompt → sequential runner → provider transport → raw JSONL + manifest → independent evaluation`

Python 3.10+ standard library, no dependency installation. `tools/benchmark-harness/providers.py` exposes request construction, transport and response normalization. Ollama uses native `/api/chat` to retain nanosecond generation/load timings. Lemonade and hosted NIM use OpenAI-compatible chat completions. Provider-specific raw fields remain in `raw_response`; unsupported measurements remain null.

To add a compatible provider, register its endpoint, choose its catalog snapshot endpoint and reuse the chat request/normalizer. A noncompatible provider adds explicit request construction and normalization branches. Add a fixture test for its response and errors. Do not force native metrics into generic total-time-derived throughput.

No embeddings, vector database, UI, router or telemetry service is needed for fixed context. Retrieval is absent, not perfect: all five documents are supplied in a fixed order. The next increment can measure deterministic evidence selection separately from generation.

## Reuse inventory

`mac-mini-llm-roster` inspected at `4fbf1e5`; its branch was three commits ahead of origin with an existing modified `litellm-example/config.yaml`. No files changed there. Six historical run folders, two Python speed scripts, raw JSON, reports and LiteLLM/OTel examples were inspected. Current example routes use oMLX and hosted NIM, so historical Ollama availability cannot be assumed.

Reused methodology: standard-library HTTP, sequential calls, monotonic wall timing, explicit context/output budgets, Ollama `eval_count / (eval_duration / 1e9)`. Those small mechanics were generalized; old scripts and data remain intact. The former 300-character response truncation is not carried over. A model's separated reasoning and provider usage remain available in raw data. LiteLLM is useful operationally but not placed between the experiment and native metrics.

The primary research repo initially contained README and MIT license only, on clean `main` at `c1f406c3548b63c242cc6cee6c900840f281b64c`.
