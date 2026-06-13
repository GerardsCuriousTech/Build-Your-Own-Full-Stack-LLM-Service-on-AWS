# Project: SEC Lambda (SAM)

In this project you build two AWS Lambda functions deployed with SAM CLI. Together they form an event-driven backend that keeps SEC EDGAR data fresh and answers questions about company filings on demand.

## Architecture

The project contains two functions with different invocation patterns:

**Lambda 1 — EDGAR File Refresh (scheduled)**
Downloads the SEC EDGAR company-tickers JSON file and uploads it to an S3 bucket. A SAM `Schedule` event triggers the function daily. The S3 bucket has versioning enabled so each upload creates a recoverable snapshot rather than overwriting the previous data.

**Lambda 2 — Document Retrieval (synchronous)**
Accepts a JSON request conforming to the [Lambda Contract](../reference/contract.md), retrieves the specified 10-K or 10-Q filing text, and returns a response through a synchronous `Invoke` call.

Both functions reuse the SEC modules you built in earlier projects (CIK lookup, EDGAR API library). The key lesson is that Lambda is *not* your laptop: dependencies must be explicitly packaged, environment variables replace hardcoded paths, and the SEC Fair Access policy still applies in the cloud.

## What you will learn

- Initializing a SAM project with `sam init` and structuring `template.yaml`
- Packaging Python dependencies (notably `requests`) into a Lambda deployment
- Scheduling Lambda invocations with EventBridge via SAM event configuration
- Handling synchronous Lambda invocations and mapping request/response to a defined contract
- Reading CloudWatch logs to diagnose runtime failures

## Prerequisites

- Completed: Project SEC CIK Lookup Module
- Completed: Project SEC EDGAR API Library
- An AWS account with CLI access configured (see [Setup: AWS Account](../reference/setup-aws-account.md))
- Bedrock model access enabled (see [Setup: Bedrock Access](../reference/setup-bedrock-access.md))
- SAM CLI installed ([AWS SAM CLI install guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))
- Python 3.12

## Pages in this module

| Page | Purpose |
|------|---------|
| [Lambda Project Setup](lambda-project-setup.md) | Initialize the SAM project, configure `template.yaml`, package dependencies |
| [Lambda Error Handling](lambda-error-handling.md) | Error patterns, CloudWatch logs, local debugging with `sam local invoke` |
