#!/bin/sh
# LX1-b round 15: rebuild fx_monthly from the live Federal Reserve feed in a scratch copy (tools/fetch_data.py --fetch),
# then compare the snapshot bytes and the MANIFEST entry with the committed ones. The checkout is not written.
# Usage: sh ledgers/LX1/scripts/LX1-b-r15/fx_rebuild_r15.sh <checkout>
R="$1"
S=/tmp/lx1b-r15-rebuild
rm -rf "$S" && mkdir -p "$S/tools" "$S/course/assets/data/market" "$S/raw"
cp "$R/tools/fetch_data.py" "$R/tools/data_sources.yaml" "$S/tools/"
cp "$R/course/assets/data/market/"* "$S/course/assets/data/market/"
cd "$S" || exit 1
"$R/.venv/bin/python" -I tools/fetch_data.py --fetch --only fx_monthly --keep-raw "$S/raw"; echo "exit=$?"
shasum -a 256 "$S/raw/fx_monthly.raw"
cmp "$S/course/assets/data/market/fx_monthly.csv" "$R/course/assets/data/market/fx_monthly.csv" && echo CSV_BYTE_IDENTICAL
"$R/.venv/bin/python" -I -c "
import json
a=[x for x in json.load(open('$R/course/assets/data/market/MANIFEST.json'))['datasets'] if x['id']=='fx_monthly'][0]
b=[x for x in json.load(open('$S/course/assets/data/market/MANIFEST.json'))['datasets'] if x['id']=='fx_monthly'][0]
for k in ('raw_sha256','sha256','rows','first','last','retrieved','bytes'): print(k, a[k], b[k], a[k]==b[k])
"
