#!/usr/bin/env bash
# Emit SHA-256 hashes for every karnstack-canonical file as JSON.
# karnstack's /api/v1/byox/verify rejects payloads whose hashes do not
# match the canonical set for the template version this fork was
# created from (reason: `files_modified`).
#
# Files included:
#   - the workflow + the two helper scripts (no smuggling an alternate verifier)
#   - .mise.toml (no rewriting the test task to no-op)
#   - pyproject.toml (no smuggling test deps that mock the runner)
#   - every tests/test_stage*.py (no editing the tests to pass trivially)
#
# Files NOT included: bloom/__init__.py (your implementation), README.md, LICENSE.

set -euo pipefail

if command -v sha256sum >/dev/null 2>&1; then
  hash_file() { sha256sum "$1" | awk '{print $1}'; }
elif command -v shasum >/dev/null 2>&1; then
  hash_file() { shasum -a 256 "$1" | awk '{print $1}'; }
else
  echo "neither sha256sum nor shasum found" >&2
  exit 1
fi

declare -a FILES=(
  ".github/workflows/verify-stages.yml"
  ".karnstack/compute-hashes.sh"
  ".karnstack/parse-stages.sh"
  ".karnstack/sync.sh"
  ".mise.toml"
  "pyproject.toml"
)

shopt -s nullglob
for f in tests/test_stage*.py; do
  FILES+=("$f")
done
shopt -u nullglob

JSON="{}"
for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "missing canonical file: $f" >&2
    exit 1
  fi
  sha=$(hash_file "$f")
  JSON=$(echo "$JSON" | jq --arg k "$f" --arg v "$sha" '. + {($k): $v}')
done

echo "$JSON" | jq -S .
