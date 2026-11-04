#!/bin/bash
# Static checks for M3 slice c (L07-L09 and twins), round 7. Run from the checkout root.
set -u
M=course/modules/M/M3
echo "## duplicate ids per page"
for f in L07 L08 L09; do echo "$f: $(grep -o -E ' id="[^"]+"' $M/$f.html | sort | uniq -d | wc -l) duplicated ids"; done
echo "## formal Definition blocks per page"
grep -n -o -E 'Definition [0-9.a-z]+ <span class="name">\([^)]*\)' $M/L0[789].html
echo "## orthogonal-matrix definitions in M3 lessons (L06 Definition 1.1 vs L09 Definition 1.2a)"
grep -n -o -E 'Definition 1\.1 <span class="name">\(orthogonal matrix\)|Definition 1\.2a <span class="name">\(orthogonal matrix\)' $M/L06.html $M/L09.html
echo "## restated plain definitions in L09 (transpose, trace)"
grep -n -o -E 'The transpose .{0,40}|the trace .{0,60}' $M/L09.html | head -4
echo "## level-slope-curvature wording (introduces row, definition, disclaimers)"
grep -n -o -E 'Level, slope and curvature factors[^<]*|level-like[^.]{0,60}|no claim about the shape of any observed yield curve|not about any yield curve|real curve[^.]{0,40}' $M/L08.html | head -12
echo "## concept registry entry"
python3 -c "import json;c=json.load(open('curriculum/curriculum.json'))['concepts'];print('level-slope-curvature ->',c.get('level-slope-curvature'))"
echo "## TeX macros used on the three pages (count)"
for f in L07 L08 L09; do echo "$f:"; grep -o -E '\\(operatorname|mathrm|mathbb|tr|diag|R|ast|top)[^a-zA-Z]' $M/$f.html | sort | uniq -c | tr -s ' ' | tr '\n' ' '; echo; done
echo "## banned filler and placeholder phrases"
grep -n -i -E 'for brevity|details omitted|beyond the scope|you can add more|important to note|studies show|experts agree|well known|obviously|clearly|left as an exercise|it can be shown|TODO|TBD|lorem' $M/L07.html $M/L08.html $M/L09.html | wc -l
echo "## citations and outside names"
grep -n -i -E 'higham|litterman|scheinkman|eckart|nelson|gurkaynak|axler|strang|data-cite|data-locator' $M/L07.html $M/L08.html $M/L09.html | wc -l
echo "## ellipsis at quiz stems (count)"
grep -n -E '\.\.\.</p>|…' $M/L07.html $M/L08.html $M/L09.html | cut -c1-120
echo "## MANIFEST series with tenors (ust_daily columns)"
python3 -c "import json;m=json.load(open('course/assets/data/market/MANIFEST.json'));[print(d['id'],d['columns']) for d in m['datasets']]"
echo "## degenerate curvature shape check (L08 Definition 3.1)"
.venv/bin/python -I -W error ledgers/M3/scripts/M3-c-r7/l08_definition31_degenerate.py
