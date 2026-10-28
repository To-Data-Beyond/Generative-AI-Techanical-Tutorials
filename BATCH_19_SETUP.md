# Batch 19: comparison and notebook collections

## Framework comparison

Open [LangChain vs LlamaIndex](./LangChain_vs_LlamaIndex.ipynb) and install the
exact packages listed at its top in a fresh Python 3.13 environment. Set
`OPENAI_API_KEY` locally, never in notebook cells; optional `MODEL` and
`EMBEDDING_MODEL` select your configured models. Tested models are
`gpt-5.4-mini` and `text-embedding-3-small`; actual API calls incur charges.
Run all six cells in order. The final regression cell verifies real retrieval,
context, named intermediate fields and tool execution. Model prose may vary.
Sales and feedback are fictional records; writes affect only a local dictionary.
The original four code blocks and original comparison table are in the appendix.

## Collections

- [Nine efficient-Python notebooks](./collections/efficient-python/README.md).
- [Six LangChain foundation notebooks](./collections/langchain-foundations/README.md).

Each has a separate contents table and Markdown-only index notebook. Canonical
notebooks stay in their existing folders: no duplicate copies. Open each actual
notebook and follow its own setup in a separate fresh environment, since their
dependencies differ. Package/model/data downloads may need internet.

The new [vectorized reward companion](./Pandas_Vectorized_Reward_Calculation.ipynb)
uses NumPy 2.3.3 / pandas 3.1.0 and all 10,000 seeded synthetic rows. It compares actual
timings without guaranteeing a 1000-fold gain, checks equality/boundaries and
preserves every original block in its appendix. It needs no API key.

The prompt/parsing/memory notebooks run local default paths; fixture-based
checks are not live hosted inference. Their hosted appendices are disabled by
default and were not enabled for this batch. Chains/agents/evaluation use real
OpenAI requests and incur charges. Early weather tools are fixed examples;
later web-search tools make read-only public requests. No remote database,
email, public dashboard, paid cloud deployment or unrestricted Python tool runs.

All 403 default-path code cells across the comparison and fifteen collection
targets were executed in fresh kernels. Original research/marketing claims and
historical performance figures are not certified as new measurements. Keep
upstream warnings visible and never commit credentials or saved outputs.
