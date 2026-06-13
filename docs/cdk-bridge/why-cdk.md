# Why CDK?

## When SAM is enough

SAM CLI works best when your infrastructure is a small, self-contained unit: one or two Lambda functions, a single trigger, and a deployment bucket. The SEC Lambda project fits that shape. You write a `template.yaml`, run `sam build && sam deploy`, and the deployment finishes in under a minute.

SAM's strength is brevity. Its `AWS::Serverless::Function` resource hides the underlying CloudFormation machinery — the IAM execution role, the log group, the deployment package upload. For a single-function project, that hiding is a feature.

## When SAM stops scaling

Add a second function that reads from S3. Now you need an S3 bucket resource, a bucket policy, and an IAM policy statement granting the function read access. Add Bedrock invocation — another IAM permission block. Add an API Gateway in front — a RestApi resource, a deployment stage, a method, a Lambda permission, and CORS configuration.

Each new resource in `template.yaml` adds 10-30 lines of YAML. Worse, the relationships between resources are expressed as string references (`!Ref`, `!GetAtt`) with no validation until deploy time. A typo in a logical ID silently produces a broken stack.

SAM does not prevent you from building complex stacks. It just offers no help once you leave the single-function sweet spot.

## What CDK gives you

CDK is an infrastructure-as-code framework where you define AWS resources in a general-purpose programming language. This course uses Python 3.12.

### Type-checked resource definitions

CDK constructs are Python classes with typed parameters. Your editor catches invalid property names, wrong types, and missing required fields before you deploy. Compare:

**SAM (YAML, validated at deploy time):**

```yaml
Resources:
  InferenceFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.12
      Handler: handler.lambda_handler
      Policies:
        - Statement:
            - Effect: Allow
              Action: bedrock:InvokeModel
              Resource: "*"
```

**CDK (Python, validated at synth time):**

```python
inference_fn = _lambda.Function(
    self, "InferenceFunction",
    runtime=_lambda.Runtime.PYTHON_3_12,
    handler="handler.lambda_handler",
    code=_lambda.Code.from_asset("lambda"),
)
inference_fn.add_to_role_policy(
    iam.PolicyStatement(
        actions=["bedrock:InvokeModel"],
        resources=["*"],
    )
)
```

The CDK version is slightly longer, but if you misspell `runtime` or pass an integer where a string is expected, the error appears immediately — not after a two-minute CloudFormation rollback.

### Automatic cross-resource wiring

When one resource needs to reference another, CDK handles the glue. Granting a Lambda function read access to an S3 bucket:

```python
bucket.grant_read(inference_fn)
```

That single line generates the IAM policy statement, attaches it to the function's execution role, and sets up the dependency ordering so the bucket exists before the function deploys. In SAM/CloudFormation you would write all three pieces by hand.

### Constructs compose

A CDK "construct" is a reusable building block. You can wrap a pattern (Lambda + API Gateway + CORS configuration) into a single class and instantiate it across stacks. The 10Q Inference project uses this to define its multi-function architecture without repeating boilerplate.

### Synthesize before deploy

`cdk synth` generates the CloudFormation template locally. You can inspect exactly what will be created, diff it against the deployed stack (`cdk diff`), and catch misconfigurations before any AWS API call is made.

## When to stay with SAM

SAM remains the right choice when:

- Your project is a single Lambda function with a simple trigger.
- You need `sam local invoke` for rapid local iteration (CDK does not have a built-in local execution equivalent — you use `pytest` or invoke the function directly).
- Your team already has SAM templates in production and migration cost outweighs benefit.

This course uses SAM for the SEC Lambda project because it is genuinely simpler there. The transition to CDK happens here, at the point where complexity justifies the tooling shift.

## Summary

| Dimension | SAM | CDK |
|-----------|-----|-----|
| Language | YAML (CloudFormation shorthand) | Python 3.12 (or TypeScript, Java, etc.) |
| Validation timing | Deploy (CloudFormation) | Synth (local, before any API call) |
| Cross-resource wiring | Manual `!Ref` / `!GetAtt` | Automatic via `.grant_*()` and construct references |
| Reuse pattern | Copy-paste YAML sections | Compose constructs as Python classes |
| Best for | Single-function, simple-trigger stacks | Multi-resource stacks with cross-service permissions |
| Local testing | `sam local invoke` | `pytest` + direct Lambda invocation |

The next page walks you through initializing your first CDK project.

---
Last verified: 2026-06
