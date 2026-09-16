# Ollama control

The historical roster scripts used Ollama directly. At Phase 0 inventory, the binary and downloaded models were absent and port 11434 was unavailable. Homebrew installed Ollama 0.34.0 for this experiment. No existing roster code or data was changed.

```sh
brew install ollama
ollama serve
```

Use the exact GGUF downloaded by Lemonade to hold local weights and quantization constant. Create a `Modelfile` containing `FROM /absolute/path/to/gemma-3-4b-it-Q4_K_M.gguf` and `PARAMETER num_ctx 4096`, then:

```sh
ollama create phase0-gemma3:4b-q4km -f /path/to/Modelfile
ollama show phase0-gemma3:4b-q4km
python3 -B tools/benchmark-harness/run.py --provider ollama \
  --model phase0-gemma3:4b-q4km --model-family gemma-3 --parameter-count 3.9B \
  --quantization Q4_K_M --runtime-version 0.34.0 --context 4096 \
  --context-limit 131072 --execution local --repetitions 2
```

Import autodetected `gemma3-instruct`; the model reports 3.9B parameters, 131072 maximum context and Q4_K_M. No multimodal projector was imported, because the workload uses text only. Although weights match Lemonade, templates, runtime defaults, prompt caching and multimodal loading differ. This is not a controlled runtime speed ranking.

The adapter uses `/api/chat`, `num_predict`, `num_ctx`, temperature and optional seed. It preserves native durations and derives generation throughput only from `eval_count` and `eval_duration`. Five-minute keepalive allows warm requests; first-call load is retained rather than hidden. Stop the temporary server after use. Do not add a login service unless needed.

Official import reference, checked 2026-09-16: https://docs.ollama.com/import
