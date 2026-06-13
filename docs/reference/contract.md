# Lambda Contract

This page defines the canonical request and response schema for the course Lambda function. Every project page that specifies Lambda input or output links here and conforms to this schema.

## Request Schema

The Lambda function accepts a JSON object with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | yes | The natural-language question to answer |
| `ticker` | string | yes | Stock ticker symbol (e.g., `"AAPL"`) |
| `year` | integer | yes | Filing year in four-digit format (e.g., `2024`) |
| `period` | enum | yes | Filing period: `"Q1"`, `"Q2"`, `"Q3"`, `"Q4"`, or `"FY"` |

### Field rules

- `question` must be a non-empty string.
- `ticker` must be a non-empty string containing only uppercase letters.
- `year` must be a four-digit integer (1900 or later).
- `period` must be exactly one of: `Q1`, `Q2`, `Q3`, `Q4`, `FY`.

## Response Schema

The Lambda function returns a JSON object with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | The LLM-generated answer text |
| `meta` | object | Metadata about the invocation (model used, token count, latency) |

## Valid Example

A well-formed request and its corresponding response:

**Request:**

```json
{
  "question": "What was the revenue growth compared to the prior quarter?",
  "ticker": "AAPL",
  "year": 2024,
  "period": "Q3"
}
```

**Response:**

```json
{
  "answer": "Based on the 10-Q filing, revenue grew 5% compared to the prior quarter, driven primarily by services segment growth.",
  "meta": {
    "model": "the canonical model from reference/models.md",
    "input_tokens": 1847,
    "output_tokens": 312,
    "latency_ms": 2150
  }
}
```

## Invalid Example

A malformed request and its expected validation error:

**Request (invalid):**

```json
{
  "question": "What were the earnings?",
  "ticker": "AAPL",
  "year": 2024,
  "period": "Annual"
}
```

**Validation error:**

```json
{
  "error": "ValidationError",
  "message": "Invalid value for 'period': 'Annual'. Must be one of: Q1, Q2, Q3, Q4, FY."
}
```

The `period` field accepts only the five enumerated values. `"Annual"` is not valid; use `"FY"` for full-year filings.
