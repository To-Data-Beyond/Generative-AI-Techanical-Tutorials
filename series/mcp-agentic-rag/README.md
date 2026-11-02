# MCP-powered agentic RAG series

The host owns model decisions and answer generation. The MCP server exposes two
read-only evidence tools over real loopback Streamable HTTP. Durable local
Qdrant uses all ten original FAQ topics and the original pinned native Nomic
embedding model; Docker is not required by this small local path. No cloud
database, remote-code execution, hosted tracing or public server is enabled.

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [MCP foundations](https://todatabeyond.com/blog/building-mcp-powered-agentic-rag-application-step-by-step-guide-1-2) | [Notebook](./MCP_Agentic_RAG_1.ipynb) |
| 2 | [Tools, retrieval and the AI host](https://todatabeyond.com/blog/building-mcp-powered-agentic-rag-application-step-by-step-guide-2-2) | [Notebook](./MCP_Agentic_RAG_2.ipynb) |

Install requirements.txt with Python3.13, download the supplied files together,
and run cells in order from this series folder. Local model downloads and free
search/documentation requests require Internet access. Polars queries fetch its
official documentation live; other public topics use bounded DDGS search.
Unavailable evidence fails clearly rather than generating a fake search result.

Part2 makes paid OpenAI calls only after you configure OPENAI_API_KEY locally
and set RUN_OPENAI=1. The bounded host defaults to gpt-5.4-mini with four request
rounds and a conservative cumulative one-dollar ledger per session. Set
TEST_BUDGET_LEDGER to one shared owned path for tests/reruns; never reset it to
evade a budget. Review pricing before using another model. API keys must not be
stored in notebook cells or committed files. Only public teaching FAQ/docs text
is used here, not private documents. MCP is not a security or accuracy guarantee.

The notebook owns and stops its local servers. For interactive use, start
`mcp_server.py` on loopback, then use `rag_client.py` from another terminal.
The foundation server intentionally advertises no tools. Original complete
source code/transcripts remain in nonexecuting appendices. Committed notebooks
contain no outputs, keys, model weights or retrieved website dumps.
