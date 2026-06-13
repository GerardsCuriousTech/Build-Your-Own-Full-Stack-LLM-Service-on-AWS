# Setup: AWS Account

This page walks through creating an AWS account, setting up an IAM user for programmatic access, and configuring the AWS CLI on your machine. Complete these steps before starting the Cloud Deployment modules.

## Create an AWS account

1. Go to [https://aws.amazon.com/](https://aws.amazon.com/) and choose **Create an AWS Account**.
2. Provide an email address, account name, and password for the root user.
3. Enter payment information. AWS requires a valid payment method even for Free Tier usage.
4. Verify your identity via phone or text.
5. Select the **Basic (Free)** support plan unless your organization requires otherwise.

After creation, sign in to the AWS Management Console using the root user email and password.

## Create an IAM user

The root user has unrestricted access to every service and billing setting. Day-to-day work should use an IAM user with scoped permissions.

1. Open the **IAM** console: search for "IAM" in the console search bar.
2. In the left sidebar, choose **Users**, then **Create user**.
3. Enter a username (e.g., `course-dev`).
4. On the permissions page, choose **Attach policies directly** and attach `AdministratorAccess`. For a learning environment this is acceptable; production accounts should use least-privilege policies.
5. Complete the wizard and note the user's ARN.

### Create an access key

1. From the IAM user's **Security credentials** tab, choose **Create access key**.
2. Select **Command Line Interface (CLI)** as the use case.
3. Copy the **Access key ID** and **Secret access key**. Store them securely — the secret is shown only once.

## Install the AWS CLI

Install version 2 of the AWS CLI. Follow the instructions for your operating system:

- **macOS**: `brew install awscli` or download the `.pkg` installer from the [AWS CLI install page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- **Linux / WSL**: download and run the bundled installer per the install page linked above.
- **Windows**: download the `.msi` installer from the same page.

Verify the installation:

```bash
aws --version
```

You should see output starting with `aws-cli/2.x.x`.

## Configure credentials

Run the configure command and enter the access key ID and secret from the previous step:

```bash
aws configure
```

When prompted:

| Prompt | Value |
|--------|-------|
| AWS Access Key ID | Your access key ID |
| AWS Secret Access Key | Your secret access key |
| Default region name | `us-east-1` (or your preferred region) |
| Default output format | `json` |

This writes credentials to `~/.aws/credentials` and config to `~/.aws/config`. The AWS CLI and boto3 (used in Python 3.12 Lambda functions) both read from these files automatically.

### Verify access

```bash
aws sts get-caller-identity
```

A successful response returns your account ID, user ARN, and user ID.

## Region selection

This course uses `us-east-1` in examples. Bedrock model availability varies by region — see [Setup: Bedrock Access](setup-bedrock-access.md) for details. If you choose a different region, use it consistently across all projects.

---

Last verified: 2026-06
