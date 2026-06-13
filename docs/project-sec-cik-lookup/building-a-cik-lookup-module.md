# Building a CIK Lookup Module

For our application we need a way to look up a company CIK without using the web form.

The SEC has a page called [accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data). On that page CIK data is in 3 formats.

* [company\_tickers.json](https://www.sec.gov/files/company_tickers.json): data file for ticker, CIK, EDGAR conformed company name associations.
* [company\_tickers\_exchange.json](https://www.sec.gov/files/company_tickers_exchange.json): data file for EDGAR conformed company name, CIK, ticker, exchange associations
* [company\_tickers\_mf.json](https://www.sec.gov/data/company_tickers_mf.json): fund CIK, series, class, ticker&#x20;

## NOTE: Follow the SEC EDGAR Fair Access Policy&#x20;

Fair access is described on the [accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) page.

> ### Fair access
>
> * **Current max request rate: 10 requests/second.**
>
> To ensure everyone has equitable access to SEC EDGAR content, please use efficient scripting. Download only what you need and please moderate requests to minimize server load.
>
> SEC reserves the right to limit request rates to preserve fair access for all users. See our [Internet Security Policy](https://www.sec.gov/privacy.htm#security) for our current rate request limit.
>
> The SEC does not allow botnets or automated tools to crawl the site. Any request that has been identified as part of a botnet or an automated tool outside of the acceptable policy will be managed to ensure fair access for all users.
>
> Please declare your user agent in request headers:
>
> Sample Declared Bot Request Headers:

| User-Agent:      | Sample Company Name AdminContact@\<sample company domain>.com |
| ---------------- | ------------------------------------------------------------- |
| Accept-Encoding: | gzip, deflate                                                 |
| Host:            | [www.sec.gov](http://www.sec.gov)                             |

### Our Python Module

Our Python Module will be a class that initializes and stores the EDGAR company data into a hash map (dictionary). Once we store the data we can use it to go from company name or ticker to its CIK number

* Write a class that initializes two dictionaries.&#x20;
  * One where the company name is the key
  * One where the stock ticker is the key.&#x20;
* When the method initializes it should retrieve a fresh copy of the data from the URLs provided by SEC EDGAR
  * This will allow your function to always have the latest and correct data.
* The class should have two methods. (Method names should follow [PEP8 Style Guide](https://peps.python.org/pep-0008/#method-names-and-instance-variables))
  * Ex: `name_to_cik`
  * Ex: `ticker_to_cik`
  * The return values should be a tuple that _**at least**_ includes CIK, Name, Ticker but could include more information.

{% embed url="https://www.youtube.com/watch?v=JBexmhrqWd0" %}
