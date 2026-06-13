# Sample Prompt without Context

> **Capture-Dated Example** — results shown may differ from your own.

The prompt below was sent to the model without any filing context. The model's response demonstrates that it lacks specific knowledge of facts published after its training cutoff.

**Prompt:**

`How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?`

**Response:**

```
In Q3 2023, Amazon announced it would invest up to $4 billion in Anthropic. In January 2024 (Q1 2024), Amazon completed an initial $1.25 billion investment in Anthropic as part of that agreement, with the potential to invest up to $2.75 billion more in the future. So the confirmed investment amounts are:

Q3 2023: Announced up to $4 billion (but no money invested yet)
Q1 2024: $1.25 billion actually invested

The remaining potential investment of up to $2.75 billion has not been made as of early 2024 and would depend on future decisions by Amazon.
```

The [10-Q filing](https://www.sec.gov/ix?doc=/Archives/edgar/data/1018724/000101872424000130/amzn-20240630.htm) shows the actual figures differ from the model's response. The model conflated announced intent with actual investment amounts and got the Q3 2023 amount wrong.

**Key takeaway:** An LLM answering without context produces plausible but inaccurate financial details. This is why Part 2 provides the filing text as context.

When you run this exercise, pick a recent filing (within the last few months) and ask about a specific figure from it. The model's training cutoff means it will not have seen very recent disclosures — use that gap to demonstrate the value of retrieval-augmented context.
