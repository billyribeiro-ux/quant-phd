#!/usr/bin/env bash
# LX1-c round 19: rebuild fx_monthly from the live feed in a scratch copy, then compare with the committed snapshot.
# Usage: bash rebuild_fx_monthly_r19.sh <checkout_root> <new empty scratch dir>
set -u
ROOT="$1"; SCR="$2"
mkdir -p "$SCR/tools" "$SCR/course/assets/data/market" "$SCR/raw"
cp "$ROOT/tools/fetch_data.py" "$ROOT/tools/data_sources.yaml" "$SCR/tools/"
cp "$ROOT/course/assets/data/market/"* "$SCR/course/assets/data/market/"
cd "$SCR" && "$ROOT/.venv/bin/python" -I tools/fetch_data.py --fetch --only fx_monthly --keep-raw "$SCR/raw"
cmp "$SCR/course/assets/data/market/fx_monthly.csv" "$ROOT/course/assets/data/market/fx_monthly.csv" && echo "CSV byte-identical"
shasum -a 256 "$SCR/course/assets/data/market/fx_monthly.csv" "$SCR/raw/fx_monthly.raw"
