#!/bin/sh
# Round-7 gate outputs for BK4-d (slice d: cards.json against L01-L05). Run from the checkout root.
S=ledgers/BK4/scripts/BK4-d-r7
O=$S/out
mkdir -p $O
echo "== check_pages --unit BK4"; .venv/bin/python tools/check_pages.py --unit BK4 > $O/check_pages_bk4.out 2>&1; echo "exit $?" >> $O/check_pages_bk4.out; cat $O/check_pages_bk4.out
echo "== check_dag --unit BK4"; .venv/bin/python tools/check_dag.py --unit BK4 > $O/check_dag_bk4.out 2>&1; echo "exit $?" >> $O/check_dag_bk4.out; cat $O/check_dag_bk4.out
echo "== run_labs --unit BK4"; .venv/bin/python tools/run_labs.py --unit BK4 > $O/run_labs_bk4.out 2>&1; echo "exit $?" >> $O/run_labs_bk4.out; cat $O/run_labs_bk4.out
echo "== cards_check_r7"; python3 -I $S/cards_check_r7.py . > $O/cards_check_r7.out 2>&1; echo "exit $?" >> $O/cards_check_r7.out
echo "== dump_cards_r7"; python3 -I $S/dump_cards_r7.py . > $O/cards_dump_r7.txt 2>&1; echo "exit $?" >> $O/cards_dump_r7.txt
