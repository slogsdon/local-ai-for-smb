# Research plan

Research question: When does running AI locally make more sense for a small or midsize business than relying entirely on cloud AI services?

## Testable hypotheses (not conclusions)

1. Some bounded knowledge tasks are useful on modest local hardware; usefulness requires grounded answers, not merely successful API calls.
2. Runtime, template, quantization and context configuration can change application behavior even with shared weights.
3. Operational overhead and utilization can reverse a token-price-only cost comparison.
4. Hybrid routing may improve the privacy/capability tradeoff, but requires explicit data policy and reliability testing.

## Phases

- Phase 0: fixed-context knowledge assistant, provider adapters, synthetic versioned inputs, environment manifests, raw responses, evaluation rubric, initial cost structure. No retrieval quality claim.
- Phase 1: deterministic retrieval with separate evidence-recall measurement; blinded human review; repeated runs with controlled warmup, sampling and background load.
- Phase 2: hardware-dependent experiments on available non-Apple GPU/NPU systems. Reuse the workload and manifests, test matched weights and context where feasible. No vendor acquisition assumption.
- Later: document processing, support assistance, business agents, development/IT assistance and hybrid routing, one workload at a time.

The existing README remains the broader research thesis. Phase 0 does not implement all six workloads, a production app, or a universal ranking.

## Protocol

Freeze evidence and expected behavior before inference. Send identical baseline messages without provider-specific prompt tuning. Retain failures, finish reasons and unknown metrics. Distinguish API success, format compliance and semantic task completion. Use a human rubric rather than treating exact output strings or citation presence as correctness.

Application latency includes network, queueing, prompt processing and generation. Native generation throughput is a different measurement. Hosted NIM and local Lemonade cannot isolate hardware effects. Model families, sizes, templates and quantization must be disclosed. Two repeats of eight questions are integration evidence, not a statistically representative SMB benchmark.

See [methodology](docs/methodology/phase0.md), [architecture](docs/architecture/phase0.md), [environment](docs/environments/apple-m4.md), and [findings](docs/findings/phase0.md).
