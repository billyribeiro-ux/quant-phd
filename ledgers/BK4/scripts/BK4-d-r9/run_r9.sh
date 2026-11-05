#!/bin/sh
# Re-runs every BK4-d round-9 check from the checkout root. Usage: sh ledgers/BK4/scripts/BK4-d-r9/run_r9.sh
set -e
D=ledgers/BK4/scripts/BK4-d-r9
for f in L01 L02 L03 L04 L05; do python3 -I $D/extract_text.py course/modules/BK/BK4/$f.html > $D/out/$f.txt; done
python3 -I $D/card_numbers.py course/modules/BK/BK4/cards.json $D/out > $D/out/card_numbers.out
python3 -I $D/card_structure.py course/modules/BK/BK4/cards.json $D/out > $D/out/card_structure.out
python3 -I $D/rederive.py > $D/out/rederive.out
python3 -I $D/lab_compare.py "$PWD" $D/out > $D/out/lab_compare.out
.venv/bin/python -c "import sys,json; sys.path.insert(0,'tools'); import ledger; print(ledger.validate(json.load(open('ledgers/BK4/BK4-d.json')), 'BK4-d'))"
