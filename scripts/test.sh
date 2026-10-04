#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests 2>&1 | tee /tmp/out.log
total=$(sed -n 's/^Ran \([0-9]*\) test.*/\1/p' /tmp/out.log)
if grep -q '^OK' /tmp/out.log; then passed=$total; else passed=0; fi
echo "TESTS: $passed/$total"