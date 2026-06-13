# LangChain and RAG

The 10Q Inference module proved that injecting an entire filing into the prompt produces grounded answers. That approach works for short documents, but a full 10-K filing runs to hundreds of pages — far exceeding any model's context window. Retrieval Augmented Generation (RAG) solves this by retrieving only the relevant passages before prompting.

This module teaches you to build a RAG pipeline using LangChain on AWS. You will chunk SEC filings into manageable pieces, embed them into a vector store, and retrieve only the passages that are relevant to a given question. The retrieved context feeds into the same inference pattern you built earlier — grounding the model's answer in real data without exhausting its context window.

## Module structure

| Page | Focus |
|------|-------|
| [RAG Concepts](rag-concepts.md) | Chunking, embedding, vector stores, retrieval, and LangChain overview |
| [Project: RAG Pipeline](project-rag-pipeline.md) | Build a chunked-and-embedded retrieval pipeline on top of the 10Q Inference data flow |

## Prerequisites

- Completed [Project: 10Q Inference (CDK)](../project-10q-inference/README.md) — you have a working inference pipeline that retrieves filings and prompts the model with context
- Completed [MCP Module](../mcp-module/README.md) — familiarity with wrapping Lambda functions as external tools
- Bedrock model access enabled per [Setup: Bedrock Access](../reference/setup-bedrock-access.md)
- Python 3.12

## Why RAG

Stuffing the full document into the prompt is fragile:

- **Token limits.** Large filings exceed the model's context window, causing truncation or rejection.
- **Cost.** Every input token is billed. Sending 200 pages when you need two paragraphs wastes money.
- **Noise.** Irrelevant sections dilute the model's attention, degrading answer quality.

RAG addresses all three by selecting only the passages most likely to contain the answer. The model sees less text, produces more focused answers, and costs less per invocation.

## Key references

- [Models](../reference/models.md) — the canonical model identifier for all Bedrock calls
- [Lambda Contract](../reference/contract.md) — the request/response schema your pipeline must conform to

---
Last verified: 2026-06
