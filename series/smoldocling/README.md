# Local OCR with SmolDocling

Run with Python 3.11 and the pinned requirements. The notebook uses the full official SmolDocling checkpoint on CPU, downloads the original article input image and performs real inference twice. It parses actual DocTags, checks the full slide body and exports Markdown/HTML to an owned temporary directory. The generated output omits the slide heading; no missing text is fabricated. No FlashAttention, API key or paid GPU is required.

Part 2 supplies app.py with cached local inference, validated five-megabyte image uploads, safe Markdown and isolated per-session results. Run it with streamlit run app.py --server.address=127.0.0.1 --browser.gatherUsageStats=false. Its notebook exercises real OCR via Streamlit AppTest and a separate actual loopback HTTP server. Browser file-transfer testing is not claimed.

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Building Local OCR Application SmolDocling: A Step-by-Step Guide [Part 1]](https://todatabeyond.com/blog/building-local-ocr-application-smoldocling-a-step-by-step-guide-part-1) | [Notebook](./SmolDocling_OCR_1.ipynb) |
| 2 | [Building Local OCR Application SmolDocling: Part 2](https://todatabeyond.com/blog/building-local-ocr-application-smoldocling-a-step-by-step-guide-part-2) | [Notebook](./SmolDocling_OCR_2.ipynb) |

Each notebook preserves every original archive code block and transcript in a nonexecuting Markdown appendix. Committed notebooks contain no saved outputs or credentials.
