# Project: MCP Server

Build an MCP server that wraps your existing SEC filing Lambda function, making it available as a tool to any MCP-compatible client.

## Goal

Create a Python MCP server that exposes a `query_sec_filing` tool. The tool accepts the same parameters as your Lambda function (conforming to the [Lambda Contract](../reference/contract.md)), invokes the Lambda via the AWS SDK, and returns the result to the MCP client. When complete, you will be able to point Claude Desktop (or any MCP client) at your server and ask questions about SEC filings — with the Lambda doing the actual work behind the scenes.

## Contract

Your MCP server exposes one tool:

**Tool name:** `query_sec_filing`

**Input schema** (maps to the [Lambda Contract](../reference/contract.md) request):

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | string | The natural-language question to answer |
| `ticker` | string | Stock ticker symbol |
| `year` | integer | Filing year (four digits) |
| `period` | enum | Filing period: `Q1`, `Q2`, `Q3`, `Q4`, or `FY` |

**Output:** The tool returns the Lambda response `answer` field as text content. The `meta` object is included in a separate metadata block for client inspection.

The server must respond to the standard MCP lifecycle methods: `initialize`, `tools/list`, and `tools/call`.

## Required Reading

- [MCP Concepts](mcp-concepts.md) — protocol architecture, transport, and capability types
- [Lambda Contract](../reference/contract.md) — the request/response schema your tool wraps
- [Models](../reference/models.md) — the canonical model your Lambda invokes
- [MCP Specification](https://modelcontextprotocol.io/specification) — the official protocol reference

## Constraints

- Python 3.12.
- Use the `mcp` Python SDK (`pip install mcp`). Do not implement the JSON-RPC protocol from scratch.
- The server must support both **stdio** and **HTTP+SSE** transports. The `mcp` SDK handles this via its built-in server class — you configure it, not implement it.
- Invoke the Lambda function using `boto3`. Do not duplicate the Lambda's logic inside the MCP server — call the deployed function.
- The tool's input schema must match the [Lambda Contract](../reference/contract.md) request fields exactly. Do not add parameters the Lambda does not accept.
- Validate the `period` parameter against the allowed enum values (`Q1`, `Q2`, `Q3`, `Q4`, `FY`) before invoking the Lambda. Return a clear error through the MCP error mechanism if validation fails.
- The server must include a descriptive `tool.description` that tells the LLM when this tool is appropriate to call.
- Do not hardcode AWS credentials. The server relies on the standard credential chain (`AWS_PROFILE`, environment variables, or instance role).
- Do not hardcode the Lambda function name. Accept it via an environment variable (`SEC_LAMBDA_FUNCTION_NAME`).

## Acceptance Criteria

1. Running the server locally via stdio and calling `tools/list` returns a single tool named `query_sec_filing` with the correct input schema.
2. Calling `tools/call` with valid parameters invokes the Lambda and returns the answer text.
3. Calling `tools/call` with an invalid `period` value returns an MCP error without invoking the Lambda.
4. The server starts in HTTP+SSE mode when configured to do so, and a remote MCP client can connect and invoke the tool.
5. Adding the server to Claude Desktop's configuration (stdio mode) allows Claude to answer SEC filing questions by calling the tool.

## Hints

- The `mcp` SDK provides a `Server` class with decorator-based tool registration. A minimal server needs fewer than 50 lines of application code.
- Use `@server.tool()` to register your tool function. The decorator reads the function's type hints and docstring to generate the JSON Schema and description automatically.
- For the Lambda invocation, use `boto3.client("lambda").invoke(...)` with `InvocationType="RequestResponse"`. Parse the response payload as JSON.
- The `FunctionError` field in the Lambda invoke response indicates the function raised an exception. Check for it before parsing the payload — if present, return an MCP tool error rather than a malformed result.
- To run in stdio mode: `python server.py` (the SDK's `server.run()` defaults to stdio).
- To run in HTTP+SSE mode: `python server.py --transport sse --port 8080`. The `mcp` SDK's CLI runner handles this flag.
- Test your tool in isolation first with `mcp dev server.py` — this launches an interactive inspector that lets you call tools without configuring a full client.
- Structure your project directory alongside your CDK stack or as a standalone package — either works. The server is a thin wrapper, not a large application.

---
Last verified: 2026-06
