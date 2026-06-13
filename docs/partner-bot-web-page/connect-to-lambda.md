# Connect to Lambda via API Gateway

## Goal

Replace the stub handler from the previous page with a live connection to your deployed inference Lambda. You will create an API Gateway HTTP API, integrate it with your existing Lambda, configure CORS for your Amplify domains, and call the endpoint from your React app using the Vite environment variable pattern.

## Contract

Your frontend sends a POST request to the API Gateway endpoint. The request body conforms to the [Lambda Contract](../reference/contract.md):

```json
{
  "question": "What were the key revenue drivers this quarter?",
  "ticker": "MSFT",
  "year": 2024,
  "period": "Q2"
}
```

The Lambda returns a response conforming to the [Lambda Contract](../reference/contract.md):

```json
{
  "answer": "...",
  "meta": {}
}
```

API Gateway uses **Lambda proxy integration** with **payload format version 2.0**, so your Lambda receives the full HTTP event and must return `statusCode`, `headers`, and `body`.

## Required Reading

- API Gateway HTTP API concepts: <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html>
- Working with HTTP API Lambda integrations: <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html>
- HTTP API payload format version 2.0: <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html#http-api-develop-integrations-lambda.proxy-format>
- Configuring CORS for HTTP APIs: <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>
- Vite environment variables: <https://vite.dev/guide/env-and-mode>
- [Lambda Contract](../reference/contract.md)

## Constraints

1. Use **API Gateway HTTP API** (not REST API) with Lambda proxy integration.
2. Payload format version must be **2.0** — your Lambda receives the event shape documented in the required reading above.
3. CORS allowed origins must include both your local dev URL (`http://localhost:5173`) and your deployed Amplify domain.
4. Store the API endpoint in a Vite environment variable (`VITE_INFERENCE_API`) — do not hardcode URLs in component source.
5. The frontend `fetch` call must send `Content-Type: application/json` and handle non-2xx responses by surfacing an error to the user.
6. Do not add authentication yet — that is the next page's concern. The endpoint is open for now (CORS-restricted only).

## Acceptance Criteria

- [ ] An HTTP API exists in API Gateway with a `POST /inference` route integrated with your Lambda.
- [ ] A curl request to the endpoint with a valid contract-conforming body returns HTTP 200 and a JSON response containing `answer` and `meta`.
- [ ] CORS is configured: a preflight OPTIONS request from your Amplify origin returns the correct `Access-Control-Allow-*` headers.
- [ ] The React app reads `import.meta.env.VITE_INFERENCE_API` for the endpoint URL.
- [ ] Submitting the form in the browser calls the live Lambda and renders the `answer` below the form.
- [ ] A malformed request (missing a required field) returns HTTP 400 and the error displays in the UI.

## Hints

<details>
<summary>API Gateway console vs CLI</summary>

The console workflow is: Create HTTP API, add a Lambda integration (select your function), add route `POST /inference`, create a `prod` stage with auto-deploy, then note the invoke URL.

With the AWS CLI, the key commands are `aws apigatewayv2 create-api`, `create-integration`, `create-route`, and `create-stage`. You also need `aws lambda add-permission` to grant API Gateway invoke access.

</details>

<details>
<summary>Invoke permission</summary>

API Gateway needs explicit permission to invoke your Lambda. The source ARN pattern is:

```
arn:aws:execute-api:{region}:{account}:{api-id}/*/POST/inference
```

Without this, you get a 500 from the gateway even though your route and integration look correct.

</details>

<details>
<summary>Vite environment variable pattern</summary>

Create `.env.local` (for development) and `.env.production` (for the deployed build):

```
VITE_INFERENCE_API=https://abc123.execute-api.us-east-1.amazonaws.com/inference
```

Access it in code as `import.meta.env.VITE_INFERENCE_API`. Vite only exposes variables prefixed with `VITE_`.

</details>

<details>
<summary>Replacing the stub handler</summary>

In the previous page you defined a stub function. Replace it with a real fetch:

```tsx
const response = await fetch(import.meta.env.VITE_INFERENCE_API, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload),
});
```

Parse the response and handle errors as before.

</details>

<details>
<summary>CORS troubleshooting</summary>

If the browser shows a CORS error but curl works, check that your HTTP API CORS configuration includes the exact origin (protocol + host + port). Common issues: missing `http://localhost:5173` in the allowed origins list, or `Authorization` not listed in allowed headers (needed in the next page).

</details>

<details>
<summary>Lambda response format for proxy integration</summary>

With payload format 2.0, your Lambda must return an object with at least `statusCode` and `body` (a JSON string). If you omit `statusCode`, API Gateway returns 500.

</details>

---

Last verified: 2026-06
