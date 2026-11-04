#!/bin/sh
# LX2-d round 1: line locators of SR 26-2 attachment quotations and the printed-page footers (att.txt from fetch_sources.sh).
cd /tmp/lx2d-src || exit 1
for pat in "complex quantitative" "simple arithmetic" "potential for adverse" "does not set forth" "will not result in supervisory" "Validating conceptual soundness" "Outcomes analysis compares" "persistent deviations" "Ongoing model monitoring" "Outcomes Analysis" "Components of Model"; do
  echo "== $pat"; grep -n "$pat" att.txt
done
echo "== footer lines (printed page numbers, 20+ leading spaces)"; grep -n "^ \{20,\}[0-9]\{1,2\} *$" att.txt
