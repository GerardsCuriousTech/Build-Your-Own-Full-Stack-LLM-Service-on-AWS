# Project SEC EDGAR API Library

For this project we are going to expand our CIK Lookup Module to add additional methods to make it a client we can use to find and retrieve the 10K and 10Q documents.\
\
To get more context on this explore the SEC Website using the EDGAR search tool.&#x20;

* [SEC EDGAR Full Text Search](https://www.sec.gov/edgar/search/)
  * [Full Text Search FAQ](https://www.sec.gov/edgar/search/efts-faq.html)
* [SEC EDGAR CIK Search](https://www.sec.gov/search-filings/cik-lookup)
* [How do I use EDGAR?](https://www.sec.gov/search-filings/edgar-search-assistance/how-do-i-use-edgar)
* [EDGAR Application Programming Interfaces (APIs)](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

1. Review the links above
   1. Read through the API and test the API by making calls with cURL and inspecting the results.
      1. If you need a tool to help parse the JSON while testing on the command line check out [JQ](https://jqlang.github.io/jq/)
2. Find a Company 10Q
   1. Search For a Company&#x20;
   2. Find the latest 10Q they submitted
   3. Open the 10Q
   4. Skim through it to better understand the type of information included

We are going to fully automate the `Find a Company 10Q` steps.
