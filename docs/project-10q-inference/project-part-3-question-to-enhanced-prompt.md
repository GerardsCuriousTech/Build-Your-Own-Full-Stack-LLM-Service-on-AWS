# Project Part 3: Question to Enhanced Prompt

Create a Lambda that takes a question, a company stock ticker, a year, and a filing period. It should invoke the [canonical course model](../reference/models.md), providing the relevant 10-K or 10-Q document as context, and return the response. Reuse the Lambdas and S3 documents from previous assignments to retrieve the filing text.

Your Lambda's input and output must conform to the [Lambda Contract](../reference/contract.md).

### Example Lambda Input

```json
{
  "question": "How much did the company invest in AI infrastructure this quarter?",
  "ticker": "AMZN",
  "year": 2024,
  "period": "Q2"
}
```

Pick a recent filing and a question whose answer appears in that filing. The example above is illustrative — use your own company and question so you can verify the response against the source document.
