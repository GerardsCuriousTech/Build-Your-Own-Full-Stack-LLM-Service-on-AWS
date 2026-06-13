# ROADMAP

Ordered feature list for agent-router sessions. Pick the **first uncompleted item** and implement exactly that one. Read all linked spec files before writing code. After merging, check the box and add the PR link.

Each item targets ~500 lines of new/modified content (Markdown pages, scripts, or YAML) and groups several `tasks.md` sub-tasks to reach that size; large modules are split across consecutive items. The sub-task IDs on each `Spec:` line are the exact `tasks.md` entries to implement and to check off on completion.

This is a GitBook-synced documentation repository, not an application. There is no `cargo`, no unit tests, and no performance tests. "Build & test" means the content-quality validators described in `AGENTS.md`. A minimal `.github/workflows/ci.yml` is seeded from the start — it hard-gates `docs/SUMMARY.md`/internal-link resolution and runs markdownlint non-blocking — so every PR into `development` produces a `check_run`. Item 9 extends that workflow with the grep-gate + JSON validators; item 17 adds contract validation, an external link check, and tightens markdownlint.

Items are listed in dependency order (a topological sort of the wave graph in `tasks.md`). When you pick the first unchecked item, all of its prerequisites are already merged into `development`.

---

## Active Roadmap

### 1. Phase 0 — Bootstrap & repo restructuring

Create `.gitbook.yaml` (`root: docs/`). Move every existing course module folder, `SUMMARY.md`, and the course `README.md` into `docs/`, fixing all internal links. Rename `project-sec-cik-lookup-module` → `docs/project-sec-cik-lookup` and `optional-front-end-module-with-aws-amplify` → `docs/partner-bot-web-page`. Write the full target `docs/SUMMARY.md` nav tree (part groups: Foundations, Cloud Deployment — SAM, Cloud Deployment — CDK, Full-Stack Integration, Advanced Modules, Reference) with non-blank placeholder READMEs for the new `cdk-bridge/`, `mcp-module/`, `langchain-and-rag/` modules and placeholder `docs/reference/` pages. Add repo-root `README.md` (repo purpose, distinct from the course intro), `tasks.md`, `docs-map.md`, and `freshness-checklist.md`. (`course-content-audit.md` is already seeded at the repo root — preserve it; do not stub or regenerate it.) Land this atomically — a half-moved state with content under `docs/` but no `.gitbook.yaml`/`SUMMARY.md` breaks the published book.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `1.1`, `1.2`, `1.3`, `1.4`, `1.5`, `1.6`, `1.7`
- [x] Complete · PR: #1

---

### 2. Canonical models & contract reference pages

Write `docs/reference/models.md` — the single source of truth for the model identifier: Claude Sonnet 4.5 on Bedrock via a Cross-Region Inference Profile, the profile ARN pattern, and the rule that every other page links here instead of embedding an ID. Write `docs/reference/contract.md` — the Lambda request schema (`question` string, `ticker` string, `year` integer, `period` enum `Q1`/`Q2`/`Q3`/`Q4`/`FY`) and response schema (`answer` string, `meta` object), with one valid JSON example and one invalid example plus its expected validation error. These are dependency-free leaf pages every later module links to.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `6.1`, `6.2`
- [x] Complete · PR: #3

---

### 3. SEC Lambda (SAM) — module overview & setup page

Rewrite `docs/project-sec-lambda/README.md` for a SAM CLI deployment focus. Write `docs/project-sec-lambda/lambda-project-setup.md`: `sam init`, `template.yaml`, Python 3.12 runtime, the `requests` library included in the deployment package/layer (not assumed built-in), a custom User-Agent header on all SEC EDGAR requests, no comments inside JSON blocks, Lambda I/O linked to `reference/contract.md`, and model references linked to `reference/models.md`. Follow the pedagogy template; no complete solution code.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `3.1`, `3.2`
- [x] Complete · PR: #4

---

### 4. SEC Lambda (SAM) — error handling, model-link sweep & rot-proofing

Rewrite `docs/project-sec-lambda/lambda-error-handling.md` following the pedagogy template: try/except patterns, boto3 caller FunctionError detection, a CloudWatch log walkthrough (find log group, read an invocation), `sam logs`/`sam local invoke` for local reproduction, and a single consolidated error list. Replace every hardcoded `anthropic.claude` / `us.anthropic.claude` ID across `docs/` with a link to `reference/models.md`. Convert SEC demonstrations to date-relative phrasing and add `Capture-Dated Example` labels where outputs are shown. Consult `course-content-audit.md` per-page notes (accession-number dash-stripping, EventBridge UTC, CIK normalization) before editing.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `3.3`, `3.4`, `3.5`
- [x] Complete · PR: #5

---

### 5. Credibility sweep

Across all of `docs/`: remove AI-chat artifacts (`Sure!`, `Great question!`, `As an AI`, `I'd be happy to`, `Let me explain`) and rewrite affected passages in direct voice; strip all emoji; remove "optional" from the front-end module title and headings (use `(advanced — skim)` for non-essential asides); consolidate duplicated instructional content into a single canonical page and link from the others; fix audit-identified typos; and standardize all Python references to 3.12.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `4.1`, `4.2`, `4.3`, `4.4`, `4.5`, `4.6`
- [x] Complete · PR: #6

---

### 6. Reference & setup pages — AWS account, Bedrock access, conventions

Write `docs/reference/setup-aws-account.md` (account creation, IAM user setup, CLI configuration; freshness stamp), `docs/reference/setup-bedrock-access.md` (Bedrock model access enablement; link to `reference/models.md`; freshness stamp), and `docs/reference/conventions.md` (course naming conventions and a glossary of terms).

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `15.1`, `15.2`, `15.3`
- [x] Complete · PR: #7

---

### 7. Reference & setup pages — GitHub setup, venv reposition, services trim

Expand the GitHub setup page to cover repository creation, branch protection, and commit conventions. Move the Python virtual-environment setup instructions into `docs/introduction-to-python/python-install.md` and remove any standalone venv reference page. Write `docs/reference/aws-services.md` trimmed to only the AWS services the course projects actually use; add a freshness stamp.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `15.4`, `15.5`, `15.6`
- [x] Complete · PR: #8

---

### 8. Contract alignment & SAM finalization

Update existing project pages to reference `reference/contract.md` instead of embedding inline Lambda I/O definitions, and ensure their JSON examples conform to the schema. Finalize the SAM `template.yaml` examples in the Lambda module (Python 3.12 runtime, JSON blocks parse, event/response aligned to the contract). Add `Last verified: YYYY-MM` freshness stamps to the SEC Lambda pages.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `6.3`, `7.1`, `7.2`
- [x] Complete · PR: #9

---

### 9. CI extension — grep-gate & JSON validator

Write `.grep-gate-rules.yml` defining the banned-pattern rules (hardcoded model IDs allowed only in `reference/models.md`; banned everywhere: `optional` headings, AI-chat artifacts, emoji, non-3.12 Python, CRA references, chatbot phrases). Write `scripts/grep-gate.sh` that reads the rules, scans `docs/`, and exits non-zero with `file:line` plus the rule name on any match — use `grep -P` for the emoji range, anchor the CRA pattern with `\bCRA\b`, and catch any 3.x Python that is not 3.12. Write `scripts/validate-json-blocks.py` that parses every fenced `json` block in `docs/` and reports `file:line` on failure. Wire both into the already-seeded `.github/workflows/ci.yml` as steps (alongside the existing link/SUMMARY gate) so they run on every PR.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `16.1`, `16.2`, `16.3`
- [x] Complete · PR: #10

---

### 10. CDK Bridge module

Write `docs/cdk-bridge/README.md` (module purpose: the SAM → CDK transition), `docs/cdk-bridge/why-cdk.md` (when and why to move from SAM to CDK; CDK advantages for multi-resource stacks), and `docs/cdk-bridge/project-cdk-init.md` (pedagogy template; `cdk init` targeting Python 3.12; CDK project structure). Every module after this one in the sequence uses CDK as its deployment tool.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `8.1`, `8.2`, `8.3`
- [x] Complete · PR: #11

---

### 11. 10Q Inference (CDK) — overview, inference test & context

Rewrite `docs/project-10q-inference/README.md` for CDK-based deployment. Write `part-1-inference-test.md` (fold in the old `project-part-1-inference-test/sample-prompt-without-context.md`) and `part-2-inference-with-context.md` (date-relative 10-Q filing selection; fold in the old `project-part-2-inference-with-context/sample-prompt-with-context.md`). Follow the pedagogy template; link to `reference/models.md` and `reference/contract.md`. Consult `course-content-audit.md` per-page notes. These old nested pages are the **current** `docs/SUMMARY.md` targets — repoint SUMMARY to the new flat pages and delete the now-empty `project-part-1-inference-test/` and `project-part-2-inference-with-context/` directories.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `9.1`, `9.2`, `9.3`
- [ ] Complete · PR: —

---

### 12. 10Q Inference (CDK) — text extraction & enhanced prompt

Write `docs/project-10q-inference/part-3-text-extraction.md` (extracting text from SEC filing documents — new content) and `docs/project-10q-inference/part-4-question-to-enhanced-prompt.md` with Lambda I/O aligned to `reference/contract.md`. `part-4` supersedes the existing `project-part-3-question-to-enhanced-prompt.md` — migrate its content, repoint `docs/SUMMARY.md` to the new `part-3`/`part-4` entries, and delete the old page. Both follow the pedagogy template and use CDK for deployment.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `9.4`, `9.5`
- [ ] Complete · PR: —

---

### 13. Partner Bot Web Page — setup & chat form

Rewrite `docs/partner-bot-web-page/README.md` with the title "Partner Bot Web Page" (no "optional" qualifier), positioned as a mandatory midpoint deliverable. Write `amplify-gen2-setup.md` (Amplify Gen 2 project init with Vite; no Create React App references) and `build-the-chat-form.md` (React form with Amplify UI components). Migrate relevant content from the existing `optional-project-1-amplify-react-quickstart.md` and `amplify-concepts-amplify-functions-and-amplify-ui.md` (currently the SUMMARY targets) and repoint `docs/SUMMARY.md`. Follow the pedagogy template.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `11.1`, `11.2`, `11.3`
- [ ] Complete · PR: —

---

### 14. Partner Bot Web Page — Lambda integration & auth

Write `docs/partner-bot-web-page/connect-to-lambda.md` (API Gateway integration with the existing Lambda; reference `reference/contract.md` for request/response format) and `docs/partner-bot-web-page/authentication-with-cognito.md` (Cognito auth via Amplify Gen 2). Migrate from the existing `optional-project-2-adapt-todo-app-to-llm-inference/` pages — preserve Task 3's production-hardening reference material per `course-content-audit.md`. Repoint `docs/SUMMARY.md` to the new pages and delete the old `optional-project-*` files once their content is migrated. Both follow the pedagogy template.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `11.4`, `11.5`
- [ ] Complete · PR: —

---

### 15. MCP module

Write `docs/mcp-module/README.md` (module purpose and prerequisites), `docs/mcp-module/mcp-concepts.md` (MCP fundamentals — tools, resources, prompts; how MCP relates to the Lambda built earlier; a live-demo section that has students connect an MCP client such as Claude to the course site's own endpoint `https://llm-aws.course.gspivey.com/~gitbook/mcp` and query the content), and `docs/mcp-module/project-mcp-server.md` (pedagogy template; build an MCP server wrapping the existing course Lambda).

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `12.1`, `12.2`, `12.3`
- [ ] Complete · PR: —

---

### 16. LangChain & RAG module

Write `docs/langchain-and-rag/README.md` (module purpose and prerequisites), `docs/langchain-and-rag/rag-concepts.md` (chunking, embedding, vector stores, retrieval; LangChain overview), and `docs/langchain-and-rag/project-rag-pipeline.md` (pedagogy template; a chunked-and-embedded retrieval pipeline that builds on the 10Q Inference data flow).

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `13.1`, `13.2`, `13.3`
- [ ] Complete · PR: —

---

### 17. CI pipeline finalization

Write `scripts/validate-contract.py` (load the schema from `reference/contract.md`'s JSON blocks, scan project pages for Lambda request/response JSON, validate against the schema). Add `.markdownlint.yml` (GitBook-flavored rules plus enforcement that project pages contain the six pedagogy-template headings) and promote markdownlint from non-blocking to a hard gate. Extend the already-seeded `.github/workflows/ci.yml` with the contract-validation step and an external link check (lychee), so the full gate is checkout → link/SUMMARY → markdownlint → grep-gate → JSON validation → contract validation. This is the final, authoritative quality gate.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `16.4`, `16.5`, `16.6`
- [ ] Complete · PR: —

---

### 18. Final SUMMARY verification & freshness stamps

Validate `docs/SUMMARY.md` against the filesystem: every entry resolves to an existing file, and no content file is orphaned outside SUMMARY.md. Add `Last verified: YYYY-MM` stamps to every page naming a versioned AWS service or console navigation path, and populate `freshness-checklist.md` with all stamped pages and their next-review dates.

- Spec: `.kiro/specs/course-2026-refresh/` · tasks `18.1`, `18.2`
- [ ] Complete · PR: —

---

## Notes for the maintainer

- `tasks.md` defines six human **checkpoints** (its tasks 2, 5, 10, 14, 17, 19) at phase boundaries. These are not roadmap items because they produce no PR. Review the merged `development` branch at the boundaries after items 1, 5, 10/12, 16, and 17 before letting agents continue.
- Items deliberately do **not** map one-to-one to phases. Phase 0 is kept whole (the restructure must be atomic); large multi-page modules (10Q, front-end) are split to keep each PR near ~500 lines.
- A minimal `.github/workflows/ci.yml` is seeded from the start so every PR gets a `check_run`; items 9 and 17 **extend** it rather than create it.
- Phase 0 (PR #1) created the full target page set as empty placeholders and orphaned the original 10Q/front-end content. This was cleaned up post-merge: `docs/SUMMARY.md` now points at the real pages, and items 11–14 carry the rename/fold/delete + SUMMARY repoint.
