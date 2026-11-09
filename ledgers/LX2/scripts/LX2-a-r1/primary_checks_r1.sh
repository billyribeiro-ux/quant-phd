#!/bin/sh
# Round-1 delta checks on primary text. Usage: sh primary_checks_r1.sh <scratch dir with comps1884.txt etc.>
set -u
D="$1"
cd "$D" || exit 1
echo "== 2(a) 'in effect' occurrences in section 2 (lines 34-391 of comps1884.txt)"
sed -n 34,391p comps1884.txt | grep -n -i "in effect" || echo "none"
echo "== 8(d) text"
grep -n "fifteen days after such no" comps1884.txt
echo "== 15(d)(1) third sentence"
grep -n "1,200 persons" comps1885.txt
echo "== Dirks pdf pages (pdftotext -f/-l)"
for p in 10 14 15 18; do echo "-- pdf page $p header:"; pdftotext -f $p -l $p -layout USREPORTS-463-646.pdf - | grep -E "DIRKS v. SEC|OCTOBER TERM" | head -1; done
echo "-- 'Unlike insiders' pdf page:"; pdftotext -f 10 -l 10 USREPORTS-463-646.pdf - | grep -c "Unlike insiders"
echo "-- fn 23 on pdf 18:"; pdftotext -f 18 -l 18 USREPORTS-463-646.pdf - | tr '\n' ' ' | tr -s ' ' | grep -o "23 Scienter.\{0,120\}"
echo "-- O'Hagan 'temporarily become' pdf page 11 header:"; pdftotext -f 11 -l 11 -layout USREPORTS-521-642.pdf - | grep -E "^ *652 " | head -1
