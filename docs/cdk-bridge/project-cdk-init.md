# Project: CDK Init

## Goal

Initialize a CDK Python project that will serve as the deployment foundation for the 10Q Inference module. By the end of this project you will have a working CDK app that synthesizes a valid CloudFormation template, even though it deploys no resources yet. The 10Q Inference project builds on top of this skeleton.

## Contract

This project produces infrastructure code, not a Lambda function. There is no request/response contract here. The Lambda functions you deploy in later modules conform to the [Lambda Contract](../reference/contract.md) — the CDK stack is the mechanism that deploys them.

The model your Lambda will invoke is defined in [Models](../reference/models.md). You will reference that page when adding Bedrock permissions in the next module.

## Required Reading

- [Why CDK?](why-cdk.md) — the preceding page in this module
- [AWS CDK Getting Started (Python)](https://docs.aws.amazon.com/cdk/v2/guide/getting-started.html) — official install and bootstrapping guide
- [AWS CDK API Reference — aws-cdk-lib](https://docs.aws.amazon.com/cdk/api/v2/python/) — construct library documentation

## Constraints

- Use Python 3.12 as both the CDK app language and the target Lambda runtime in later stacks.
- Install the CDK CLI globally via npm (`npm install -g aws-cdk`). Do not use a Python-packaged CDK CLI wrapper.
- Use CDK v2 (`aws-cdk-lib`). Do not use CDK v1 individual packages.
- The project must synthesize cleanly (`cdk synth` exits zero and produces a valid template) before you consider this project complete.
- Do not deploy to AWS yet. `cdk synth` and `cdk diff` are sufficient for this project. Deployment happens in the 10Q Inference module.

## Acceptance Criteria

1. Running `cdk init app --language python` in a fresh directory produces a working project skeleton.
2. The project uses a Python 3.12 virtual environment with dependencies installed from `requirements.txt`.
3. `cdk synth` produces a CloudFormation template in `cdk.out/` without errors.
4. The generated stack class is in a Python module under the project directory (not in `app.py` directly).
5. You can explain what each generated file does — `app.py`, the stack module, `cdk.json`, `requirements.txt`, and the `tests/` directory.

## Hints

### Installing the CDK CLI

```bash
npm install -g aws-cdk
cdk --version
```

You need Node.js 18 or later. The CDK CLI is a Node package regardless of which language your CDK app uses.

### Bootstrapping your AWS account

Before any CDK app can deploy (in later modules), the target account/region needs a one-time bootstrap:

```bash
cdk bootstrap aws://<ACCOUNT_ID>/<REGION>
```

This creates an S3 bucket and IAM roles that CDK uses for deployments. Run it once per account/region pair. You do not need to bootstrap for `cdk synth` — only for `cdk deploy`.

### Initializing the project

```bash
mkdir cdk-10q-inference
cd cdk-10q-inference
cdk init app --language python
```

This generates:

| File/Directory | Purpose |
|----------------|---------|
| `app.py` | Entry point — instantiates the CDK app and your stack |
| `cdk_10q_inference/` | Python package containing your stack class |
| `cdk_10q_inference/cdk_10q_inference_stack.py` | The stack definition (where you add resources) |
| `cdk.json` | CDK configuration — tells the CLI how to run your app |
| `requirements.txt` | Python dependencies (`aws-cdk-lib`, `constructs`) |
| `requirements-dev.txt` | Dev dependencies (e.g., `pytest`) |
| `tests/` | Test directory with a placeholder unit test |

### Activating the virtual environment

After `cdk init`, activate the generated virtual environment and install dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Use Python 3.12 explicitly. If your system default is a different version, specify the full path or use `python3.12` directly.

### Verifying the skeleton

```bash
cdk synth
```

This runs `app.py`, which instantiates your stack, and outputs the synthesized CloudFormation template to stdout. It also writes the full output to `cdk.out/`. If this exits zero, your project structure is correct.

### Understanding `app.py`

The entry point is minimal — it creates a `cdk.App`, instantiates your stack class, and calls `app.synth()`. All resource definitions belong in the stack class, not in `app.py`.

### The stack class

Open the generated stack file (e.g., `cdk_10q_inference/cdk_10q_inference_stack.py`). It subclasses `Stack` and currently has an empty `__init__`. In the next module you will add Lambda functions, S3 buckets, and IAM policies here.

### What `cdk.json` controls

The `app` field in `cdk.json` tells the CDK CLI how to execute your app:

```json
{
  "app": "python3 app.py"
}

```

If you renamed `app.py` or need to pass environment variables, this is where you configure it.

### Next step

Once `cdk synth` succeeds with no errors, this project is complete. The 10Q Inference module picks up from this skeleton and adds the actual Lambda and supporting resources.

---
Last verified: 2026-06
