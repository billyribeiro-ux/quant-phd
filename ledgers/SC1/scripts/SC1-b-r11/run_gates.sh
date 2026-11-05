#!/bin/bash
# Round 11 slice b gates, run from the checkout root. Output in out/.
cd /Users/billyribeiro/.fanout/wt/verifyE11-SC1-b || exit 1
O=ledgers/SC1/scripts/SC1-b-r11/out
.venv/bin/python tools/check_pages.py --unit SC1 > $O/check_pages_unit.txt 2>&1; echo "check_pages_unit exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/check_pages.py --unit SC1 --page L04 > $O/check_pages_L04.txt 2>&1; echo "check_pages_L04 exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/check_pages.py --unit SC1 --page L05 > $O/check_pages_L05.txt 2>&1; echo "check_pages_L05 exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/check_pages.py --unit SC1 --page L06 > $O/check_pages_L06.txt 2>&1; echo "check_pages_L06 exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/check_dag.py --unit SC1 > $O/check_dag.txt 2>&1; echo "check_dag exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/run_labs.py --unit SC1 --page L04 > $O/run_labs_L04.txt 2>&1; echo "run_labs_L04 exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/run_labs.py --unit SC1 --page L05 > $O/run_labs_L05.txt 2>&1; echo "run_labs_L05 exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/run_labs.py --unit SC1 --page L06 > $O/run_labs_L06.txt 2>&1; echo "run_labs_L06 exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/verify_refs.py --offline > $O/verify_refs_offline.txt 2>&1; echo "verify_refs_offline exit=$?" >> $O/exit_codes.txt
.venv/bin/python tools/verify_refs.py --offline --unit SC1 > $O/verify_refs_unit_offline.txt 2>&1; echo "verify_refs_unit exit=$?" >> $O/exit_codes.txt
