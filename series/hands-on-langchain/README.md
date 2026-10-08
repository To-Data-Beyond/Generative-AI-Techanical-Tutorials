# Hands-On LangChain for LLM Applications Development

Companion notebooks for the Hands-On LangChain article series.

| Part | Article | Companion notebook |
| --- | --- | --- |
| 1 | [Document Loading](https://todatabeyond.com/blog/hands-on-langchain-for-llm-applications-development-documents-loading) | [Notebook](./Hands_On_LangChain_01_Document_Loading.ipynb) |
| 2 | [Document Splitting, Part 1](https://todatabeyond.com/blog/hands-on-langchain-for-llm-applications-development-documents-splitting-part-1) | [Notebook](./Hands_On_LangChain_02_Document_Splitting_Part_1.ipynb) |
| 3 | [Document Splitting, Part 2](https://todatabeyond.com/blog/hands-on-langchain-for-llm-applications-development-documents-splitting-part-2) | [Notebook](./Hands_On_LangChain_03_Document_Splitting_Part_2.ipynb) |
| 4 | [Vector Database & Text Embeddings](https://todatabeyond.com/blog/hands-on-langchain-for-llm-applications-development-vector-database-text-embeddings) | [Notebook](./Hands_On_LangChain_04_Vector_Databases_Text_Embeddings.ipynb) |
| 5 | [Information Retrieval](https://todatabeyond.com/blog/hands-on-langchain-for-llm-applications-development-information-retrieval) | [Notebook](./Hands_On_LangChain_05_Information_Retrieval.ipynb) |

The notebooks create their own local sample files and verify their default paths
without API keys. Parts 2 and 3 use current `langchain-text-splitters` APIs to
cover character, recursive, token, PDF, and Markdown header-aware splitting.
Additional series notebooks will be added as their complete archive articles are
published.

Part 4 downloads the pretrained all-MiniLM-L6-v2 model on its first run and uses
local inference with a persistent Chroma database. Assertions verify semantic
relationships, three retrieval queries, duplicate removal, metadata filtering,
and reopening the database. Its optional hosted appendix preserves the complete
updated OpenAI/PDF workflow; enable it only after supplying an OpenAI key and the
three CS229 PDFs. Hosted model calls may incur charges, and the historical blog
outputs are not claimed as reproduced by the local example.

Part 5 uses the same pretrained local model and Chroma to verify similarity
search, MMR diversification, source filtering, and persistence. Scripted
`FakeListLLM` responses test real self-query parsing, filter translation, and
compression composition without paid calls; these are integration tests, not
live model reasoning. Its complete hosted appendix requires `OPENAI_API_KEY`,
`OPENAI_CHAT_MODEL`, and the three CS229 PDFs, and was not executed live. Rankings
and MMR diversity depend on the selected model and parameters; MMR is not a
guaranteed duplicate-removal algorithm.
