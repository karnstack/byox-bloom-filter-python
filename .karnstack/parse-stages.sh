#!/usr/bin/env bash
# Parse `pytest -v` output and emit JSON:
#
#   {"passing_stages": [1, 2, 3]}
#
# A stage passes only when every test_stageNN_* function for that stage
# reports PASSED. Any FAILED / ERROR on a test_stageNN_* fails that
# stage.
#
# Portable across bash 3.2 (macOS) and bash 4+ (Linux).

set -euo pipefail

LOG="${1:-/dev/stdin}"
TMP=$(mktemp -t parse-stages.XXXXXX)
trap 'rm -f "$TMP"' EXIT

# pytest -v lines look like:
#   tests/test_stage07_foo.py::test_stage07_added_key_is_present PASSED [ 20%]
#   tests/test_stage07_foo.py::test_stage07_bit_array_boundary FAILED [ 40%]
#
# Extract one line per (RESULT, NN). Map ERROR -> FAIL (a crashed test is a fail).
grep -E '::test_stage[0-9]{2}_[A-Za-z0-9_]+ +(PASSED|FAILED|ERROR)' "$LOG" \
  | sed -E 's/.*::test_stage([0-9]{2})_[A-Za-z0-9_]+ +(PASSED|FAILED|ERROR).*/\2 \1/' \
  | sed -E 's/^ERROR/FAIL/; s/^FAILED/FAIL/; s/^PASSED/PASS/' \
  > "$TMP" || true

FAILED=$(awk '$1=="FAIL" {print $2}' "$TMP" | sort -u)
SEEN=$(awk '{print $2}' "$TMP" | sort -u)

if [ -z "$SEEN" ]; then
  echo '{"passing_stages": []}'
  exit 0
fi

PASSING=$(comm -23 <(printf '%s\n' "$SEEN") <(printf '%s\n' "$FAILED"))

if [ -z "$PASSING" ]; then
  echo '{"passing_stages": []}'
  exit 0
fi

printf '%s\n' "$PASSING" \
  | sed -E 's/^0+//' \
  | sort -n \
  | jq -R 'tonumber' \
  | jq -sc '{passing_stages: .}'
