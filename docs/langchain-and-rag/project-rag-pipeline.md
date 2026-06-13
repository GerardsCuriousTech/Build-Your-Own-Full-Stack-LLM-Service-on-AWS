# Project: RAG Pipeline

Build a retrieval-augmented generation pipeline that chunks and embeds SEC filing text, retrieves relevant passages at query time, and produces grounded answers — improving on the full-document approach from the 10Q Inference module.

## Goal

Create a CDK-deployed Lambda function that accepts the same request as your 10Q Inference Lambda (conforming to the [Lambda Contract](../reference/contract.md)) but uses a RAG approach internally. Instead of stuffing the entire filing into the prompt, your function chunks the filing text, embeds the chunks, retrieves the most relevant passages for the user's question, and prompts the model with only those passages as context. The external contract is identical; the internal strategy is smarter.

## Contract

Your RAG Lambda conforms to the [Lambda Contract](../reference/contract.md):

**Input:** `question`, `ticker`, `year`, `period`

**Output:** `answer`, `meta`

The `meta` object should additionally include:

| Field | Type | Description |
|-------|------|-------------|
| `chunks_retrieved` | integer | Number of chunks used as context |
| `chunk_strategy` | string | Chunking method used (e.g., `"recursive_character"`) |

These extra fields are informational and do not break contract conformance (the contract specifies `meta` as an object without restricting its keys).

## Required Reading

- [RAG Concepts](rag-concepts.md) — chunking, embedding, vector stores, and retrieval fundamentals
- [Lambda Contract](../reference/contract.md) — the request/response schema your Lambda must conform to
- [Models](../reference/models.md) — the canonical model identifier for Bedrock invocations
- [Project: 10Q Inference (CDK)](../project-10q-inference/README.md) — the existing pipeline your RAG version builds on
- [LangChain documentation: Retrieval](https://python.langchain.com/docs/concepts/retrieval/) — the official retrieval abstractions reference

## Constraints

- Python 3.12.
- Deploy with **AWS CDK** (Python). This Lambda lives in the same CDK app as your 10Q Inference stack, or a new stack within the same app.
- Use **LangChain** (`langchain`, `langchain-aws`, `langchain-community`) for the retrieval chain. Do not re-implement vector search from scratch.
- Use **FAISS** (`faiss-cpu`) as the vector store. It runs in-memory within the Lambda — no additional infrastructure required.
- Use **Amazon Titan Embeddings** via Bedrock for embedding (accessed through `langchain-aws`'s `BedrockEmbeddings` class). Do not use a self-hosted embedding model.
- Use the canonical model from [Models](../reference/models.md) for the generation step (accessed through `langchain-aws`'s `ChatBedrock` class).
- Chunk size: between 500 and 1500 characters, with 10-20% overlap. The exact values are your design choice.
- Retrieve the top-K chunks where K is between 3 and 8. Again, your choice — but document it.
- The Lambda must retrieve the filing from SEC EDGAR at invocation time (reuse your EDGAR library from earlier modules). Do not pre-index filings into a persistent store.
- Do not hardcode model identifiers. Use environment variables for the model ID and embedding model ID, configured in CDK.
- The Lambda function must include a custom `User-Agent` header on all SEC EDGAR requests.
- Do not include complete solution code. Build incrementally using the hints.

## Acceptance Criteria

1. The Lambda accepts a request conforming to the [Lambda Contract](../reference/contract.md) and returns a valid response.
2. The filing text is chunked (not passed whole) before being used as context.
3. Only the top-K most relevant chunks appear in the prompt sent to the model.
4. The `meta` field in the response includes `chunks_retrieved` and `chunk_strategy`.
5. Invoking the Lambda with the same question and filing produces a more focused answer than the full-document approach (qualitative — compare the two side by side).
6. The function deploys via `cdk deploy` without manual steps beyond what CDK handles.
7. Invalid `period` values return a validation error without invoking the model.

## Hints

- Start from your 10Q Inference Lambda. The filing retrieval and text extraction steps are identical. You are replacing the "build prompt" step with a retrieval chain.
- LangChain's `RecursiveCharacterTextSplitter` handles chunking with overlap in a single call. Instantiate it with your chosen `chunk_size` and `chunk_overlap`.
- `BedrockEmbeddings` from `langchain-aws` wraps the Titan Embeddings model. You only need to supply the model ID and a `boto3` client.
- `FAISS.from_documents(chunks, embeddings)` builds the vector index in one line. The index lives in Lambda memory — no persistence needed since the filing is fetched fresh on each invocation.
- Use the retriever interface: `retriever = vector_store.as_retriever(search_kwargs={"k": your_k})`. Then `retriever.invoke(question)` returns the relevant documents.
- Build the final prompt by joining the retrieved chunk texts with newlines, then wrapping them in a system message that instructs the model to answer using only the provided context.
- For the CDK stack, bundle your Lambda dependencies using a `requirements.txt` that includes `langchain`, `langchain-aws`, `langchain-community`, `faiss-cpu`, and `requests`. CDK's `PythonFunction` construct (from `aws-cdk.aws-lambda-python-alpha`) handles `pip install` during deployment.
- Test locally with `sam local invoke` or a simple Python script that calls your handler function directly with a test event. Compare the output against your original 10Q Inference Lambda to confirm the RAG version produces tighter, more relevant answers.
- FAISS index construction takes a few seconds for a typical 10-Q (~50-100 chunks). This is acceptable for a learning project. A production system would pre-index filings and persist the index.
