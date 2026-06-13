# MCP Module

The Model Context Protocol (MCP) gives LLM-based applications a standardized way to discover and invoke external tools. Instead of hard-wiring each integration, an MCP server exposes capabilities — tools, resources, prompts — through a JSON-RPC interface that any compliant client can consume.

In this module you first experience MCP as a user (connecting a client to a live endpoint), then build your own MCP server that wraps the Lambda functions you deployed in the SEC Lambda and 10Q Inference modules. The result is a tool-equipped endpoint that any MCP-compatible agent can call to retrieve and analyze SEC filings on demand.

## Module structure

| Page | Focus |
|------|-------|
| [MCP Concepts](mcp-concepts.md) | Protocol fundamentals, architecture, and a live demo using the course site's MCP endpoint |
| [Project: MCP Server](project-mcp-server.md) | Build an MCP server that wraps your existing Lambda functions |

## Prerequisites

- Completed [Project: SEC Lambda (SAM)](../project-sec-lambda/README.md) — you have a deployed Lambda function conforming to the [Lambda Contract](../reference/contract.md)
- Completed [Project: 10Q Inference (CDK)](../project-10q-inference/README.md) — you have a working inference pipeline
- Python 3.12
- Familiarity with JSON-RPC (covered briefly in [Introduction to APIs](../introduction-to-apis/README.md))

## Why MCP matters

Lambda functions are powerful but isolated. A user must know the exact request schema, invoke the function directly, and parse the response. MCP removes that friction: an LLM client discovers available tools at runtime, understands their parameters from schema metadata, and invokes them without custom glue code.

Building an MCP server around your existing Lambda means any compatible client — Claude Desktop, Cursor, a custom agent — can query SEC filings through your infrastructure without modification.

---
Last verified: 2026-06
