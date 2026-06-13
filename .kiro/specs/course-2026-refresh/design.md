# Design Document

## Overview

This project restructures a GitBook-synced course repository to isolate published content inside a `docs/` folder, centralize model and contract references, add new modules (CDK Bridge, MCP, LangChain & RAG), and enforce content quality through a CI pipeline. The deliverables are Markdown files; there is no application runtime. The "system" is the file layout, the SUMMARY.md navigation tree, and the GitHub Actions pipeline that gates publication.

## Architecture

### Design Principles

1. **Single Source of Truth** — model IDs, contract schemas, and Python version live in exactly one canonical page; all other pages link rather than duplicate.
2. **Content Isolation** — repo-root files (audit docs, CI config, task tracking) are invisible to GitBook readers because `.gitbook.yaml` scopes rendering to `docs/`.
3. **Fail-Fast Quality** — CI catches content violations (banned strings, broken links, invalid JSON, format drift) before they reach main.
4. **Pedagogy Consistency** — every project page follows a fixed template so students always know where to find goals, constraints, and acceptance criteria.

---

## Components and Interfaces

### 1. Repository Layout (`docs/` folder pattern)

```
repo-root/
├── .gitbook.yaml              # root: docs/
├── .github/
│   └── workflows/
│       └── ci.yml             # CI pipeline
├── README.md                  # Repo description (not published)
├── course-content-audit.md    # Audit tracking
├── tasks.md                   # Refresh work items
├── docs-map.md                # Intended page hierarchy
├── freshness-checklist.md     # Quarterly review schedule
└── docs/                      # ← GitBook content root
    ├── README.md              # Course introduction page
    ├── SUMMARY.md             # GitBook navigation tree
    ├── reference/
    │   ├── models.md          # Canonical model identifier
    │   ├── contract.md        # Lambda request/response schema
    │   ├── conventions.md     # Naming conventions & glossary
    │   ├── setup-aws-account.md
    │   ├── setup-bedrock-access.md
    │   └── aws-services.md
    ├── introduction-to-python/
    ├── project-sec-cik-lookup/
    ├── introduction-to-git-and-github/
    ├── introduction-to-apis/
    ├── project-sec-edgar-api-library/
    ├── introduction-to-aws/
    ├── project-sec-lambda/         # SAM CLI deployment
    ├── cdk-bridge/                 # NEW — SAM → CDK transition
    ├── project-10q-inference/      # CDK deployment
    ├── partner-bot-web-page/       # Renamed from "optional" amplify module
    ├── mcp-module/                 # NEW — Model Context Protocol
    └── langchain-and-rag/          # NEW — LangChain & RAG
```

Key decisions:
- `.gitbook.yaml` with `root: docs/` keeps repo-management files out of the published book.
- Module directory names use kebab-case slugs matching their SUMMARY.md group labels.
- The `reference/` directory groups all cross-cutting reference pages so links stay short (`../reference/models.md`).

### 2. Target SUMMARY.md Structure

The `docs/SUMMARY.md` file defines the GitBook left-nav tree. Order encodes the pedagogical sequence.

```markdown
# Table of contents

* [Introduction](README.md)

## Foundations

* [Introduction to Python](introduction-to-python/README.md)
  * [Setup Your IDE](introduction-to-python/setup-your-ide.md)
  * [Python Install & Virtual Environment](introduction-to-python/python-install.md)
  * [Python Basics](introduction-to-python/python-basics.md)
  * [Python Modules](introduction-to-python/python-modules.md)
  * [Python Package](introduction-to-python/python-package.md)
  * [Additional Resources](introduction-to-python/additional-resources.md)
* [Project: SEC CIK Lookup Module](project-sec-cik-lookup/README.md)
  * [Building a CIK Lookup Module](project-sec-cik-lookup/building-a-cik-lookup-module.md)
* [Introduction to Git and GitHub](introduction-to-git-and-github/README.md)
  * [Getting Started with Git](introduction-to-git-and-github/getting-started-with-git.md)
  * [Project: GitHub Setup](introduction-to-git-and-github/project-github-setup.md)
* [Introduction to APIs](introduction-to-apis/README.md)
  * [Types of APIs](introduction-to-apis/types-of-apis.md)
  * [REST APIs](introduction-to-apis/rest-apis.md)
  * [What is cURL?](introduction-to-apis/what-is-curl.md)
  * [Data Formats](introduction-to-apis/data-formats.md)
* [Project: SEC EDGAR API Library](project-sec-edgar-api-library/README.md)
  * [Find Company Submissions](project-sec-edgar-api-library/find-company-submissions.md)
  * [Filter Submissions and Retrieve Doc](project-sec-edgar-api-library/filter-submissions-and-retrieve-doc.md)
  * [Expanding Your CIK Module](project-sec-edgar-api-library/expanding-your-cik-module.md)

## Cloud Deployment — SAM

* [Introduction to AWS](introduction-to-aws/README.md)
  * [AWS Services](introduction-to-aws/aws-services.md)
  * [Key Reading](introduction-to-aws/key-reading.md)
* [Project: SEC Lambda (SAM)](project-sec-lambda/README.md)
  * [Lambda Project Setup](project-sec-lambda/lambda-project-setup.md)
  * [Lambda Error Handling](project-sec-lambda/lambda-error-handling.md)

## Cloud Deployment — CDK

* [CDK Bridge: SAM to CDK](cdk-bridge/README.md)
  * [Why CDK?](cdk-bridge/why-cdk.md)
  * [Project: CDK Init](cdk-bridge/project-cdk-init.md)
* [Introduction to Large Language Models](introduction-to-large-language-models.md)
* [Project: 10Q Inference (CDK)](project-10q-inference/README.md)
  * [Part 1: Inference Test](project-10q-inference/part-1-inference-test.md)
  * [Part 2: Inference with Context](project-10q-inference/part-2-inference-with-context.md)
  * [Part 3: Text Extraction](project-10q-inference/part-3-text-extraction.md)
  * [Part 4: Question to Enhanced Prompt](project-10q-inference/part-4-question-to-enhanced-prompt.md)

## Full-Stack Integration

* [Partner Bot Web Page](partner-bot-web-page/README.md)
  * [Amplify Gen 2 Setup](partner-bot-web-page/amplify-gen2-setup.md)
  * [Build the Chat Form](partner-bot-web-page/build-the-chat-form.md)
  * [Connect to Lambda via API Gateway](partner-bot-web-page/connect-to-lambda.md)
  * [Authentication with Cognito](partner-bot-web-page/authentication-with-cognito.md)

## Advanced Modules

* [MCP Module](mcp-module/README.md)
  * [MCP Concepts](mcp-module/mcp-concepts.md)
  * [Project: MCP Server](mcp-module/project-mcp-server.md)
* [LangChain and RAG](langchain-and-rag/README.md)
  * [RAG Concepts](langchain-and-rag/rag-concepts.md)
  * [Project: RAG Pipeline](langchain-and-rag/project-rag-pipeline.md)

## Reference

* [Models](reference/models.md)
* [Lambda Contract](reference/contract.md)
* [Conventions & Glossary](reference/conventions.md)
* [Setup: AWS Account](reference/setup-aws-account.md)
* [Setup: Bedrock Access](reference/setup-bedrock-access.md)
* [AWS Services Reference](reference/aws-services.md)
```

Design notes:
- Part groups (Foundations, Cloud Deployment — SAM, Cloud Deployment — CDK, Full-Stack Integration, Advanced Modules, Reference) give the sidebar visual structure.
- The CDK Bridge sits immediately after SEC Lambda (SAM) creating a clear tooling transition point.
- MCP and RAG modules form an "Advanced Modules" section at the end of the instructional sequence.
- Reference pages are grouped last — they are navigational landing pages, not sequential reading.

### 3. CI Pipeline Architecture

A single GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push to `main` and on pull requests targeting `main`.

```yaml
# Pseudocode structure — actual implementation in tasks
name: Course CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality-gates:
    runs-on: ubuntu-latest
    steps:
      # 1. Checkout
      - uses: actions/checkout@v4

      # 2. Markdownlint
      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v16
        with:
          globs: "docs/**/*.md"

      # 3. Grep Gate (banned strings)
      - name: Grep Gate
        run: bash scripts/grep-gate.sh

      # 4. JSON Validation
      - name: Validate JSON blocks
        run: python scripts/validate-json-blocks.py docs/

      # 5. Link Check
      - name: Check links
        uses: lycheeverse/lychee-action@v1
        with:
          args: "docs/**/*.md"
          fail: true

      # 6. Contract Schema Validation
      - name: Validate contract conformance
        run: python scripts/validate-contract.py docs/
```

#### Grep Gate Script Design

The `scripts/grep-gate.sh` script is the core enforcement mechanism. It searches `docs/` for banned patterns and exits non-zero on any match.

**Banned pattern categories:**

| Category | Patterns | Allowed Location |
|----------|----------|-----------------|
| Hardcoded model IDs | `anthropic.claude-*`, `us.anthropic.claude-*` | `reference/models.md` only |
| "Optional" in headings | `^#+.*[Oo]ptional` | Nowhere in docs/ |
| AI-chat artifacts | `Sure!`, `Great question!`, `As an AI` | Nowhere in docs/ |
| Emoji | Unicode emoji ranges | Nowhere in docs/ |
| Non-3.12 Python | `python3\.(9|10|11|13)`, `runtime.*3\.(9|10|11|13)` | Nowhere in docs/ |
| CRA references | `create-react-app`, `react-scripts` | Nowhere in docs/ |
| Chatbot phrases | `I'd be happy to`, `Let me explain` | Nowhere in docs/ |

The script reads a `.grep-gate-rules.yml` config file so new rules can be added without modifying the script logic.

#### JSON Validation Script Design

`scripts/validate-json-blocks.py` extracts fenced code blocks tagged as `json` from all Markdown files and runs `json.loads()` on each. Failures are reported with file path and line number.

#### Contract Validation Script Design

`scripts/validate-contract.py` loads the schema defined in `docs/reference/contract.md` (extracted from its JSON code blocks), then scans all project pages for JSON blocks matching Lambda request/response structure and validates them against the schema.

### 4. Content Standards Enforcement

#### Pedagogy Template

Every project page must contain these headings in order:

```markdown
## Goal
## Contract
## Required Reading
## Constraints
## Acceptance Criteria
## Hints
```

The markdownlint configuration (`.markdownlint.yml`) combined with a custom rule or CI script validates project pages contain the required heading set.

#### Freshness Stamp Convention

Pages referencing versioned services include this metadata line at the bottom:

```markdown
---
Last verified: 2026-06
```

The quarterly freshness checklist (`freshness-checklist.md` at repo root) indexes all stamped pages with their next review date.

#### Voice and Style Rules

- Direct prose: no emoji, no chatbot conversational phrases, no AI-chat artifacts.
- Advanced non-essential sections labeled `(advanced — skim)` — never "optional."
- No complete solution code in project pages.
- Demonstrations use date-relative language. Absolute dates only inside blocks labeled: `> **Capture-Dated Example** — results shown may differ from your own.`

### 5. Module Dependency Graph

The course modules have prerequisite dependencies that constrain both the SUMMARY.md ordering and the content cross-references.

```
Introduction
    │
    ▼
Introduction to Python
    │
    ▼
Project: SEC CIK Lookup ──────────────────────────────┐
    │                                                  │
    ▼                                                  │
Introduction to Git & GitHub                           │
    │                                                  │
    ▼                                                  │
Introduction to APIs                                   │
    │                                                  │
    ▼                                                  │
Project: SEC EDGAR API Library ◄───────────────────────┘
    │               (depends on CIK module)
    ▼
Introduction to AWS
    │
    ▼
Project: SEC Lambda (SAM) ─────────── reference/contract.md
    │                                  reference/models.md
    ▼
CDK Bridge: SAM → CDK
    │
    ▼
Introduction to LLMs
    │
    ▼
Project: 10Q Inference (CDK) ──────── reference/contract.md
    │                                  reference/models.md
    ▼
Partner Bot Web Page (Amplify Gen 2)
    │
    ▼
MCP Module ────────────────────────── (wraps SEC Lambda)
    │
    ▼
LangChain & RAG ───────────────────── (builds on 10Q Inference)
```

**Dependency rules:**
- `reference/models.md` and `reference/contract.md` are leaf dependencies — they are referenced from project pages but have no inbound content dependencies.
- Every module after CDK Bridge assumes CDK is the deployment tool.
- MCP Module wraps the Lambda created in SEC Lambda, so SEC Lambda must precede it.
- RAG Module extends the 10Q Inference data pipeline, so 10Q Inference must precede it.
- The Partner Bot Web Page consumes the Lambda API, so all Lambda modules must precede it.

---

## Data Models

### Models Page Schema (`reference/models.md`)

```markdown
## Canonical Model

| Field | Value |
|-------|-------|
| Model ID | (defined here, single source of truth) |
| Provider | Anthropic via Amazon Bedrock |
| Deployment | Cross-Region Inference Profile |
| Profile ARN pattern | `arn:aws:bedrock:{region}:inference-profile/...` |

## Usage

All project pages link here instead of embedding the model ID.
When the canonical model changes, update ONLY this page.
```

### Contract Page Schema (`reference/contract.md`)

```markdown
## Lambda Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | yes | The user's natural-language question |
| ticker | string | yes | Stock ticker symbol |
| year | integer | yes | Filing year (YYYY) |
| period | enum | yes | Filing period: `Q1`, `Q2`, `Q3`, `Q4`, or `FY` |

## Lambda Response Schema

| Field | Type | Description |
|-------|------|-------------|
| answer | string | LLM-generated answer text |
| meta | object | Metadata (model used, tokens, latency) |
```

### Grep Gate Rules Config (`.grep-gate-rules.yml`)

```yaml
rules:
  - name: hardcoded-model-id
    pattern: "anthropic\\.claude|us\\.anthropic\\.claude"
    allow_in:
      - "docs/reference/models.md"
    message: "Hardcoded model ID found. Use a link to reference/models.md instead."

  - name: optional-heading
    pattern: "^#+.*[Oo]ptional"
    allow_in: []
    message: "Do not use 'optional' in headings. Use '(advanced — skim)' for non-essential content."

  - name: ai-chat-artifacts
    pattern: "Sure!|Great question!|As an AI|I'd be happy to|Let me explain"
    allow_in: []
    message: "AI-chat artifact detected. Rewrite in direct voice."

  - name: emoji
    pattern: "[\\x{1F600}-\\x{1F64F}\\x{1F300}-\\x{1F5FF}\\x{1F680}-\\x{1F6FF}\\x{2600}-\\x{26FF}]"
    allow_in: []
    message: "Emoji detected. Remove and use plain text."
    note: "Requires grep -P (PCRE) or implement as a Python script for portable Unicode matching."

  - name: wrong-python-version
    pattern: "(?:python|Python)\\s*3\\.(?!12)\\d+|runtime.*3\\.(?!12)\\d+"
    allow_in: []
    message: "Non-standard Python version. Course requires Python 3.12."

  - name: cra-reference
    pattern: "create-react-app|react-scripts|\\bCRA\\b"
    allow_in: []
    message: "Create React App reference found. Course uses Vite + Amplify Gen 2."
```

---

## Error Handling

### CI Pipeline Failures

| Failure Mode | Behavior | Resolution |
|-------------|----------|------------|
| Markdownlint violation | Build fails, violation file:line printed | Fix formatting in flagged file |
| Grep gate match | Build fails, matched line and rule name printed | Remove banned string or move to allowed location |
| Invalid JSON block | Build fails, file path and line number printed | Fix JSON syntax in code block |
| Broken link | Build fails, dead URL listed | Update or remove broken link |
| Contract schema mismatch | Build fails, non-conforming snippet shown | Align JSON example with contract.md schema |

### GitBook Sync Errors

| Failure Mode | Behavior | Resolution |
|-------------|----------|------------|
| SUMMARY.md references non-existent file | GitBook build warning, page shows 404 | Create the missing file or fix SUMMARY.md path |
| File exists but not in SUMMARY.md | File is unreachable in GitBook nav | Add entry to SUMMARY.md |
| .gitbook.yaml misconfigured | GitBook renders from wrong root | Ensure `root: docs/` is set |

---

## Interfaces

### GitBook ↔ Repository

- **Sync mechanism:** GitBook Git Sync (bidirectional on `main` branch)
- **Content root:** Defined by `.gitbook.yaml` → `root: docs/`
- **Navigation:** Driven entirely by `docs/SUMMARY.md`

### CI ↔ Repository

- **Trigger:** Push to `main` or PR targeting `main`
- **Input:** All files in `docs/` directory
- **Output:** Pass/fail status on the GitHub commit/PR
- **Scripts directory:** `scripts/` at repo root (not inside docs/, invisible to GitBook)

### Cross-Page References

- Project pages link to `reference/models.md` for model IDs
- Project pages link to `reference/contract.md` for Lambda schemas
- Advanced sections link back to prerequisite module README pages for required reading

---

## Testing Strategy

Since this is a documentation project (no application code), testing is performed by CI scripts that validate the Markdown content itself:

- **Property-based tests**: The grep gate, JSON validator, and pedagogy template checker are all suited for property-based testing — they assert universal rules across all files in `docs/`. A test harness can generate synthetic Markdown files with various content patterns and verify the scripts correctly pass or fail.
- **Example-based tests**: Specific structural checks (file existence, SUMMARY.md ordering, specific page content) are validated with concrete assertions.
- **Integration tests**: The full CI workflow is tested by running the GitHub Actions pipeline on a PR branch containing intentional violations and verifying it fails.

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Course content resides inside docs/

For any Markdown file referenced in `docs/SUMMARY.md`, its relative path SHALL resolve to a file inside the `docs/` directory.

**Validates: Requirements 1.2**

### Property 2: Grep gate catches all banned strings

For any Markdown file in `docs/` and for any banned pattern defined in the grep gate rules, if the file matches the pattern and is not in the pattern's `allow_in` list, then the grep gate script SHALL exit with a non-zero code. This covers: hardcoded model IDs (Req 2.3, 2.4), "optional" in headings (Req 6.2, 6.3), AI-chat artifacts and emoji (Req 14.1, 14.2, 14.3), non-3.12 Python versions (Req 15.2), CRA references (Req 9.3), and chatbot phrases (Req 16.3, 16.4).

**Validates: Requirements 2.3, 2.4, 6.2, 6.3, 9.3, 14.1, 14.2, 14.3, 15.2, 16.3, 16.4**

### Property 3: No absolute dates outside labeled sections

For any Markdown file in `docs/`, any string matching the pattern `YYYY-MM-DD` or a month-year reference to a specific date SHALL appear only within a block preceded by the "Capture-Dated Example" label, OR as a Freshness_Stamp matching the exact pattern `Last verified: YYYY-MM` at the end of the page.

**Validates: Requirements 3.2, 13.1**

### Property 4: Capture-dated sections carry the required label

For any Markdown file in `docs/` that contains a capture-dated example block, the block SHALL be preceded by a clearly visible label reading "Capture-Dated Example — results shown may differ from your own."

**Validates: Requirements 3.3**

### Property 5: All JSON code blocks parse successfully

For any fenced code block tagged as `json` in any Markdown file within `docs/`, calling a JSON parser on its contents SHALL succeed without error.

**Validates: Requirements 4.3, 5.4**

### Property 6: Project pages follow pedagogy template

For any Markdown file identified as a project page (pages whose path contains `project-` or whose SUMMARY.md entry is indented under a project group), the file SHALL contain all six required headings: Goal, Contract, Required Reading, Constraints, Acceptance Criteria, and Hints.

**Validates: Requirements 4.5, 8.3, 9.4, 10.3, 11.3, 16.1**

### Property 7: Lambda I/O examples conform to contract schema

For any JSON code block in a project page that represents a Lambda request or response (identified by containing the `question` or `answer` field), the block's fields SHALL be a subset of the fields defined in `reference/contract.md`.

**Validates: Requirements 5.3**

### Property 8: Post-CDK-Bridge modules use CDK

For any module that appears after the CDK Bridge module in the `docs/SUMMARY.md` sequence and contains deployment instructions, the deployment tool referenced SHALL be CDK (not SAM CLI).

**Validates: Requirements 7.4**

### Property 9: Freshness stamps on versioned-service pages

For any Markdown file in `docs/` that references an AWS service by specific version number or console navigation path, the file SHALL contain a line matching the pattern `Last verified: YYYY-MM`.

**Validates: Requirements 13.1**

### Property 10: Python version consistency

For any Markdown file in `docs/` that specifies a Python runtime version (in setup instructions, Lambda configuration code blocks, or CDK definitions), the version specified SHALL be `3.12`.

**Validates: Requirements 15.1**
