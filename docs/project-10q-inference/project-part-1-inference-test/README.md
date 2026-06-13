# Project Part 1: Inference Test

Invoke Bedrock using the [canonical course model](../../reference/models.md).

* [Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)
* [InvokeModel API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
* [Invoke Model Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html#inference-example-invoke)

Use the Python Boto3 API and test asking the model a range of questions.

For example:

* Can you explain a solar eclipse?
* Can you write a Python module and give sample code?
* Can you explain what the SEC EDGAR library is for?

After you get a feel for asking questions and parsing responses, find a company's most recent 10-Q filing on SEC EDGAR. Pick any publicly traded company and locate its latest quarterly filing — the one filed within the last few months. Use the EDGAR API skills from the previous project to retrieve it.

Within that document, find a fact that the LLM is unlikely to know the answer to. Model training data has a cutoff — facts from very recent filings are beyond that cutoff. Look in sections like "Management's Discussion and Analysis of Financial Condition and Results of Operations" for specific dollar figures, investment amounts, or operational metrics disclosed in the filing.

Compose 1-3 questions of your own, ask the LLM, and take note of how it responds. Save both the questions and responses — you will use them in Part 2.
