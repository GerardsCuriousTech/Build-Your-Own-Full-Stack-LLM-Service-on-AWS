---
description: >-
  You will extend the TODO app with dropdowns and a text input to gather query
  parameters for your 10-Q inference Lambda. Then you'll call the function and
  render the answer.
---

# Adapt TODO App to LLM Inference

## Project Overview: Cognito-Protected API Gateway with Edge Lambda

In this project, you'll build a **secure, full-stack pipeline** that connects an authenticated React frontend (Amplify Authenticator) to a Lambda-powered backend, with **API Gateway and Amazon Cognito** enforcing who can call your code.

Instead of exposing your core Lambda directly to the world, you'll create a lightweight **"edge" Lambda** that sits behind API Gateway. This edge function will:

* Accept only requests from **signed-in users** via a Cognito User Pool Authorizer.
* Parse, validate, and enrich the request with the user's identity claims.
* Call an **existing core Lambda** using the AWS SDK for Python (boto3), then return its results to the browser.

By the end, you'll have a **repeatable blueprint** for protecting any AWS Lambda behind a proper identity layer — something you can re-use in professional projects, capstone demos, or production workloads.

***

### What you'll build

1. **React Frontend with Amplify Authenticator**
   * A sign-in experience backed by Amazon Cognito.
   * Code that retrieves a user's ID token and calls a secured API.
2. **API Gateway HTTP API**
   * Single `/inference` route.
   * Configured CORS for your dev and prod Amplify domains.
   * Cognito User Pool Authorizer to verify JWTs.
3. **Edge Lambda (Python)**
   * Validates input payloads.
   * Reads JWT claims to identify the caller.
   * Invokes the existing "core" Lambda via boto3 and returns the response.
4. **Core Lambda**
   * Your existing business logic — unchanged, but now safely tucked behind the edge.

***

### Key skills you'll learn

| Area                      | Skills                                                                                                            |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Frontend Auth**         | Using Amplify Authenticator with Cognito User Pool; retrieving JWTs in React; adding Auth headers to API calls.   |
| **Backend Security**      | Configuring API Gateway with Cognito User Pool Authorizers; enforcing per-route auth; securing CORS.              |
| **AWS Lambda**            | Creating a new Lambda in Python; parsing API Gateway v2.0 event payloads; reading JWT claims; enriching requests. |
| **AWS SDK (boto3)**       | Programmatically invoking other Lambdas from Python; handling synchronous responses and errors.                   |
| **Architecture Patterns** | Separating authentication/validation from core business logic; using an "edge" Lambda as a secure proxy.          |
| **Debugging & Testing**   | End-to-end testing with signed and unsigned requests; tracing failures in CloudWatch Logs.                        |

***

### Why this pattern matters

* **Security**: Only authenticated Amplify users can invoke your core Lambda — no more open endpoints.
* **Maintainability**: Auth, input validation, and request shaping are handled in one place without touching core logic.
* **Reusability**: You can drop any other Lambda behind this edge with minimal changes.
* **Teaching value**: Demonstrates a real-world architecture that blends front-end authentication with back-end authorization.

***

### Learning flow

1. **Set up** the new edge Lambda and wire it to API Gateway.
2. **Add** Cognito User Pool Authorizer referencing Amplify's pool.
3. **Configure** CORS so only your domains can call the API.
4. **Write** the Python event parser and boto3 invoker.
5. **Update** React code to attach the Cognito ID token to API requests.
6. **Test** with both logged-in and logged-out states to see the security in action.

***

### End-to-End Architecture Diagram

```
[ React App + Amplify Authenticator ] 
         |  (User signs in -> gets Cognito ID token)
         v
 [ Fetch API Call w/ Authorization: <ID Token> ]
         |
         v
[ Amazon API Gateway (HTTP API) ]
   +- Cognito User Pool Authorizer
      -> Verifies JWT (issued by Amplify's User Pool)
         |
         v
[ Edge Lambda (Python) ]
   - Parses JSON body & validates fields
   - Reads JWT claims (sub, email, etc.)
   - Enriches payload with identity metadata
   - Uses boto3 to invoke:
         v
[ Inference Lambda (existing logic) ]
   - Runs inference / business logic
   - Returns structured JSON
         ^
         |
[ Edge Lambda returns response to API Gateway ]
         ^
         |
[ React App receives & renders results ]
```

***

### Request flow step-by-step

1. **Sign-in**: Student uses Amplify Authenticator; Cognito issues ID token.
2. **Frontend request**: React `fetch()` POSTs to API Gateway with the token in `Authorization` header.
3. **Gateway auth**: API Gateway's Cognito Authorizer verifies the token against the User Pool.
4. **Edge Lambda**:
   * Accepts only authenticated traffic.
   * Validates payload shape.
   * Logs caller identity (from token claims).
   * Calls the **Inference Lambda** via boto3 `invoke()`.
5. **Inference Lambda**: Runs the heavy lifting — e.g., processing, model calls, data lookup.
6. **Response**: Edge Lambda wraps the output, returns JSON to API Gateway then to the React app.
7. **UI update**: Browser renders the data; errors appear in the form if validation or auth failed.
