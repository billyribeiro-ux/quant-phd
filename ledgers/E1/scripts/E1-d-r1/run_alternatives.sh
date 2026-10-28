#!/bin/bash
# Runs the E1 grader suite (test_project.py, instance.py from the repository grader directory) against each
# alternative correct implementation, for seeds 0-49. Usage: run_alternatives.sh <repo-root>
ROOT="$1"; P="$ROOT/.venv/bin/python"; S="$ROOT/ledgers/E1/scripts/E1-d-r1/alternatives"; W=$(mktemp -d)
for f in "$S"/*.py; do
  d="$W/$(basename "$f" .py)"; mkdir -p "$d"; cp "$ROOT/course/modules/E/E1/grader/test_project.py" "$ROOT/course/modules/E/E1/grader/instance.py" "$d/"; cp "$f" "$d/market_structure.py"
  for s in $(seq 0 49); do (cd "$d" && QF_SEED=$s "$P" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1); done | sed 's/ in .*//' | sort | uniq -c | sed "s|^|$(basename "$f"): |"
done
