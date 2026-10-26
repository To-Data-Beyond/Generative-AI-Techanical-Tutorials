# Python Data Science Interview Series

Complete runnable examples for the three To Data & Beyond interview guides.
Run each notebook from top to bottom in a fresh Python 3.11 kernel. Setup cells
install pinned dependencies; no API keys or GPU are required. The deep-learning
notebook downloads the official ImageNet VGG16 backbone weights. All original
source code is preserved in nonexecuting Markdown appendices.

| Part | Article | Notebook | Colab |
| --- | --- | --- | --- |
| 1 — Python concepts | [Article](https://todatabeyond.com/blog/top-important-python-questions-for-data-science-interviews-conceptual-questions) | [Notebook](./01_Python_Concepts.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/python-data-science-interviews/01_Python_Concepts.ipynb) |
| 2 — Data cleaning and preprocessing | [Article](https://todatabeyond.com/blog/top-important-python-questions-for-data-science-interviews-data-cleaning-and-preprocessing) | [Notebook](./02_Data_Cleaning_Preprocessing.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/python-data-science-interviews/02_Data_Cleaning_Preprocessing.ipynb) |
| 3 — Machine and deep learning | [Article](https://todatabeyond.com/blog/top-important-python-questions-for-data-science-interviews-machine-and-deep-learning) | [Notebook](./03_Machine_Deep_Learning.ipynb) | [Open](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/python-data-science-interviews/03_Machine_Deep_Learning.ipynb) |

The notebooks contain 30, 67 and 16 executable cells respectively, including
independent regression checks. Committed outputs are cleared for readability.
The preprocessing examples define explicit missing-value, outlier, feature and
mixed-type classification data instead of requiring an unavailable local CSV.
Target encoding excludes each row’s target through out-of-fold calculation.
The VGG16 example uses 120 real bundled digit images, a frozen pretrained
backbone and ten training epochs of the new head; it is not a benchmark.
The callback example deliberately uses random labels to demonstrate callback
behavior, rather than to claim predictive performance.
