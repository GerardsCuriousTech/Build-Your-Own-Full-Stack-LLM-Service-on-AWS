---
description: >-
  This module adds a modern, production-ready front end to your 10Q Inference
  service using AWS Amplify and React.
---

# Partner Bot Web Page

## Front-end module with AWS Amplify

This module adds a modern, production-ready front end to your 10Q Inference service using AWS Amplify and React. It mixes short conceptual pages with hands-on projects so students learn the "why" and the "how," then apply it with clear, reproducible steps.

### What is AWS Amplify?

AWS Amplify is a full-stack toolkit for building cloud-connected web and mobile apps. It provides a declarative developer experience to define backends (data, auth, functions, storage, and hosting) and a set of UI libraries to connect those resources to your React app.

#### Why it matters for this course

* **Full-stack glue:** Amplify helps you wire React components to cloud resources (like your Lambda for 10-Q inference) with minimal boilerplate.
* **Faster iteration:** Local "sandbox" dev against cloud services speeds feedback cycles without complex manual configuration.
* **Production lifecycle:** Built-in hosting, environments, and CI-friendly workflows make moving from prototype to production predictable.

#### Core pieces at a glance

* **Amplify backend:** Define APIs, functions, auth, and data in code, then provision to AWS.
* **Amplify UI React:** Prebuilt, accessible components (forms, modals, theming) that pair well with data-bound patterns.
* **Hosting and environments:** Simple deploys and environment isolation to match your dev-review-prod flow.

> Tip: Treat Amplify as an orchestrator for AWS services rather than a "black box." You still own IAM, API surface design, and observability choices.
