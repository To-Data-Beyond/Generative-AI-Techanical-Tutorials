# Cloudflare Browser Run for LLM pipelines

Run [Cloudflare_Browser_Rendering.ipynb](../Cloudflare_Browser_Rendering.ipynb) from the repository root in an isolated Python environment:

```bash
python -m pip install -r cloudflare-browser-rendering/requirements.txt
```

The default notebook fetches public example.com and checks local HTML/Markdown parsing, same-origin links, request serialization, JSON schemas, crawl polling, failures, timeouts and pagination. Fixture responses are not live Cloudflare results. No Cloudflare account or token was available for this review, and no Cloudflare service call or remote CDP session was executed.

For your own opt-in live run, configure `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` and `RUN_CLOUDFLARE=1` locally. These requests can incur Browser Run and Workers AI charges. Never commit credentials. Review access rights, robots/content signals and provider pricing before acquisition. The source allow-list is deliberately narrow, not a general SSRF sandbox. A client polling timeout does not cancel a remote job: inspect or cancel that exact job explicitly.

`browser_rendering.py` uses the documented `/browser-run/` endpoint and `response_format.json_schema`. `browser_session.mjs` is an optional CDP example, syntax-checked only. It requires `playwright-core` and Cloudflare access; it navigates to a real main element instead of assuming example.com has a search form. It closes its browser in `finally`.

Every original code block and original source output remains in the notebook's nonexecuting Markdown appendix. The historical top-level notebook is maintained in place rather than duplicated.
