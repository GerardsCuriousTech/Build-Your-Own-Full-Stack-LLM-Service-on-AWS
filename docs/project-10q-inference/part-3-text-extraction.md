# Part 3: Text Extraction

## Goal

Build a reusable text-extraction utility that converts a raw SEC filing (HTML) into clean plain text suitable for inclusion in an LLM prompt. SEC EDGAR serves 10-Q filings as HTML documents. Passing raw HTML to the model wastes tokens on markup and confuses extraction. This part teaches you to strip the markup, estimate the resulting token count, and truncate intelligently so the text fits within the model's context window.

## Contract

This part produces a utility function, not a standalone Lambda. The function accepts raw HTML (as returned by your EDGAR API library) and returns plain text ready for prompt injection.

The utility is consumed by the Lambda you build in [Part 4](part-4-question-to-enhanced-prompt.md), which conforms to the [Lambda Contract](../reference/contract.md).

**Function signature (conceptual):**

```text
extract_text(html: str, max_tokens: int) -> str
```

- `html` — the raw HTML body of a 10-Q filing retrieved from SEC EDGAR.
- `max_tokens` — the maximum number of tokens the returned text should approximate (a budget, not a hard guarantee).
- Returns plain text with HTML tags stripped and whitespace normalized, truncated to fit within `max_tokens`.

## Required Reading

- Python standard library: [`html.parser`](https://docs.python.org/3.12/library/html.parser.html)
- [Bedrock runtime quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) — understand input token limits
- [Models](../reference/models.md) — the canonical model and its context window size
- [Filter Submissions and Retrieve Doc](../project-sec-edgar-api-library/filter-submissions-and-retrieve-doc.md) — how your EDGAR library retrieves filing HTML

## Constraints

- Use Python 3.12.
- Use only the Python standard library for HTML parsing (no BeautifulSoup, no lxml). The stdlib `html.parser` module is sufficient for this task.
- Deploy any supporting infrastructure via CDK.
- Your extraction must handle the common structure of SEC 10-Q filings: nested tables, inline styles, `<ix:` XBRL tags, and `&nbsp;` entities.
- The token estimate does not need to be exact. A simple heuristic (characters divided by four, or words multiplied by 1.3) is acceptable. Do not call the Bedrock tokenizer API for this step.
- Your truncation strategy must preserve complete sentences or paragraphs — do not cut mid-word or mid-sentence.

## Acceptance Criteria

1. Given a raw 10-Q HTML document, your function returns readable plain text with no HTML tags, no inline CSS, and no XBRL markup.
2. Whitespace is normalized: no runs of blank lines, no leading/trailing whitespace on lines, no tab characters.
3. When the extracted text exceeds `max_tokens` (estimated), the function truncates to the budget while preserving sentence boundaries.
4. Your function handles at least three different companies' 10-Q filings without crashing or producing garbled output.
5. You can demonstrate the token reduction: show the raw HTML character count versus the extracted text character count for a sample filing.

## Hints

Start with a subclass of `html.parser.HTMLParser`. Override `handle_data` to collect text content and `handle_starttag`/`handle_endtag` to insert whitespace where block-level elements end (e.g., `</p>`, `</div>`, `</tr>`). Skip content inside `<style>` and `<script>` tags entirely.

SEC filings use XBRL inline tags (`<ix:nonFraction>`, `<ix:nonNumeric>`, etc.) that wrap the actual text. Your parser should treat these as transparent — extract the text inside them without emitting the tag names.

For `&nbsp;` and other HTML entities, `HTMLParser` calls `handle_entityref` or `handle_charref`. Convert them to their plain-text equivalents (a non-breaking space becomes a regular space).

For token estimation, a simple ratio works: one token is roughly four characters of English text. If your extracted text has 40,000 characters, that is approximately 10,000 tokens. This is imprecise but sufficient for budgeting. The model will not reject a prompt that is slightly over or under — you are avoiding the failure mode of sending a 200,000-token document into a model with a smaller context window.

Truncation strategy: split the text into paragraphs (double newline). Accumulate paragraphs until adding the next one would exceed the budget. This preserves document structure and avoids cutting mid-thought. If even the first paragraph exceeds the budget, fall back to sentence-level splitting.

Test with filings from different companies. SEC formatting varies — some use deeply nested tables for financial statements, others use flat `<p>` tags. Your parser should handle both gracefully.

---
Last verified: 2026-06
