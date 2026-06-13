#!/usr/bin/env python3
"""validate-json-blocks.py — parse every fenced `json` block in docs/ Markdown files.

Usage: python scripts/validate-json-blocks.py [docs_dir]

Exits non-zero if any JSON block fails to parse, printing file:line for each failure.
"""
import json
import pathlib
import re
import sys

def find_json_blocks(text):
    """Yield (line_number, content) for each fenced ```json block."""
    lines = text.splitlines()
    in_block = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(lines):
        if not in_block:
            if re.match(r'^```json\s*$', line):
                in_block = True
                block_start = i + 1  # 0-indexed line of opening fence
                block_lines = []
        else:
            if re.match(r'^```\s*$', line):
                in_block = False
                yield (block_start, "\n".join(block_lines))
            else:
                block_lines.append(line)

def validate_file(md_path):
    """Validate all JSON blocks in a single file. Returns list of (line, error)."""
    errors = []
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [(0, str(e))]

    for line_num, content in find_json_blocks(text):
        content_stripped = content.strip()
        if not content_stripped:
            continue
        try:
            json.loads(content_stripped)
        except json.JSONDecodeError as e:
            # Report 1-indexed line number of the block start
            errors.append((line_num + 1, str(e)))
    return errors

def main():
    docs_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("docs")
    if not docs_dir.is_dir():
        print(f"no {docs_dir}/ directory — skipping")
        sys.exit(0)

    failures = 0
    for md_file in sorted(docs_dir.rglob("*.md")):
        errors = validate_file(md_file)
        for line_num, err in errors:
            print(f"{md_file}:{line_num}: invalid JSON — {err}")
            failures += 1

    if failures:
        print(f"\n{failures} JSON block(s) failed validation.")
        sys.exit(1)
    else:
        print("All JSON blocks valid.")

if __name__ == "__main__":
    main()
