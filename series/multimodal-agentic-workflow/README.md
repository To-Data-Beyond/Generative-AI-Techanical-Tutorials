# Multimodal Agentic Application with CrewAI

## Series contents

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Architecture and setup](https://todatabeyond.com/blog/building-a-multimodal-agentic-application-with-crewai-part-1) | [Part_1_Setup.ipynb](./Part_1_Setup.ipynb) |
| 2 | [Tools and the complete workflow](https://todatabeyond.com/blog/building-a-multimodal-agentic-application-with-crewai-part-2) | [Part_2_Workflow.ipynb](./Part_2_Workflow.ipynb) |

## Run locally

Use Python 3.13. From this directory:

```bash
python -m venv crew-venv
source crew-venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.\crew-venv\Scripts\activate` instead.
Open Part 1 first, then run Part 2 in order. Notebooks have no saved outputs.
They import the adjacent application files (or locate them from the repository
root); do not copy an individual notebook away from its series files.

Copy `.env.example` to your ignored `.env`, replace the placeholder locally,
and set `RUN_OPENAI=1` only when you intend to make paid routing/vision calls.
The default routing and vision model is `gpt-5.4-mini`. Model names and base URLs
are configurable separately; compatible providers must support the required
structured outputs, tool calls and image inputs. No other provider is implied
to have been exercised. Do not commit keys or upload private images.

The default notebook path still runs local CPU image/speech and free search;
hosted cells make no requests without opt-in. From a configured shell:

```bash
python main.py "Search the web for Python programming language official documentation"
python main.py "Describe the attached image" --image /path/to/image.png
```

## Model and result contracts

- TinySD: official `segmind/tiny-sd`, revision
  `cad0bd7495fa6c4bcca01b19a723dc91627fe84f`, CreativeML Open RAIL-M.
- English speech: official `facebook/mms-tts-eng`, revision
  `c71de0fe7204c83f1c10820a7d696d0b450048ba`, CC-BY-NC-4.0
  (noncommercial; review the model card before other reuse).
- Both models download on first use and run locally on CPU. Their checkpoints
  are not included in Git. The original TinySD pipeline has no bundled safety
  checker; do not treat this demonstration as a public-content safety system.
- A request selects one of four capabilities. Compound/unsupported requests
  stop; invalid routes never become an implicit web search.
- The execution tool owns no user-controlled shell, arbitrary URL fetch or
  filesystem-write destination. It accepts only a controller-bound request and
  writes generated files to its result directory. Describe only local validated
  PNG/JPEG files (5 MB / four-million-pixel bounds).
- Text-to-speech speaks the supplied request string; there is no extra model
  rewrite extracting or editing the narration.
- Failures clear the result and repeated execution is rejected. The controller
  returns actual helper data, not the executor model's claimed result.

## Original archive appendix

Both notebooks retain all original code in nonexecuting Markdown appendices,
including the historical Groq/Replicate/Tavily integration. Original figures
are preserved in `original-assets/`; the old feature is not used by the website.
This is a completed two-part series, not a promise of a missing Part 3.
