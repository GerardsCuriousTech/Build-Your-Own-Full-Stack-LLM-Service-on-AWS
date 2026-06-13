# Models

This page is the single source of truth for LLM model identifiers used throughout the course. Every project page links here rather than embedding a model ID directly.

## Canonical Model

| Field | Value |
|-------|-------|
| Model | Claude Sonnet 4.5 |
| Provider | Anthropic via Amazon Bedrock |
| Deployment | Cross-Region Inference Profile |
| Model ID | `us.anthropic.claude-sonnet-4-5-20250514-v1:0` |
| Profile ARN pattern | `arn:aws:bedrock:{region}:{account-id}:inference-profile/us.anthropic.claude-sonnet-4-5-20250514-v1:0` |

## Cross-Region Inference Profile

A Cross-Region Inference Profile routes Bedrock requests across multiple AWS regions transparently. This improves availability and reduces throttling during peak usage without requiring application-level retry logic.

When you invoke the model, you call the inference profile ARN rather than the base model ARN. Bedrock handles region selection behind the scenes.

### Setting up the profile

1. Open the Amazon Bedrock console in your primary region (e.g., `us-east-1`).
2. Navigate to **Cross-region inference** in the left sidebar.
3. Locate the Claude Sonnet 4.5 profile and note its ARN.

Use this ARN in your Lambda function's `model_id` parameter and in any CDK or SAM configuration that references the model.

### Example: invoking the model in Python 3.12

```python
import boto3
import json

bedrock = boto3.client("bedrock-runtime")

response = bedrock.invoke_model(
    modelId="us.anthropic.claude-sonnet-4-5-20250514-v1:0",
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Summarize the quarterly results."}
        ]
    })
)
```

## Updating the canonical model

When the course adopts a newer model, update only this page. All other pages link here, so a single edit propagates the change across the course.

1. Update the table above with the new model ID, ARN pattern, and name.
2. Update the Python example to reflect the new `modelId` value.
3. Run the grep-gate to confirm no other page embeds the old or new ID directly.

---
Last verified: 2026-06
