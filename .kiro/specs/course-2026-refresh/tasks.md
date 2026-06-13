# Implementation Plan: Course 2026 Refresh

## Overview

Phased restructuring of the GitBook course repository. Phase 0 (bootstrap) blocks everything. Reference pages `models.md` and `contract.md` (tasks 6.1, 6.2) ship with bootstrap (wave 1) since they are dependency-free leaf pages that downstream tasks in waves 2+ link to. Phases 1–2 (breaking fixes, credibility sweep) run in parallel after Phase 0. Phase 3 contract alignment (6.3) gates 5/7/8. The IaC narrative is linear: Phase 5 (SAM) → 6 (CDK Bridge) → 7 (10Q) → 8 (Front-End). Phases 9–10 (MCP, RAG) depend on 8. Phase 11 (reference pages) is parallelizable, with 11.2 shipping alongside Phase 1. Phase 12 (CI) ships last except the grep-gate/JSON check which can land after Phase 2.

## Tasks

- [x] 1. Phase 0 — Bootstrap & Repo Restructuring
  - [x] 1.1 Create `.gitbook.yaml` at repo root with `root: docs/`
    - File content: `root: docs/`
    - _Requirements: 1.1_
  - [x] 1.2 Create `docs/` directory and move all existing course Markdown content into it
    - Move all module folders and their files into `docs/`
    - Move current `SUMMARY.md` into `docs/SUMMARY.md`
    - Move current course `README.md` to `docs/README.md`
    - _Requirements: 1.2_
  - [x] 1.3 Create a new repo-root `README.md` describing the repository purpose
    - Distinct from the course intro page inside `docs/`
    - _Requirements: 1.3_
  - [x] 1.4 Create repo-root management files
    - Create `course-content-audit.md` at repo root
    - Create `tasks.md` at repo root for refresh work items
    - Create `docs-map.md` documenting the intended page hierarchy
    - Create `freshness-checklist.md` at repo root listing pages with freshness stamps
    - _Requirements: 1.4, 1.5, 1.6, 13.6_
  - [x] 1.5 Rename module directories to kebab-case slugs
    - `project-sec-cik-lookup-module` → `docs/project-sec-cik-lookup`
    - `optional-front-end-module-with-aws-amplify` → `docs/partner-bot-web-page`
    - Ensure all internal links update accordingly
    - _Requirements: 1.2, 6.1_
  - [x] 1.6 Create stub `docs/SUMMARY.md` with target structure
    - Implement the full SUMMARY.md navigation tree from the design document
    - Include part groups: Foundations, Cloud Deployment — SAM, Cloud Deployment — CDK, Full-Stack Integration, Advanced Modules, Reference
    - Create placeholder README.md files for new modules that don't exist yet (`cdk-bridge/`, `mcp-module/`, `langchain-and-rag/`)
    - Each placeholder README must read: "This module unlocks later in the course. Content is scheduled — check back after Week 6." Do NOT leave them blank.
    - _Requirements: 1.2, 7.1, 10.4, 11.4_
  - [x] 1.7 Create `docs/reference/` directory with placeholder pages
    - Create `docs/reference/models.md` (placeholder)
    - Create `docs/reference/contract.md` (placeholder)
    - Create `docs/reference/conventions.md` (placeholder)
    - Create `docs/reference/setup-aws-account.md` (placeholder)
    - Create `docs/reference/setup-bedrock-access.md` (placeholder)
    - Create `docs/reference/aws-services.md` (placeholder)
    - _Requirements: 12.1, 12.2, 12.3, 12.6_

- [ ] 2. Phase 0 Checkpoint
  - Ensure the `docs/` structure renders correctly via `.gitbook.yaml`, all existing links resolve, and SUMMARY.md references only files that exist.
  - Verify round-trip sync: make one trivial GitBook-UI edit and confirm it lands as a commit under `docs/` without duplicating files at the repo root (the known Git Sync quirk after a root change).
  - Ask the user if questions arise.

- [ ] 3. Phase 1 — Breaking Fixes (SEC Lambda SAM Rewrite)
  - [x] 3.1 Rewrite `docs/project-sec-lambda/README.md` module overview
    - Update module title and description for SAM CLI deployment focus
    - _Requirements: 4.4_
  - [x] 3.2 Create `docs/project-sec-lambda/lambda-project-setup.md`
    - SAM CLI init, `template.yaml`, Python 3.12 runtime
    - Include `requests` library in deployment package/layer
    - Include custom User-Agent header for SEC EDGAR API
    - Remove any invalid comments inside JSON blocks
    - Align Lambda I/O to Contract_Page schema (link to `reference/contract.md`)
    - Link to `reference/models.md` for any model references
    - _Requirements: 4.1, 4.2, 4.3, 4.6, 5.3, 2.3, 15.1_
  - [x] 3.3 Rewrite `docs/project-sec-lambda/lambda-error-handling.md`
    - Follow Pedagogy_Template (Goal, Contract, Required Reading, Constraints, Acceptance Criteria, Hints)
    - Focus on error handling patterns: try/except, FunctionError detection by boto3 callers, CloudWatch log walkthrough (find log group, read an invocation)
    - Consolidate overlapping error lists into a single canonical list
    - Add `sam logs` and `sam local invoke` for local error reproduction
    - Consult `course-content-audit.md` per-page notes for this page's specific findings
    - _Requirements: 4.5, 14.4_
  - [x] 3.4 Replace hardcoded model IDs across all existing pages
    - Grep for `anthropic.claude` and `us.anthropic.claude` in `docs/`
    - Replace inline references with links to `../reference/models.md`
    - _Requirements: 2.3, 2.4_
  - [x] 3.5 Apply rot-proof demonstration approach to SEC modules
    - Replace absolute-dated filing instructions with date-relative phrasing
    - Add "Capture-Dated Example" labels where screenshots/outputs are shown
    - Consult `course-content-audit.md` per-page notes for each affected page's specific findings (accession-number dash-stripping, EventBridge UTC note, CIK normalization hint)
    - _Requirements: 3.1, 3.2, 3.3_

- [ ] 4. Phase 2 — Credibility Sweep
  - [x] 4.1 Remove AI-chat artifacts from all pages in `docs/`
    - Search and remove: "Sure!", "Great question!", "As an AI", "I'd be happy to", "Let me explain"
    - Rewrite affected passages in direct voice
    - _Requirements: 14.1, 14.3_
  - [x] 4.2 Remove emoji from all pages in `docs/`
    - Strip all Unicode emoji characters
    - Replace with plain text descriptions where meaning would be lost
    - _Requirements: 14.3_
  - [x] 4.3 Remove "optional" from front-end module titles and headings
    - Rename module title to "Partner Bot Web Page"
    - Replace any "optional" labels with "(advanced — skim)" where appropriate
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  - [x] 4.4 Consolidate overlapping instructional content
    - Identify pages with duplicated content
    - Choose canonical location, consolidate, and link from other pages
    - _Requirements: 14.4_
  - [x] 4.5 Fix typographical errors identified during audit
    - Run spell-check across `docs/` and fix confirmed typos
    - _Requirements: 14.5_
  - [x] 4.6 Apply Python 3.12 version standard across all pages
    - Search for non-3.12 Python version references
    - Update to 3.12 in setup instructions, Lambda configs, CDK definitions
    - _Requirements: 15.1, 15.2_

- [ ] 5. Phase 2 Checkpoint
  - Ensure no banned strings remain in `docs/`. Run grep for AI artifacts, emoji, "optional" headings, and non-3.12 Python versions. Ask the user if questions arise.

- [ ] 6. Phase 3 — Canonical Contract & Models Pages
  - [x] 6.1 Write `docs/reference/models.md`
    - Define canonical model: Claude Sonnet 4.5 on Bedrock
    - Document Cross_Region_Inference_Profile configuration
    - Include ARN pattern and usage instructions
    - _Requirements: 2.1, 2.2_
  - [x] 6.2 Write `docs/reference/contract.md`
    - Define Lambda request schema: `question` (string), `ticker` (string), `year` (integer), `period` (enum: Q1, Q2, Q3, Q4, FY)
    - Define Lambda response schema: `answer` (string), `meta` (object)
    - Include one valid JSON example and one invalid example with the expected validation error
    - _Requirements: 5.1, 5.2_
  - [x] 6.3 Update all existing project pages to reference Contract_Page
    - Replace inline Lambda I/O definitions with links to `reference/contract.md`
    - Ensure JSON examples in project pages conform to contract schema
    - _Requirements: 5.3, 5.4_

- [ ] 7. Phase 5 — SEC Lambda SAM Finalization
  - [x] 7.1 Finalize SAM `template.yaml` examples in Lambda module
    - Ensure all code blocks use Python 3.12 runtime
    - Validate JSON blocks parse correctly
    - Cross-reference contract schema for Lambda event/response
    - _Requirements: 4.4, 4.6, 15.1_
  - [x] 7.2 Add freshness stamps to SEC Lambda pages
    - Add `Last verified: YYYY-MM` to pages referencing AWS services
    - _Requirements: 13.1_

- [ ] 8. Phase 6 — CDK Bridge Module
  - [x] 8.1 Write `docs/cdk-bridge/README.md` module overview
    - Explain module purpose: transition from SAM to CDK
    - _Requirements: 7.1_
  - [x] 8.2 Write `docs/cdk-bridge/why-cdk.md` concepts page
    - When to use SAM vs CDK
    - CDK advantages for multi-resource stacks
    - _Requirements: 7.2_
  - [x] 8.3 Write `docs/cdk-bridge/project-cdk-init.md` project page
    - Follow Pedagogy_Template structure
    - Guide through `cdk init` with Python 3.12
    - Include CDK project structure explanation
    - _Requirements: 7.3, 7.4, 16.1_

- [ ] 9. Phase 7 — 10Q Inference CDK Rewrite
  - [x] 9.1 Rewrite `docs/project-10q-inference/README.md` for CDK deployment
    - Update module overview to reflect CDK-based deployment
    - _Requirements: 8.1_
  - [x] 9.2 Rewrite `docs/project-10q-inference/part-1-inference-test.md`
    - Follow Pedagogy_Template
    - Use CDK for deployment
    - Link to Models_Page and Contract_Page
    - Fold content from the old `sample-prompt-without-context.md` into this page, then delete `docs/project-10q-inference/project-part-1-inference-test/sample-prompt-without-context.md`
    - Consult `course-content-audit.md` per-page notes for specific findings on this page
    - _Requirements: 8.1, 8.3, 8.4_
  - [x] 9.3 Rewrite `docs/project-10q-inference/part-2-inference-with-context.md`
    - Follow Pedagogy_Template
    - Use date-relative demonstration approach for 10-Q filing selection
    - Fold content from the old `sample-prompt-with-context.md` into this page, then delete `docs/project-10q-inference/project-part-2-inference-with-context/sample-prompt-with-context.md`
    - Consult `course-content-audit.md` per-page notes for specific findings on this page
    - _Requirements: 3.1, 8.1, 8.3_
  - [x] 9.4 Write `docs/project-10q-inference/part-3-text-extraction.md`
    - New section covering SEC filing text extraction
    - Follow Pedagogy_Template
    - _Requirements: 8.2, 8.3_
  - [x] 9.5 Rewrite `docs/project-10q-inference/part-4-question-to-enhanced-prompt.md`
    - Follow Pedagogy_Template
    - Align Lambda I/O to contract schema
    - _Requirements: 8.3, 8.4_

- [ ] 10. Phase 7 Checkpoint
  - Ensure CDK Bridge and 10Q Inference modules follow pedagogy template, reference contract/models pages, and use CDK for deployment. Ask the user if questions arise.

- [ ] 11. Phase 8 — Partner Bot Web Page (Front-End Amplify Gen 2)
  - [x] 11.1 Rewrite `docs/partner-bot-web-page/README.md` module overview
    - Title: "Partner Bot Web Page" — no "optional" qualifier
    - Position as mandatory midpoint deliverable
    - _Requirements: 6.1, 6.2_
  - [x] 11.2 Write `docs/partner-bot-web-page/amplify-gen2-setup.md`
    - Amplify Gen 2 project initialization with Vite
    - No CRA references
    - Follow Pedagogy_Template
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  - [x] 11.3 Write `docs/partner-bot-web-page/build-the-chat-form.md`
    - React form with Amplify UI components
    - Follow Pedagogy_Template
    - _Requirements: 9.4, 16.1_
  - [ ] 11.4 Write `docs/partner-bot-web-page/connect-to-lambda.md`
    - API Gateway integration with existing Lambda
    - Reference Contract_Page for request/response format
    - Follow Pedagogy_Template
    - _Requirements: 5.3, 9.4, 16.1_
  - [ ] 11.5 Write `docs/partner-bot-web-page/authentication-with-cognito.md`
    - Cognito auth setup via Amplify Gen 2
    - Follow Pedagogy_Template
    - _Requirements: 9.1, 9.4, 16.1_

- [ ] 12. Phase 9 — MCP Module
  - [ ] 12.1 Write `docs/mcp-module/README.md` module overview
    - Explain MCP module purpose and prerequisites
    - _Requirements: 10.1_
  - [ ] 12.2 Write `docs/mcp-module/mcp-concepts.md` concepts page
    - MCP fundamentals: tools, resources, prompts
    - How MCP relates to Lambda functions built earlier
    - Include live demo section: students connect an MCP client (e.g., Claude) to the course site's MCP endpoint (`https://llm-aws.course.gspivey.com/~gitbook/mcp`) and query the course — experiencing MCP before building their own server
    - _Requirements: 10.1, 10.2_
  - [ ] 12.3 Write `docs/mcp-module/project-mcp-server.md` project page
    - Follow Pedagogy_Template
    - Guide through building MCP server wrapping existing Lambda
    - _Requirements: 10.2, 10.3_

- [ ] 13. Phase 10 — LangChain & RAG Module
  - [ ] 13.1 Write `docs/langchain-and-rag/README.md` module overview
    - Explain RAG module purpose and prerequisites
    - _Requirements: 11.1_
  - [ ] 13.2 Write `docs/langchain-and-rag/rag-concepts.md` concepts page
    - RAG fundamentals: chunking, embedding, vector stores, retrieval
    - LangChain overview
    - _Requirements: 11.1_
  - [ ] 13.3 Write `docs/langchain-and-rag/project-rag-pipeline.md` project page
    - Follow Pedagogy_Template
    - Guide through implementing chunked and embedded retrieval pipeline
    - Builds on 10Q Inference data pipeline
    - _Requirements: 11.2, 11.3_

- [ ] 14. Phase 9–10 Checkpoint
  - Ensure MCP and RAG modules follow pedagogy template, are positioned correctly in SUMMARY.md after 10Q Inference, and reference prior Lambda work. Ask the user if questions arise.

- [ ] 15. Phase 11 — Reference & Setup Pages
  - [x] 15.1 Write `docs/reference/setup-aws-account.md`
    - AWS account creation, IAM user setup, CLI configuration
    - Add freshness stamp
    - _Requirements: 12.1, 13.1_
  - [x] 15.2 Write `docs/reference/setup-bedrock-access.md`
    - Bedrock model access enablement steps
    - Link to Models_Page for canonical model
    - Add freshness stamp
    - _Requirements: 12.2, 13.1_
  - [x] 15.3 Write `docs/reference/conventions.md`
    - Course naming conventions, glossary of terms
    - _Requirements: 12.3_
  - [x] 15.4 Expand GitHub setup page
    - Cover repository creation, branch protection, commit conventions
    - _Requirements: 12.4_
  - [x] 15.5 Reposition Python virtual environment setup into Python intro module
    - Ensure venv instructions are within `docs/introduction-to-python/python-install.md`
    - Remove any standalone venv reference page if it exists
    - _Requirements: 12.5_
  - [x] 15.6 Write `docs/reference/aws-services.md`
    - Trim to cover only services actively used in course projects
    - Add freshness stamp
    - _Requirements: 12.6, 13.1_

- [ ] 16. Phase 12 — CI Pipeline
  - [x] 16.1 Create `.grep-gate-rules.yml` at repo root
    - Define all banned pattern rules per design document
    - Include `allow_in` exceptions for models.md
    - _Requirements: 2.4, 6.3, 14.2, 15.2_
  - [x] 16.2 Create `scripts/grep-gate.sh`
    - Read rules from `.grep-gate-rules.yml`
    - Scan `docs/` for banned patterns
    - Exit non-zero on match, printing file:line and rule name
    - Use `grep -P` (PCRE) for Unicode emoji patterns, or implement the emoji check in a companion Python script for portability
    - Anchor the CRA pattern with word boundaries (`\bCRA\b`) to avoid false positives on substrings like "sCRAtch"
    - Python version rule must catch ANY 3.x that isn't 3.12 (not just a hardcoded list)
    - _Requirements: 2.4, 13.4_
  - [x] 16.3 Create `scripts/validate-json-blocks.py`
    - Extract fenced `json` code blocks from all Markdown files in `docs/`
    - Run `json.loads()` on each, report failures with file path and line number
    - _Requirements: 5.4, 13.3_
  - [ ] 16.4 Create `scripts/validate-contract.py`
    - Load schema from `docs/reference/contract.md` JSON blocks
    - Scan project pages for Lambda request/response JSON
    - Validate against schema, report mismatches
    - _Requirements: 5.3, 5.4_
  - [ ] 16.5 Create `.markdownlint.yml` configuration
    - Configure rules appropriate for GitBook-flavored Markdown
    - _Requirements: 13.5_
  - [ ] 16.6 Create `.github/workflows/ci.yml`
    - Checkout, markdownlint, grep gate, JSON validation, link check, contract validation
    - Trigger on push to `main` and PRs targeting `main`
    - _Requirements: 13.2, 13.3, 13.4, 13.5_

- [ ] 17. Phase 12 Checkpoint
  - Run CI pipeline locally (or via a test PR with intentional violations) to verify all gates work. Ensure grep-gate catches banned strings, JSON validator catches malformed blocks, and link checker catches broken refs. Ask the user if questions arise.

- [ ] 18. Final SUMMARY.md Verification
  - [ ] 18.1 Validate `docs/SUMMARY.md` against file system
    - Ensure every entry in SUMMARY.md points to an existing file
    - Ensure no orphaned content files exist outside SUMMARY.md
    - _Requirements: 1.2_
  - [ ] 18.2 Add freshness stamps to all pages referencing versioned services
    - Scan for AWS service names, SDK versions, console paths
    - Add `Last verified: YYYY-MM` where missing
    - Update `freshness-checklist.md` with all stamped pages
    - _Requirements: 13.1, 13.6_

- [ ] 19. Final Checkpoint
  - Full validation pass: all CI checks green, SUMMARY.md complete, no orphaned files, no banned strings, no broken links. Ask the user if questions arise.

## Notes

- This is a documentation-only project — no application runtime code is produced.
- Tasks are Markdown file creation/editing and CI script authoring.
- The grep-gate and JSON validator scripts (Phase 12) can partially ship after Phase 2 to catch regressions early.
- Task 15.2 (Bedrock access reference page) ideally ships alongside Phase 1 since Lambda pages need to link to it.
- Checkpoints ensure incremental validation at phase boundaries.
- Each task references specific requirements for traceability.
- **Audit linkage**: Any task that rewrites an existing page MUST consult `course-content-audit.md`'s per-page notes before writing. Small gold details (accession-number dash-stripping, EventBridge UTC, CIK normalization hint, CloudWatch walkthrough, FunctionError field) live there and aren't captured in the requirements.
- **Freshness stamps and date-rot**: The date-check CI script must whitelist the exact Freshness_Stamp pattern (`Last verified: YYYY-MM`) when enforcing Property 3 (no absolute dates outside Capture-Dated blocks).
- **Contract `period` enum**: The canonical values are `Q1`, `Q2`, `Q3`, `Q4`, `FY`. The value `Annual` from early drafts is superseded by `FY`.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4"] },
    { "id": 1, "tasks": ["1.5", "1.6", "1.7", "6.1", "6.2"] },
    { "id": 2, "tasks": ["3.1", "3.2", "3.4", "3.5", "4.1", "4.2", "4.3", "4.5", "4.6", "15.1", "15.2", "15.3", "15.5"] },
    { "id": 3, "tasks": ["3.3", "4.4", "15.4", "15.6"] },
    { "id": 4, "tasks": ["6.3", "7.1", "7.2", "16.1", "16.2", "16.3"] },
    { "id": 5, "tasks": ["8.1", "8.2", "8.3"] },
    { "id": 6, "tasks": ["9.1", "9.2", "9.3", "9.4", "9.5"] },
    { "id": 7, "tasks": ["11.1", "11.2", "11.3", "11.4", "11.5"] },
    { "id": 8, "tasks": ["12.1", "12.2", "12.3", "13.1", "13.2", "13.3"] },
    { "id": 9, "tasks": ["16.4", "16.5", "16.6"] },
    { "id": 10, "tasks": ["18.1", "18.2"] }
  ]
}
```
