# Project SEC Lambda

In this project, we will create two AWS Lambda functions written in Python and leveraging AWS EventBridge. The project will utilize the SEC Module created in a previous project. Lambda 1: Download and Upload SEC Edgar JSON Files. The first Lambda function will download the SEC Edgar JSON files, which are used by the SEC Module to create dictionaries for finding company CIKs based on their name or their stock ticker. The Lambda function will then upload these JSON files to an S3 bucket. This Lambda function should be scheduled to run daily and update the same S3 locations. The S3 bucket should have version history enabled. Lambda 2: Process Requests for 10-K and 10-Q Documents. The second Lambda function will be triggered by JSON input. The JSON input should specify a request type of either "Annual" or "Quarter".

* If the request type is "Annual", the Lambda function should take a stock ticker or a company name and the year as input.
* If the request type is "Quarter", the Lambda function should take a stock ticker or a company name, the year, and the quarter as input. The Lambda function will then return the contents of either a 10-K or 10-Q document to the caller.

### Lambda 1: Download and Upload SEC Edgar JSON Files

This Lambda function will be responsible for downloading the SEC Edgar JSON files and uploading them to an S3 bucket. Here's a basic code sample:

```python
import boto3
import requests

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    url = "https://www.sec.gov/files/company_tickers.json"  # replace with the actual URL
    response = requests.get(url)
    s3.put_object(Bucket='your-bucket-name', Key='company_tickers.json', Body=response.content)
```

This code uses the requests library to download the file and the boto3 library to upload the file to S3. You'll need to replace 'your-bucket-name' with the name of your S3 bucket and the url with the actual URL of the SEC Edgar JSON files. Going forward your SEC Edgar module can use your S3 location instead of the SEC URL. This allows you to remove a run time dependency from the SEC's website for looking up files.

### Lambda 2: Process Requests for 10-K and 10-Q Documents

This Lambda function will process JSON input and return the contents of a 10-K or 10-Q document. Running a Lambda this way is a synchronous [Invoke](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html).&#x20;

Here's a basic code sample:

```python
import json

def lambda_handler(event, context):
    request_type = event['request_type']
    company = event['company']
    year = event['year']
    
    
    if request_type == 'Annual':
        # process annual request
        document = get_annual_document(company, year)
    elif request_type == 'Quarter':
        quarter = event['quarter']
        # process quarterly request
        document = get_quarterly_document(company, year, quarter)
    
    return {
        'statusCode': 200,
        'body': json.dumps(document)
    }
```

This code takes a JSON input with the request type, company, and year. If the request type is 'Quarter', it also expects a quarter. The sample code assumes the json format below but this is just a sample, your layout and field choices are your own. For example you may have chosen quarter to be an `int`1-4 in your SEC module.

```json
{
  "request_type": "Quarter",
  "company": "AAPL",
  "year": "2022",
  "quarter": "Q2"
}
```

It then calls the get\_annual\_document or get\_quarterly\_document function to get the document. These functions are not defined in this sample, you should already have them implemented in your SEC module so import your module and use it here. Remember to replace 'your-bucket-name' with the name of your S3 bucket and the url with the actual URL of the SEC Edgar JSON files. Scheduling Lambda 1To schedule the first Lambda function to run daily, you can use AWS EventBridge. Here's how you can do it:

* In the AWS Management Console, go to the EventBridge service.
* Click on 'Create rule'.
* Enter a name and description for the rule.
* For 'Define pattern', select 'Schedule'.
* Enter a schedule expression. For example, to run the function every day at 12:00 PM, you can use the expression cron(0 12 \* \* ? \*).
  * To test this you can set this more frequently for example every minute. You can then check the logs to see that your Lamda has ran.
* For 'Select targets', choose 'Lambda function' and select your function.
* Click on 'Create'.
