# Authentication with Cognito

## Goal

Protect your API Gateway endpoint with a Cognito User Pool authorizer so that only signed-in users can invoke the inference Lambda. You will create an edge Lambda that validates payloads, reads JWT claims for caller identity, and invokes your core Lambda via boto3. The React frontend attaches the Cognito ID token using Amplify Gen 2's `fetchAuthSession`.

## Contract

The frontend sends the same [Lambda Contract](../reference/contract.md) request body as before, but now includes an `Authorization` header containing the Cognito ID token (JWT).

API Gateway verifies the JWT before the request reaches your edge Lambda. The edge Lambda receives the verified claims at:

```
event["requestContext"]["authorizer"]["jwt"]["claims"]
```

The edge Lambda validates the request body, invokes the core Lambda with the contract-conforming payload, and returns the core Lambda's response to the browser.

## Required Reading

- HTTP API JWT authorizers: <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html>
- API Gateway HTTP API payload format v2.0 — `requestContext.authorizer`: <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html#http-api-develop-integrations-lambda.proxy-format>
- Amplify Gen 2 `fetchAuthSession`: <https://docs.amplify.aws/react/build-a-backend/auth/connect-your-frontend/sign-in/#sign-in-with-an-external-identity-provider>
- boto3 Lambda invoke: <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html>
- [Lambda Contract](../reference/contract.md)

## Constraints

1. Use an **API Gateway JWT authorizer** configured with your Amplify Cognito User Pool — not a Lambda authorizer.
2. The edge Lambda runtime must be **Python 3.12**.
3. The edge Lambda must **validate the request body** against the contract fields (`question`, `ticker`, `year`, `period`) and return HTTP 400 with missing field names if validation fails.
4. The edge Lambda must invoke the core Lambda using boto3's `invoke` with `InvocationType="RequestResponse"`. Check the `FunctionError` key in the response to detect core Lambda failures.
5. The edge Lambda's IAM role must have an inline policy granting `lambda:InvokeFunction` on the core Lambda only — not a wildcard.
6. The frontend must use `fetchAuthSession` from `aws-amplify/auth` to retrieve the ID token, and pass it in the `Authorization` header. Use the Amplify Gen 2 configuration pattern (`amplify_outputs.json`) and Vite environment variables (`import.meta.env.VITE_*`).
7. CORS allowed headers must include `Authorization`.

## Acceptance Criteria

- [ ] A Cognito JWT authorizer is attached to the `POST /inference` route on your HTTP API.
- [ ] An unauthenticated request (no `Authorization` header) returns HTTP 401.
- [ ] A request with a valid token but a malformed body (missing required fields) returns HTTP 400 with the missing field names in the response.
- [ ] A request with a valid token and valid body round-trips through the edge Lambda to the core Lambda and returns the inference answer.
- [ ] The edge Lambda checks for `FunctionError` in the boto3 invoke response and returns HTTP 502 if the core Lambda errored.
- [ ] The React app attaches the ID token from `fetchAuthSession` and successfully calls the protected endpoint when the user is signed in.
- [ ] When the user is not signed in, the app does not attempt the API call (or handles the 401 gracefully in the UI).

## Hints

<details>
<summary>Architecture diagram</summary>

```
[ React + Amplify Authenticator ]
         | fetchAuthSession() → ID token
         v
[ fetch POST /inference, Authorization: <token> ]
         |
         v
[ API Gateway HTTP API ]
   └─ JWT Authorizer (Cognito User Pool)
         |  (token verified → claims injected)
         v
[ Edge Lambda (Python 3.12) ]
   - Reads claims from event.requestContext.authorizer.jwt.claims
   - Validates body fields against the contract
   - Invokes core Lambda via boto3
         |
         v
[ Core Lambda (existing inference logic) ]
         |
         v
[ Response flows back: Edge → API Gateway → Browser ]
```

</details>

<details>
<summary>Creating the JWT authorizer</summary>

In the API Gateway console under Authorizers, create a JWT authorizer. The issuer URL is your Cognito User Pool's URL:

```
https://cognito-idp.{region}.amazonaws.com/{userPoolId}
```

The audience is your User Pool App Client ID. Attach this authorizer to your `POST /inference` route.

</details>

<details>
<summary>Reading claims in the edge Lambda</summary>

With a JWT authorizer on an HTTP API (payload v2.0), verified claims arrive at:

```python
claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
user_sub = claims["sub"]
email = claims.get("email", "")
```

This path is specific to HTTP API v2.0. REST APIs use a different event structure.

</details>

<details>
<summary>Detecting core Lambda errors</summary>

After calling `lambda_client.invoke(...)`, check for the `FunctionError` key:

```python
response = lambda_client.invoke(
    FunctionName=target_name,
    InvocationType="RequestResponse",
    Payload=json.dumps(payload).encode(),
)
if "FunctionError" in response:
    # The core Lambda threw an unhandled exception
    ...
```

Read the `Payload` stream for the error details.

</details>

<details>
<summary>Frontend: attaching the token</summary>

Use the Amplify Gen 2 auth pattern:

```tsx
import { fetchAuthSession } from "aws-amplify/auth";

const { tokens } = await fetchAuthSession();
const idToken = tokens?.idToken?.toString() ?? "";

const response = await fetch(import.meta.env.VITE_INFERENCE_API, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: idToken,
  },
  body: JSON.stringify(payload),
});
```

</details>

<details>
<summary>Security options beyond JWT authorizer (advanced — skim)</summary>

- **Lambda authorizer:** Custom logic (e.g., allow-listed emails, API keys) — more flexible but more code to maintain.
- **IAM auth with federated identities:** Strongest, but adds SigV4 client complexity.
- **Public endpoint:** CORS-limited only; no identity verification. Acceptable for non-sensitive demos but never for production.

</details>

<details>
<summary>Common pitfalls</summary>

- **CORS mismatch after adding auth:** You must add `Authorization` to the `Access-Control-Allow-Headers` list in your HTTP API CORS config. Without it, the browser's preflight fails.
- **Wrong token type:** The JWT authorizer expects the ID token, not the access token. `fetchAuthSession` returns both — use `tokens.idToken`.
- **Edge Lambda timeout:** Set to at least 15 seconds. The core Lambda may take time; ensure the edge Lambda's timeout exceeds the core Lambda's expected duration while staying under API Gateway's 30-second limit.
- **Missing invoke permission:** The edge Lambda's role needs `lambda:InvokeFunction` on the specific core Lambda ARN. A generic Lambda role does not include this.

</details>

---

Last verified: 2026-06
