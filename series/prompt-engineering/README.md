# Prompt Engineering

Runnable companions for the published articles. Start with the foundational
Parts 1–2, then explore iterative prompt development using the contents below.

| Article | Website | Notebook | Colab |
| --- | --- | --- | --- |
| Prompt Engineering Best Practices for Instruction-Tuned LLM [Part 1] | [Article](https://todatabeyond.com/blog/prompt-engineering-best-practices-for-instruction-tuned-llm-part-1) | [Notebook](./01_Clear_Instructions.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/prompt-engineering/01_Clear_Instructions.ipynb) |
| Prompt Engineering Best Practices for Instruction-Tuned LLM [Part 2] | [Article](https://todatabeyond.com/blog/prompt-engineering-best-practices-for-instruction-tuned-llm-part-2) | [Notebook](./02_Task_Decomposition_and_Hallucinations.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/prompt-engineering/02_Task_Decomposition_and_Hallucinations.ipynb) |
| Prompt Engineering Best Practices: Iterative Prompt Development | [Article](https://todatabeyond.com/blog/prompt-engineering-best-practices-iterative-prompt-development) | [Notebook](./03_Iterative_Prompt_Development.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/prompt-engineering/03_Iterative_Prompt_Development.ipynb) |
| Prompt Engineering Best Practices: Text Summarization & Information Retrieval | [Article](https://todatabeyond.com/blog/prompt-engineering-best-practices-text-summarization-and-information-retrieval) | [Notebook](./04_Summarization_and_Extraction.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/prompt-engineering/04_Summarization_and_Extraction.ipynb) |
| Prompt Engineering Best Practices: Textual Inference & Sentiment Analysis | [Article](https://todatabeyond.com/blog/prompt-engineering-best-practices-textual-inference-and-sentiment-analysis) | [Notebook](./05_Inference_and_Sentiment.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/prompt-engineering/05_Inference_and_Sentiment.ipynb) |
| Prompt Engineering Best Practices: Text Transforming & Translation | [Article](https://todatabeyond.com/blog/prompt-engineering-best-practices-text-transforming-and-translation) | [Notebook](./06_Translation_and_Transformation.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/prompt-engineering/06_Translation_and_Transformation.ipynb) |

## Setup

Tested with Python 3.13.7 and OpenAI 2.43.0. In a dedicated environment install:

```bash
python -m pip install openai==2.43.0 python-dotenv==1.2.2 bleach==6.4.0 beautifulsoup4==4.14.3 redlines==0.6.2 Markdown==3.10
```

Set `OPENAI_API_KEY` in the environment or an uncommitted local `.env` before
starting the kernel; never put keys in notebook cells. Set `MODEL` to your
compatible model if needed (tested/default: `gpt-5.4-mini`). All calls incur
charges and use bounded output with SDK retries disabled. In Colab, set the
environment variable privately before running the setup cell.

## Scope and actual validation

The first three notebooks’ 24 code cells passed in fresh kernels (7/7/10) with actual OpenAI calls:
JSON parsing and three book records, tea/no-instructions branches, few-shot
style, two-name French summaries, direct/formatted math checks, unsupported
product claims, short product descriptions, source-grounded IDs and HTML.
The word-limited description contained 40 words. Both math prompts identified
the incorrect student formula. An independent Python check verifies
`360x + 100,000` at several areas. The source fact sheet has no Product IDs;
the maintained refinement refuses to invent them. HTML is cleaned using a
restricted allowlist before display; regressions reject active tags/attributes
and check all three dimensions against the source values.

Model-generated prose is captured output, not a verified product catalog or
universal reliability guarantee. Delimiters alone do not prevent prompt
injection. Explicit task steps are inspectable outputs, not control over
private model reasoning. These distinctions match the maintained articles.

All 25 source pre blocks and 48 original quote/transcript blocks remain
verbatim in nonexecuting appendices, including historical SDK code and old
outputs. Committed notebooks are output-free. The articles carry actual fresh
outputs; prompts, counts and wording can produce different results on reruns.


## Summarization, inference and transformation

The next three complete companions passed 36 code cells in fresh Python 3.13.7
kernels (9/13/14), with actual configured OpenAI calls. All four original movie
reviews, five multilingual support messages and seven grammar examples remain.
The summarization checks measure the requested 30/20-word limits. Inference
checks sentiment, anger, extraction fields and five topic flags; invalid JSON,
wrong flag counts/types and both local NASA-alert branches are tested.
Transformation checks all five source languages and Arabic-script output, three
exact reserved-address table rows, grammar cases and real Redlines diffs.
Generated HTML, diff spans/styles and Markdown-derived HTML are cleaned before
display. No email is sent; addresses are reserved example.invalid demonstrations.

The topic prompt was clarified after one result exceeded its two-word label
limit. The grammar prompt now distinguishes surrounding quotation marks from
necessary punctuation inside a sentence; valid expanded contractions are
accepted alongside contractions. Full notebooks were rerun after those fixes.
All 37 original pre blocks and 44 transcripts remain in nonexecuting appendices.
These three notebooks are output-free in Git; the articles show actual captured
results. Automated checks do not certify universal translation or APA compliance.
