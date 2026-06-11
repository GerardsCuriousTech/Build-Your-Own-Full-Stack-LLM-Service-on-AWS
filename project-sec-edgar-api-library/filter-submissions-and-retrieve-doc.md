# Filter Submissions and Retrieve Doc

Under `filings -> recent`

There are 3 key arrays along the CIK number that is key data needed to find a document

* accessionNumber
* primaryDocument
  * This is the name of the document we are going to use
* primaryDocumentDescription
  * These will describe what the document is. In our case we care about the `10-K` and `10-Q` documents.
  * You could think about making your program configurable to handle any document type

Remember arrays are ordered. So you can use the index number to help you find the other values you care about.

The URL for the document will follow this format

`https://www.sec.gov/Archives/edgar/data/{CIK}/{accessionNumber}/{primaryDocument}`

#### Example:

`curl -A "<your orginaztion> <your name> <your email>" -v` [`https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm`](https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm)
