#!/bin/bash
# SC1-a round 18: page_smoke run alone for each slice page; output in out/
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/SC1/scripts/SC1-a-r18/out
for p in index L01 L02 L03; do
  if [ "$p" = index ]; then pages=""; else pages="$p"; fi
  { .venv/bin/python tools/page_smoke.py --unit SC1 --pages ${pages:+$pages} ; echo "rc=$?"; } > $O/page_smoke_$p.out 2>&1
done
echo DONE > $O/page_smoke_done
