# Project Part 2: Inference with Context

Now that you have experimented with asking the LLM a question it likely does not know. Lets try asking it a question with context. This time download the content of the 10-Q document you used as the source for your questions. Your EDGAR API Lambda should be an easy way to get the text of the 10-Q.\
\
Ask the LLM your questions using the example prompt format. Tell it to use the information you provide, ask your question, then append the 10-Q content.

```
Using the information below. 

<Ask your question>

<insert all the text for the 10-Q>
```
