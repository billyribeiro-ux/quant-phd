#!/bin/sh
# Round-35: is the Lab 6 null-count claim (1.395; per-rule range 0.046 to 0.048) on the current S7 pages?
cd "$1" || exit 1
echo "== 1.395 / 1.388 in S7 pages, twins, cards"
grep -n -e '1\.395' -e '1\.388' course/modules/S/S7/*.html tests/labs/S7/*.py course/modules/S/S7/cards.json || echo "none"
echo "== 0.046 / 0.048 in S7 L05 and L06 pages"
grep -n -e '0\.046' -e '0\.048' course/modules/S/S7/L05.html course/modules/S/S7/L06.html || echo "none"
echo "== 0.046 / 0.048 anywhere in S7 pages (for context)"
grep -n -e '0\.046' -e '0\.048' course/modules/S/S7/*.html | cut -c1-120
echo "== line 873 of L05 (sentence with 1.5)"
sed -n 873p course/modules/S/S7/L05.html | /usr/bin/python3 -c "import sys,re,html; t=html.unescape(re.sub(r'<[^>]+>',' ',sys.stdin.read())); i=t.find('1.5'); print(re.sub(r'\s+',' ',t[max(0,i-120):i+140]))"
