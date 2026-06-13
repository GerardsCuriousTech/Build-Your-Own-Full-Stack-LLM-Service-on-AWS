# Build Your Own Full Stack LLM Service on AWS

Source repository for the GitBook-published course. The published content lives in `docs/` and is synced to GitBook via `.gitbook.yaml`.

## Repository structure

```
.gitbook.yaml          # Points GitBook at docs/
docs/                  # All published course content (GitBook content root)
  SUMMARY.md           # GitBook navigation tree
  README.md            # Course introduction page
  reference/           # Cross-cutting reference pages
  <module folders>/    # One folder per course module
.kiro/specs/           # Requirements, design, and task specs
scripts/               # CI validation scripts (added incrementally)
course-content-audit.md  # Per-page audit notes
ROADMAP.md             # Ordered work queue for agent sessions
AGENTS.md              # Working conventions for agents and contributors
```

## Workflow

- GitBook Git Sync operates bidirectionally on `main`.
- Contributors and agents work on feature branches and merge to `development`.
- A human merges `development` into `main` to publish.

## License

All rights reserved.
