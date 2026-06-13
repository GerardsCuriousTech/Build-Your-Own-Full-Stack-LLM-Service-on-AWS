# Project: 10Q Inference (CDK)

LLMs answer from their training data. When a student asks about a company's most recent quarterly filing, the model's training cutoff means it likely has not seen that disclosure. The answer it produces sounds confident but is often wrong — invented figures, conflated dates, or outright hallucinations.

This project teaches you to close that gap. You build a CDK-deployed Lambda that retrieves a real SEC 10-Q filing, injects it as context into the prompt, and returns an answer grounded in the actual document. By the end of this module you will have seen the failure mode first-hand (Part 1), fixed it with retrieval-augmented context (Part 2), extracted clean text from a filing (Part 3), and wired it all together behind the course Lambda contract (Part 4).

## Module structure

| Part | Focus |
|------|-------|
| [Part 1: Inference Test](part-1-inference-test.md) | Invoke the model without context and observe its limitations |
| [Part 2: Inference with Context](part-2-inference-with-context.md) | Provide filing text as context and compare the results |
| Part 3: Text Extraction | Extract and prepare filing text for the prompt *(upcoming)* |
| Part 4: Question to Enhanced Prompt | End-to-end Lambda conforming to the contract *(upcoming)* |

## Prerequisites

- Completed the [CDK Bridge](../cdk-bridge/README.md) module (your CDK project is initialized)
- Working EDGAR API library from [Project: SEC EDGAR API Library](../project-sec-edgar-api-library/README.md)
- Bedrock model access enabled per [Setup: Bedrock Access](../reference/setup-bedrock-access.md)

## Deployment tool

Every part of this module uses **AWS CDK (Python 3.12)** for infrastructure deployment. If you have not yet initialized your CDK project, complete [Project: CDK Init](../cdk-bridge/project-cdk-init.md) first.

## Key references

- [Models](../reference/models.md) — the canonical model identifier for all Bedrock calls
- [Lambda Contract](../reference/contract.md) — the request/response schema your Lambda must conform to
