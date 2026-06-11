# Task 1: Build the form with Amplify UI components

#### Learning goals

* **UI composition:** Use SelectField, TextField, Button, and View from Amplify UI.
* **Contract-first design:** Define a clear request/response schema for your inference Lambda.
* **Integration:** Send form data to your Lambda and render the response.

#### Prerequisites

* **Completed Project 1:** Running Amplify React app.
* **Function ready:** A Lambda for 10‑Q inference (from your prior course module) or a new Amplify-managed function that proxies to your existing inference workflow:
  * Course reference: https://llm-aws.course.gspivey.com/project-10q-inference/project-part-3-question-to-enhanced-prompt



Build a UI out of Amplify Components. Use `SelectField` three times once for partner, then year then period.&#x20;

* partner: string (e.g., “Acme Corp”)
* year: number (e.g., 2023)
* period: enum: "Annual" | "Q1" | "Q2" | "Q3" | "Q4"

Then use the `TextField` component to write your question.

* question: string (free text)

Then have one `Button`.

* Query: Call the Lambda with the values you have

Lastly, present the results in `View`  component.

Docs:

* SelectField: https://ui.docs.amplify.aws/react/components/selectfield
* TextField: https://ui.docs.amplify.aws/react/components/textfield
* Button: https://ui.docs.amplify.aws/react/components/button
* View (for display): https://ui.docs.amplify.aws/react/getting-started/introduction

Reminder this is what the lambda input looks like. So you will likely need to add a period and keep a mapping in your `SelectField` to go from human readable Company Name to stock ticker.

```json
{
  "question": "How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?",
  "ticker": "AMZN",
  "year": "2024",
}
```
