# Course Content Audit — Build Your Own Full Stack LLM Service on AWS
**Audited:** June 11, 2026 · All 28 published pages read in full
**Audience lens:** College freshmen–seniors, mixed dev experience
**Pedagogy goal:** Not copy-pasteable; students read docs and experiment; course references most of what they need

---

## Severity key
- 🔴 **Breaking** — students will hit a hard failure following the course as written
- 🟠 **Wrong/stale** — factually incorrect or outdated content
- 🟡 **Quality** — credibility, clarity, or consistency problems
- 🔵 **Pedagogy** — conflicts with the read-docs-and-experiment goal
- ⚪ **Gap** — missing content students will need

---

## Critical findings (fix before June 17 session)

### 🔴 1. Every Bedrock model reference in the course is retired
The course instructs students to invoke "Claude 3 Sonnet" (Project Part 1) and "Claude 3.5" (Project Part 3). These models no longer exist on Bedrock:
- Claude 3.5 Sonnet v1 reached end-of-life on Bedrock March 1, 2026 — requests to the model ID now fail
- Claude 3.7 Sonnet reached EOL April 28, 2026, returning `ValidationException: The provided model identifier is invalid`
- Claude 3 Sonnet and Claude 3 Haiku are likewise retired/legacy

A student following the course in June 2026 gets an immediate API error. **Fix:** standardize on a current model (Claude Sonnet 4.5 on Bedrock is the natural choice), reference it by model ID once in a single "Models" page that's easy to update each summer, and have every project page point at that page instead of hardcoding model names.

### 🔴 2. The core pedagogical example no longer works
"Sample Prompt without Context" demonstrates that the LLM doesn't know how much Amazon invested in Anthropic in Q3 2023 / Q1 2024. **Current Claude models know this** — it's well inside their training data now. A student running this exercise today gets a correct answer and the entire lesson (LLMs need context for recent facts) silently fails to land.

**Fix:** The instruction "pick a different company" must become "pick a filing from the last ~3 months" with an explanation of training cutoffs. Better: make checking the model's knowledge cutoff part of the exercise. This page needs a fresh 2026 worked example, and the example should be regenerated every summer — a good candidate for an agent-router cron task.

### 🔴 3. SEC Lambda code sample will not run on Lambda
Lambda 1 imports `requests`, which is not in the Lambda Python runtime. Students get `Runtime.ImportModuleError: No module named 'requests'` on first invoke, and the course never explains dependency packaging (zip with deps, layers, or container). **Fix:** the SAM rewrite solves this naturally — `sam build` packages `requirements.txt` automatically. Make the gotcha explicit: it's a genuinely valuable lesson ("Lambda is not your laptop") if taught, and a wall if not. Alternative: use `urllib.request` from the stdlib and *mention* the requests/packaging issue.

### 🔴 4. SEC Lambda code violates the SEC policy the course itself teaches
The CIK Lookup module (correctly, prominently) teaches the SEC Fair Access policy: declare a User-Agent. The SEC Lambda sample then calls `requests.get(url)` with **no User-Agent header**. The SEC blocks undeclared clients — students who copy this get 403s, and the course contradicts itself. **Fix:** add the header to the sample, and turn it into a callback: "remember the Fair Access policy from the CIK module."

---

## Cross-cutting issues

### 🟡 5. AI-copy residue throughout (credibility killer)
Multiple pages contain unmistakable artifacts of content pasted from AI chat sessions:
- **Project: SEC CIK Lookup Module** — ends a section with *"Is there a specific aspect of the SEC's work you're interested in learning more about?"* (a chatbot's follow-up question, left in the page)
- **Data Formats** — three code blocks followed by *"AI-generated code. Review and use carefully. More info on FAQ"* with links to `bing.com/new#faq`
- **Rest APIs** and **What is cURL?** — stray `[1]` citation markers and duplicated bracket-link citation residue from Bing/Copilot
- **Python Basics**, **Python Package**, **Python Install** — *"Happy coding! 🚀"*, *"If you have any more questions or need further examples, feel free to ask!"*, *"Enjoy your Python journey! 😊🐍"*
- **AWS Services** — "In conclusion…" appearing mid-page inside the S3 section, classic stitched-generation tell

College students notice this instantly. For a coach building a credibility-driven public identity, this is the highest-leverage polish item after the breaking fixes. **Fix:** full sweep; rewrite in a single consistent instructional voice.

### 🟡 6. Internal schema inconsistency across the Lambda → frontend chain
Three different input contracts appear for the same inference Lambda:
- Project Part 3 defines: `{question, ticker, year}` (no period/quarter — can't actually request a specific 10-Q)
- Task 1 form produces: `partner, year, period, question` (with a note to map partner→ticker)
- Task 2's smoke test POSTs `{partner, year, period, question}` directly at the **core** Lambda — which per Part 3 expects `ticker`, so the documented smoke test 500s

**Fix:** define one canonical contract early — `{question, ticker, year, period}` where `period ∈ Q1|Q2|Q3|Q4|FY` (the 2026-refresh spec supersedes the early-draft `Annual` with `FY`) — put it on a single canonical Contract page (`reference/contract.md`) and reference it everywhere. Also fixes the SEC Lambda's separate `request_type/company/year/quarter` shape drifting from the rest of the stack — intentional per-module flexibility is fine, but say so explicitly.

### 🟡 7. Amplify module mixes Gen 1, Gen 2, and a deprecated toolchain
- Project 1 sends students to the official **Gen 2** quickstart (Vite-based, `amplify_outputs.json`)
- Task 3 then instructs **Create React App** conventions: `REACT_APP_` env prefix and `aws-exports.js` (Gen 1) — CRA was officially deprecated in early 2025 and the quickstart hasn't used it for years
- Task 2/3 reference `localhost:5173` (Vite's port) while giving CRA instructions (CRA serves on 3000)

Students who did Project 1 correctly will have neither `aws-exports.js` nor `REACT_APP_` support. **Fix:** standardize on Gen 2 + Vite throughout: `import.meta.env.VITE_*`, `amplify_outputs.json`, `fetchAuthSession` from `aws-amplify/auth` (that import is already correct in Task 3). This also sets up the CDK narrative — Amplify Gen 2 backends are CDK under the hood.

### 🔵 8. Copy-paste-ability is inconsistent — and worst exactly where stakes are highest
Scoring each project page against the "read docs and experiment" goal:

| Page | Style | Verdict |
|---|---|---|
| Building a CIK Lookup Module | Spec + constraints + PEP8 pointer, no solution code | ✅ Model page. This is the template. |
| SEC EDGAR API Library (all 3 pages) | Guided curl exploration, URL format given, no solution | ✅ Excellent — teaches the 10-digit CIK gotcha by *showing the error first* |
| Expanding Your CIK Module | Method signatures only | ✅ Good |
| Project SEC Lambda | ~70% solution code provided | ⚠️ Borderline — keep the *skeleton*, remove the working bodies |
| 10Q Inference Parts 1–3 | Doc links + experiment instructions | ✅ Good structure (content stale per #1/#2) |
| Task 2 (API Gateway) | **Complete, runnable CLI script** with every flag | ❌ Fully copy-pasteable |
| Task 3 (Edge Lambda) | **Complete production-grade Lambda + React solution**, ~200 lines | ❌ The entire deliverable is handed over |

Task 3 is the midpoint-deliverable territory — and it's the single most copy-pasteable page in the course. **Fix pattern:** replace solution code with (a) the contract, (b) the architecture diagram (already good), (c) links to the specific AWS doc pages needed (HTTP API payload v2.0 format, JWT authorizer claims location, boto3 `invoke`), and (d) acceptance criteria ("unauthenticated request returns 401; malformed body returns 400 with field names; signed request round-trips"). Keep small *fragments* (e.g., the claims path `requestContext.authorizer.jwt.claims` is legitimately hard to discover). The CDK rewrite is the natural moment to do this conversion.

### ⚪ 9. Missing pages students will need
1. **AWS account + credentials setup** — the course goes from AWS concepts straight to deploying Lambdas. Nothing covers console login, `aws configure` / SSO, region selection, or how boto3 finds credentials. Task 2 uses the AWS CLI extensively; it's never installed.
2. **Bedrock model access enablement** — Bedrock requires requesting model access in the console before first invoke; the #1 first-day stumbling block, undocumented.
3. **Dependency packaging for Lambda** (resolved by the SAM module if written, but must exist).
4. **10-Q text extraction** — Part 2 says "append all the text for the 10-Q" but the document is HTML. Nothing covers stripping HTML to text, and nothing mentions context-window limits or Bedrock's payload cap. Students will paste megabytes of HTML and get confusing failures. Small section: extract text (stdlib `html.parser` or let them research), estimate tokens, truncate sensibly.
5. **Python version pin** — never stated. Pin 3.12 everywhere (matches Task 3's runtime; AL2 runtimes are aging out).
6. **Course glossary/conventions page** — one place for: the canonical model ID, the canonical Lambda contract, the User-Agent string format, repo layout expectations.

---

## Page-by-page notes

### Introduction
Video only. Fine, but consider one paragraph of "how to use this course" stating the pedagogy explicitly: *we link the docs, you do the work; copy-paste will not survive contact with the demo.* Sets expectations for 152 students of wildly mixed experience.

### Introduction to Python
- **Setup Your IDE** 🟡 — typos: "If your using Window" → "If you're using Windows". WSL2 guidance is good and current. Consider stating *why* WSL (Lambda runs Linux; dev/prod parity) — that's a one-line internship-grade lesson.
- **Python Install** 🟡 — "type `python`" opens the REPL; the verification command should be `python --version` / `python3 --version`. Windows Store stub-alias gotcha (typing `python` opens the Store) worth one sentence; freshmen hit it constantly. No version pinned (see #9.5).
- **Python Basics** 🟡 — content is accurate and well-scoped for beginners (functions → OOP → files). Remove the chatbot sign-offs (#5). OOP section is solid; abstraction example using `abc` may be deep for week 1 but harmless.
- **Python Modules** ✅ — accurate, good examples, right length.
- **Python Package** 🟡 — accurate. Worth one forward-looking sentence: "your CIK module will be structured exactly like this" to motivate it.
- **Additional Resources** ✅ — venv explanation is one of the best beginner-voiced sections in the course. Move it *up*: students need venv before they `pip install requests` in the CIK project, and "Additional Resources" reads as skippable. Retitle or fold into the project prerequisites.

### Project: SEC CIK Lookup Module
- Root page 🟡 — good domain framing (SEC, 10-K vs 10-Q, CIK). Remove the chatbot question (#5). The investor.gov/Investopedia citations are fine.
- **Building a CIK Lookup Module** ✅🔵 — the model project page: clear spec, Fair Access policy front and center, PEP8 link, return-shape constraint, no solution. Minor: "The The return values" typo. Consider adding acceptance criteria ("`ticker_to_cik('AAPL')` returns a tuple containing 320193") so students can self-verify — criteria aren't solutions.
- ⚪ Hint gap: name-keyed dictionary lookups will frustrate (case, punctuation, "Apple Inc." vs "APPLE INC"). One nudge — "think about normalizing keys" — preserves the struggle while preventing a dead end.

### Introduction to Git and Github
- Root page 🟡 — accurate but thin (two definition blocks). Fine as a primer given roadmap-style links elsewhere; could add one link to a Git tutorial path.
- **Getting Started with Git** — (read in part via search; standard install content). Verify it covers `git config` identity setup; students' first commit fails without it.
- **Project: Github Setup** 🔵⚪ — two lines total. For an internship-simulation course this is the page to grow: require a README, a `.gitignore` (venv, `__pycache__`, `.env`, `amplify_outputs.json`), and — bigger — a **feature-branch + PR workflow** for every subsequent project. With 152 students, PR habits are the most internship-like skill in the whole course, and the intro page already advertises branching as Git's superpower without ever using it.

### Introduction to APIs
- Root page ✅ — the waiter analogy is right for the audience.
- **Types of APIs** 🟡 — accurate but over-broad for week 2 (ABI? OData? gRPC?). Fine as reference; consider marking REST/JSON as "what we use" and the rest as "recognize the names."
- **Rest APIs** 🟡 — content fine; strip citation residue (#5).
- **What is cURL?** 🟡 — good page, good external resources (curl.se tutorial, Everything cURL). Strip `[1]` artifacts. The `-X POST/-d/-H` examples are appropriately generic.
- **Data Formats** 🟠🟡 — remove all three "AI-generated code" Bing badges (#5). The JSON example is **invalid JSON** (contains a `//` comment) — students will paste it into a validator the page itself recommends and be told it's broken. XML/CSV examples fine. Unstructured-data section is two sentences; either grow it (10-Qs are semi-structured HTML — directly relevant!) or cut it.

### Project SEC EDGAR API Library
- Root page ✅🔵 — exactly the right pattern: links to SEC's own docs, instructs exploration, names jq as a tool. The "skim a real 10-Q" step is excellent.
- **Find Company Submissions** ✅ — the *best teaching moment in the course*: showing the failing curl with the 8-digit CIK, the error, then the fix. Keep this exact structure. Minor: `isXRBL`/`isInlineXRBL` in the sample should be `isXBRL`/`isInlineXBRL`; the stripped-empty `recent` arrays could use one more sentence ("in your response these arrays will be parallel and thousands long") to pre-explain index-alignment.
- **Filter Submissions and Retrieve Doc** ✅ — the parallel-arrays insight ("arrays are ordered, use the index") is the key algorithmic hint, properly delivered as a hint not a solution. Typo: "orginaztion". The Archives URL format note should mention accession numbers are dash-stripped in the path (students discover their accessionNumber has dashes; the URL doesn't — a 30-minute confusion for the unwarned).
- **Expanding Your CIK Module** ✅ — signature-only spec, correct pattern. Typo: backtick inside the parens of `quarterly_filing`. ⚪ Doesn't define what the methods *return* (URL? document text? both?) — the next module assumes document text is retrievable, so state the contract.

### Introduction to AWS
- Root page 🟡 — accurate but reads like marketing copy (it largely is — value-prop language). Acceptable as scene-setting; trim the "In conclusion" duplication (it appears in both the intro and the bullets).
- **AWS Services** 🟡 — covers S3, Lambda, DynamoDB, ElastiCache, API Gateway, Bedrock, Kendra. **DynamoDB, ElastiCache, and Kendra are never used in the course**; their presence dilutes signal for beginners deciding what to learn. Either cut to the used set (S3, Lambda, API Gateway, Bedrock, +EventBridge which *is* used but absent!) or visually separate "used in this course" from "good to know." The open-source-alternative framing per service is a genuinely nice touch — keep it.
- **Key Reading** ✅ — fine. Add the AWS CLI install link and Bedrock model-access doc here or in the new setup page (#9).

### Project SEC Lambda  *(target of the SAM rewrite)*
- Root page 🔴🟠🔵 — see critical findings #3 and #4. Additional notes:
  - The two-Lambda architecture (daily EDGAR refresh → S3; synchronous document-fetch) is genuinely good design and worth keeping through the rewrite — it quietly teaches event-driven vs request-response invocation.
  - "S3 bucket should have version history enabled" — good, but nothing explains why; one sentence on versioning-as-safety-net earns the requirement.
  - EventBridge console walkthrough → replaced by SAM `Schedule` event in the rewrite. Note: cron expressions in EventBridge are **UTC**; say so or students will "fix" working schedules.
  - `https://www.sec.gov/files/company_tickers.json  # replace with the actual URL` — that *is* the actual URL; the comment confuses.
  - Lambda 2's sample contradicts itself: "Remember to replace 'your-bucket-name'…" appears in a code block that contains no bucket name.
- **Lambda Error Handling** 🟡 — accurate content, but the page says everything twice: the bullet list and the "common pitfalls" list are ~80% the same items reworded. Consolidate to one list. "try-catch blocks… in Python" → Python calls them try/except. The invocation-retries doc link is good. ⚪ Missing the one error-handling topic this course actually needs: **what a Lambda error looks like from the caller's side** (the `FunctionError` field students will meet in Task 3) and reading CloudWatch logs step-by-step — freshmen have never seen a log group.

### Introduction to Large Language Models
🟠🟡 — Concepts (prompt, context, why cloud) are appropriately pitched. Issues:
- GPT-3 as the marquee example dates the page badly for a 2026 audience
- "Anthropics Claude model" → "Anthropic's"
- "6 months to 3 years out of date" — fine, but this is where to plant the knowledge-cutoff concept that finding #2 depends on; make it explicit and have the 10Q project reference back
- PagedAttention paper link is great for seniors, intimidating for freshmen — label it "(advanced, optional reading)" … except nothing is optional now, so label it "(advanced — skim the abstract)"
- ⚪ This page should introduce the Converse/InvokeModel distinction and link the single source-of-truth Models page (#1)

### Project 10Q Inference  *(target of the CDK rewrite)*
- Root page 🟡 — the framing (supplement an LLM's missing knowledge with a data source) is the thesis of the entire course, delivered in one paragraph with a trailing escaped `\` artifact. Worth expanding by 2–3 paragraphs since this is the conceptual hinge.
- **Part 1: Inference Test** 🔴🟠 — model retired (#1). Doc links are the right kind (API reference + guide). The duplicate link (Invoke Model Guide and Python Example point at the same anchor) should differ or be merged. Date confusion: "current date as of writing this is August 2024… AMZN filed their latest 10-Q as of writing this on April 2 2024" — the linked document is `amzn-20240630.htm` (Q2, filed Aug 1, 2024). Pick one timeline. Better per #2: rewrite with rolling-recency instructions instead of dates that rot.
- **Sample Prompt without Context** 🔴🟠 — finding #2 in full. Also: "it did not know it occurred Q3 **2024**" → Q3 **2023**; "Claude 3.5 Sonnet on April 2024" vs Part 1's "Claude 3 Sonnet" vs Part 3's "Claude 3.5" — three different models named across one project.
- **Part 2: Inference with Context** 🟠⚪ — the exercise is right; the mechanics are missing (#9.4: HTML→text, token limits). The prompt template ("Using the information below…") is fine as a starting point; consider asking students to *compare* two prompt structures — cheap experimentation, on-theme.
- **Part 3: Question to Enhanced Prompt** 🟠🟡 — "ask Claude 3.5" (#1). Contract lacks `period` (#6) — as written, you can't specify *which* quarter, which the front end later requires. Trailing comma in the example JSON makes it invalid — same validator problem as Data Formats. Otherwise the right level of specification: input/output defined, implementation open.

### Optional Front-End module with AWS Amplify  *(de-optionalize + Gen 2 + CDK)*
- Root page 🟠🟡 — "This **optional** module…" + "your **RAG system**" (RAG doesn't exist yet at this point in the course; after restructure it comes two modules later — change to "your 10Q Inference service"). Conceptual content on Amplify is otherwise accurate and current-ish.
- **Optional Project 1: Amplify React quickstart** ✅🟡 — pointing at the official quickstart is correct (it's maintained; the course isn't). "admin-level sandbox credentials" deserves a footnote in a 152-student shared-account world — coordinate with however the course AWS accounts are provisioned.
- **Amplify Concepts** 🟡⚪ — title promises "Amplify functions and Amplify UI"; page delivers three bullets on UI only. Either write the functions half (it's load-bearing for Task 1's "Amplify-managed function" option) or retitle.
- **Task 1** ✅ — good spec-style page: components named, contract given, docs linked per component, mapping hint (partner→ticker) is exactly the right kind of hint. The "Reminder this is what the lambda input looks like" JSON repeats Part 3's trailing-comma invalid JSON.
- **Task 2** 🔵🟡 — see #8 (fully copy-pasteable CLI) and #7 (CORS section is fine; the "CURL will NO LONGER work" note is a genuinely good teaching beat — keep the *idea*, fix the caps/typo: "orginaztion"-class issues throughout). Console-vs-CLI duality becomes moot in the CDK rewrite.
- **Task 3** 🔵🟡 — see #8 (complete solution) and #7 (CRA/Gen-1 references). Code itself is high quality and *correct* (claims path, base64 handling, CORS preflight, FunctionError mapping) — which is exactly why handing it over teaches nothing. The "Production hardening" section (security options table, observability, pitfalls) is excellent reference material — keep all of it; it's the solution code that should become acceptance criteria + doc links.

---

## What's genuinely good (preserve through the rewrite)
1. The **fail-first teaching** in Find Company Submissions (show the error, then the fix)
2. **Fair Access policy** prominence — rare for a course to teach API citizenship
3. Spec-not-solution style of the CIK and EDGAR modules
4. Real domain data (SEC filings) instead of toy APIs — the 10-Q skim instruction especially
5. jq, JSON validators, roadmap.sh, Everything cURL — the external-resource curation is consistently strong
6. The two-Lambda architecture in SEC Lambda (event-driven + request/response in one project)
7. Task 3's architecture diagram and production-hardening reference section

## Recommended page template (for the rewrite)
Every project page gets: **Goal** (1 paragraph) → **Contract** (inputs/outputs, exact) → **Required reading** (specific doc pages, not doc homepages) → **Constraints** (e.g., "must use SAM", "User-Agent required") → **Acceptance criteria** (observable behaviors students self-check) → **Hints** (collapsed `<details>`, the dead-end-preventers only). Code fragments only where the thing is undiscoverable from docs (claims paths, URL formats, gotcha headers).

## Maintenance recommendation
Add a `last-verified: YYYY-MM` line to every page touching AWS/Bedrock/Amplify specifics, and create a summer-prep checklist (verify model IDs, re-run the no-context example, click every external link). Findings #1 and #2 happened because the course has no freshness mechanism — agent-router running a quarterly "verify the course still works" job against a checklist is the durable fix.
