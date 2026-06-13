# CDK Bridge: SAM to CDK

This module marks the transition point in the course. Everything before this module deploys with SAM CLI. Everything after deploys with the AWS Cloud Development Kit (CDK).

SAM served you well for the SEC Lambda project — a single function, a `template.yaml`, and `sam deploy`. That workflow stays manageable when you have one or two resources. The 10Q Inference project ahead requires a Lambda function, an S3 bucket, IAM roles with cross-service permissions, a Bedrock inference profile reference, and eventually an API Gateway. Defining all of that in raw CloudFormation YAML becomes brittle. CDK lets you write that infrastructure in Python 3.12 — the same language as your Lambda code — with constructs that handle sensible defaults, cross-resource wiring, and type checking.

## What this module covers

1. **Why CDK?** — When SAM stops scaling and what CDK gives you in return.
2. **Project: CDK Init** — Initialize a CDK Python project, understand its structure, and prepare it for the 10Q Inference deployment.

## Prerequisites

- Completed: Project SEC Lambda (SAM) — you need a working Lambda before bridging to CDK
- AWS CLI configured (see [Setup: AWS Account](../reference/setup-aws-account.md))
- Python 3.12
- Node.js 18+ (CDK CLI is a Node package)

## What comes after

Every module past this point — 10Q Inference, Partner Bot Web Page, MCP Server, RAG Pipeline — deploys with CDK. The patterns you learn here carry forward unchanged.

---
Last verified: 2026-06
