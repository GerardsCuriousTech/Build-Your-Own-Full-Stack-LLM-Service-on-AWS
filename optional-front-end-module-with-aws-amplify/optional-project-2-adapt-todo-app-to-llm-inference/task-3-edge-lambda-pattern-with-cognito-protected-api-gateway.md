# Task 3: Edge Lambda pattern with Cognito-protected API Gateway

We will create an Edge Lambda behind API Gateway (protected by the Amplify Authenticator’s Cognito User Pool). That edge Lambda validates input, inspects JWT claims, and invokes your existing “core” Lambda via boto3. This cleanly separates auth and request shaping from your core logic, and it’s reproducible for coursework.

***

### Architecture overview

* **Edge Lambda:** HTTP entrypoint; receives browser request, verifies auth context, validates/normalizes payload, and calls the core Lambda.
* **Core Lambda:** Your existing business logic; no API-facing concerns.
* **API Gateway HTTP API:** Fronts the edge Lambda; uses a Cognito User Pool Authorizer; CORS restricted to your Amplify domains.
* **Amplify Authenticator:** Students sign in; frontend attaches the Cognito ID token in the Authorization header.

***

### Step-by-step setup

#### 1) Create the edge Lambda (Python)

1. **Function:** Create a new Lambda (Python 3.12). Name it something like `inference-edge`.
2. **Env vars:**
   * **TARGET\_LAMBDA\_NAME:** Name or ARN of your existing core Lambda.
   * **ALLOWED\_ORIGINS:** Comma-separated origins (e.g., `http://localhost:5173,https://main.xxxxx.amplifyapp.com`).
3. **Timeout:** Set to something sensible (e.g., 15s). Ensure the core Lambda completes with enough headroom under API Gateway’s 30s limit.
4. **Role policy:** Attach an inline policy to allow invoking the core Lambda (see “Permissions” below).

#### 2) Wire API Gateway HTTP API to the edge Lambda

1. **API:** Create an HTTP API (or use existing).
2. **Integration:** Add Lambda proxy integration → choose `inference-edge`.
3. **Route:** Add `POST /inference` pointing at the integration.
4. **Stage:** Create `prod` (auto-deploy on).

#### 3) Add Cognito authorizer (reuse Amplify User Pool)

1. **Authorizers:** Create a **Cognito** authorizer.
2. **User Pool:** Select the same User Pool used by Amplify Authenticator.
3. **Audience:** Use the User Pool App Client ID.
4. **Attach:** On `POST /inference`, set Authorization to this authorizer.

#### 4) Configure CORS on the API

* **Allowed origins:** Your Amplify domains and `http://localhost:5173`.
* **Allowed methods:** `POST, OPTIONS`.
* **Allowed headers:** `Content-Type, Authorization`.
* **Credentials:** Off unless you truly need cookies.

***

### Python edge lambda example (HTTP API v2.0 + boto3)

```python
import json
import os
import base64
import boto3

lambda_client = boto3.client("lambda")

TARGET_LAMBDA_NAME = os.environ.get("TARGET_LAMBDA_NAME", "")
ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o.strip()]

def cors_headers(origin: str | None) -> dict:
    allow_origin = origin if origin in ALLOWED_ORIGINS else (ALLOWED_ORIGINS[0] if ALLOWED_ORIGINS else "*")
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
    }

def parse_body(event) -> tuple[dict | None, str | None]:
    body = event.get("body")
    if body is None:
        return None, "Missing request body"
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    try:
        return json.loads(body), None
    except Exception:
        return None, "Body must be valid JSON"

def handler(event, context):
    # HTTP API v2.0 context
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    origin = headers.get("origin") or headers.get("referer")

    # Preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 204, "headers": cors_headers(origin), "body": ""}

    # Auth claims (from Cognito User Pool authorizer)
    claims = (event.get("requestContext", {})
                  .get("authorizer", {})
                  .get("jwt", {})
                  .get("claims"))
    if not claims:
        return {"statusCode": 401, "headers": cors_headers(origin), "body": json.dumps({"error": "Unauthorized"})}

    # Parse and validate input
    data, err = parse_body(event)
    if err:
        return {"statusCode": 400, "headers": cors_headers(origin), "body": json.dumps({"error": err})}

    # Example required fields
    required = ["partner", "year", "period", "question"]
    missing = [k for k in required if data.get(k) in (None, "")]
    if missing:
        return {
            "statusCode": 400,
            "headers": cors_headers(origin),
            "body": json.dumps({"error": f"Missing fields: {', '.join(missing)}"})
        }

    # Enrich payload with identity (optional)
    user_sub = claims.get("sub")
    email = claims.get("email")
    enriched = {
        "input": data,
        "identity": {"sub": user_sub, "email": email},
        "requestMeta": {
            "ip": headers.get("x-forwarded-for"),
            "userAgent": headers.get("user-agent"),
        },
    }

    # Invoke core Lambda
    try:
        invoke_resp = lambda_client.invoke(
            FunctionName=TARGET_LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(enriched).encode("utf-8"),
        )
        payload_bytes = invoke_resp.get("Payload").read()
        core_body = payload_bytes.decode("utf-8") if payload_bytes else ""
        # Try parse core response; if it's already JSON, pass through
        try:
            core_json = json.loads(core_body) if core_body else {}
        except Exception:
            core_json = {"raw": core_body}

        status_code = 200
        if "FunctionError" in invoke_resp:
            status_code = 502
            core_json = {"error": "Core lambda error", "detail": core_json}

        return {
            "statusCode": status_code,
            "headers": cors_headers(origin),
            "body": json.dumps(core_json),
        }
    except lambda_client.exceptions.ResourceNotFoundException:
        return {
            "statusCode": 500,
            "headers": cors_headers(origin),
            "body": json.dumps({"error": "Target lambda not found"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers(origin),
            "body": json.dumps({"error": "Invocation failure", "detail": str(e)})
        }
```

* **What it does:** Validates auth, handles CORS and preflight, parses JSON, enriches with user claims, invokes the core Lambda, and returns its result.
* **Core Lambda input:** Receives the `enriched` JSON. If you prefer pure pass‑through, send `data` directly.
* **Core Lambda response:** If your core returns `{"answer": "...", "meta": {...}}`, it flows straight back to the browser.

***

### Permissions for the edge lambda role

Attach an inline policy to the edge Lambda’s execution role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InvokeCoreLambda",
      "Effect": "Allow",
      "Action": ["lambda:InvokeFunction"],
      "Resource": [
        "arn:aws:lambda:REGION:ACCOUNT_ID:function:CORE_LAMBDA_NAME",
        "arn:aws:lambda:REGION:ACCOUNT_ID:function:CORE_LAMBDA_NAME:*"
      ]
    },
    {
      "Sid": "Logs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

* **Replace:** REGION, ACCOUNT\_ID, and CORE\_LAMBDA\_NAME accordingly.
* **Why include version/alias ARN:** Covers invocations of specific versions/aliases if you use them.

***

### Wire into your Amplify frontend

We’ll fetch from your Cognito‑protected API Gateway endpoint, passing the Amplify Authenticator’s **ID token** in the `Authorization` header.

***

### 1️⃣ Set your API endpoint as an environment variable

In **Create React App**, name it with the `REACT_APP_` prefix so it’s injected at build time:

```bash
# .env.production (for deployed build)
REACT_APP_INFERENCE_API=https://abc123.execute-api.us-east-1.amazonaws.com/inference
```

Restart your dev server after adding these.

***

### 2️⃣ Install Amplify Auth helpers (if not already)

```bash
npm install aws-amplify
```

And make sure your Amplify project is configured with your Cognito User Pool settings in something like `aws-exports.js`.

***

### 3️⃣ Create a helper function to call API Gateway

```jsx
// api.js
import { fetchAuthSession } from 'aws-amplify/auth';

export async function callInferenceAPI(payload) {
  // Get the current signed-in user's tokens
  const { tokens } = await fetchAuthSession();
  const idToken = tokens?.idToken?.toString() || '';

  const res = await fetch(process.env.REACT_APP_INFERENCE_API, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': idToken,  // JWT for Cognito User Pool authorizer
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errText = await res.text().catch(() => '');
    throw new Error(`API ${res.status}: ${errText}`);
  }

  return res.json();
}
```

***

### 4️⃣ Use it inside a React component

```jsx
// InferenceForm.js
import React, { useState } from 'react';
import { callInferenceAPI } from './api';

export default function InferenceForm() {
  const [partner, setPartner] = useState('');
  const [year, setYear] = useState(2023);
  const [period, setPeriod] = useState('Q1');
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await callInferenceAPI({ partner, year, period, question });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input value={partner} onChange={e => setPartner(e.target.value)} placeholder="Partner" />
        <input type="number" value={year} onChange={e => setYear(Number(e.target.value))} />
        <input value={period} onChange={e => setPeriod(e.target.value)} placeholder="Period" />
        <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="Question" />
        <button type="submit" disabled={loading}>Run Inference</button>
      </form>

      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
```

***

### 5️⃣ How it works

1. **User signs in** through Amplify Authenticator → Amplify stores the Cognito ID token.
2. **`fetchAuthSession()`** retrieves the token in React code.
3. **`fetch()`** sends the POST request to API Gateway with the token in `Authorization`.
4. **API Gateway Cognito Authorizer** verifies the JWT before invoking the Lambda.

***

### Production hardening and troubleshooting

#### Security options

* **Public endpoint (simplest):** CORS-limited; no auth. Suitable only for non-sensitive demos.
* **Cognito authorizer:** Protect with user sign-in; the frontend attaches the ID token.
* **Lambda authorizer:** Custom checks (e.g., allow-listed emails or API keys).
* **IAM auth (signed requests):** Strong but adds client complexity (federated identities).

#### Observability

* **Logs:** Enable detailed logs for API Gateway; use structured logs in Lambda.
* **Metrics:** Track 4xx/5xx rates, latency, and Lambda duration. Surface latency in your UI meta.

#### Common pitfalls

* **CORS mismatch:** Origin not listed or wildcard with credentials on. Align origins and headers; test OPTIONS.
* **Wrong route:** POST to / when route is /inference. Verify method and path.
* **No invoke permission:** Add lambda:InvokeFunction permission with source ARN for your API.
* **Body parsing:** event.body is a string; missing JSON.parse causes 500s.
* **Stage URL:** Missing stage in REST API URLs; for HTTP API, the base URL includes the stage automatically.

####
