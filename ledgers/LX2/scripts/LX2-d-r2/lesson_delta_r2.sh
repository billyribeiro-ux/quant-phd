#!/bin/sh
# LX2-d round 2: text delta of the four lesson pages since the round 1 pin (1c1645f3) to the checkout.
# Usage: sh lesson_delta_r2.sh <checkout>
CO=${1:-.}; S="$CO/ledgers/LX2/scripts/LX2-d-r2"
cd "$CO" || exit 1
for L in L01 L02 L03 L04; do
  git show 1c1645f3:course/modules/LX/LX2/$L.html > /tmp/lx2d-r2-old-$L.html
  python3 -I "$S/strip_lines.py" /tmp/lx2d-r2-old-$L.html | sed 's/^[0-9]*: //' > /tmp/lx2d-r2-old-$L.txt
  python3 -I "$S/strip_lines.py" course/modules/LX/LX2/$L.html | sed 's/^[0-9]*: //' > /tmp/lx2d-r2-new-$L.txt
  n=$(diff /tmp/lx2d-r2-old-$L.txt /tmp/lx2d-r2-new-$L.txt | grep -c '^[<>]')
  echo "== $L changed text lines: $n"
done
echo "== cards.json diff stat"
git diff --stat 1c1645f3 HEAD -- course/modules/LX/LX2/cards.json | tail -1
