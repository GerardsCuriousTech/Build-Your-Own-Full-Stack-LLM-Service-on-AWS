# Task 1: Build the form with Amplify UI components

#### Learning goals

* **UI composition:** Use SelectField, TextField, Button, and View from Amplify UI.
* **Contract-first design:** Build your form against the [Lambda Contract](../../reference/contract.md).
* **Integration:** Send form data to your Lambda and render the response.

#### Prerequisites

* **Completed Project 1:** Running Amplify React app.
* **Function ready:** A Lambda for 10‑Q inference (from your prior course module) or a new Amplify-managed function that proxies to your existing inference workflow:
  * Course reference: https://llm-aws.course.gspivey.com/project-10q-inference/project-part-3-question-to-enhanced-prompt



Build a UI out of Amplify Components. Your form must produce a request body conforming to the [Lambda Contract](../../reference/contract.md). Use `SelectField` three times: once for company (mapped to a stock ticker), then year, then period.

* ticker: string — use a `SelectField` with human-readable company names that maps to the uppercase stock ticker (e.g., "Apple" maps to `"AAPL"`)
* year: number (e.g., 2024)
* period: enum: `"Q1"` | `"Q2"` | `"Q3"` | `"Q4"` | `"FY"`

Then use the `TextField` component to write your question.

* question: string (free text)

Then have one `Button`.

* Query: Call the Lambda with the values you have

Lastly, present the results in `View` component.

Docs:

* SelectField: https://ui.docs.amplify.aws/react/components/selectfield
* TextField: https://ui.docs.amplify.aws/react/components/textfield
* Button: https://ui.docs.amplify.aws/react/components/button
* View (for display): https://ui.docs.amplify.aws/react/getting-started/introduction

Your `SelectField` for company displays human-readable names but your submit handler must map to the stock ticker before sending the request. See the [Lambda Contract](../../reference/contract.md) for the full schema.

```json
{
  "question": "What were the key investments disclosed this quarter?",
  "ticker": "AMZN",
  "year": 2024,
  "period": "Q2"
}
```
