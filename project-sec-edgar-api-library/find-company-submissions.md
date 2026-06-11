# Find Company Submissions

Experiment with the API using curl until you are able to find 10K and 10Q submissions. Not all companies file their reports on the same days. In order to know which 10Q and 10K documents are available to us we need to get their submissions.\
\
Lets check out the submissions API

`curl -A "MLT GS gspivey@mlt.org" https://data.sec.gov/submissions/CIK320193.json`

We attempt to cURL using Apple's CIK however we do not get a desired response.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error><Code>NoSuchKey</Code><Message>The specified key does not exist.</Message><Key>submissions/CIK320193.json</Key><RequestId>S037Y7EEH567HC5K</RequestId><HostId>tBhGAzTTCykT5nxZbXE7jR9imKH2CaMQ99DE56CsfiQpq67UyLZquL8itb1qp0+psOO7TLWTf3Y=</HostId></Error>%
```

It turns out the API expects CIK numbers to be 10 digits. Take this in consideration for your code later as you likely return a shortened CIK.

&#x20;\
`curl -A "MLT GS gspivey@mlt.org" https://data.sec.gov/submissions/CIK0000320193.json`

Now we get a response. Lots of content is stripped out but the structure was left in place. Take note that recent is made up of multiple arrays. Based on the information returned you should be able to Identify the `Accession Number` and `Filing Date` for all `10-Q` and `10-K` submissions.

<pre class="language-json"><code class="lang-json">{
   "cik":"320193",
   "entityType":"operating",
   "sic":"3571",
   "sicDescription":"Electronic Computers",
   "insiderTransactionForOwnerExists":0,
   "insiderTransactionForIssuerExists":1,
   "name":"Apple Inc.",
   "tickers":[
      "AAPL"
   ],
   "exchanges":[
      "Nasdaq"
   ],
   "ein":"942404110",
   "description":"",
   "website":"",
   "investorWebsite":"",
   "category":"Large accelerated filer",
   "fiscalYearEnd":"0928",
   "stateOfIncorporation":"CA",
   "stateOfIncorporationDescription":"CA",
   "addresses":{
      "mailing":{
         "street1":"ONE APPLE PARK WAY",
         "street2":null,
         "city":"CUPERTINO",
         "stateOrCountry":"CA",
         "zipCode":"95014",
         "stateOrCountryDescription":"CA"
      },
      "business":{
         "street1":"ONE APPLE PARK WAY",
         "street2":null,
         "city":"CUPERTINO",
         "stateOrCountry":"CA",
         "zipCode":"95014",
         "stateOrCountryDescription":"CA"
      }
   },
   "phone":"(408) 996-1010",
   "flags":"",
   "formerNames":[
      {
         "name":"APPLE INC",
         "from":"2007-01-10T00:00:00.000Z",
         "to":"2019-08-05T00:00:00.000Z"
      },
      {
         "name":"APPLE COMPUTER INC",
         "from":"1994-01-26T00:00:00.000Z",
         "to":"2007-01-04T00:00:00.000Z"
      },
      {
<strong>         "name":"APPLE COMPUTER INC/ FA",
</strong>         "from":"1997-07-28T00:00:00.000Z",
         "to":"1997-07-28T00:00:00.000Z"
      }
   ],
   "filings":{
      "recent":{
         "accessionNumber":[],
         "filingDate":[],
         "acceptanceDateTime":[],
         "act":[],
         "form":[],
         "fileNumber":[],
         "filmNumber":[],
         "items":[],
         "size":[],
         "isXRBL":[],
         "isInlineXRBL":[],
         "primaryDocument":[],
         "primaryDocumentDescription":[]
      },
      "files":[
         {
            "name":"CIK0000320193-submissions-001.json",
            "filingCount":1069,
            "filingFrom":"1994-01-26",
            "filingTo":"2014-01-26"
         }
      ]
   }
}

</code></pre>

You can use JSON formatters and query tools to explore the response

* [JQ](https://jqlang.github.io/jq/)
* [JQ Playground](https://jqplay.org/)
* [JSON Formatter & Validator](https://jsonformatter.curiousconcept.com)
