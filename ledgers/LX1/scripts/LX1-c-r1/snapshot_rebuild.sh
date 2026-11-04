#!/bin/sh
# Rebuild fx_monthly from the live Fed feed in a scratch copy (tools/fetch_data.py --fetch), then compare bytes.
# Usage: sh snapshot_rebuild.sh <checkout> <scratch-dir-empty>
set -e
CHK="$1"; S="$2"; mkdir -p "$S/repo" "$S/raw"
(cd "$CHK" && tar --exclude=.venv --exclude=./course/assets/vendor -cf - .) | (cd "$S/repo" && tar -xf -)
cd "$S/repo" && "$CHK/.venv/bin/python" tools/fetch_data.py --fetch --only fx_monthly --keep-raw "$S/raw"
cmp "$S/repo/course/assets/data/market/fx_monthly.csv" "$CHK/course/assets/data/market/fx_monthly.csv" && echo "CSV bytes identical to committed snapshot"
sha256sum "$S/repo/course/assets/data/market/fx_monthly.csv" "$CHK/course/assets/data/market/fx_monthly.csv"
