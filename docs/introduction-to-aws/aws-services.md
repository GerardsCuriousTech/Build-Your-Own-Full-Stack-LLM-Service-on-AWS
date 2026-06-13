# AWS Services

This section introduces the AWS services you will use throughout the course. For a full reference with open-source alternatives, see [AWS Services Reference](../reference/aws-services.md).

### Amazon S3

Amazon S3 (Simple Storage Service) stores and retrieves objects — files of any size, accessible via HTTP. You will use S3 to store SEC filing documents that your Lambda functions read during inference.

### AWS Lambda

AWS Lambda runs your code without provisioning servers. You upload a handler function, and Lambda executes it in response to events (HTTP requests, schedules, other AWS services). The SEC Lambda and 10Q Inference modules both deploy Lambda functions — first with SAM, then with CDK.

### Amazon API Gateway

API Gateway creates HTTP endpoints that route requests to your Lambda functions. The Partner Bot Web Page module uses API Gateway to expose the inference Lambda as a REST API the browser can call.

### Amazon Bedrock

Bedrock provides managed API access to large language models. You call Bedrock through the AWS SDK to run inference against the course's canonical model (see [Models](../reference/models.md) for details).

### Amazon EventBridge

EventBridge triggers actions on a schedule or in response to events. In this course, an EventBridge cron rule fires the daily SEC filing refresh Lambda.

### Amazon Cognito

Cognito manages user sign-up, sign-in, and access control. The Partner Bot Web Page module uses Cognito to authenticate users before they can call the inference API.
