# Local OCR with SmolDocling

Run with Python 3.11 and the pinned requirements. The notebook uses the full official SmolDocling checkpoint on CPU, downloads the original article input image and performs real inference twice. It parses actual DocTags, checks the full slide body and exports Markdown/HTML to an owned temporary directory. The generated output omits the slide heading; no missing text is fabricated. No FlashAttention, API key or paid GPU is required.

Part 2 remains in the selected publishing queue; add its local blog/notebook links when published.

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Building Local OCR Application SmolDocling: A Step-by-Step Guide [Part 1]](https://todatabeyond.com/blog/building-local-ocr-application-smoldocling-a-step-by-step-guide-part-1) | [Notebook](./SmolDocling_OCR_1.ipynb) |

Each notebook preserves every original archive code block and transcript in a nonexecuting Markdown appendix. Committed notebooks contain no saved outputs or credentials.
