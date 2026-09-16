# Phase 0 findings — 2026-09-16

The provider-neutral fixed-context foundation executed on Lemonade, Ollama and hosted NVIDIA NIM. These are integration and application-behavior results, not a provider ranking or hardware benchmark. Raw results include failures. Human semantic review remains pending.

## Recorded runs

| Run suffix | Provider / model | Requests | API failures | Strict JSON valid | Median successful application response |
|---|---|---:|---:|---:|---:|
| `71fa1e24` | NIM / Gemma 3 4B catalog candidate | 16 | 16 (404) | 0 | unavailable |
| `6339d1c9` | NIM / DeepSeek v4 Flash probe | 1 | 0 | 1 | 16.081 s |
| `f0504f31` | Lemonade / Gemma 3 4B Q4_K_M | 16 | 0 | 0 | 5.960 s |
| `01c122de` | NIM / DeepSeek v4 Flash | 16 | 1 (529) | 15 | 20.554 s |
| `078840c7` | Ollama / same Gemma GGUF | 16 | 0 | 0 | 6.355 s |

Recompute with `python3 -B tools/benchmark-harness/analyze.py`; [machine-readable summary](../../benchmarks/analysis/summary.json). Raw directories are under [benchmarks/results](../../benchmarks/results). Latencies are separate descriptive observations; different model families, network overhead, first-call residency and runtime defaults prevent causal hardware comparisons. The failed request is excluded from the successful-response median and retained in failure counts. Two repetitions do not support tail-latency estimates.

## What worked

- A single baseline workload and system prompt ran through all three adapters without per-provider prompt tuning.
- Exact local weights could be reused between Lemonade and Ollama. The historical native-Ollama measurement approach remains useful; no LiteLLM replacement was needed.
- Manifest, input snapshots, source hashes and archived executed source make precommit runs traceable. Unknown metrics are null, not guessed.
- The same dataset detects formatting failure, policy conflation, unsupported inference and ambiguity-handling variation. Successful HTTP is not task success.

## Negative findings and AI-assisted review

These observations were checked against saved responses and the fixed corpus by the implementing AI assistant. They are not human rubric scores; `human_review` remains null.

- Both local Gemma runs wrapped every response in Markdown fences, violating the requested JSON-only contract. The harness did not strip fences or improve prompts after seeing results.
- Both local runtimes conflated Standard hours with Premium coverage in both `premium-incident` repetitions. They also omitted the receipt threshold in `expense-flow` and did not request clarification in `support-ambiguity`.
- NIM DeepSeek returned valid JSON for all 15 successful full-run calls, but in both `contractor-meals` answers asserted contractors receive no allowance. The source only excludes contractors from this policy; it does not establish their allowance. Citation presence did not prevent this unsupported inference.
- NIM ambiguity behavior varied: repetition 0 asked for the plan/incident type, repetition 1 returned `answered`. Mechanical expected-status matches were 12/16, including failure as non-match; this is not a quality score.
- NIM Gemma catalog/inference mismatch produced HTTP 404. The DeepSeek full run later returned HTTP 529 for the second `external-ai` request. No automatic retry erased this event; the response status alone does not establish the underlying cause.
- Lemonade portable packaging emitted missing optional resource/web-asset warnings, but model loading and inference completed. Its managed Apple Metal path worked; this says nothing about Ryzen AI performance.

## What cannot be concluded

No provider winner, hardware speed advantage, real-world SMB task-success rate, complete RAG quality, privacy guarantee for arbitrary deployments, service uptime/SLA, rate-limit capacity, energy efficiency or economic break-even. The hosted fallback uses a different model. Text-only GGUF import and Lemonade multimodal loading are not identical runtime configurations. The desktop was not performance-isolated.

## Exit-criterion evidence

- Existing work inventoried and reusable mechanics identified: [architecture](../architecture/phase0.md).
- Three provider integrations completed documented workloads: raw runs above, including service failures.
- Representative synthetic input, fixed cases and common prompt: [dataset](../../benchmarks/datasets/smb-v1).
- Metadata, raw results, credential handling and reproducibility: [methodology](../methodology/phase0.md) and provider guides.
- Evaluation rubric exists; independent human review has not occurred.
- Limitations, initial cost structure and next experiments documented. Publication/commit approval is separate from technical execution; nothing was pushed or submitted to a challenge.

## Next experiments

1. Blind human review using the five separate rubric dimensions; avoid a composite winner score.
2. Deterministic retrieval with evidence-recall tests, before attributing errors to generation.
3. Predeclare a JSON-enforced variant applied consistently where supported; retain this prompt-only baseline.
4. Controlled warm/cold and streaming trials, fixed background load, more repetitions, backend-native telemetry validation.
5. Reuse matched weights and this dataset on whichever suitable local GPU/NPU platform becomes available. Record backend/offload and measure memory/power, then populate editable cost assumptions.
