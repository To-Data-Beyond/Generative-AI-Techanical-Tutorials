# Agentic RAG with DeepSeek R1

Run both notebooks with Python 3.11 and a local Ollama server. Install the pinned requirements, start `ollama serve`, then pull `deepseek-r1:1.5b` and `embeddinggemma`. The model is the actual distilled Qwen 1.5B variant; embeddings use a separate model. No API key is needed. Part 2 imports the complete `rag_runtime.py` in this folder.

Real free search needs network access. Current New York weather comes from timestamped NWS evidence, not a saved fixture. An unavailable/stale source raises an error. Small-model routing/grading is fallible; the controller bounds retries and returns source sentences with citations. Stop your local Ollama service after use.

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Building Agentic RAG Application with DeepSeek R1 — A Step-by-Step Guide [Part 1]](https://todatabeyond.com/blog/building-agentic-rag-application-with-deepseek-r1-a-step-by-step-guide-part-1) | [Notebook](./DeepSeek_Agentic_RAG_1.ipynb) |
| 2 | [Building Agentic RAG Application with DeepSeek R1 — A Step-by-Step Guide [Part 2]](https://todatabeyond.com/blog/building-agentic-rag-application-with-deepseek-r1-a-step-by-step-guide-part-2) | [Notebook](./DeepSeek_Agentic_RAG_2.ipynb) |

Each notebook preserves every original archive code block and transcript in a nonexecuting Markdown appendix. Committed notebooks contain no saved outputs or credentials.
