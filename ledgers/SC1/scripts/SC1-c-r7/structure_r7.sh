#!/bin/bash
# SC1-c round 7: grep-level checks on L07/L08 (run from the checkout root).
cd "$(dirname "$0")/../../../.." || exit 1
P="course/modules/SC/SC1/L07.html course/modules/SC/SC1/L08.html"
echo "== banned phrases (BUILDER_RULES 1.3-1.4)"
grep -n -i -E 'TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|well known|obviously|clearly' $P | wc -l
echo "== ellipses"
grep -c '…\|\.\.\.' $P
echo "== data-cite markup"
grep -c 'data-cite' $P
echo "== \\kappa in L07/L08"
grep -c '\\kappa' $P
echo "== walk identity occurrences (term check)"
grep -n -o '.\{25\}walk identity.\{25\}' $P | head -20
echo "== 'discrete reflection/tail identity' in L06 (name the lesson uses)"
grep -o 'discrete reflection identity\|discrete tail identity' course/modules/SC/SC1/L06.html | sort | uniq -c
echo "== 'walk identity' anywhere in L06"
grep -c 'walk identity' course/modules/SC/SC1/L06.html
echo "== reflection link anchors"
grep -n -o 'reflection identity of.\{0,160\}' $P | cut -c1-260
echo "== data-hours"
grep -o 'data-hours="[0-9]*"' $P
grep -o 'data-hours-lessons="[0-9]*"\|data-hours-project="[0-9]*"' course/modules/SC/SC1/index.html
echo "== macros used in L07/L08"
grep -o '\\[A-Za-z]*' $P | sort | uniq -c | sort -rn | awk '{print $2}' | tr '\n' ' '; echo
