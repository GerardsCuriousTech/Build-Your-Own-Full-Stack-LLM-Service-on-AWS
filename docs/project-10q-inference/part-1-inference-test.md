# Part 1: Inference Test

## Goal

Invoke the [canonical course model](../reference/models.md) on Bedrock and observe how it responds to questions about information beyond its training cutoff. You will see first-hand that the model produces plausible but inaccurate answers when asked about very recent SEC filings — establishing the motivation for retrieval-augmented context in Part 2.

## Contract

This part has no Lambda contract yet — you are calling the model interactively from a Python script. Part 4 wraps this into the full [Lambda Contract](../reference/contract.md).

Your script invokes the Bedrock `InvokeModel` or `Converse` API and prints the response text to stdout.

## Required Reading

- [InvokeModel API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
- [Converse API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [Invoke Model Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html)
- [Models](../reference/models.md) — use the canonical model identifier listed there

## Constraints

- Use Python 3.12 and boto3.
- Use the model identifier from [Models](../reference/models.md). Do not hardcode a model ID in your script.
- Deploy your inference script's supporting infrastructure (IAM role, any test Lambda) via CDK.
- Do not provide any filing text as context in this part — the point is to observe the model's limitations without help.

## Acceptance Criteria

1. Your script successfully invokes the model and prints a response.
2. You ask the model at least one question about a specific figure from a company's most recent 10-Q filing (filed within the last three months). Use the EDGAR API skills from the previous project to identify a recent filing.
3. You document the model's response and compare it against the actual filing. The model should produce an inaccurate or incomplete answer — demonstrating the training cutoff gap.
4. You save both the question(s) and response(s) for comparison in Part 2.

## Hints

Start by confirming your Bedrock access works. Ask the model a general knowledge question — something it will answer correctly — to verify your boto3 call is wired up:

- "Can you explain what a 10-Q filing contains?"
- "What is a stock ticker symbol?"

Once the plumbing works, shift to the real exercise: find a company's most recent quarterly filing on SEC EDGAR. Look for filings from the last few months — these are beyond the model's training cutoff. Within the filing, find a specific dollar figure (revenue, investment amount, operating expense) in a section like "Management's Discussion and Analysis."

Ask the model about that figure without providing the filing. Note how confident the response sounds despite being wrong or incomplete.

The model's training data has a cutoff date. Facts disclosed in very recent filings are invisible to it. This is not a bug — it is the fundamental limitation that Part 2 solves with retrieval-augmented context.

---

> **Capture-Dated Example** — results shown may differ from your own.

The prompt below was sent to the model without any filing context. The model's response demonstrates that it lacks specific knowledge of facts published after its training cutoff.

**Prompt:**

`How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?`

**Response:**

```text
In Q3 2023, Amazon announced it would invest up to $4 billion in Anthropic. In January 2024 (Q1 2024), Amazon completed an initial $1.25 billion investment in Anthropic as part of that agreement, with the potential to invest up to $2.75 billion more in the future. So the confirmed investment amounts are:

Q3 2023: Announced up to $4 billion (but no money invested yet)
Q1 2024: $1.25 billion actually invested

The remaining potential investment of up to $2.75 billion has not been made as of early 2024 and would depend on future decisions by Amazon.
```

The [10-Q filing](https://www.sec.gov/ix?doc=/Archives/edgar/data/1018724/000101872424000130/amzn-20240630.htm) shows the actual figures differ from the model's response. The model conflated announced intent with actual investment amounts.

**Key takeaway:** an LLM answering without context produces plausible but inaccurate financial details. This is why Part 2 provides the filing text as context.

When you run this exercise, pick a recent filing (within the last few months) and ask about a specific figure from it. The model's training cutoff means it will not have seen very recent disclosures — use that gap to demonstrate the value of retrieval-augmented context.

---
Last verified: 2026-06
