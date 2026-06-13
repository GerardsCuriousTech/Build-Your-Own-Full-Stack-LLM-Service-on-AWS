# Project: GitHub Setup

This project establishes the repository you will use for every subsequent module in the course. By the end you will have a GitHub repo with a README, a `.gitignore`, branch protection, and a feature-branch workflow you will repeat in every project that follows.

## Create Your Repository

1. Sign in to [github.com](https://github.com) (create a free account if you do not have one).
2. Click **New repository** (the `+` menu in the top-right corner).
3. Name the repository something descriptive — `sec-llm-service` works well.
4. Set visibility to **Private** (you will share it with instructors via collaborator invite).
5. Check **Add a README file** so the repo initializes with a default branch.
6. Click **Create repository**.

## Add a `.gitignore`

Create a `.gitignore` at the repository root. At minimum it should exclude:

```text
# Python virtual environment
venv/

# Byte-compiled files
__pycache__/

# Environment variables / secrets
.env

# Amplify build output (added later in the course)
amplify_outputs.json
```

Commit the file to your default branch before continuing.

## Enable Branch Protection

Branch protection prevents direct pushes to your main branch and requires pull requests for every change — the same workflow used in professional teams.

1. In your repository, go to **Settings > Branches**.
2. Under **Branch protection rules**, click **Add rule**.
3. Set **Branch name pattern** to `main`.
4. Enable **Require a pull request before merging**.
5. (Recommended) Enable **Require status checks to pass before merging** once you add CI later in the course.
6. Click **Create**.

With this rule active you cannot push directly to `main`; all changes flow through pull requests.

## Feature-Branch and Pull Request Workflow

Every project in this course follows a feature-branch workflow:

1. **Create a branch** from `main` for the work you are about to do:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/sec-cik-module
   ```

2. **Make commits** as you work. Keep commits small and descriptive:

   ```bash
   git add src/cik_lookup.py
   git commit -m "feat: add ticker_to_cik lookup function"
   ```

3. **Push the branch** to GitHub:

   ```bash
   git push -u origin feature/sec-cik-module
   ```

4. **Open a pull request** on GitHub comparing your feature branch into `main`. Write a short description of what changed and why.

5. **Review and merge.** Once you are satisfied the code is correct, merge the pull request on GitHub. Delete the feature branch after merging to keep the branch list clean.

Repeat this cycle for every project module. The habit of branching, committing with clear messages, and merging through a PR is the single most transferable workflow skill in this course.

## Commit Message Conventions

Use short, imperative-mood subject lines:

| Pattern | Example |
|---------|---------|
| `feat: <what>` | `feat: add quarterly_filing helper` |
| `fix: <what>` | `fix: handle missing CIK gracefully` |
| `docs: <what>` | `docs: add API usage notes to README` |
| `refactor: <what>` | `refactor: extract SEC URL builder` |

Keep the subject under 72 characters. If more context is needed, add a blank line followed by a body paragraph.
