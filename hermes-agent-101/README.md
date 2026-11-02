# Hermes Agent 101: isolated persistence walkthrough

Pinned official source: [NousResearch/hermes-agent, 8e6feea9](https://github.com/NousResearch/hermes-agent/tree/8e6feea936883b84125f671cfdc88888e3d2f5ca), MIT licensed. Python 3.14.5 was tested on macOS; the cost guard uses POSIX fcntl. This is not a Windows execution claim.

From the companion repository root:

```bash
uv venv --python 3.14 .venv
uv --no-config pip install --python .venv/bin/python --overrides hermes-agent-101/overrides.txt -r hermes-agent-101/requirements.txt
```

Use that environment's kernel for [Hermes_Agent_101.ipynb](../Hermes_Agent_101.ipynb). The overrides match the pinned project's own published UV overrides; ordinary pip resolution otherwise conflicts on Pillow 12.3 versus 13.0. The installed runtime uses OpenAI 2.54.0. No global installer/postinstall, browser/computer driver or service was started.

Default checks create an owned temporary `HERMES_HOME`, two native profiles without shell aliases or bundled skills, native memory writes/reload and native skill discovery/loading. OS HOME is unchanged. Profiles separate state, not filesystem permissions. Current config clones can copy curated MEMORY.md/USER.md; inspect cloned state and credentials deliberately.

Paid tests are opt-in: configure `OPENAI_API_KEY`, `RUN_OPENAI=1` and one persistent `TEST_BUDGET_LEDGER` path locally. `guarded_openai.py` permits only non-streamed, text-only gpt-5.4-mini inference to the explicit OpenAI origin, with capped output and cumulative conservative reservations up to $1. Failed requests retain reservations. Do not reset the ledger between attempts. Review model prices before changing it. The harness disables other requests-based networking; it is not a general network/OS sandbox.

Fresh real tests used the native AIAgent memory tool and a new agent instance recalling saved conventions. Only memory tools were advertised. Streaming is disabled for complete usage accounting; the notebook restores IPython's stdout/stderr after the native agent replaces its stream wrappers. No mocked model responses or saved answers are substituted.

No external memory provider, GEPA run, Curator maintenance, live research browsing, session-history search, terminal/code-edit agent task, Telegram/bot, gateway, cron job, message, public upload or hosted trace was tested. These article sections remain manual workflows, not newly executed integrations. Every original block and quotation stays in the nonexecuting notebook appendix. Never put secrets into memory or notebook outputs.
