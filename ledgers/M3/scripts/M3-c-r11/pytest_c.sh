#!/bin/bash
# Round-11 M3 slice c: the relevant pytest subset (labs, run_labs, page checks), M3 selection.
cd /Users/billyribeiro/.fanout/wt/verifyD11-M3-c || exit 1
.venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k "M3" -p no:cacheprovider -rA
echo "pytest exit=$?"
