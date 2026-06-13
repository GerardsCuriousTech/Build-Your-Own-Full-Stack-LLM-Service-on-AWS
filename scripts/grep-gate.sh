#!/usr/bin/env bash
# grep-gate.sh — scan docs/ for banned patterns defined in .grep-gate-rules.yml.
# Exits non-zero if any rule matches a file not in that rule's allow_in list.
# Requires: python3 (for YAML parsing and regex matching including Unicode).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RULES_FILE="$REPO_ROOT/.grep-gate-rules.yml"
DOCS_DIR="$REPO_ROOT/docs"

if [ ! -f "$RULES_FILE" ]; then
  echo "ERROR: $RULES_FILE not found" >&2; exit 1
fi
if [ ! -d "$DOCS_DIR" ]; then
  echo "no docs/ directory — skipping"; exit 0
fi

exec python3 - "$RULES_FILE" "$DOCS_DIR" "$REPO_ROOT" <<'PYTHON'
import sys, re, pathlib, os

rules_file = pathlib.Path(sys.argv[1])
docs_dir = pathlib.Path(sys.argv[2])
repo_root = pathlib.Path(sys.argv[3])


def parse_rules(text):
    """Minimal parser for the .grep-gate-rules.yml format.

    Handles single-quoted and double-quoted YAML string values.
    Single-quoted: only '' is an escape (for literal ').
    Double-quoted: standard YAML escapes (not needed for our patterns).
    """
    rules = []
    current = None
    in_allow_in = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- name:"):
            if current:
                rules.append(current)
            in_allow_in = False
            current = {
                "name": extract_value(stripped.split(":", 1)[1]),
                "pattern": "",
                "allow_in": [],
                "message": "",
            }
        elif current and stripped.startswith("pattern:"):
            current["pattern"] = extract_value(stripped.split(":", 1)[1])
            in_allow_in = False
        elif current and stripped.startswith("message:"):
            current["message"] = extract_value(stripped.split(":", 1)[1])
            in_allow_in = False
        elif current and stripped.startswith("allow_in:"):
            rest = stripped.split(":", 1)[1].strip()
            in_allow_in = True
            if rest == "[]":
                current["allow_in"] = []
                in_allow_in = False
        elif current and in_allow_in and stripped.startswith("-"):
            val = extract_value(stripped[1:].strip())
            current["allow_in"].append(val)
        else:
            in_allow_in = False

    if current:
        rules.append(current)
    return rules


def extract_value(raw):
    """Strip surrounding quotes from a YAML scalar value."""
    raw = raw.strip()
    if raw.startswith("'") and raw.endswith("'"):
        # YAML single-quoted: '' escapes to '
        return raw[1:-1].replace("''", "'")
    if raw.startswith('"') and raw.endswith('"'):
        # YAML double-quoted: process common escapes
        val = raw[1:-1]
        val = val.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"').replace("\\\\", "\\")
        return val
    return raw


rules_text = rules_file.read_text(encoding="utf-8")
rules = parse_rules(rules_text)

# Build compiled regex for each rule
compiled_rules = []
for rule in rules:
    pattern_str = rule["pattern"]
    # Convert \x{NNNN} Unicode escapes to actual characters
    pattern_str = re.sub(
        r"\\x\{([0-9A-Fa-f]+)\}",
        lambda m: chr(int(m.group(1), 16)),
        pattern_str,
    )
    try:
        compiled = re.compile(pattern_str)
    except re.error as e:
        print(f"WARNING: cannot compile pattern for rule '{rule['name']}': {e}", file=sys.stderr)
        continue
    compiled_rules.append((rule, compiled))

failures = 0
md_files = sorted(docs_dir.rglob("*.md"))

for md_file in md_files:
    rel_path = str(md_file.relative_to(repo_root)).replace(os.sep, "/")

    try:
        lines = md_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        continue

    for rule, pattern in compiled_rules:
        if rel_path in rule["allow_in"]:
            continue
        for line_num, line_text in enumerate(lines, start=1):
            if pattern.search(line_text):
                print(f"{rel_path}:{line_num}: [{rule['name']}] {rule['message']}")
                failures += 1

if failures:
    print(f"\n{failures} violation(s) found.")
sys.exit(1 if failures > 0 else 0)
PYTHON
