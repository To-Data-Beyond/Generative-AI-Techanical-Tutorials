# LLM Preference Tuning

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Visual Guide to RLHF and PPO](https://todatabeyond.com/blog/visual-guide-to-llm-preference-tuning-with-rlhf-and-ppo) | Conceptual article |
| 2 | [Direct Preference Optimization](https://todatabeyond.com/blog/hands-on-direct-preference-optimization-from-ppo-to-dpo) | [CPU DPO notebook](./Direct_Preference_Optimization.ipynb) |

Python 3.13: `python -m pip install -r requirements.txt`. Run all cells in order.
The complete official Apache-2.0 SmolLM2-135M-Instruct checkpoint is pinned at
`12fd25f77366fa6b3b4b768ec3050bf629380bac`; model weights download on first use.
No API key, paid inference, GPU, hosted trace or model upload is needed.
The notebook has no saved outputs and preserves the complete original draft
through [Original_DPO_Draft.md](./Original_DPO_Draft.md) and its original figures.

Eight author-created training pairs and two disjoint held-out prompts illustrate
completion-token masking, detached fixed-reference scores, stable DPO loss,
230400 trainable LoRA parameters, twelve CPU updates and adapter save/reload.
The executed training loss decreases but held-out loss worsens; this tiny
exercise is not a model-quality benchmark, PPO implementation or reproduction
of the original DPO paper's experiments. No arithmetic accuracy gain is claimed.
