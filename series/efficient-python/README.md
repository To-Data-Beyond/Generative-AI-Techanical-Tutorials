# Efficient Python for Data Scientists

Complete companion notebooks for the two-part efficiency series. Run cells in
order in a Python 3.11+ IPython kernel. CPU only; no API keys or GPU required.
Timing measurements vary across machines and runs.

| Part | Article | Notebook | Colab |
| --- | --- | --- | --- |
| 1 | [Defining & Measuring Code Efficiency](https://todatabeyond.com/blog/write-efficient-python-code-for-data-scientists-defining-and-measuring-code-efficiency) | [Notebook](./Python_Efficiency_Measurement.ipynb) | [Open in Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/efficient-python/Python_Efficiency_Measurement.ipynb) |
| 2 | [Optimizing Your Code](https://todatabeyond.com/blog/write-efficient-python-code-for-data-scientists-optimizing-your-code) | [Notebook](./Python_Code_Optimization.ipynb) | [Open in Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/efficient-python/Python_Code_Optimization.ipynb) |

Part 1 installs pinned NumPy, psutil, line_profiler and memory_profiler and creates
a temporary source module for real memory profiling. Part 2 installs pinned
NumPy, pandas and certifi, then downloads the original Pokémon and baseball CSVs
from an immutable author-repository commit with HTTPS and SHA-256 verification.
Both contain regression tests; outputs and execution counts are intentionally
cleared before committing. No benchmark ranking is asserted.

The root `Python_Efficiency_Measurement.ipynb` remains a byte-identical
compatibility mirror so existing GitHub and Colab links keep working. Maintain
it alongside the canonical copy in this folder.
