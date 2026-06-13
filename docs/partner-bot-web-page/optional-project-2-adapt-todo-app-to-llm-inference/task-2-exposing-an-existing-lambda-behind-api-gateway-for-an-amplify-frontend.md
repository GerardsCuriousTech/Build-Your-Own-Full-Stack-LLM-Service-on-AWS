# Task 2: Exposing an existing Lambda behind API Gateway for an Amplify frontend

### Overview

* **API type:** Use API Gateway HTTP API for simpler setup and managed CORS. Choose REST API only if you need advanced features (usage plans, API keys, request transformations).
* **Integration style:** Use Lambda proxy integration so your function receives the raw request and returns a simple statusCode/headers/body response.
* **Route design:** POST /inference (or similar) to accept JSON payloads from your form.

***

### Prerequisites

* **Existing Lambda:** Deployed in the target AWS account and region.
* **Amplify app:** Local dev URL (e.g., http://localhost:5173) and hosted domain (e.g., https://main.xxxxx.amplifyapp.com).
* **Schema clarity:** Input JSON conforming to the [Lambda Contract](../../reference/contract.md) (`ticker`, `year`, `period`, `question`) and output shape (`answer`, `meta`).

***

### Create the API and integrate Lambda

#### Console steps (HTTP API, recommended)

1. **Create HTTP API**
   * **API type:** HTTP API.
   * **Name:** inference-api (or similar).
2. **Add integration**
   * **Integration type:** Lambda.
   * **Function:** Select your existing 10Q inference Lambda.
   * Confirm the console adds invoke permissions for API Gateway to your Lambda.
3. **Add a route**
   * **Method and path:** POST /inference.
   * **Integration target:** The Lambda integration from step 2.
4. **Create a stage**
   * **Stage name:** prod (or dev).
   * **Auto-deploy:** Enabled, so config changes go live without manual deployments.
5. **Note your invoke URL**
   * It looks like: https://abc123.execute-api.us-east-1.amazonaws.com
   * Your full endpoint is: https://abc123.execute-api.us-east-1.amazonaws.com/inference

#### AWS CLI steps (HTTP API)

```bash
# 0) Variables
REGION=us-east-1
LAMBDA_ARN=arn:aws:lambda:$REGION:123456789012:function:tenq-inference
API_NAME=inference-api

# 1) Create API
API_ID=$(aws apigatewayv2 create-api \
  --name "$API_NAME" \
  --protocol-type HTTP \
  --region $REGION \
  --query 'ApiId' --output text)

# 2) Create Lambda integration
INTEGRATION_ID=$(aws apigatewayv2 create-integration \
  --api-id $API_ID \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations \
  --payload-format-version 2.0 \
  --region $REGION \
  --query 'IntegrationId' --output text)

# 3) Create route
aws apigatewayv2 create-route \
  --api-id $API_ID \
  --route-key "POST /inference" \
  --target integrations/$INTEGRATION_ID \
  --region $REGION

# 4) Grant invoke permission to API Gateway
aws lambda add-permission \
  --function-name $LAMBDA_ARN \
  --statement-id apigw-$API_ID \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn arn:aws:execute-api:$REGION:123456789012:$API_ID/*/POST/inference \
  --region $REGION

# 5) Create stage with auto-deploy
aws apigatewayv2 create-stage \
  --api-id $API_ID \
  --stage-name prod \
  --auto-deploy \
  --region $REGION

# 6) Get URL
aws apigatewayv2 get-apis --region $REGION --query "Items[?ApiId=='$API_ID'].ApiEndpoint" --output text
```

***

### Test the endpoint and connect from Amplify

#### Smoke test with curl

```bash
ENDPOINT="https://abc123.execute-api.us-east-1.amazonaws.com/inference"
curl -i -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker":"MSFT",
    "year":2024,
    "period":"Q2",
    "question":"Summarize revenue growth drivers."
  }'
```

* **Expect:** HTTP/1.1 200 and a JSON body. If you see 403 “Missing Authentication Token,” the route or method doesn’t match. If you see 500, log the Lambda error and confirm event.body parsing.

### Enable CORS and deploy

#### CORS for HTTP API

1. **Open CORS settings** in your HTTP API.
2. **Allowed origins:** Add your dev and prod origins.
   * https://main.xxxxx.amplifyapp.com (and any branch previews you use)
3. **Allowed methods:** POST, OPTIONS.
4. **Allowed headers:** Content-Type, Authorization.
5. **Expose headers:** Content-Type (and any custom headers you need).
6. **Credentials:** Off unless you require cookies.
7. **Save:** With auto-deploy enabled, changes go live immediately.

> Tip: Also return CORS headers from Lambda on success and error:
>
> * Access-Control-Allow-Origin: your domain (or “\*” for public)
> * Access-Control-Allow-Headers: Content-Type
> * Access-Control-Allow-Methods: POST, OPTIONS

CURL will NO LONGER work after adding this check. This is the first step in securing your endpoint. We are limiting it to the front end. However this is not actual authorization. We will add that later.

***
