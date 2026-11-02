# Claude Code loop engineering

Run [Claude_Code_Loops.ipynb](../Claude_Code_Loops.ipynb) from the repository root. Python 3.14.5, nbformat 5.11.1, nbclient 0.11.0 and ipykernel 7.4.0 were used.

The notebook executes actual Bash mkdir/touch setup in an owned temporary directory and tests `verify_loop.py` with deterministic fictional reports/state. Positive checks, missing-section rejection, forbidden final workspace changes, unchanged progress and symlinks are checked. This is a mechanical completion checker, not a Claude reasoning test or an enforcing sandbox. It does not prove that instructions were read or that a report is factually correct, and cannot detect a transient edit restored before the final snapshot.

No Claude model/session, actual Claude permission enforcement, `/loop`, `/goal`, scheduler, connector, message or external action was executed. The article's prompts, templates and optional commands remain manual instructions. `/loop` fixed schedules require a running session, can be restored on resume with documented exceptions, must be explicitly cancelled when finished, and expire after seven days. Branches alone are not separate working directories; use worktrees and actual security boundaries as appropriate.

All 111 complete original blocks are preserved in the notebook's nonexecuting appendix, including the malformed Markdown fence that is repaired in the public article.
