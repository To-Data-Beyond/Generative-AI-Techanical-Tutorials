# Data Structures for Data Science Coding Interviews

Complete runnable companions for the two-part To Data & Beyond series.

## Table of contents

| Part | Topics | Article | Notebook | Run |
| --- | --- | --- | --- | --- |
| 1 | Arrays, linked lists, stacks, queues, trees and graphs | [Part 1](https://todatabeyond.com/blog/foundations-of-data-structures-essential-concepts-for-data-science-coding-interviews-part-1) | [01_Arrays_To_Graphs.ipynb](./01_Arrays_To_Graphs.ipynb) | [Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/data-structures-interviews/01_Arrays_To_Graphs.ipynb) |
| 2 | Hashing, heaps, tries, sets/maps, dynamic programming and union-find | [Part 2](https://todatabeyond.com/blog/foundations-of-data-structures-essential-concepts-for-data-science-coding-interviews-part-2) | [02_Hashing_To_Union_Find.ipynb](./02_Hashing_To_Union_Find.ipynb) | [Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/data-structures-interviews/02_Hashing_To_Union_Find.ipynb) |

## Running

Python 3.11 or newer, standard library only. No keys, external datasets or GPU.
Run each notebook from top to bottom in its own fresh kernel. Each example
includes actual use; final cells run independent correctness regressions.
The blocking-queue test uses a bounded producer thread and closes it before
finishing. The queue-prefix reversal example assumes exclusive access to its
queue, rather than concurrent mutation.

Original archive code is preserved verbatim in nonexecuting Markdown appendices.
Maintained examples contain the approved correctness repairs; notebook outputs
and execution counts are cleared for version control.

Related guide: [Coding interview expectations](https://todatabeyond.com/blog/what-to-expect-in-a-data-science-coding-interview)
and [its notebook](../../Coding_Interview_Expectations.ipynb).
