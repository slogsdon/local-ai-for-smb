# Hosted NVIDIA NIM

Existing roster work already used NIM. This integration builds on its direct hosted route.

```sh
export NVIDIA_API_KEY='your-key'  # Set privately; never commit it.
python3 -B tools/benchmark-harness/run.py --provider nvidia-nim \
  --model deepseek-ai/deepseek-v4-flash-0731 --model-family deepseek-v4 \
  --execution remote --repetitions 2
```

Default base: `https://integrate.api.nvidia.com/v1`; POST `/chat/completions`. `NIM_BASE_URL` can override it using HTTPS. The key is sent only as an Authorization header. Do not set the variable to an untrusted endpoint. Model availability and account access can change; inspect the live catalog and do a single-case probe before a full run (`--only meal-limit`).

On 2026-09-16 the live catalog listed `google/gemma-3-4b-it`, but 16 inference requests returned HTTP 404. Those failures are preserved. The existing `deepseek-ai/deepseek-v4-flash-0731` route returned a response in the subsequent probe. Do not assume catalog presence guarantees inference availability.

The fallback differs from local Gemma in family, size, tokenizer and likely implementation. Parameter count, hosted quantization, hardware, backend and context configuration remain unknown where not verified. No hardware comparison is justified. Response usage and full raw response are retained; latency includes network and service overhead. No rate-limit capacity or price claim is made.

Official API reference, checked 2026-09-16: https://docs.api.nvidia.com/nim/re/reference/llm-apis
