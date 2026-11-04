#!/bin/sh
# Banned-phrase, ellipsis and process-word scans of course/modules/E/E4/project.html (BUILDER_RULES 1.3-1.4; CLAUDE.md).
# Usage: sh ledgers/E4/scripts/E4-d-r2/banned_and_process.sh <repo-root>
P="$1/course/modules/E/E4/project.html"
for w in TODO TBD lorem "for brevity" "details omitted" "beyond the scope" "left as an exercise" "you can add more" \
  "it is important to note" "studies show" "experts agree" "it is well known" obviously clearly builder verifier \
  REQUEST planner fixer architect "unit report"; do
  printf '%-26s %s\n' "$w:" "$(grep -ci -- "$w" "$P")"
done
printf '%-26s %s\n' "ellipsis (...):" "$(grep -c '\.\.\.' "$P")"
printf '%-26s %s\n' "round (process word?):" "$(grep -ci 'round' "$P")"
grep -n -i 'round' "$P" | cut -c1-90
