# Requirements Document

## Introduction

A comprehensive refresh of the GitBook-based course "Build Your Own Full Stack LLM Service on AWS." The course repository is the source of truth; GitBook Git Sync operates bidirectionally on the main branch. This refresh restructures the repository, centralizes model references, eliminates date-rot, rewrites deployment modules to use SAM CLI and CDK, adds new modules (MCP, LangChain & RAG), and establishes maintenance machinery for long-term freshness.

## Glossary

- **Course_Repository**: The Git repository containing all course content, served via GitBook Git Sync on the main branch.
- **Docs_Folder**: The `docs/` directory at the repository root that serves as the GitBook-synced content root, scoped by `.gitbook.yaml`.
- **Models_Page**: The single reference page at `reference/models.md` inside the Docs_Folder that defines all LLM model identifiers used throughout the course.
- **Contract_Page**: The single reference page at `reference/contract.md` inside the Docs_Folder that defines the canonical Lambda request/response JSON schema.
- **Freshness_Stamp**: A metadata line reading "Last verified: YYYY-MM" placed on every page that names AWS services or third-party tool specifics.
- **Pedagogy_Template**: The standard project page structure consisting of Goal, Contract, Required Reading, Constraints, Acceptance Criteria, and Hints sections—providing no complete solutions.
- **CI_Pipeline**: The GitHub Actions continuous integration workflow that runs on every push to main.
- **Grep_Gate**: A CI check that fails the build when banned strings (hardcoded model IDs, "optional" labels, emoji, chatbot phrases) appear outside allowed locations.
- **SAM_CLI**: AWS Serverless Application Model Command Line Interface used for Lambda deployment in early project modules.
- **CDK**: AWS Cloud Development Kit (Python, version 2) used for infrastructure deployment in mid-to-late project modules.
- **Amplify_Gen2**: AWS Amplify Gen 2 framework using Vite as the build tool for front-end hosting and deployment.
- **MCP_Module**: The new course module teaching Model Context Protocol server development.
- **RAG_Module**: The new course module teaching LangChain-based Retrieval Augmented Generation.
- **Cross_Region_Inference_Profile**: The Bedrock deployment mechanism that routes model requests across regions for availability.

## Requirements

### Requirement 1: Repository Restructuring

**User Story:** As a course maintainer, I want all GitBook-synced content isolated in a `docs/` folder so that repo-root files (audit docs, task tracking, CI config) remain invisible to the published course.

#### Acceptance Criteria

1. WHEN the repository is restructured, THE Course_Repository SHALL contain a `.gitbook.yaml` file at the repository root that sets `root: docs/` as the GitBook content scope.
2. WHEN the repository is restructured, THE Course_Repository SHALL place all GitBook-rendered Markdown content inside the Docs_Folder.
3. THE Course_Repository SHALL contain a repo-root `README.md` that describes the repository purpose and is distinct from the course introduction page inside the Docs_Folder.
4. THE Course_Repository SHALL contain a `course-content-audit.md` file at the repository root.
5. THE Course_Repository SHALL contain a `tasks.md` file at the repository root for tracking refresh work items.
6. THE Course_Repository SHALL contain a `docs-map.md` file at the repository root that documents the intended page hierarchy inside the Docs_Folder.

### Requirement 2: Model Centralization

**User Story:** As a course maintainer, I want a single reference page for all model identifiers so that updating the canonical model requires changing only one page.

#### Acceptance Criteria

1. THE Models_Page SHALL define the canonical model identifier, its Bedrock deployment mechanism, and the Cross_Region_Inference_Profile configuration.
2. THE Models_Page SHALL specify Claude Sonnet 4.5 on Bedrock with Cross_Region_Inference_Profile as the initial canonical model.
3. WHEN a project page references an LLM model, THE project page SHALL link to the Models_Page instead of embedding a hardcoded model identifier.
4. THE Grep_Gate SHALL fail the CI build when a hardcoded model identifier string appears in any Markdown file outside the Models_Page.

### Requirement 3: Rot-Proof Demonstrations

**User Story:** As an instructor, I want demonstrations to use a date-relative approach so that examples remain valid regardless of when a student takes the course.

#### Acceptance Criteria

1. WHEN a demonstration requires a 10-Q filing, THE demonstration page SHALL instruct the student to locate a recent 10-Q filing from a specified company using SEC EDGAR search relative to the current date.
2. THE Docs_Folder SHALL contain no absolute dates in demonstration instructions except within sections explicitly labeled as "Capture-Dated Example."
3. WHEN a page contains a capture-dated example, THE page SHALL include a clearly visible label stating "Capture-Dated Example — results shown may differ from your own."

### Requirement 4: SEC Lambda Fixes and SAM Rewrite

**User Story:** As a student, I want the SEC Lambda module to deploy correctly with modern tooling so that I can complete the project without encountering outdated instructions or runtime errors.

#### Acceptance Criteria

1. WHEN the SEC Lambda module is rewritten, THE project page SHALL instruct students to include a custom User-Agent header in all SEC EDGAR API requests.
2. WHEN the SEC Lambda module is rewritten, THE project page SHALL specify that the `requests` library is included in the Lambda deployment package or layer, not assumed as a runtime built-in.
3. THE SEC Lambda module SHALL contain no invalid code comments (e.g., comments inside JSON configuration blocks where comments are syntactically illegal).
4. WHEN the SEC Lambda module is rewritten, THE project page SHALL use SAM_CLI as the deployment tool.
5. THE SEC Lambda project pages SHALL follow the Pedagogy_Template structure.
6. THE SEC Lambda module SHALL align its Lambda function input/output to the schema defined in the Contract_Page.

### Requirement 5: Canonical API Contract

**User Story:** As a student, I want a single reference defining the Lambda request/response schema so that all projects share a consistent integration interface.

#### Acceptance Criteria

1. THE Contract_Page SHALL define the Lambda request schema with fields: `question` (string), `ticker` (string), `year` (integer), and `period` (enum: `"Q1"`, `"Q2"`, `"Q3"`, `"Q4"`, `"FY"`).
2. THE Contract_Page SHALL define the Lambda response schema with fields: `answer` (string) and `meta` (object).
3. WHEN a project page specifies Lambda input or output, THE project page SHALL reference the Contract_Page and conform to its schema.
4. THE CI_Pipeline SHALL validate all JSON example snippets in the Docs_Folder against the contract schema.

### Requirement 6: De-Optionalize Front-End Module

**User Story:** As an instructor, I want the front-end module positioned as a mandatory midpoint deliverable so that students treat it as core curriculum.

#### Acceptance Criteria

1. WHEN the front-end module is restructured, THE module title SHALL be "Partner Bot Web Page" with no "optional" qualifier.
2. THE Docs_Folder SHALL contain no page titles or body text that label the front-end module as optional.
3. THE Grep_Gate SHALL fail the CI build when the string "optional" appears in any front-end module page title or heading.
4. WHEN an advanced aside appears within the front-end module, THE aside SHALL use the label format "(advanced — skim)" instead of "optional."

### Requirement 7: CDK Bridge Module

**User Story:** As a student, I want a module that teaches the transition from SAM to CDK so that I understand why subsequent projects use CDK and how to set it up.

#### Acceptance Criteria

1. THE Docs_Folder SHALL contain a CDK Bridge module positioned after the SEC Lambda (SAM) module in the course sequence.
2. THE CDK Bridge module SHALL include a concepts page explaining when and why to transition from SAM_CLI to CDK.
3. THE CDK Bridge module SHALL include a project page guiding students through initializing a CDK Python project targeting Python 3.12.
4. WHEN a module appears after the CDK Bridge module in the course sequence, THE module SHALL use CDK as the deployment tool.

### Requirement 8: 10Q Inference CDK Rewrite

**User Story:** As a student, I want the 10Q Inference project deployed via CDK with text-extraction coverage so that it aligns with the post-bridge deployment standard.

#### Acceptance Criteria

1. WHEN the 10Q Inference module is rewritten, THE project pages SHALL use CDK as the deployment tool.
2. THE 10Q Inference module SHALL include a section on text extraction from SEC filing documents.
3. THE 10Q Inference module project pages SHALL follow the Pedagogy_Template structure.
4. THE 10Q Inference module SHALL align its Lambda function input/output to the schema defined in the Contract_Page.

### Requirement 9: Front-End Amplify Gen 2

**User Story:** As a student, I want the front-end module to use Amplify Gen 2 with Vite so that I learn current AWS front-end tooling without encountering deprecated CRA references.

#### Acceptance Criteria

1. WHEN the front-end module is rewritten, THE project pages SHALL specify Amplify_Gen2 as the hosting and deployment framework.
2. WHEN the front-end module is rewritten, THE project pages SHALL specify Vite as the build tool for the React application.
3. THE Docs_Folder SHALL contain no references to Create React App (CRA) in any front-end module page.
4. THE front-end module project pages SHALL follow the Pedagogy_Template structure.

### Requirement 10: New MCP Module

**User Story:** As a student, I want a module on Model Context Protocol so that I learn how to expose existing Lambda functions as tools for LLM agents.

#### Acceptance Criteria

1. THE Docs_Folder SHALL contain an MCP_Module with a concepts page explaining Model Context Protocol fundamentals.
2. THE MCP_Module concepts page SHALL include a live demo section instructing students to connect an MCP client (e.g., Claude) to the course site's own MCP endpoint (`https://llm-aws.course.gspivey.com/~gitbook/mcp`) and query the course content — providing hands-on MCP experience before students build their own server.
3. THE MCP_Module SHALL contain a project page guiding students through building an MCP server that wraps existing course Lambda functions.
4. THE MCP_Module project page SHALL follow the Pedagogy_Template structure.
5. THE MCP_Module SHALL be positioned after the 10Q Inference module in the course sequence.

### Requirement 11: New LangChain and RAG Module

**User Story:** As a student, I want a module on LangChain and Retrieval Augmented Generation so that I learn chunked and embedded retrieval approaches for improving LLM answers.

#### Acceptance Criteria

1. THE Docs_Folder SHALL contain a RAG_Module with a concepts page explaining LangChain and Retrieval Augmented Generation fundamentals.
2. THE RAG_Module SHALL contain a project page guiding students through implementing a chunked and embedded retrieval pipeline.
3. THE RAG_Module project page SHALL follow the Pedagogy_Template structure.
4. THE RAG_Module SHALL be positioned after the MCP_Module in the course sequence.

### Requirement 12: Reference and Setup Pages

**User Story:** As a student, I want consolidated reference and setup pages so that I can find environment configuration and service documentation in a single location.

#### Acceptance Criteria

1. THE Docs_Folder SHALL contain a `reference/setup-aws-account.md` page covering AWS account creation and initial configuration.
2. THE Docs_Folder SHALL contain a `reference/setup-bedrock-access.md` page covering Bedrock model access enablement.
3. THE Docs_Folder SHALL contain a `reference/conventions.md` page documenting course naming conventions and a glossary of terms.
4. THE Docs_Folder SHALL contain an expanded GitHub setup page covering repository creation, branch protection, and commit conventions.
5. THE Docs_Folder SHALL reposition the Python virtual environment setup instructions within the Python introduction module rather than a standalone reference page.
6. THE Docs_Folder SHALL contain a `reference/aws-services.md` page trimmed to cover only AWS services actively used in the course projects.

### Requirement 13: Maintenance Machinery

**User Story:** As a course maintainer, I want automated freshness checks and CI gates so that stale content and formatting violations are caught before publication.

#### Acceptance Criteria

1. WHEN a page names an AWS service or third-party tool by specific version or console path, THE page SHALL include a Freshness_Stamp.
2. THE CI_Pipeline SHALL include a link-checking step that fails the build when a broken internal or external link is detected.
3. THE CI_Pipeline SHALL include a JSON validation step that fails the build when a malformed JSON code block is detected in any Markdown file.
4. THE CI_Pipeline SHALL include a Grep_Gate step that fails the build when banned strings are detected outside allowed locations.
5. THE CI_Pipeline SHALL include a markdownlint step that enforces consistent Markdown formatting across all files in the Docs_Folder.
6. THE Course_Repository SHALL contain a quarterly freshness checklist document listing all pages with Freshness_Stamps and their next review dates.

### Requirement 14: Credibility Sweep

**User Story:** As an instructor, I want all AI-chat artifacts removed and a consistent editorial voice applied so that the published course reads as professionally authored.

#### Acceptance Criteria

1. THE Docs_Folder SHALL contain no AI-chat artifacts (e.g., "Sure!", "Great question!", "As an AI language model").
2. THE Grep_Gate SHALL fail the CI build when AI-chat artifact phrases appear in any Markdown file.
3. THE Docs_Folder SHALL use direct voice consistently: no emoji characters and no chatbot conversational phrases.
4. WHEN two or more pages contain overlapping instructional content, THE Docs_Folder SHALL consolidate the content into a single canonical location and link from other pages.
5. THE Docs_Folder SHALL contain no typographical errors that were identified during the credibility audit.

### Requirement 15: Python Runtime Standard

**User Story:** As a course maintainer, I want a single Python version specified across all modules so that students encounter no version conflicts between projects.

#### Acceptance Criteria

1. THE Docs_Folder SHALL specify Python 3.12 as the required runtime version in all module setup instructions, Lambda configurations, and CDK project definitions.
2. THE Grep_Gate SHALL fail the CI build when a Python version other than 3.12 is specified in any project configuration or instruction page.

### Requirement 16: Pedagogy and Voice Standards

**User Story:** As an instructor, I want consistent pedagogical structure and editorial voice so that every project page is teachable and professional.

#### Acceptance Criteria

1. WHEN a project page is created or rewritten, THE project page SHALL follow the Pedagogy_Template structure (Goal, Contract, Required Reading, Constraints, Acceptance Criteria, Hints).
2. THE Docs_Folder SHALL contain no complete solution code in any project page.
3. WHEN a section is considered advanced but non-essential, THE page SHALL label the section with "(advanced — skim)" and not "optional."
4. THE Docs_Folder SHALL use direct, concise prose with no emoji and no chatbot phrases across all pages.
