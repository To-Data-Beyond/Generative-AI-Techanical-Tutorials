# Time Series with Python

Complete companion notebooks for the first three parts of the series. Start with setup, then run every cell in order in Python 3.11 or Colab. No API keys or GPU are required. Setup installs pinned packages and verifies downloaded historical datasets by SHA-256. Restart an already-used kernel before running.

## Contents

| Part | Article | Notebook | Colab |
| --- | --- | --- | --- |
| 1 | [Manipulating Time Series Data In Python](https://todatabeyond.com/blog/manipulating-time-series-data-in-python) | [01_Time_Series_Manipulation.ipynb](./01_Time_Series_Manipulation.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/01_Time_Series_Manipulation.ipynb) |
| 2 | [Time Series Data Analysis In Python](https://todatabeyond.com/blog/time-series-data-analysis-in-python) | [02_Time_Series_Analysis.ipynb](./02_Time_Series_Analysis.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/02_Time_Series_Analysis.ipynb) |
| 3 | [Time Series Data Visualization In Python](https://todatabeyond.com/blog/time-series-data-visualization-in-python) | [03_Time_Series_Visualization.ipynb](./03_Time_Series_Visualization.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/03_Time_Series_Visualization.ipynb) |

## Later parts

These existing archive articles have not yet been migrated in this batch. Their links will be changed to website routes when published.

- [Time Series Forecasting with ARIMA Models In Python [Part 1]](https://pub.towardsai.net/time-series-forecasting-with-arima-models-in-python-part-1-c2940a7dbc48)
- [Time Series Forecasting with ARIMA Models In Python [Part 2]](https://pub.towardsai.net/time-series-forecasting-with-arima-models-in-python-part-2-91a30d10efb0)
- [Machine Learning for Time Series Data [Regression]](https://pub.towardsai.net/machine-learning-for-time-series-data-in-python-regression-5e19fa2e7471)

## Data and maintenance

See [data provenance](./data/README.md). Setup uses the original author repository at immutable commit `65d4ae5d3436be3c0a921a3dcbda1b52e3ac8597`; the original 14 input files are not silently reduced. Missing GDP and annual temperature files use the documented public snapshots. The source multi-asset data are recovered from the original `price.csv`.

The index example uses the source-intended 2016 window, label-aligned company share counts and common observed benchmark dates. It is an educational historical construction, not a validated investment backtest. Amazon data are quarterly adjusted stock prices, not revenue. The temperature forecast is a univariate statistical exercise, not a physical climate projection.

All 136 code cells (69 manipulation, 21 analysis, 46 visualization) were executed in fresh Python 3.11.14 kernels. Final regression cells independently verify returns, window means, weighted-index calculations, OLS/ACF/AR recurrences, forecast means and intervals, seasonal decomposition and correlations. Notebooks remain output-free in Git. All 129 complete original embedded code blocks are retained verbatim in nonexecuting markdown appendices.
