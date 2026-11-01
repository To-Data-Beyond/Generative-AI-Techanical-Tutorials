# Hands-On LangSmith Series

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Part 1: What Is LangSmith?](https://todatabeyond.com/blog/hands-on-langsmith-course-1-7-what-is-langsmith) | Conceptual introduction |
| 2 | [Part 2: Tracing with LangSmith](https://todatabeyond.com/blog/hands-on-langsmith-series-2-tracing-with-langsmith) | [Notebook](./LangSmith_2_Tracing.ipynb) |
| 3 | [Part 3: Playground & Prompts Hub](https://todatabeyond.com/blog/hands-on-langsmith-series-3-playground-and-prompts-hub) | [Notebook](./LangSmith_3_Prompts_and_Playground.ipynb) |

Only Parts 1–3 have published article material in this archive selection; this
is not a claim that all seven originally planned parts are available.

## Running the notebooks

Use the pinned installation command in each notebook, then configure
`OPENAI_API_KEY` and `LANGSMITH_API_KEY` locally. `MODEL` defaults to
`gpt-5.4-mini`. Never commit credentials or paste them into a notebook cell.
These examples incur model charges and send tutorial queries, search snippets
and generated guides to LangSmith. Do not use confidential inputs. Each run
creates a uniquely named private tracing project; Part 3 also creates a private
prompt with two commits. No public prompt/run sharing is enabled.

Part 2 checks the actual hosted hierarchy and API token counts. Part 3 pins
real prompt commits, uses the same freshly retrieved snippets for both
revisions and verifies rollback. The Canvas screenshots illustrate the UI;
the reproducible version edit is performed through the SDK, not a claimed
automated UI or optimizer execution. Free search availability can vary; errors
raise after bounded attempts instead of inventing recipe context.

Original archive code and transcripts remain in nonexecuting appendices.
Committed notebooks contain no saved outputs. Keep private test artifacts
private and delete only your own test projects/prompts if you no longer need them.
