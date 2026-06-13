# RAG Concepts

Retrieval Augmented Generation (RAG) is a pattern that combines information retrieval with LLM prompting. Instead of relying on the model's training data alone, a RAG system fetches relevant documents at query time and injects them as context — the same principle you used in the 10Q Inference module, now scaled to handle arbitrarily large document collections.

## The RAG pipeline at a glance

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌───────────┐
│  Ingest  │ ──► │  Chunk   │ ──► │   Embed &    │ ──► │  Vector   │
│  (docs)  │     │  (split) │     │   Store      │     │  Store    │
└──────────┘     └──────────┘     └──────────────┘     └─────┬─────┘
                                                              │
                                                         query time
                                                              │
┌──────────┐     ┌──────────────┐     ┌──────────┐          │
│  Answer  │ ◄── │  Prompt +    │ ◄── │ Retrieve │ ◄────────┘
│  (LLM)   │     │  Context     │     │ (search) │
└──────────┘     └──────────────┘     └──────────┘
```

Two phases:

1. **Ingestion** — documents are split into chunks, each chunk is converted to a numerical vector (embedding), and those vectors are stored in a searchable index.
2. **Query** — the user's question is embedded using the same model, the vector store returns the most similar chunks, and those chunks are injected as context into the LLM prompt.

## Chunking

A 10-Q filing is a single large document. Feeding it whole to an embedding model is impractical (embedding models have their own token limits) and unhelpful (a single vector for a 100-page document captures no fine-grained meaning). Chunking splits the document into smaller, semantically coherent pieces.

### Chunking strategies

| Strategy | How it works | When to use |
|----------|-------------|-------------|
| Fixed-size | Split every N characters or tokens | Simple baseline; works when structure is uniform |
| Recursive character | Split on paragraph breaks, then sentences, then characters — progressively smaller separators until chunks fit | Good default for prose documents |
| Section-based | Split on document headings or HTML tags | Works when the document has reliable structural markup |
| Semantic | Use an embedding model to detect topic boundaries | Expensive but produces the most coherent chunks |

For SEC filings, recursive character splitting with overlap works well. Filings are structured prose with inconsistent heading levels, so heading-based splitting is unreliable.

### Overlap

Adjacent chunks share a small overlap (typically 10-20% of chunk size) so that information spanning a chunk boundary is not lost. If a key sentence sits at the boundary between chunk 47 and chunk 48, overlap ensures at least one of them contains the full sentence.

### Chunk size tradeoffs

- **Too small** — each chunk lacks context, retrieval returns fragments that are hard to interpret.
- **Too large** — each chunk mixes topics, retrieval returns noise alongside signal. Embedding quality degrades as the text diverges from a single idea.
- **Practical range** — 500 to 1500 characters (roughly 100 to 400 tokens) per chunk for most RAG applications.

## Embedding

An embedding model converts text into a fixed-length numerical vector that captures semantic meaning. Texts with similar meaning produce vectors that are close together in the embedding space.

### How embeddings work in RAG

1. Each chunk is passed through the embedding model to produce a vector (e.g., 1024 dimensions).
2. The vectors are stored in a vector database alongside the original chunk text.
3. At query time, the user's question is embedded with the same model.
4. The vector store finds the stored chunks whose vectors are closest to the query vector.

### Amazon Bedrock embeddings

Amazon Titan Embeddings is available through Bedrock and produces vectors suitable for RAG. You call it the same way you call a text model — via the Bedrock Runtime API — but the response is a vector rather than generated text.

*(advanced -- skim)* Other embedding models (Cohere Embed, open-source models via SageMaker) work the same way conceptually. The choice of embedding model affects vector dimensionality and retrieval quality, but the pipeline architecture stays identical.

## Vector stores

A vector store is a database optimized for similarity search over high-dimensional vectors. Unlike a traditional database that matches exact values, a vector store finds the N vectors closest to a query vector using distance metrics (cosine similarity, Euclidean distance, or dot product).

### Options on AWS

| Store | Type | When to use |
|-------|------|-------------|
| FAISS (in-memory) | Library | Local development, small corpora, Lambda functions with predictable data size |
| OpenSearch Serverless (vector engine) | Managed service | Production workloads needing scalable, persistent vector search |
| PostgreSQL + pgvector | Managed (RDS/Aurora) | Teams already running PostgreSQL who want to add vector search without a new service |

For this course project, FAISS is sufficient. The filing corpus is small enough to fit in Lambda memory, and FAISS requires no additional infrastructure. A production system handling thousands of filings would move to OpenSearch Serverless.

### Indexing

When you ingest a document:

1. Chunk the text.
2. Embed each chunk.
3. Insert each (vector, chunk_text, metadata) tuple into the vector store.

Metadata typically includes the source file name, chunk index, and any structural tags (section heading, page number) that help the user trace an answer back to its origin.

### Retrieval

When a user asks a question:

1. Embed the question using the same embedding model.
2. Query the vector store for the top-K nearest vectors (K is typically 3 to 10).
3. Return the associated chunk texts as context for the LLM prompt.

The retrieved chunks are the bridge between the user's question and the answer. The LLM sees only these chunks plus the question — not the full document.

## Retrieval quality

Retrieval quality directly determines answer quality. If the retriever returns irrelevant chunks, the LLM produces an irrelevant answer no matter how capable it is.

Factors that affect retrieval quality:

- **Chunk granularity** — chunks too large dilute the embedding; chunks too small lose context.
- **Embedding model quality** — better models produce embeddings where semantic similarity correlates with topical relevance.
- **Query formulation** — the raw user question may not embed well. Techniques like query expansion or hypothetical document embedding (HyDE) can improve retrieval.
- **Top-K selection** — too few results may miss the answer; too many results add noise to the prompt.

## LangChain overview

LangChain is a Python framework that provides composable abstractions for building LLM-powered applications. It is not required to build a RAG pipeline — you could wire up chunking, embedding, vector search, and prompting yourself — but it reduces boilerplate by providing standard interfaces for each step.

### Core abstractions relevant to RAG

| Abstraction | Role in the pipeline |
|-------------|---------------------|
| `Document` | A chunk of text plus metadata |
| `TextSplitter` | Splits raw text into `Document` objects using a chunking strategy |
| `Embeddings` | Interface to an embedding model (wraps Bedrock, OpenAI, or local models) |
| `VectorStore` | Interface to a vector database (wraps FAISS, OpenSearch, pgvector, etc.) |
| `Retriever` | Queries the vector store and returns relevant documents |
| `Chain` | Connects retriever output to an LLM prompt and returns the final answer |

### Why LangChain for this project

- **Bedrock integration** — `langchain-aws` provides `ChatBedrock` and `BedrockEmbeddings` classes that handle the Bedrock API details.
- **Swappable components** — switch from FAISS to OpenSearch by changing one class instantiation. The rest of the pipeline stays unchanged.
- **Standardized retrieval interface** — the `Retriever` abstraction means your chain code does not depend on the vector store implementation.

### LangChain installation

LangChain uses a modular package structure. For a Bedrock-based RAG pipeline, install:

```bash
pip install langchain langchain-aws langchain-community faiss-cpu
```

- `langchain` — core framework (chains, prompts, document loaders)
- `langchain-aws` — Bedrock LLM and embedding integrations
- `langchain-community` — community-maintained integrations including FAISS vector store
- `faiss-cpu` — the FAISS library itself (CPU-only build, sufficient for Lambda)

## Connecting RAG to the 10Q Inference pipeline

Your 10Q Inference module already:

1. Retrieves a 10-Q filing from SEC EDGAR.
2. Extracts text from the filing.
3. Builds an enhanced prompt with the filing text as context.
4. Invokes the model and returns an answer conforming to the [Lambda Contract](../reference/contract.md).

The RAG enhancement replaces step 3's "stuff the whole document" approach with a targeted retrieval:

1. Retrieve the filing (unchanged).
2. Extract text (unchanged).
3. **Chunk** the extracted text into passages.
4. **Embed** each chunk and store in a vector index.
5. **Retrieve** the top-K chunks most relevant to the user's question.
6. Build the prompt using only the retrieved chunks as context.
7. Invoke the model and return the answer (unchanged contract).

The external interface — the [Lambda Contract](../reference/contract.md) request and response — does not change. The improvement is internal: better answers from less context, at lower cost.

## Next step

In [Project: RAG Pipeline](project-rag-pipeline.md) you implement this pipeline end-to-end using LangChain and FAISS, deployed via CDK.
