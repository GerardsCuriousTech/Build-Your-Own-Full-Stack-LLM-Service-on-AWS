# Sample Prompt with Context

> **Capture-Dated Example** — results shown may differ from your own.

This example demonstrates the same question from Part 1, but this time the full 10-Q filing text is provided as context. With the filing content available, the model accurately extracts the investment figures.

**Prompt structure:**

```
Using the information below. How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?

<full 10-Q filing text inserted here>
```

The prompt included the complete text of Amazon's 10-Q for the quarter ended June 30, 2024 (filed August 2024). The filing runs to thousands of lines — scroll to the bottom to see the model's response.

When you run this exercise, download the text of the most recent 10-Q for your chosen company using your EDGAR API Lambda, then paste it into the prompt after your question.

---

**Response:**

```
Based on the information provided in the quarterly report:

- Amazon invested $1.25 billion in a convertible note from Anthropic in Q3 2023.

- Amazon invested $2.75 billion in a second convertible note from Anthropic in Q1 2024.

So the total investment in Anthropic across Q3 2023 and Q1 2024 was $4 billion.
```

**Key takeaway:** With the filing text as context, the model extracts the correct figures directly from the disclosure. Compare this to the incorrect response in Part 1 where no context was provided.
