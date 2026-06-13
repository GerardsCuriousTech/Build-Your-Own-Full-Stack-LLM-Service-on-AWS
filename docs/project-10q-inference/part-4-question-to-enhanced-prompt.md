# Part 4: Question to Enhanced Prompt

## Goal

Build and deploy a CDK-backed Lambda that accepts a question, a stock ticker, a filing year, and a period — retrieves the relevant 10-Q filing from SEC EDGAR, extracts clean text using your Part 3 utility, constructs an enhanced prompt with the filing as context, invokes the [canonical course model](../reference/models.md), and returns the answer. This is the end-to-end pipeline: the Lambda receives a structured request and returns a grounded answer that the front-end (Partner Bot Web Page) will consume.

## Contract

Your Lambda's input and output must conform to the [Lambda Contract](../reference/contract.md).

**Request:**

```json
{
  "question": "What was the company's total revenue this quarter?",
  "ticker": "AMZN",
  "year": 2024,
  "period": "Q3"
}
```

**Response:**

```json
{
  "answer": "Based on the 10-Q filing, total net sales for the quarter were $158.9 billion, an increase of 11% compared to the same quarter in the prior year.",
  "meta": {
    "model": "the canonical model from reference/models.md",
    "input_tokens": 9842,
    "output_tokens": 287,
    "latency_ms": 3200
  }
}
```

The `period` field accepts `Q1`, `Q2`, `Q3`, `Q4`, or `FY`. Use the period to locate the correct filing on SEC EDGAR.

## Required Reading

- [Lambda Contract](../reference/contract.md) — the schema your Lambda must conform to
- [Models](../reference/models.md) — use the canonical model identifier
- [Converse API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [Part 3: Text Extraction](part-3-text-extraction.md) — the utility that converts filing HTML to prompt-ready text
- [Filter Submissions and Retrieve Doc](../project-sec-edgar-api-library/filter-submissions-and-retrieve-doc.md) — filing retrieval via EDGAR
- [Project: CDK Init](../cdk-bridge/project-cdk-init.md) — CDK project structure

## Constraints

- Use Python 3.12 and boto3.
- Deploy via CDK. Define the Lambda function, its IAM role (Bedrock invoke permission, network egress for SEC EDGAR), and any supporting resources in your CDK stack.
- Use the model identifier from [Models](../reference/models.md). Do not hardcode a model ID.
- Validate the incoming event against the contract schema. Return a structured error (not a stack trace) for invalid requests.
- Use your Part 3 text-extraction utility to convert the filing HTML to plain text before injecting it into the prompt.
- Set a token budget for the filing context that leaves room for the question, the system instructions, and the model's response. A reasonable default: reserve 80% of the model's context window for the filing text.
- Include a custom `User-Agent` header on all SEC EDGAR HTTP requests.
- Do not provide complete solution code. Your implementation is the deliverable.

## Acceptance Criteria

1. Your Lambda accepts a valid contract request and returns a valid contract response.
2. Given an invalid request (missing field, invalid `period` value, non-uppercase ticker), your Lambda returns a structured validation error — not an unhandled exception.
3. The Lambda retrieves the correct 10-Q filing for the specified ticker, year, and period from SEC EDGAR.
4. The filing HTML is converted to plain text using your Part 3 extraction utility, respecting the token budget.
5. The enhanced prompt includes both the user's question and the extracted filing text as context.
6. The model's response answers the question using information from the filing (verifiable by reading the source document).
7. The `meta` object in the response includes the model identifier, input token count, output token count, and latency.
8. The Lambda is deployed via CDK with appropriate IAM permissions (Bedrock `InvokeModel`, network egress).

## Hints

The Lambda handler orchestrates four steps in sequence:

1. **Validate** — check that all required fields are present and conform to the contract. Return early with an error response if validation fails.
2. **Retrieve** — use your EDGAR API library to fetch the filing HTML for the given ticker, year, and period. Map the `period` value to the correct fiscal quarter endpoint on EDGAR.
3. **Extract** — pass the HTML through your Part 3 text-extraction function with a token budget.
4. **Invoke** — construct the enhanced prompt and call the model via the Converse API.

For the prompt structure, a pattern that works well:

```text
Using only the SEC filing text provided below, answer the following question. If the answer is not contained in the filing, say so explicitly.

Question: {question}

Filing ({ticker} {period} {year}):
{extracted_text}
```

The instruction to answer "only from the filing" reduces hallucination. Including the ticker, period, and year in the prompt gives the model context about what document it is reading.

For the `meta` object, the Converse API response includes token usage in the `usage` field (`inputTokens`, `outputTokens`). Capture latency by timing the API call with `time.perf_counter()`.

Map `period` to the fiscal quarter when searching EDGAR submissions. A company filing a 10-Q for `Q2` of `2024` reports the quarter ended June 30, 2024 (for most calendar-year filers). Your EDGAR library's `filter_submissions` function should accept a form type (`10-Q`) and date range to locate the correct filing.

For `FY` (full-year), the relevant form type is `10-K`, not `10-Q`. Handle this case explicitly in your retrieval logic.

Pick a recent filing and verify the Lambda's answer against the source document. The integration test is: invoke the Lambda, read the answer, open the filing on EDGAR, and confirm the figure appears in the text.
