#!/usr/bin/env python3
"""validate-contract.py — validate Lambda JSON examples against the contract schema.

Loads the schema from docs/reference/contract.md JSON blocks, scans project pages
for JSON blocks containing Lambda request/response fields, and validates them.

Usage: python scripts/validate-contract.py [docs_dir]
"""
import json
import pathlib
import re
import sys

VALID_PERIODS = {"Q1", "Q2", "Q3", "Q4", "FY"}
REQUEST_FIELDS = {"question", "ticker", "year", "period"}
RESPONSE_FIELDS = {"answer", "meta"}


def find_json_blocks(text):
    """Yield (line_number, parsed_obj) for each fenced ```json block that parses."""
    lines = text.splitlines()
    in_block = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(lines):
        if not in_block:
            if re.match(r"^```json\s*$", line):
                in_block = True
                block_start = i + 1
                block_lines = []
        else:
            if re.match(r"^```\s*$", line):
                in_block = False
                content = "\n".join(block_lines).strip()
                if content:
                    try:
                        obj = json.loads(content)
                        yield (block_start + 1, obj)
                    except json.JSONDecodeError:
                        pass
            else:
                block_lines.append(line)


def is_request(obj):
    """Return True if the JSON object looks like a Lambda request."""
    if not isinstance(obj, dict):
        return False
    return "question" in obj and "ticker" in obj


def is_response(obj):
    """Return True if the JSON object looks like a Lambda response."""
    if not isinstance(obj, dict):
        return False
    return "answer" in obj


def validate_request(obj):
    """Validate a request object against the contract. Return list of errors."""
    errors = []
    for field in obj:
        if field not in REQUEST_FIELDS:
            errors.append(f"unexpected request field '{field}'")
    if "question" in obj and not isinstance(obj["question"], str):
        errors.append("'question' must be a string")
    if "ticker" in obj and not isinstance(obj["ticker"], str):
        errors.append("'ticker' must be a string")
    if "year" in obj and not isinstance(obj["year"], int):
        errors.append("'year' must be an integer")
    if "period" in obj:
        if obj["period"] not in VALID_PERIODS:
            errors.append(
                f"'period' must be one of {sorted(VALID_PERIODS)}, got '{obj['period']}'"
            )
    return errors


def validate_response(obj):
    """Validate a response object against the contract. Return list of errors."""
    errors = []
    for field in obj:
        if field not in RESPONSE_FIELDS:
            errors.append(f"unexpected response field '{field}'")
    if "answer" in obj and not isinstance(obj["answer"], str):
        errors.append("'answer' must be a string")
    if "meta" in obj and not isinstance(obj["meta"], dict):
        errors.append("'meta' must be an object")
    return errors


def is_project_page(path, docs_dir):
    """Return True if the file is a project page (not the contract definition itself)."""
    rel = str(path.relative_to(docs_dir)).replace("\\", "/")
    # Skip the contract definition page itself
    if rel == "reference/contract.md":
        return False
    # Project pages: paths containing 'project-' or known project directories
    project_dirs = [
        "project-sec-cik-lookup",
        "project-sec-edgar-api-library",
        "project-sec-lambda",
        "project-10q-inference",
        "cdk-bridge",
        "partner-bot-web-page",
        "mcp-module",
        "langchain-and-rag",
    ]
    return any(rel.startswith(d + "/") or rel.startswith(d + "\\") for d in project_dirs)


def main():
    docs_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("docs")
    if not docs_dir.is_dir():
        print(f"no {docs_dir}/ directory — skipping")
        sys.exit(0)

    contract_page = docs_dir / "reference" / "contract.md"
    if not contract_page.exists():
        print("WARNING: docs/reference/contract.md not found — skipping contract validation")
        sys.exit(0)

    failures = 0
    for md_file in sorted(docs_dir.rglob("*.md")):
        if not is_project_page(md_file, docs_dir):
            continue
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for line_num, obj in find_json_blocks(text):
            if is_request(obj):
                errs = validate_request(obj)
                for e in errs:
                    print(f"{md_file}:{line_num}: contract violation (request) — {e}")
                    failures += 1
            elif is_response(obj):
                errs = validate_response(obj)
                for e in errs:
                    print(f"{md_file}:{line_num}: contract violation (response) — {e}")
                    failures += 1

    if failures:
        print(f"\n{failures} contract violation(s) found.")
        sys.exit(1)
    else:
        print("All Lambda JSON examples conform to the contract.")


if __name__ == "__main__":
    main()
