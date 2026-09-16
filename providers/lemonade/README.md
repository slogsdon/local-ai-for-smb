# Lemonade on Apple Silicon

Validated runtime: official **11.9.0 macOS arm64 embeddable** release. This is a supported portable distribution, not the retired Python SDK installation path. Global `.pkg` installation is also documented upstream. Portable installation keeps research configuration separate.

Download `lemonade-embeddable-11.9.0-macos-arm64.tar.gz` from the official release. Verify SHA256 `cc7ed41939d7d57a91a67f6a3aadafa7902ccf4dbe891005c16e398fae085bb1`, extract, then from the extracted directory:

```sh
./lemond --host 127.0.0.1 --port 8001 --no-broadcast ./cache ./config
# In another terminal in that directory:
./lemonade --port 8001 config set ctx_size=4096 llamacpp.backend=metal llamacpp.prefer_system=false
./lemonade --port 8001 pull Gemma-3-4b-it-GGUF
./lemonade --port 8001 load Gemma-3-4b-it-GGUF
```

Run from research repository root:

```sh
python3 -B tools/benchmark-harness/run.py --provider lemonade \
  --model Gemma-3-4b-it-GGUF --model-family gemma-3 --parameter-count 4B \
  --quantization Q4_K_M --runtime-version 11.9.0 --backend llama.cpp-metal \
  --configured-context 4096 --execution local --repetitions 2
```

The observed route is `/api/v1/chat/completions`, not simply `/v1`. Configuration selected managed llama.cpp **b10723**, Metal, a 4096-token slot and Apple M4; there is no AMD GPU/NPU acceleration. The portable package warns about missing web assets and architecture_defaults.json; API operation succeeded despite those warnings. Telemetry was disabled. Model download used the shared Hugging Face cache despite dedicated runtime cache/config directories.

Model source: `ggml-org/gemma-3-4b-it-GGUF`, revision `d0976223747697cb51e056d85c532013931fe52e`, `gemma-3-4b-it-Q4_K_M.gguf`; SHA256 `882e8d2db44dc554fb0ea5077cb7e4bc49e7342a1f0da57901c0802ea21a0863`. Lemonade also downloaded the F16 multimodal projector; this workload is text-only. Weights are not distributed in this research repository; follow upstream model license terms.

Unload after use with `./lemonade --port 8001 unload`; stop `lemond` with Ctrl-C. No login service is required. API load was performed before this benchmark; first benchmark call is not a cold model-load measurement.

Sources checked 2026-09-16:
- https://github.com/lemonade-sdk/lemonade/releases/tag/v11.9.0
- https://lemonade-server.ai/docs/guide/install/
- https://lemonade-server.ai/docs/embeddable/
- https://lemonade-server.ai/docs/guide/configuration/llamacpp/
