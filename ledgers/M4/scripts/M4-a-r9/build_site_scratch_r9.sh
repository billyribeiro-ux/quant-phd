#!/bin/bash
# Round 9: reproduce the stale-generated-file finding in a scratch copy of the pin (no edits to the checkout).
# Usage: build_site_scratch_r9.sh <checkout-root> <pin>
set -e
CK="$1"; PIN="$2"; S=/tmp/m4a-r9-scratch
rm -rf "$S"; mkdir -p "$S"
git -C "$CK" archive "$PIN" | tar -x -C "$S"
ln -s "$CK/.venv" "$S/.venv"
cd "$S"
.venv/bin/python tools/build_site.py --check || true
.venv/bin/python tools/build_site.py
.venv/bin/python -I -c "
import json,sys
a=json.load(open('$CK/course/assets/data/glossary.json')); b=json.load(open('$S/course/assets/data/glossary.json'))
print('glossary entries checked:', len(a), len(b))
ka = a if isinstance(a, dict) else dict(enumerate(a))
kb = b if isinstance(b, dict) else dict(enumerate(b))
diff = [k for k in ka if ka.get(k) != kb.get(k)]
for k in diff: print('DIFF key', k, '| checked-in:', str(ka[k])[:160], '| regenerated:', str(kb.get(k))[:160])
print('differing entries:', len(diff), 'of', len(ka))
"
cd "$CK" && .venv/bin/python -I -c "
import sys; sys.path.insert(0,'tools')
" ; grep -rln 'level-like, slope-like' course/modules/M/M3 | head -3
