# Lambda Project Setup

## Goal

Initialize a SAM project containing two Lambda functions (EDGAR file refresh and document retrieval), configure `template.yaml` for Python 3.12, and deploy the stack so that both functions run in AWS with their dependencies correctly packaged.

## Contract

Your Lambda 2 (document retrieval) function accepts requests and returns responses conforming to the [Lambda Contract](../reference/contract.md).

The model used for inference is defined in [Models](../reference/models.md). Link there rather than hardcoding an identifier.

## Required Reading

- [AWS SAM CLI Developer Guide — sam init](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-init.html)
- [AWS SAM template anatomy](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy.html)
- [AWS::Serverless::Function](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html)
- [Lambda runtimes — Python 3.12](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)
- [SEC EDGAR Fair Access policy](https://www.sec.gov/os/webmaster-faq#developers)
- [Lambda Contract](../reference/contract.md)
- [Models](../reference/models.md)

## Constraints

1. **SAM CLI only.** Use `sam init`, `sam build`, and `sam deploy` for all infrastructure. No console-click deployments; no raw CloudFormation uploads.

2. **Python 3.12 runtime.** Both functions must declare `Runtime: python3.12` in `template.yaml`.

3. **Package `requests` explicitly.** The `requests` library is not included in the Lambda Python runtime. List it in a `requirements.txt` at each function's root so that `sam build` bundles it into the deployment artifact.

4. **Custom User-Agent on all SEC EDGAR requests.** The SEC Fair Access policy requires a declared identity. Every HTTP call to `sec.gov` must include a `User-Agent` header with your name and contact email. Recall the pattern from the CIK Lookup project.

5. **No comments inside JSON blocks.** JSON does not support comments. Configuration examples in your code (event payloads, `template.yaml` outputs) must contain only valid JSON.

6. **Lambda I/O matches the contract.** Lambda 2 must accept exactly the fields defined in the [request schema](../reference/contract.md) and return the [response schema](../reference/contract.md). Do not invent additional fields or rename existing ones.

7. **S3 bucket versioning enabled.** Lambda 1 uploads to a versioned S3 bucket. Configure this in `template.yaml`, not after the fact in the console.

8. **EventBridge schedule for Lambda 1.** Use a SAM `Schedule` event to trigger the daily refresh. Note: EventBridge cron expressions evaluate in UTC.

## Acceptance Criteria

- `sam build` completes without errors.
- `sam deploy --guided` creates the CloudFormation stack with both functions, an S3 bucket (versioning enabled), and an EventBridge rule.
- Lambda 1 executes on schedule, downloads `https://www.sec.gov/files/company_tickers.json`, and uploads it to S3. CloudWatch logs show a successful invocation.
- Lambda 2, when invoked with a valid [contract request](../reference/contract.md), returns a well-formed response. When invoked with an invalid `period` value, it returns a validation error.
- All SEC EDGAR HTTP requests include a `User-Agent` header matching your declared identity.
- `sam local invoke` with a sample event file produces a response locally before deploying.

## Hints

<details>
<summary>Project initialization</summary>

`sam init` offers templates. Choose the "Hello World" Python template, then replace the generated function code with your own. The directory structure SAM creates is significant: each function lives in its own subdirectory with its own `requirements.txt`.
</details>

<details>
<summary>template.yaml structure</summary>

You need two `AWS::Serverless::Function` resources. Each specifies `Runtime`, `Handler`, `CodeUri` (pointing to the function subdirectory), and its event source. Lambda 1 gets a `Schedule` event; Lambda 2 gets no event source in the template (it is invoked programmatically).

The S3 bucket is a separate `AWS::S3::Bucket` resource with `VersioningConfiguration` set.
</details>

<details>
<summary>Packaging requests</summary>

Create a `requirements.txt` in each function's `CodeUri` directory containing `requests`. When you run `sam build`, SAM installs those dependencies into the build artifact automatically. Verify by checking the `.aws-sam/build/` directory.
</details>

<details>
<summary>User-Agent header</summary>

Pass a `headers` dict to every `requests.get()` call targeting `sec.gov`:

```python
headers = {"User-Agent": "YourName your@email.edu"}
```

This is the same pattern you used in the CIK module. Extract it to a constant or environment variable so it is easy to update.
</details>

<details>
<summary>Local testing</summary>

Create a JSON file (e.g., `events/retrieve.json`) containing a valid contract request. Then:

```bash
sam local invoke DocumentRetrievalFunction --event events/retrieve.json
```

This runs the function in a Docker container matching the Lambda runtime. If you see `No module named 'requests'`, run `sam build` first.
</details>

<details>
<summary>EventBridge UTC gotcha</summary>

SAM `Schedule` expressions use UTC. If you set `cron(0 12 * * ? *)` expecting noon local time, it fires at noon UTC. Adjust for your timezone during testing, or set a frequent schedule (every 5 minutes) to verify quickly, then switch to daily.
</details>
