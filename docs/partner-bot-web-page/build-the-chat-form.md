# Build the Chat Form

## Goal

Compose a query form from Amplify UI components that collects the four fields required by the [Lambda Contract](../reference/contract.md), submits them to a handler function, and renders the inference response. This page focuses on the UI layer only — connecting to the live Lambda happens in the next page.

## Contract

Your form must produce a request body conforming to the [Lambda Contract](../reference/contract.md):

```json
{
  "question": "What were the key investments disclosed this quarter?",
  "ticker": "AMZN",
  "year": 2024,
  "period": "Q2"
}
```

The response shape (also defined in the contract) is:

```json
{
  "answer": "...",
  "meta": {}
}
```

Your UI renders the `answer` field to the user.

## Required Reading

- Amplify UI React introduction: <https://ui.docs.amplify.aws/react/getting-started/introduction>
- SelectField: <https://ui.docs.amplify.aws/react/components/selectfield>
- TextField: <https://ui.docs.amplify.aws/react/components/textfield>
- Button: <https://ui.docs.amplify.aws/react/components/button>
- View: <https://ui.docs.amplify.aws/react/components/view>
- [Lambda Contract](../reference/contract.md)

## Constraints

1. Use **Amplify UI components** (`SelectField`, `TextField`, `Button`, `View`) — do not introduce a separate component library.
2. The company `SelectField` must display human-readable names (e.g., "Apple") but your submit handler must map them to the uppercase stock ticker (`"AAPL"`) before building the request body.
3. The `year` field must submit as an integer, not a string.
4. The `period` field must offer exactly the enum values defined in the contract: `Q1`, `Q2`, `Q3`, `Q4`, `FY`.
5. Do not hardcode a Lambda endpoint in this page. Wire a **stub handler** that logs the request body to the console and returns a fake response. The real integration is the next page's concern.
6. Display a loading indicator while the handler is in flight and an error message if it rejects.

## Acceptance Criteria

- [ ] The form renders four inputs: company (select), year (select), period (select), and question (text).
- [ ] Submitting the form logs a JSON object to the browser console whose shape matches the Lambda Contract request schema.
- [ ] The `ticker` value in the logged object is the mapped stock ticker, not the display name.
- [ ] The `year` value is a number.
- [ ] After submission, the stub response's `answer` field renders in a `View` component below the form.
- [ ] A loading state is visible between submission and response.
- [ ] If the handler throws, an error message appears in the UI.

## Hints

<details>
<summary>Mapping company names to tickers</summary>

Define a mapping object outside your component:

```tsx
const COMPANIES: Record<string, string> = {
  Apple: "AAPL",
  Amazon: "AMZN",
  Microsoft: "MSFT",
};
```

Iterate over its keys to build `SelectField` options, then look up the ticker on submit.

</details>

<details>
<summary>Stub handler pattern</summary>

Create an async function that simulates a network call:

```tsx
async function submitQuery(body: RequestBody): Promise<ResponseBody> {
  console.log("Request:", JSON.stringify(body, null, 2));
  await new Promise((r) => setTimeout(r, 800));
  return { answer: "Stub response — replace with real Lambda call.", meta: {} };
}
```

Replace this function with a real `fetch` call in the next page.

</details>

<details>
<summary>Managing loading and error state</summary>

Use React state to track submission status:

```tsx
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

Wrap your handler in a try/catch that sets these values. Amplify UI's `Button` accepts an `isLoading` prop; `View` can conditionally render the error.

</details>

<details>
<summary>Year select — generating a range</summary>

Generate year options dynamically so the form stays current:

```tsx
const currentYear = new Date().getFullYear();
const years = Array.from({ length: 5 }, (_, i) => currentYear - i);
```

</details>

---
Last verified: 2026-06
