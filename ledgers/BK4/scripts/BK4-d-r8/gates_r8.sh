#!/bin/sh
# Round-8 gate outputs for BK4-d (slice d: cards.json against L01-L05). Run from the checkout root (pin 0dee921a).
S=ledgers/BK4/scripts/BK4-d-r8
O=$S/out
mkdir -p $O
echo "== lesson text dumps (extract_text.py from round 6, stdlib)"
for L in L01 L02 L03 L04 L05; do python3 -I ledgers/BK4/scripts/BK4-d-r6/extract_text.py course/modules/BK/BK4/$L.html > $O/$L.txt; done
echo "== cards structure, numbers, cross-references, duplicates, banned words (round-7 script, unchanged)"
python3 -I ledgers/BK4/scripts/BK4-d-r7/cards_check_r7.py . > $O/cards_check_r8.out 2>&1; echo "exit $?" >> $O/cards_check_r8.out
echo "== independent re-derivation of card numbers (round-7 script, unchanged)"
python3 -I ledgers/BK4/scripts/BK4-d-r7/rederive_cards_r7.py . > $O/rederive_cards_r8.out 2>&1; echo "exit $?" >> $O/rederive_cards_r8.out
echo "== check_pages, check_dag, run_labs (BK4)"
.venv/bin/python tools/check_pages.py --unit BK4 > $O/check_pages_bk4.out 2>&1; echo "exit $?" >> $O/check_pages_bk4.out
.venv/bin/python tools/check_dag.py --unit BK4 > $O/check_dag_bk4.out 2>&1; echo "exit $?" >> $O/check_dag_bk4.out
.venv/bin/python tools/run_labs.py --unit BK4 > $O/run_labs_bk4.out 2>&1; echo "exit $?" >> $O/run_labs_bk4.out
echo "== each lab twin alone under python -I -W error"
for f in L01 L02 L03 L04 L05; do python3 -I -W error tests/labs/BK4/lab-BK4-$f-1.py > $O/lab-BK4-$f-1.stdout 2> $O/lab-BK4-$f-1.stderr; echo "$f exit $? stderr_bytes $(wc -c < $O/lab-BK4-$f-1.stderr)"; done
echo "== verify_refs offline"
.venv/bin/python tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "exit $?" >> $O/verify_refs_offline.out
echo "== page_smoke for the two lesson pages changed or cited (no sweep)"
.venv/bin/python tools/page_smoke.py --unit BK4 --pages L01 L03 --skip-sweep > $O/page_smoke_bk4_L01_L03.out 2>&1; echo "exit $?" >> $O/page_smoke_bk4_L01_L03.out
echo "== Duffie registry record, plain curl to Crossref (no personal data)"
curl -s -o $O/crossref_duffie_r8.json -w "%{http_code}\n" "https://api.crossref.org/works/10.1093/rapstu/rar001"
