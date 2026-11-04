#!/bin/bash
# Run each slice lab twin standalone: python -I -W error, scratch cwd, empty environment.
R=/Users/billyribeiro/.fanout/wt/verifyE1-E4-c
O=$R/ledgers/E4/scripts/E4-c-r1/out
for t in "$@"; do
  s=$(mktemp -d /tmp/e4c-run.XXXXXX)
  ( cd "$s" && env -i PATH=/usr/bin:/bin "$R/.venv/bin/python" -I -W error "$R/tests/labs/E4/lab-E4-$t.py" > "$O/lab-E4-$t.out" 2> "$O/lab-E4-$t.err"; echo "lab-E4-$t exit=$?" >> "$O/twins_exit.out" )
  rm -rf "$s"
done
