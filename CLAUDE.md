# CLAUDE.md

The working conventions for this repository live in **[AGENTS.md](AGENTS.md)** — read it in
full before starting any task. This file exists only to point you there and to repeat the
rules most often gotten wrong.

## Non-negotiables

- **Never push to `main`.** GitBook Git Sync owns `main` (bidirectional). Work on
  `agent/<slug>` branches and merge to `development`. See [prompts/agent-router.md](prompts/agent-router.md).
- **One ROADMAP item per session.** Pick the first unchecked item in
  [ROADMAP.md](ROADMAP.md); implement exactly that; open exactly one PR against `development`.
- **Read the spec first.** For any `.kiro/specs/course-2026-refresh/tasks.md` sub-task,
  read that spec's `requirements.md` and `design.md` before writing. Rewriting an existing
  page also requires reading its `course-content-audit.md` notes.
- **Single source of truth.** Link to `docs/reference/models.md` (model IDs) and
  `docs/reference/contract.md` (Lambda schema) — never embed copies. Python is 3.12.
- **Voice.** No emoji, no AI-chat artifacts, no "optional" headings (use `(advanced —
  skim)`), no Create React App. Project pages follow the six-heading pedagogy template with
  no complete solution code.
- **Finish the loop.** On completion, tick the `ROADMAP.md` checkbox (with the PR number)
  and the matching `tasks.md` checkboxes before merging.
