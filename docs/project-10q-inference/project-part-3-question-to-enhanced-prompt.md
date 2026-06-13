# Project Part 3: Question to Enhanced Prompt

Create a Lambda that takes a question, a company stock ticker, and a year.\
It should ask Claude 3.5 the question providing the latest 10-K or 10-Q document as context and return the response. You should use other Lambda's created or documents stored in S3 from previous assignments that will help you complete this project.

### Example Lambda Input

```json
{
  "question": "How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?",
  "ticker": "AMZN",
  "year": "2024",
}
```
