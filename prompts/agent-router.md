> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
> "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
> interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Repo: https://github.com/GerardsCuriousTech/Build-Your-Own-Full-Stack-LLM-Service-on-AWS

This is a **GitBook-synced documentation repository**. The product is Markdown content,
CI scripts, and YAML config — there is no application to build or run. GitBook Git Sync is
**bidirectional on `main`**, so agents work on `agent/<slug>` branches and merge into
`development`. A human merges `development` → `main`.

---

## 1. Setup

The agent MUST create a persistent working directory outside of `/tmp`:

```bash
mkdir -p /home/agentrouter/agent-runs
WORKDIR=/home/agentrouter/agent-runs/$(date +%Y%m%d-%H%M%S)-course
mkdir -p "$WORKDIR" && cd "$WORKDIR"
git clone https://github.com/GerardsCuriousTech/Build-Your-Own-Full-Stack-LLM-Service-on-AWS.git
cd Build-Your-Own-Full-Stack-LLM-Service-on-AWS
git checkout development
gh auth setup-git   # point git's HTTPS credential at the session token agent-router provides
```

The agent MUST read `AGENTS.md` and `CLAUDE.md` before writing any content. The session's
GitHub token is provisioned by agent-router; the agent MUST NOT add, replace, or edit Git
credentials beyond the `gh auth setup-git` above.

---

## 2. Roadmap Selection

The agent MUST select the first entry in `ROADMAP.md` whose completion checkbox is
unchecked (`- [ ] Complete · PR: —`). The agent MUST implement exactly that one item and
open exactly one PR in this session. The agent MUST NOT begin a second item.

The agent MUST read every spec file referenced on the selected item's `Spec:` line —
including the matching `requirements.md` and `design.md`, not only `tasks.md` — before
writing anything. If the item rewrites an existing page, the agent MUST also read that
page's notes in `course-content-audit.md`.

---

## 3. Implementation

1. The agent MUST create a branch off `development`:
   `git checkout -b agent/<short-item-slug>`.
2. The agent MUST follow the content standards in `AGENTS.md` (single-source-of-truth
   links, pedagogy template, voice/freshness rules, Python 3.12, docs/ isolation).
3. The agent MUST run, locally, whichever validators already exist on the branch and MUST
   fix any failure before proceeding:
   ```bash
   bash scripts/grep-gate.sh                     # if present
   python scripts/validate-json-blocks.py docs/  # if present
   python scripts/validate-contract.py docs/     # if present
   npx markdownlint-cli2 "docs/**/*.md"          # if config present
   ```
   Regardless of which scripts exist, the agent MUST verify every `docs/SUMMARY.md` entry
   resolves to an existing file and that the item introduced no banned strings.
4. After every commit the agent MUST push:
   `git push -u origin agent/<short-item-slug>` (subsequent pushes: `git push`).
5. The agent MUST open a PR with `gh pr create --base development`, with a title matching
   the roadmap item name and a body identifying the roadmap item addressed, the spec
   sub-tasks completed, the pages/scripts changed, and any tradeoffs.
6. The agent MUST immediately call the agent-router MCP `register_pr` tool with the PR
   number and MUST NOT push additional commits until registration is confirmed.

---

## 4. CI Iteration

After any `git push` the agent MUST stop and wait. The agent MUST NOT poll for CI results
by executing `gh run view`, `gh run watch`, or `gh run list` in a loop. Agent-router
delivers CI results as `check_run` events. When a result arrives, the agent MUST act: fix
failures and push, or proceed if green.

`.github/workflows/ci.yml` runs on every PR into `development`, so every PR produces a
`check_run` — today it hard-gates `docs/SUMMARY.md`/internal-link resolution and runs
markdownlint non-blocking; later items add the grep-gate, JSON, and contract checks. The
agent MUST fix a red required check before merge and MUST NOT merge a PR with one failing.

---

## 5. Finalize

Before requesting merge the agent MUST commit both of the following to the feature branch:

1. An update to `ROADMAP.md`: change the selected item's completion line from
   `- [ ] Complete · PR: —` to `- [x] Complete · PR: #<number>`.
2. The matching sub-task checkboxes ticked in
   `.kiro/specs/course-2026-refresh/tasks.md` for every `tasks.md` ID listed on the item's
   `Spec:` line.

Both changes MUST be present on the feature branch before merge.

---

## 6. Merge

Once CI (or the local validators, pre-item-17) is green and the feature branch contains the
`ROADMAP.md` update and the `tasks.md` checkbox updates, the agent MUST squash-merge to
`development`. The session is then complete. The agent MUST NOT start a second item.

---

## 7. Constraints

- **One PR per session.** The agent MUST NOT open additional PRs or select a second
  roadmap item.
- **Never `main`.** The agent MUST NOT push to or open PRs against `main` — GitBook Git
  Sync owns that branch. All agent work targets `development`.
- **Atomic restructure.** ROADMAP item 1 (Phase 0) MUST land as a single coherent PR; a
  state with content moved into `docs/` but no `.gitbook.yaml`/`SUMMARY.md` breaks the
  published book and MUST NOT be merged.
- **Missing toolchain.** If a required tool (`gh`, `python`, `node`/`npx`) is absent, the
  agent MUST stop and report the missing dependency in a PR comment or session message. The
  agent MUST NOT bootstrap a toolchain via conda, snap, or any user-space package manager.
- **Auth failures — stop on the first one; never route around them.** If `git push`,
  `gh pr create`, or any GitHub write fails with a `401`/`403`/permission error, the agent
  MUST stop on the **first** failure and report it. The agent MUST NOT retry with a
  different token, account, or remote; MUST NOT edit Git credentials or credential helpers;
  and MUST NOT attempt any alternate write path (the GitHub REST contents/git-data API,
  `gh api` tree/commit creation, a fork, etc.) to get the change in. The session token is
  provisioned by agent-router and a denial is authoritative — halt, do not work around it.
- **CI divergence.** If the agent cannot converge after a reasonable number of CI cycles, it
  MUST post a PR comment summarizing the blocker and stop.
- **No root.** The agent MUST NOT run `sudo`. If a task requires root, the agent MUST report
  it and stop.
