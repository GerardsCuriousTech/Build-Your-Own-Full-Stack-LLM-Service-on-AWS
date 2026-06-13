# Setup: Bedrock Access

Amazon Bedrock requires you to explicitly enable access to each model before you can invoke it. This page covers enabling model access for the course's canonical model. For the model identifier and invocation details, see [Models](models.md).

## Enable model access

1. Open the **Amazon Bedrock** console in your chosen region (e.g., `us-east-1`).
2. In the left sidebar, choose **Model access**.
3. Choose **Modify model access**.
4. Locate **Anthropic** in the provider list and check the box for the canonical model listed on the [Models](models.md) page.
5. Choose **Next**, review the selection, and choose **Submit**.

Access typically activates within a few minutes. The status column changes from "Available to request" to "Access granted."

## Verify access

Use the AWS CLI to confirm the model responds. Replace `MODEL_ID` below with the canonical model ID from [Models](models.md):

```bash
aws bedrock-runtime invoke-model \
  --model-id "MODEL_ID" \
  --content-type "application/json" \
  --accept "application/json" \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":64,"messages":[{"role":"user","content":"Say hello."}]}' \
  /dev/stdout
```

A successful response returns a JSON body with the model's reply. If you receive `AccessDeniedException`, model access has not finished activating or you selected the wrong model in the console.

## Cross-Region Inference

The course uses a Cross-Region Inference Profile, which routes requests across multiple regions for availability. The profile is preconfigured by AWS once you enable the model — no additional setup is required on your part. See [Models](models.md) for the profile ARN pattern and usage instructions.

## Region availability

Not all Bedrock models are available in every region. At the time of writing, the canonical course model is available in `us-east-1`, `us-west-2`, and `eu-west-1` among others. If you configured a different default region in [Setup: AWS Account](setup-aws-account.md), confirm model availability in the Bedrock console before proceeding.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `AccessDeniedException` | Model access not granted | Check the Model access page; request access if status is not "Access granted" |
| `ValidationException: The provided model identifier is invalid` | Incorrect model ID or model retired | Confirm the model ID matches the one on [Models](models.md) |
| `ThrottlingException` | Too many requests in a short window | The Cross-Region Inference Profile mitigates this; retry after a brief pause |

---

Last verified: 2026-06
