# Lemonade developer challenge candidate material

Working title: A reproducible SMB knowledge-assistant evaluation across inference runtimes.

Contribution: a dependency-free harness with synthetic policy evidence, explicit hallucination/ambiguity cases, native Ollama metric preservation and OpenAI-compatible Lemonade/NIM adapters. Lemonade ran Gemma 3 4B through llama.cpp Metal on an existing Apple M4. Full reproducibility instructions and negative results accompany the implementation.

Evidence: [provider setup](README.md), [methodology](../../docs/methodology/phase0.md), [actual findings](../../docs/findings/phase0.md), and recorded Lemonade run `20260916T212250Z-lemonade-f0504f31`.

Developer/community usefulness: adding another runtime does not require rewriting business inputs or evaluation criteria. Honest format and grounding failures demonstrate why API text output alone is insufficient.

Limitations: no Ryzen AI, AMD GPU/NPU or hardware-efficiency claim. No comparative winner claim. No challenge submission has been made. Current eligibility, deadline and submission requirements have not been verified in this implementation; this is derivable candidate material, not a claim of eligibility or acceptance.
