# Project Part 1: Inference Test

Invoke the Bedrock using Claude 3 Sonnet.

* [Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)
* [InvokeModel API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
* [Invoke Model Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html#inference-example-invoke)
* [Python Invoke Model Example](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html#inference-example-invoke)

Use the Python Boto3 API and test asking the model a range of questions.

For example

* Can you explain a solar eclipse?
* Can you write explain how to write a python module and give sample code?
* Can you explain what the SEC Edgar library is for?

After you get a feel for asking questions and parsing responses. Find a companies latest 10-Q filing. The current date as of writing this is August 2024.  For example AMZN filed their latest [10-Q ](https://www.sec.gov/ix?doc=/Archives/edgar/data/1018724/000101872424000130/amzn-20240630.htm)as of writing this on April 2 2024. AMZN is used as an example however pick a different company so you can explore the power of LLM context for yourself.\
\
Within that document find a fact that the LLM is unlikely to know the answer to. For example in the "Management's Discussion and Analysis if Financial Condition and Results of Operations"&#x20;

* How much did Amazon invest in Anthropic in Q3 2023 and Q1 2024?

This is an example question. Find 1-3 questions of your own the ask the LLM and take note of how it responds. Save the questions and responses.&#x20;
