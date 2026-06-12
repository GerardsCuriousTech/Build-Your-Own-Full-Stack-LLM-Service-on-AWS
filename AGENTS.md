# AGENTS.md — Repository Guide for AI Agents

## Project Overview

**Build Your Own Full Stack LLM Service on AWS** is a GitBook-published course. The
content is the product; there is no application runtime. Deliverables are Markdown
pages, CI scripts, and YAML config.

This repository is the **source of truth**. GitBook Git Sync operates **bidirectionally
on the `main` branch** — GitBook can write commits to `main`, and commits you push to
`main` publish to the book. Autonomous agents therefore **never push to `main`**: work
on `agent/<slug>` branches and merge into `development` (see `prompts/agent-router.md`).
A human merges `development` → `main` deliberately.

Detailed requirements, designs, and tasks live in `.kiro/specs/**/*.md`. Whenever you
work a task from a `.kiro/specs` sub-directory you MUST read the matching `design.md` and
`requirements.md` before writing anything. For example, working a task from
`.kiro/specs/course-2026-refresh/tasks.md` requires reading
`.kiro/specs/course-2026-refresh/design.md` and
`.kiro/specs/course-2026-refresh/requirements.md` first. When you finish, mark the
corresponding sub-tasks complete in that `tasks.md`.

`ROADMAP.md` at the repo root is the agent-router work queue: each item bundles a set of
`tasks.md` sub-tasks into one ~500-line PR.

## Repository Layout (target after Phase 0)

```
repo-root/
├── .gitbook.yaml              # root: docs/  (keeps repo-mgmt files out of the book)
├── .github/workflows/ci.yml   # CI quality gates (item 17)
├── .grep-gate-rules.yml       # banned-pattern rules (item 9)
├── .markdownlint.yml          # markdown + pedagogy-heading rules (item 17)
├── README.md                  # repo purpose (NOT published)
├── ROADMAP.md                 # agent-router work queue
├── AGENTS.md                  # this file
├── CLAUDE.md                  # pointer to this file
├── prompts/agent-router.md    # the session driver prompt
├── course-content-audit.md    # per-page audit notes (gold details — consult before rewriting)
├── tasks.md                   # repo-root refresh tracker (distinct from the spec tasks.md)
├── docs-map.md                # intended page hierarchy
├── freshness-checklist.md     # stamped pages + next review dates
├── scripts/                   # grep-gate.sh, validate-json-blocks.py, validate-contract.py
├── .kiro/specs/               # requirements / design / tasks
└── docs/                      # ← GitBook content root (everything published lives here)
    ├── README.md  SUMMARY.md
    ├── reference/ (models.md, contract.md, conventions.md, setup-*.md, aws-services.md)
    └── <module folders…>
```

Until Phase 0 (ROADMAP item 1) runs, course content still sits at the repo root — moving
it into `docs/` is that item's job.

## Content Standards (the steering rules)

These come from `.kiro/specs/course-2026-refresh/design.md`. They are also what the CI
grep-gate enforces once it exists.

### Single source of truth
- **Model IDs:** defined only in `docs/reference/models.md` (canonical: Claude Sonnet 4.5
  on Bedrock via Cross-Region Inference Profile). Every other page **links** there — never
  embed `anthropic.claude…` / `us.anthropic.claude…` anywhere else.
- **Lambda contract:** request/response schema defined only in `docs/reference/contract.md`
  (`question`, `ticker`, `year`, `period` ∈ `Q1|Q2|Q3|Q4|FY` → `answer`, `meta`). Project
  pages link to it and their JSON examples must conform.
- **Python version:** 3.12 everywhere (setup, Lambda runtime, CDK). No other 3.x.

### Pedagogy template (every project page)
Six headings, in order: `## Goal`, `## Contract`, `## Required Reading`,
`## Constraints`, `## Acceptance Criteria`, `## Hints`. **No complete solution code** on
any project page — teach, constrain, and hint.

### Voice & freshness
- No emoji. No AI-chat artifacts (`Sure!`, `Great question!`, `As an AI`, `I'd be happy
  to`, `Let me explain`). Direct, concise prose.
- Non-essential asides are labeled `(advanced — skim)`, never "optional".
- No Create React App (`create-react-app`, `react-scripts`, `CRA`) — the front-end uses
  Vite + Amplify Gen 2.
- Demonstrations are **date-relative**. Absolute dates appear only inside a block labeled
  `> **Capture-Dated Example** — results shown may differ from your own.`
- Pages naming a versioned AWS service or console path carry a `Last verified: YYYY-MM`
  freshness stamp at the bottom, indexed in `freshness-checklist.md`.

### Deployment tooling sequence
SAM CLI for the SEC Lambda module; the **CDK Bridge** module is the transition point;
every module after it uses CDK (Python 3.12).

## Build & Validate

There is no compiler. Before considering work done, run whichever validators exist on the
branch — they are added incrementally by ROADMAP item 9 (grep-gate, JSON) and item 17
(contract, markdownlint, link check, `ci.yml`):

```bash
# Run only those that exist yet:
bash scripts/grep-gate.sh                 # banned strings (item 9+)
python scripts/validate-json-blocks.py docs/   # JSON blocks parse (item 9+)
python scripts/validate-contract.py docs/      # Lambda JSON matches contract (item 17+)
npx markdownlint-cli2 "docs/**/*.md"      # formatting + pedagogy headings (item 17+)
```

Always, regardless of which scripts exist:
1. **Every `docs/SUMMARY.md` entry resolves** to a file that exists, and no content file is
   orphaned outside SUMMARY.md.
2. **No banned strings** you introduced (model IDs outside `models.md`, emoji, "optional"
   headings, non-3.12 Python, CRA, AI-chat phrases).
3. **JSON blocks parse** and Lambda examples conform to the contract.

`.github/workflows/ci.yml` is the **authoritative** gate once item 17 lands. After you push,
agent-router delivers results as `check_run` events — do not poll CI in a loop.

## DO / DON'T

### DO
- Read `requirements.md` + `design.md` for the spec before touching its tasks.
- **Consult `course-content-audit.md` per-page notes before rewriting an existing page** —
  it holds gold details (accession-number dash-stripping, EventBridge UTC, CIK
  normalization, CloudWatch walkthrough, FunctionError field) not captured in requirements.
- Keep each PR scoped to exactly one ROADMAP item.
- Link to `reference/models.md` and `reference/contract.md` instead of duplicating.
- Update both the `ROADMAP.md` checkbox and the spec `tasks.md` checkboxes on completion.

### DON'T
- **Don't push to `main`** — GitBook syncs it bidirectionally. Merge to `development`.
- Don't embed model IDs, emoji, "optional" headings, CRA refs, or non-3.12 Python in `docs/`.
- Don't put repo-management files inside `docs/` — they must stay invisible to the book.
- Don't add comments inside JSON code blocks (they make the block invalid).
- Don't put complete solution code on a project page.
- Don't start a second ROADMAP item in the same session.
- Don't run `sudo`. If a task needs root or a missing toolchain, stop and report.

## Domain Knowledge

| Document | When to read |
|----------|--------------|
| `.kiro/specs/course-2026-refresh/requirements.md` | Before any task — the acceptance criteria |
| `.kiro/specs/course-2026-refresh/design.md` | Before any task — layout, SUMMARY tree, grep-gate rules, properties |
| `course-content-audit.md` | Before rewriting ANY existing page — per-page gold details |
| `docs/reference/models.md` | Before referencing a model anywhere |
| `docs/reference/contract.md` | Before writing any Lambda request/response JSON |
| `docs-map.md` | Before adding or moving a page in the hierarchy |
