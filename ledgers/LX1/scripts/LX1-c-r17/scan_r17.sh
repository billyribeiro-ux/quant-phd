#!/usr/bin/env bash
# Round-17 verifier: banned-phrase and process-word scan of project.html (BUILDER_RULES 1.3-1.4), plus notation scan.
P=course/modules/LX/LX1/project.html
for w in TODO TBD lorem 'for brevity' 'details omitted' 'beyond the scope' 'left as an exercise' 'you can add more' \
  'it is important to note' 'studies show' 'experts agree' 'it is well known' obviously clearly 'about 6' 'roughly half' \
  historically 'It can be shown' Pseudocode 'checks that' 'round [0-9]' 'verifier' 'builder' 'ruling' 'this round' 'LX1-c'; do
  echo "$w: $(grep -i -c -- "$w" "$P")"
done
echo "--- agreement / statistics / two-pass claims (page and twin)"
grep -n -i 'agree\|statistics\|two-pass' "$P" tests/labs/LX1/lab-LX1-project-3.py | cut -c1-160
echo "--- concept links on project page"
grep -c 'data-concept' "$P"
