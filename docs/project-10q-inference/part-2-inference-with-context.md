# Part 2: Inference with Context

## Goal

Demonstrate that providing a 10-Q filing as prompt context transforms the model's output from confident guessing to accurate extraction. You will ask the same question from Part 1, but this time include the filing text in the prompt. The contrast between the two responses is the core lesson of this module: retrieval-augmented context gives an LLM access to information beyond its training cutoff.

## Contract

This part has no Lambda contract yet — you are calling the model interactively. Part 4 wraps the full flow into the [Lambda Contract](../reference/contract.md).

Your script sends a prompt containing both your question and the filing text, then prints the response.

## Required Reading

- [Converse API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [Models](../reference/models.md) — use the canonical model identifier
- [Lambda Contract](../reference/contract.md) — the schema your final Lambda will conform to in Part 4

Review the SEC EDGAR module pages for retrieving filing documents programmatically:

- [Filter Submissions and Retrieve Doc](../project-sec-edgar-api-library/filter-submissions-and-retrieve-doc.md)

## Constraints

- Use Python 3.12 and boto3.
- Use the model identifier from [Models](../reference/models.md).
- Deploy supporting infrastructure via CDK.
- Use a 10-Q filing from the last three months. Do not hardcode a specific filing date or company — your approach must work for any recent filing.
- Retrieve the filing text programmatically using your EDGAR API library or Lambda from previous modules.

## Acceptance Criteria

1. Your script retrieves the text of a recent 10-Q filing (filed within the last three months) for your chosen company.
2. Your script sends a prompt that includes both the question and the filing text as context.
3. The model's response accurately extracts the requested figure from the filing, in contrast to the inaccurate response from Part 1.
4. You compare the Part 1 (no context) and Part 2 (with context) responses side by side, confirming the improvement.

## Hints

Structure your prompt so the model knows to answer from the provided text rather than its training data. A pattern that works well:

```text
Using the information below, answer the following question.

Question: <your question here>

Document:
<filing text here>
```

Retrieve the filing text using your EDGAR API Lambda or library. The 10-Q is HTML on SEC EDGAR — you need the text content, not the raw markup. For now, a basic approach (strip tags, extract readable text) is sufficient. Part 3 covers text extraction in depth.

Be aware of the model's input token limit. A full 10-Q can be tens of thousands of tokens. If your filing is very long, truncate to the relevant section (the one containing the answer to your question). The model performs better on focused context than on a massive document dump.

Pick the same company and question you used in Part 1. The side-by-side comparison is the deliverable — it demonstrates that context is the difference between a wrong answer and a right one.

---

> **Capture-Dated Example** — results shown may differ from your own.

This example uses the same question from Part 1, but provides the full 10-Q filing text as context.

**Prompt structure:**

```text
Using the information below, answer the following question.

Question: How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?

Document:
<full 10-Q filing text inserted here>
```

The prompt included the complete text of Amazon's 10-Q for the quarter ended June 30, 2024 (filed August 2024).

**Response:**

```text
Based on the information provided in the quarterly report:

- Amazon invested $1.25 billion in a convertible note from Anthropic in Q3 2023.

- Amazon invested $2.75 billion in a second convertible note from Anthropic in Q1 2024.

So the total investment in Anthropic across Q3 2023 and Q1 2024 was $4 billion.
```

**Key takeaway:** with the filing text as context, the model extracts the correct figures directly from the disclosure. Compare this to the incorrect response in Part 1 where no context was provided. The model did not learn new facts — it simply had access to the relevant document.

When you run this exercise, use the same company and question from Part 1. Download the filing text using your EDGAR API library and include it in the prompt. The contrast between your two responses is the core deliverable of this part.

---
Last verified: 2026-06
