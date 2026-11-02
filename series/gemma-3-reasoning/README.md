# Gemma 3 reasoning fine-tuning series

These notebooks retain the complete original Google Gemma 3 4B checkpoint and original datasets. Configure approved Hugging Face access locally; never paste credentials into notebooks. No Hub uploads run. On the tested local path, native nested NF4 linear weights plus bfloat16 unquantized weights keep storage near 3.2GB; float32 quantized-linear compute and float32 adapters run on MPS, with a CPU fallback. Four genuine QLoRA optimizer updates use complete original examples, masked prompt/padding labels and a separately selected validation pair. This is a bounded training demonstration, not a clinical/financial accuracy benchmark or a full-epoch reproduction.

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Gemma 3 Reasoning Fine-Tuning Series #1: Medical Reasoning](https://todatabeyond.com/blog/gemma-3-reasoning-fine-tuning-crash-course-1-medical-reasoning) | [Notebook](./Gemma_3_Medical_Reasoning.ipynb) |
| 2 | [Gemma 3 Reasoning Fine-Tuning Series #2: Financial Reasoning](https://todatabeyond.com/blog/gemma-3-fine-tuning-crash-course-2-financial-reasoning-fine-tuning) | [Notebook](./Gemma_3_Financial_Reasoning.ipynb) |

Install requirements.txt with Python 3.11 and run cells in order. The original clinical query and first financial query remain generation examples, outside the selected training records. Financial target arithmetic is checked independently. Generated outputs may be truncated at the explicit 200-token budget; no clinical correctness or EOS-completion guarantee is made. Original code/transcripts remain verbatim in nonexecuting appendices. Committed notebooks are output-free.
