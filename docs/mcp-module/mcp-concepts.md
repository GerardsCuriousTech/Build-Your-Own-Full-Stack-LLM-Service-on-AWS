# MCP Concepts

The Model Context Protocol (MCP) is an open standard that defines how LLM applications communicate with external data sources and tools. It decouples the client (the LLM application) from the server (the tool provider) through a well-defined JSON-RPC 2.0 interface.

## Core architecture

MCP follows a client-server model:

```
┌──────────────┐         JSON-RPC 2.0         ┌──────────────┐
│  MCP Client  │ ◄──────────────────────────► │  MCP Server  │
│ (LLM app)    │    stdio / HTTP+SSE          │ (tool host)  │
└──────────────┘                              └──────────────┘
```

The **client** is any LLM application that wants to use external tools — Claude Desktop, Cursor, or a custom agent. The **server** exposes capabilities the client can discover and invoke at runtime.

## Transport

MCP supports two transport mechanisms:

- **stdio** — the client spawns the server as a subprocess and communicates over standard input/output. Best for local development and desktop integrations.
- **HTTP with Server-Sent Events (SSE)** — the client connects to the server over HTTP. The server streams responses via SSE. Best for remote deployments and shared services.

Both transports carry identical JSON-RPC 2.0 messages. Your server code stays the same regardless of which transport a client uses.

## Capability types

An MCP server can expose three kinds of capabilities:

### Tools

Tools are functions the LLM can call. Each tool has a name, a description, and an input schema (JSON Schema). The client presents available tools to the LLM, which decides when and how to call them based on the user's request.

Example: a `query_sec_filing` tool that accepts a ticker, year, and period, then returns the filing analysis.

### Resources

Resources are data the client can read. Unlike tools, resources are not invoked — they are fetched. A resource has a URI, a MIME type, and content.

Example: a resource at `sec://filings/AAPL/2024/Q3` that returns the raw 10-Q text.

### Prompts

Prompts are reusable prompt templates the server offers to clients. They let the server suggest how to frame a request, while the client retains control over whether and how to use them.

Example: a `filing_analysis` prompt template that structures a question about quarterly earnings.

## How MCP relates to your Lambda

The Lambda functions you built earlier accept a structured JSON request and return an answer. Wrapping them in an MCP server means:

1. The tool's input schema maps directly to the [Lambda Contract](../reference/contract.md) request fields (`question`, `ticker`, `year`, `period`).
2. The tool's output is the Lambda response (`answer` and `meta`).
3. Any MCP client can discover and call your filing-analysis capability without knowing the underlying AWS infrastructure.

The Lambda stays unchanged. The MCP server is a thin adapter that translates between the MCP protocol and your existing function.

## Live demo: connect to the course MCP endpoint

Before building your own server, experience MCP from the client side. This course's GitBook site exposes an MCP endpoint that lets you query the course content itself.

### Endpoint

```
https://llm-aws.course.gspivey.com/~gitbook/mcp
```

### Connect with Claude Desktop

1. Open your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the course endpoint as an MCP server:

```json
{
  "mcpServers": {
    "llm-aws-course": {
      "url": "https://llm-aws.course.gspivey.com/~gitbook/mcp"
    }
  }
}
```

3. Restart Claude Desktop. The course tools appear in the tools menu (the hammer icon).

4. Ask Claude a question that requires course content:

   > "What is the Lambda request schema used in this course?"

   Claude calls the course MCP endpoint, retrieves the relevant content, and answers using the actual course material.

### What to observe

- Claude discovers the available tools automatically — you did not write any integration code.
- The tool call is visible in the response (expand the tool-use block to see the request and response).
- The server returns course content that Claude uses to ground its answer, reducing hallucination.

This is the same pattern you will implement in the project: expose a capability via MCP, and any compatible client can use it without custom wiring.

### Connect with other MCP clients

The endpoint works with any client that supports HTTP+SSE transport. If you use Cursor, VS Code with an MCP extension, or another compatible tool, add the URL as a remote MCP server following that client's configuration documentation.

## Protocol lifecycle

A typical MCP session follows this sequence:

1. **Initialize** — the client sends an `initialize` request; the server responds with its capabilities (which of tools/resources/prompts it supports).
2. **Discover** — the client calls `tools/list`, `resources/list`, or `prompts/list` to enumerate available capabilities.
3. **Invoke** — the client calls `tools/call` with the tool name and arguments; the server executes the tool and returns the result.
4. **Close** — either side terminates the session.

All messages are JSON-RPC 2.0. The client never calls a tool it has not first discovered — discovery is mandatory.

## Key design principles

- **Server declares, client decides.** The server advertises what it can do; the LLM decides whether and when to call a tool.
- **Schema-driven.** Every tool includes a JSON Schema for its inputs. Clients use this to validate arguments before sending them.
- **Stateless tools.** Each tool invocation is independent. The server does not maintain conversational state between calls (though it may cache data internally).
- **Transport-agnostic logic.** Your tool implementation does not depend on whether the client connected via stdio or HTTP.

## Next step

In [Project: MCP Server](project-mcp-server.md) you build an MCP server that exposes your SEC Lambda as a tool, deploy it, and test it with a real client.

---
Last verified: 2026-06
