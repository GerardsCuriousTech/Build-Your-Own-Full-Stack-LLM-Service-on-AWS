# AWS Services Reference

This page covers the AWS services used in this course. Each service is introduced briefly here; you will work with them hands-on in the project modules that follow.

## Amazon S3

Amazon S3 (Simple Storage Service) is an object storage service for storing and retrieving any amount of data. In this course, S3 holds SEC filing documents that your Lambda functions read at inference time.

Open-source alternative: [MinIO](https://min.io/) provides an S3-compatible object storage API you can run locally for development.

## AWS Lambda

AWS Lambda is a serverless compute service that runs your code in response to events without requiring you to provision servers. You write a handler function, deploy it, and Lambda executes it when triggered. This course builds multiple Lambda functions — starting with SAM CLI deployments and transitioning to CDK.

Open-source alternative: [Apache OpenWhisk](https://openwhisk.apache.org/) provides a serverless platform you can self-host.

## Amazon API Gateway

Amazon API Gateway creates, deploys, and manages HTTP APIs that front your Lambda functions. In the Partner Bot Web Page module, API Gateway exposes your inference Lambda as a REST endpoint the front-end application calls.

Open-source alternative: [Kong](https://konghq.com/) offers API gateway and management features with a self-hosted option.

## Amazon Bedrock

Amazon Bedrock is a managed service providing API access to large language models from multiple providers. This course uses Bedrock to invoke the canonical model (see [Models](models.md)) for inference. Bedrock handles hosting and scaling; you interact with it through the AWS SDK.

Open-source alternative: [Hugging Face Inference Endpoints](https://huggingface.co/inference-endpoints) lets you deploy open-weight models behind an API, though you manage capacity yourself.

## Amazon EventBridge

Amazon EventBridge is a serverless event bus that routes events between AWS services on a schedule or in response to state changes. In this course, an EventBridge rule triggers the daily SEC filing refresh Lambda on a cron schedule.

Open-source alternative: [Temporal](https://temporal.io/) provides durable workflow orchestration including scheduled triggers.

## Amazon Cognito

Amazon Cognito handles user authentication and authorization. In the Partner Bot Web Page module, Cognito protects the API Gateway endpoint so only authenticated users can invoke the inference Lambda.

Open-source alternative: [Keycloak](https://www.keycloak.org/) is a self-hosted identity and access management server supporting OAuth 2.0 and OpenID Connect.

---

Last verified: 2026-06
