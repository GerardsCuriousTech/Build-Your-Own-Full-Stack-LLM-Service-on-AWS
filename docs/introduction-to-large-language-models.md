# Introduction to Large Language Models

The roadmap.sh site does a great job at describing the Large Language Models and Prompt Engineering.  We will attempt to summarize the concept however [following the Prompt Engineering](https://roadmap.sh/prompt-engineering) roadmap path is highly recommended.&#x20;

### What are LLMs?

> LLMs, or Large Language Models, are advanced Artificial Intelligence models specifically designed for understanding and generating human language. These models are typically based on deep learning architectures, such as Transformers, and are trained on massive amounts of text data from various sources to acquire a deep understanding of the nuances and complexities of language.
>
> LLMs have the ability to achieve state-of-the-art performance in multiple Natural Language Processing (NLP) tasks, such as machine translation, sentiment analysis, summarization, and more. They can also generate coherent and contextually relevant text based on given input, making them highly useful for applications like chatbots, question-answering systems, and content generation.
>
> As an example, OpenAI's GPT-3 is a prominent LLM that has gained significant attention due to its capability to generate high-quality text and perform a variety of language tasks with minimal fine-tuning.

Quote from [Roadmap.sh What are LLMs?](https://github.com/kamranahmedse/developer-roadmap/blob/master/src/data/roadmaps/prompt-engineering/content/100-basic-llm/100-what-are-llms.md)

### Why Run LLMs in the cloud?

Large Language Models are computationally intensive typically requiring GPU offload for additional computation and a large amount of system memory to host them. [Efficient Memory Management for Large Language Model Service with PagedAttention](https://dl.acm.org/doi/pdf/10.1145/3600006.3613165) dives deep on the Key Value (KV) space and its effect on required VRAM and how to more effectively minimize the VRAM usage reducing memory requirements.\
\
The main takeaway is while there are some people experimenting running LLMs themselves the infrastructure required to make use of them at scale lends itself well to cloud computing.\
\
For this course we are using AWS's Bedrock Service which hosts a set of LLM models. On that platform we will use [Anthropic's Claude model](https://www.anthropic.com/claude). Using Claude through Bedrock makes it easier to integrate with other AWS services.&#x20;

### LLM Prompt Context

#### What is a Prompt?

A prompt is the input given to an LLM to generate a response. It can be a question, a statement, or any text that guides the model on what kind of output is expected. For example, if you ask an LLM, "What is the capital of France?", the prompt is "What is the capital of France?".&#x20;

#### What is Prompt Context?

Prompt context refers to the additional information or background provided to the LLM to help it generate a more accurate and relevant response. This context can include:

* **Previous conversation history:** If you're having a chat with an LLM, the context includes all the previous messages exchanged.
* **Specific instructions:** Guidelines on how the LLM should respond, such as the tone, style, or format.
* **Relevant details:** Any additional information that can help the LLM understand the prompt better.&#x20;

#### Why is Prompt Context Important?

Prompt context is crucial because it helps the LLM generate responses that are more accurate, coherent, and relevant to the user's needs. Without context, the model might produce responses that are off-topic or lack depth.

---
Last verified: 2026-06
