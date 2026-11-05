#!/bin/sh
# LX1-b round 11: rebuild fx_monthly from the live feed in a scratch copy (plain fetch, no bot-check bypass),
# compare the snapshot bytes with the checkout, and diff the MANIFEST (provenance fields only are expected to change).
# Usage: sh ledgers/LX1/scripts/LX1-b-r11/fx_rebuild_r11.sh <checkout> <scratch-dir> <outdir>
CHECK="$1"; SCR="$2"; OUT="$3"
rm -rf "$SCR" && mkdir -p "$SCR" "$OUT" && OUT=$(cd "$OUT" && pwd)
(cd "$CHECK" && git archive 11d7077 tools references course/assets/data/market | tar -x -C "$SCR")
cd "$SCR" || exit 1
/Users/billyribeiro/dev/quant-phd/.venv/bin/python tools/fetch_data.py --fetch --only fx_monthly > "$OUT/fetch_rebuild_fx_monthly_r11.out" 2>&1
echo "exit=$?" >> "$OUT/fetch_rebuild_fx_monthly_r11.out"
sha256sum course/assets/data/market/fx_monthly.csv >> "$OUT/fetch_rebuild_fx_monthly_r11.out"
cmp course/assets/data/market/fx_monthly.csv "$CHECK/course/assets/data/market/fx_monthly.csv" && echo CSV_BYTE_IDENTICAL >> "$OUT/fetch_rebuild_fx_monthly_r11.out"
diff "$CHECK/course/assets/data/market/MANIFEST.json" course/assets/data/market/MANIFEST.json >> "$OUT/fetch_rebuild_fx_monthly_r11.out"
echo "manifest_diff_exit=$?" >> "$OUT/fetch_rebuild_fx_monthly_r11.out"
