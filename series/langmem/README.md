# Managing Agentic Memory with LangMem

A five-part series about an email assistant with semantic, episodic, and
procedural memory, built with LangGraph and LangMem.

## Series contents

| Part | Article | Companion status |
| --- | --- | --- |
| 1 | [Introduction to Agentic Memory](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-part-1-introduction-to-agentic-memory) | Conceptual introduction; no executable code in the source article |
| 2 | [Building a Baseline Agent](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-2-5-building-baseline-agent) | [Notebook](./LangMem_02_Baseline_Email_Agent.ipynb) · [Python](./baseline_agent.py) · [Tests](./test_baseline_agent.py) |
| 3 | [Assistant Agent with Semantic Memory](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-part-3-assistant-agent-with-semantic-memory) | [Notebook](./LangMem_03_Semantic_Memory.ipynb) · [Python](./semantic_memory_agent.py) · [Tests](./test_semantic_memory_agent.py) |
| 4 | [Building an Agent with Semantic and Episodic Memory](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-part-4-semantic-and-episodic-memory) | [Notebook](./LangMem_04_Semantic_Episodic_Memory.ipynb) · [Python](./episodic_memory_agent.py) · [Tests](./test_episodic_memory_agent.py) |
| 5 | [Building an Agent with Semantic, Episodic, and Procedural Memory](https://todatabeyond.com/blog/managing-agentic-memory-with-langmem-part-5-semantic-episodic-procedural-memory) | [Notebook](./LangMem_05_Semantic_Episodic_Procedural_Memory.ipynb) · [Python](./procedural_memory_agent.py) · [Tests](./test_procedural_memory_agent.py) |

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

## Part 4: reviewed episodic examples

The complete notebook executes real MiniLM embeddings, indexed example retrieval,
LangMem semantic tools and LangGraph routing. Chat classifications/replies are
explicit scripted fixtures. All fifteen regression tests passed, including the
source's `harrison`/`Youssef` mismatch, the corrected feedback flow, user scoping,
a real paraphrase retrieval, invalid/unreviewed/conflicting labels, deletion,
JSON formatting/truncation, and separate examples/semantic collections.

Use the Part 3 dependency installation above, then run:

```bash
LANGMEM_RUN_HOSTED=0 python episodic_memory_agent.py
LANGMEM_RUN_HOSTED=0 python -m unittest -v test_episodic_memory_agent
```

Feedback changes retrieved context, not model weights. The fixture's initial
sales-email response is deliberately illustrative, not a recommended anti-spam
policy or proof of live-model behaviour. The score threshold is uncalibrated;
one paraphrase test is not a robustness benchmark. Only reviewed classification
labels should influence triage; email text is untrusted data. The example helper
does synchronous manual insertion, not an automatic background learning loop.
RAM storage, namespaces, sandbox and hosted-path limitations remain as above.

## Part 5: reviewed procedural updates

The self-contained notebook completes the series with all nineteen maintained
source code placements and fifteen execution-tested regressions. It runs actual
MiniLM retrieval, LangMem CRUD, LangGraph and multi-prompt optimizer orchestration.
The optimizer's credit-assignment/rewrite responses and agent chat choices are
explicit scripted model fixtures, **not learned optimization or inference**.

Use the Part 3 installation above, then run from this folder:

```bash
LANGMEM_RUN_HOSTED=0 python procedural_memory_agent.py
LANGMEM_RUN_HOSTED=0 python -m unittest -v test_procedural_memory_agent
LANGMEM_RUN_HOSTED=0 python -m unittest -v test_baseline_agent test_semantic_memory_agent test_episodic_memory_agent test_procedural_memory_agent
```

The Python workflow reuses Part 4's maintained foundation (which also runs its
sandbox demo when imported); the notebook includes every definition inline and
needs no sibling files. Set SEMANTIC_MODEL_CACHE to reuse a model cache.

Updates match names, not result positions. Missing/duplicate/unknown/invalid
proposals and stale snapshots are rejected before writes. The same outer graph
reloads preferences on its next call. Default review is an explicit scripted
demo approval; hosted mode displays the full diff and requires typing APPLY.
This is not authenticated review, semantic safety validation, atomic compare-and-
swap, a database transaction, durable audit, rollback, or injection resistance.
Fixed safety instructions are outside the editable preference, but this does
not prove a model will obey them. Prompt changes do not update model weights.

**Do not deploy the source's blanket Alice-ignore rule:** it suppresses the
example's urgent outage report. The notebook reproduces only toy sandbox wiring;
production incident exceptions and human escalation are not implemented. Hosted
chat/optimizer/OpenAI embeddings remain opt-in and unexecuted. All action tools
remain sandbox-only; RAM contents disappear on restart. No credentials, outputs
or execution counts are saved in the notebook.

All five series entries now link to To Data & Beyond. Publish the companion
before the website article so its main-branch notebook link resolves.

## References

- [Official LangMem concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/)
- [Official LangMem documentation](https://langchain-ai.github.io/langmem/)

Memory in this series is managed by the application, not a change to model
weights. Production applications need user isolation, permission checks,
retention/deletion rules, and validation of memory extracted from untrusted
email content. Human-memory terminology is an analogy, not a guarantee of
human-like cognition or accurate recall.
