#!/bin/bash
# Round-16 gate runs for E4 slice e (cards against lessons), on pin 56cc575a.
# Run from the checkout root: bash ledgers/E4/scripts/E4-e-r16/run_gates_r16.sh
set -u
OUT=ledgers/E4/scripts/E4-e-r16/outputs
mkdir -p "$OUT"
.venv/bin/python tools/check_pages.py --unit E4 > "$OUT/check_pages.txt" 2>&1; echo "check_pages exit=$?" | tee -a "$OUT/exit_codes.txt"
.venv/bin/python tools/check_dag.py --unit E4 > "$OUT/check_dag.txt" 2>&1; echo "check_dag exit=$?" | tee -a "$OUT/exit_codes.txt"
.venv/bin/python tools/check_projects.py --unit E4 > "$OUT/check_projects.txt" 2>&1; echo "check_projects exit=$?" | tee -a "$OUT/exit_codes.txt"
.venv/bin/python tools/verify_refs.py --offline > "$OUT/verify_refs_offline.txt" 2>&1; echo "verify_refs exit=$?" | tee -a "$OUT/exit_codes.txt"
.venv/bin/python tools/run_labs.py --unit E4 > "$OUT/run_labs.txt" 2>&1; echo "run_labs exit=$?" | tee -a "$OUT/exit_codes.txt"
for f in L03 L06; do
  n=$(echo $f | tr -d L)
  python3 -I tests/labs/E4/lab-E4-L${n}-1.py > "$OUT/twin_L${n}.txt" 2>&1; echo "twin L${n} exit=$?" | tee -a "$OUT/exit_codes.txt"
done
.venv/bin/python tools/page_smoke.py --unit E4 --skip-sweep --pages L03.html L06.html > "$OUT/page_smoke_L03_L06.txt" 2>&1; echo "page_smoke exit=$?" | tee -a "$OUT/exit_codes.txt"
python3 -I ledgers/E4/scripts/E4-e-r16/card_scan_r16.py course/modules/E/E4/cards.json > "$OUT/card_scan_r16.txt"; echo "card_scan exit=$?" | tee -a "$OUT/exit_codes.txt"
python3 -I ledgers/E4/scripts/E4-e-r16/rederive_r16.py > "$OUT/rederive_r16.txt"; echo "rederive exit=$?" | tee -a "$OUT/exit_codes.txt"
