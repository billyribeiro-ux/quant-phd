#!/bin/sh
# Round-14 verifier: rebuild fx_monthly from the live H.10 feed in a scratch copy (never the committed tree).
# Arguments: $1 = checkout root (for tools/ and the committed snapshot), $2 = empty scratch directory.
set -e
ROOT="$1"; S="$2"
mkdir -p "$S/course/assets/data" && cp -R "$ROOT/tools" "$S/tools" && cp -R "$ROOT/course/assets/data/market" "$S/course/assets/data/market"
cd "$S" && "$ROOT/.venv/bin/python" -I tools/fetch_data.py --fetch --only fx_monthly --keep-raw "$S/raw"
shasum -a 256 "$S/course/assets/data/market/fx_monthly.csv" "$ROOT/course/assets/data/market/fx_monthly.csv"
cmp "$S/course/assets/data/market/fx_monthly.csv" "$ROOT/course/assets/data/market/fx_monthly.csv" && echo "CSV byte-identical"
