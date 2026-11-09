#!/bin/sh
# Slice a round 2: run each slice twin alone under python -I -W error; count quiz items, problems, misconceptions, key-result rows, lab sections and why-it-matters words per page.
ROOT="$1"
cd "$ROOT" || exit 1
for n in L01 L02 L03 L04; do
  .venv/bin/python -I -W error tests/labs/M5/lab-M5-$n-1.py > /dev/null 2>/tmp/m5a_r2_$n.err
  echo "twin lab-M5-$n-1 exit=$? stderr_bytes=$(wc -c < /tmp/m5a_r2_$n.err | tr -d ' ')"
done
for p in index L01 L02 L03 L04; do
  f="course/modules/M/M5/$p.html"
  echo "$p quiz_items=$(grep -c 'class="item"' "$f") problems=$(grep -c 'class="problem"' "$f") solutions=$(grep -c 'class="solution"' "$f") misconceptions=$(grep -c 'class="misconception"' "$f") labs=$(grep -c 'class="lab"' "$f") explain=$(grep -c 'class="explain"' "$f")"
done
