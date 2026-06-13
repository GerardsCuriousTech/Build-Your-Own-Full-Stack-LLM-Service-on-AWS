# Lambda Error Handling

## Goal

Build a robust error-handling layer for your SEC Lambda functions so that failures surface clearly in logs, callers receive structured error responses, and you can diagnose problems without redeploying.

## Contract

Your Lambda function must:

- Return a structured JSON error response (not a stack trace) when something goes wrong.
- Distinguish between client errors (bad input) and server errors (downstream failures).
- Produce CloudWatch log entries that let you trace a specific invocation from request to failure.
- Set the appropriate HTTP status code when invoked behind API Gateway (via the [Lambda contract](../reference/contract.md)).

When another Lambda invokes yours synchronously, the caller must detect failures via the `FunctionError` field in the `invoke` response — not by parsing the payload alone.

## Required Reading

- [AWS Lambda error handling (Python)](https://docs.aws.amazon.com/lambda/latest/dg/python-exceptions.html)
- [Invocation response — FunctionError field](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_ResponseSyntax)
- [Lambda retry behavior](https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html)
- [CloudWatch Logs concepts](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Monitoring-CloudWatch-Metrics.html)
- [SAM CLI logs command](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-logs.html)
- [Lambda contract](../reference/contract.md)
- [Models reference](../reference/models.md)

## Constraints

1. Use `try`/`except` (Python's term — not "try/catch").
2. Every `except` block must log the exception with enough context to identify the failing invocation (request ID, input parameters).
3. Never return a raw traceback to callers. Return a JSON body with an `error` key describing the failure class.
4. When invoking another Lambda with `boto3`, always check the response for the `FunctionError` key before reading the payload.
5. Use `sam logs` and `sam local invoke` for local reproduction before deploying diagnostic changes.
6. All model references link to the [Models reference page](../reference/models.md).

## Acceptance Criteria

1. Your handler wraps all business logic in a `try`/`except` that catches specific exception types before a final catch-all `Exception`.
2. A Bedrock `invoke_model` call that fails (throttle, invalid input, expired model) is caught, logged with the request context, and returned as a structured error.
3. An SEC EDGAR HTTP request that fails (network timeout, 403 from missing User-Agent, non-200 status) is caught and surfaced with the URL that failed.
4. When Lambda A invokes Lambda B synchronously, Lambda A checks `response["FunctionError"]` and handles the downstream failure without crashing.
5. You can find your Lambda's log group in CloudWatch, locate a specific invocation by request ID, and read the error output.
6. You can reproduce a failure locally using `sam local invoke` with a test event, and stream deployed logs using `sam logs --tail`.

## Hints

<details>
<summary>Structuring the try/except</summary>

Catch the narrowest exceptions first. For Bedrock calls, `botocore.exceptions.ClientError` covers API-level failures. For HTTP calls, `requests.exceptions.RequestException` covers network-level failures. A final `except Exception` prevents unhandled crashes but should log at ERROR level — it means you missed a case.

</details>

<details>
<summary>Detecting FunctionError from a caller</summary>

When you call `lambda_client.invoke(FunctionName=..., Payload=...)`, the response dict always has a `StatusCode`. But a 200 status does NOT mean the invoked function succeeded — Lambda returns 200 for the transport even when the function itself raised an error. Check `response.get("FunctionError")`. If present, the value is `"Handled"` or `"Unhandled"` and the `Payload` contains the error output, not your expected result.

</details>

<details>
<summary>Finding your log group in CloudWatch</summary>

Lambda log groups follow the naming pattern `/aws/lambda/<function-name>`. Inside the log group, each invocation creates log entries prefixed with the request ID. Search for that ID to isolate a single execution. The `START`, `END`, and `REPORT` lines bracket each invocation and show duration, memory used, and billed duration.

</details>

<details>
<summary>Using sam logs and sam local invoke</summary>

`sam logs -n YourFunctionName --stack-name your-stack --tail` streams live logs from the deployed function — useful during integration testing. `sam local invoke YourFunctionName -e events/test-event.json` runs the function in a local Docker container using your `template.yaml` definition — useful for reproducing errors without deploying.

</details>

<details>
<summary>Consolidated error list</summary>

Your SEC Lambda functions will encounter these error categories:

| Category | Example | Suggested Response |
|----------|---------|-------------------|
| Input validation | Missing `ticker` field | 400 — describe the missing/invalid field |
| SEC EDGAR network | Timeout or connection refused | 502 — upstream unreachable |
| SEC EDGAR 403 | Missing or malformed User-Agent | 502 — access denied by upstream |
| SEC EDGAR 404 | Invalid CIK or accession number | 404 — filing not found |
| Bedrock throttle | `ThrottlingException` | 429 — retry after backoff |
| Bedrock model error | Invalid model ID or payload | 502 — model invocation failed |
| Bedrock response parse | Unexpected response shape | 500 — internal parse error |
| S3 access | Bucket/key not found, permission denied | 500 — storage access failed |
| Unhandled | Anything not caught above | 500 — internal error (log full traceback) |

</details>

---

Last verified: 2026-06
