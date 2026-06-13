# Partner Bot Web Page

This module connects your 10Q Inference Lambda to a browser-based front end. By the end you will have a working React application — hosted on AWS Amplify — that lets a user select a company, filing period, and question, then displays the LLM-generated answer.

The module is the midpoint deliverable of the course: everything before it builds backend services; everything after it extends or secures the full stack. Completing it proves your Lambda, your deployment pipeline, and your front-end tooling all work together end to end.

## Technology choices

| Layer | Tool | Why |
|-------|------|-----|
| Hosting & backend orchestration | AWS Amplify Gen 2 | Declarative infrastructure, sandbox dev environments, CI-friendly deploys |
| Build tool | Vite | Fast HMR, native ESM, zero-config React support |
| UI components | Amplify UI for React | Accessible, themeable primitives that integrate with Amplify data and auth |
| Auth (later) | Amazon Cognito via Amplify Auth | Token-based identity with minimal custom code |

## Module sequence

| Page | What you will do |
|------|-----------------|
| [Amplify Gen 2 Setup](amplify-gen2-setup.md) | Initialize a Vite + React project with Amplify Gen 2 and deploy a sandbox |
| [Build the Chat Form](build-the-chat-form.md) | Compose a query form from Amplify UI components and render inference results |
| [Connect to Lambda via API Gateway](connect-to-lambda.md) | Wire the form to your 10Q Inference Lambda through an HTTP API |
| [Authentication with Cognito](authentication-with-cognito.md) | Add sign-in/sign-up and protect the API route with a JWT authorizer |

## Prerequisites

- A deployed 10Q Inference Lambda that accepts requests conforming to the [Lambda Contract](../reference/contract.md)
- Node.js LTS and npm installed
- An AWS account with Amplify and Bedrock access enabled ([Setup: AWS Account](../reference/setup-aws-account.md))
- Git configured with a remote repository ([GitHub Setup](../introduction-to-git-and-github/project-github-setup.md))
