# Apple Silicon Phase 0 environment — 2026-09-16

Live `sysctl`: Mac16,10, Apple M4, 34359738368 bytes unified memory (32 GiB). `sw_vers`: macOS 26.6.2, build 25G83. This is existing modest local hardware, not representative of future GPU/NPU workstations. Other desktop applications were not stopped; no idle/power/thermal isolation claim.

## Runtime evidence

- Original Ollama endpoint unavailable; binary absent, manifests empty. Installed Homebrew Ollama 0.34.0; Homebrew also installed mlx-c and upgraded xz as dependencies. Temporary `ollama serve`; no login service enabled.
- Lemonade 11.9.0 official portable archive checksum verified. Installed at `~/.local/share/local-ai-phase0/lemonade-11.9.0/lemonade-embeddable-11.9.0-macos-arm64`. Separate `lemonade-cache` and `lemonade-config` under the same parent. Hugging Face model cache remained at `~/.cache/huggingface/hub`.
- Lemonade startup reported Apple M4 Metal device, no NPU, no NVIDIA GPU, telemetry disabled. Load log explicitly reported `Using LlamaCpp Backend: metal`, managed version `b10723`; llama-server reported `n_slots = 1, n_ctx_slot = 4096` and bound to `127.0.0.1:8003`. Public inference API bound to loopback port 8001.
- Lemonade was explicitly loaded before its run, then unloaded before Ollama ran. Ollama's first measured request recorded 16.497 seconds native load duration. These start states differ.
- Ollama `/api/ps` after the run reported 4096 context, GGUF Q4_K_M, 3.9B and `size_vram=2758625197`. This is provider-reported placement, not independently sampled memory usage. Backend remains null in its original manifest; the subsequent server-log review confirmed Metal on Apple M4. Exact backend version remains unknown. See [machine-readable supplemental evidence](phase0-evidence.json).
- NIM execution was remote; this Mac was only the client. Remote hardware, quantization, service version, context allocation and load state are unknown. NVIDIA credentials were already exported; no key values were printed or stored.

## Model identity

Both local runtime runs used the same GGUF SHA256 `882e8d2db44dc554fb0ea5077cb7e4bc49e7342a1f0da57901c0802ea21a0863` from Hugging Face revision `d0976223747697cb51e056d85c532013931fe52e`. Ollama manifest digest is `cef7514d3f7ca67581eef0c8dd9e756e5d2ed00722d65a70f2a50fefed3763f3`; a runtime manifest digest is distinct from a weight-file hash. Lemonade's named model does not expose an immutable version through the generic adapter; this document supplies the resolved revision.

Hosted Gemma was catalog-listed but not usable (404). Hosted DeepSeek used the existing roster route `deepseek-ai/deepseek-v4-flash-0731`; identifier is recorded, but immutability is not guaranteed. All catalogs captured in per-run snapshots. No matched hosted/local model result exists.

## Known missing measurements

No power meter, GPU/CPU sampling, whole-system memory sampling, controlled background load, streaming TTFT or service-side hardware telemetry. No conclusions about AMD GPU/NPU, local NVIDIA acceleration, hardware efficiency or TCO break-even.
