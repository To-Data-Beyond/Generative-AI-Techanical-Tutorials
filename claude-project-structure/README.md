# Claude project structure companion

The notebook tests real formatter-hook processes on isolated, fictional files;
it does not change the current repository's `.claude` configuration or global
Claude settings. It validates JSON/frontmatter and original example structure.
No Claude model call or hosted agent execution is required or claimed.

To try the optional formatter in your own project, review the supplied files,
copy the Python and shell helpers into `.claude/hooks/`, merge the example
settings deliberately, and install the pinned Ruff version from the notebook.
PostToolUse runs after an edit: formatting does not undo an edit or constitute a
security sandbox. Permission entries cover matching Read operations, not every
possible way another tool or shell command could access a secret.

Directory trees and Markdown instruction/workflow examples are documentation,
not executable shell. Original code and prose examples remain in the notebook
appendix; runnable tests are separate and output-free in Git.
