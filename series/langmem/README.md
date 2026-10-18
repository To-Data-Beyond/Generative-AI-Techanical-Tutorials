# Managing Agentic Memory with LangMem

A five-part series about an email assistant with semantic, episodic, and
procedural memory, built with LangGraph and LangMem.

## Series contents

| Part | Article | Companion status |
| --- | --- | --- |
| 1 | [Introduction to Agentic Memory](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-part-1-introduction-to-agentic-memory) | Conceptual introduction; no executable code in the source article |
| 2 | [Building a Baseline Agent](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-2-5-building-baseline-agent) | [Notebook](./LangMem_02_Baseline_Email_Agent.ipynb) · [Python](./baseline_agent.py) · [Tests](./test_baseline_agent.py) |
| 3 | [Assistant Agent with Semantic Memory](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-part-3-assistant-agent-with-semantic-memory) | [Notebook](./LangMem_03_Semantic_Memory.ipynb) · [Python](./semantic_memory_agent.py) · [Tests](./test_semantic_memory_agent.py) |
| 4 | [Building an Agent with Semantic and Episodic Memory](https://medium.com/@yousefhosni/managing-agentic-meomery-with-langmem-4-5-building-agent-with-semantic-episodic-memory-f1c892df97b1) | On Medium; website publication and maintained notebook pending |
| 5 | [Building an Agent with Semantic, Episodic, and Procedural Memory](https://medium.com/@yousefhosni/building-agent-with-semantic-episodic-procedural-memory-8f481aee9614) | On Medium; website publication and maintained notebook pending |

Part 1 explains the memory types and hot-path/background update strategies. It
does not contain code, so there is no Part 1 notebook or code-execution claim.
Future maintained notebooks belong in this folder and must be added to this
table when published; do not link to nonexistent notebooks.

## Part 2: runnable baseline

The notebook contains the complete maintained workflow and runs without API keys
by default, using explicitly scripted model fixtures with real LangChain,
LangGraph, schema validation, and sandbox tools. Nine tests exercise all routing
branches, input aliases, invalid schemas, stateless invocations, tool validation,
the calendar/meeting loop, and real OpenAI SDK request/parsing via a **mocked HTTP
transport**. These are integration tests, not live model reasoning.

The final notebook section also runs actual CPU `google/flan-t5-small` triage
inference and exposes its observed successes/failures. First use downloads public
model weights. The small model is not a production tool-calling replacement.

Run the Python workflow and regression suite from this folder:

```bash
pip install langchain==1.2.12 langchain-core==1.6.8 langgraph==1.1.2 langchain-openai==1.7.0 pydantic==2.14.0 python-dotenv==1.2.4 httpx
python baseline_agent.py
LANGMEM_RUN_HOSTED=0 python -m unittest -v test_baseline_agent
```

For optional hosted execution, configure `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL`,
and `LANGMEM_RUN_HOSTED=1` locally. Never paste secrets into chat or commit `.env`
files. The hosted path is not claimed as execution-tested without those keys.
All tools remain sandbox-only: no emails are sent and no meetings are booked.
Save notebooks without credentials, execution counts, or outputs.

## Part 3: semantic memory

The complete notebook runs actual LangMem create/search/update/delete tools,
LangGraph agents and a real vector index with CPU pretrained
`sentence-transformers/all-MiniLM-L6-v2` embeddings (384 dimensions). First use
downloads public weights; `SEMANTIC_MODEL_CACHE` can point to an existing cache.
Agent decisions/final replies are explicit scripted fixtures, not learned chat
inference. Thirteen execution-tested regressions cover real paraphrase retrieval,
independent calls, namespace isolation, CRUD/invalid actions, missing user ID,
duplicates, non-durability, and the complete first-email/follow-up flow.

```bash
pip install langmem==0.0.30 langchain==1.2.12 langchain-core==1.4.8 langgraph==1.1.2 langchain-openai==1.1.11 pydantic==2.13.4 python-dotenv==1.2.2 sentence-transformers==5.1.2 transformers==4.57.3 torch==2.10.0
LANGMEM_RUN_HOSTED=0 python semantic_memory_agent.py
LANGMEM_RUN_HOSTED=0 python -m unittest -v test_semantic_memory_agent
```

The in-memory store survives separate calls **only while that same store object
exists**, not process restarts. Namespace tests are not authentication tests:
production must derive user IDs from a trusted authenticated backend. Memory can
be wrong, poisoned or duplicated; it is not evidence that an action occurred.
All email/calendar tools remain sandbox-only. Hosted chat and OpenAI embeddings
are opt-in via the environment variables above and are **not execution-tested**
without configured credentials. The notebook includes every definition inline;
no sibling-module import is needed. Commit no saved outputs or credentials.

When each remaining article is published on todatabeyond.com, replace its
temporary Medium URL here and in every published website article in the series.
The original Medium slugs intentionally retain their historical spelling.

## References

- [Official LangMem concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/)
- [Official LangMem documentation](https://langchain-ai.github.io/langmem/)

Memory in this series is managed by the application, not a change to model
weights. Production applications need user isolation, permission checks,
retention/deletion rules, and validation of memory extracted from untrusted
email content. Human-memory terminology is an analogy, not a guarantee of
human-like cognition or accurate recall.
