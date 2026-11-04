#!/bin/sh
# Slice e, round 2: reproduce every card-slice check. Usage (from the checkout root): sh ledgers/E4/scripts/E4-e-r2/run_slice_e_r2.sh
# Writes the lesson renderings to scratch/txt and runs each check; exits nonzero on the first failing command.
set -e
S=ledgers/E4/scripts/E4-e-r2
mkdir -p scratch/txt
for i in 01 02 03 04 05 06 07 08 09; do
  .venv/bin/python -I $S/html_to_text.py course/modules/E/E4/L$i.html > scratch/txt/L$i.txt
done
echo "== card_scan"; .venv/bin/python -I $S/card_scan.py course/modules/E/E4/cards.json references/references.json
echo "== card_refs"; .venv/bin/python -I $S/card_refs.py course/modules/E/E4/cards.json scratch/txt
echo "== card_numbers"; .venv/bin/python -I $S/card_numbers.py course/modules/E/E4/cards.json scratch/txt
echo "== indep_checks"; .venv/bin/python -I $S/indep_checks.py
echo "== check_pages"; .venv/bin/python tools/check_pages.py --unit E4
echo "== check_dag"; .venv/bin/python tools/check_dag.py --unit E4
echo "== run_labs"; .venv/bin/python tools/run_labs.py --unit E4
echo "== twins"; sh $S/run_twins.sh
echo "== verify_refs offline"; .venv/bin/python tools/verify_refs.py --offline
