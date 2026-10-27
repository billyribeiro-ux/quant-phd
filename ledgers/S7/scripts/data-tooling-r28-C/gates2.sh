#!/bin/bash
# Round-28 part C, second batch: whole-registry live verify_refs, page_smoke --all, live fetch in a scratch copy,
# raw-dir rebuild, collect-only twice, and the 83 killer test ids named in the tooling mutants.
R=/tmp/verify-s7-r2-C
D=/tmp/ap1-r5/dt-C-r28
L=$R/ledgers/S7/scripts/data-tooling-r28-C/logs
PY=$R/.venv/bin/python
cd $R || exit 1
run() { name=$1; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > $L/$name.log 2>&1; echo "$name: $(tail -1 $L/$name.log)"; }
while pgrep -f "gates.sh" >/dev/null; do sleep 5; done
run page_smoke_all $PY tools/page_smoke.py --all
run verify_refs_whole_live $PY tools/verify_refs.py
run collect1 $PY -m pytest --collect-only -q -p no:cacheprovider tests/test_fetch_data.py tests/test_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_build_site.py
run collect2 $PY -m pytest --collect-only -q -p no:cacheprovider tests/test_fetch_data.py tests/test_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_build_site.py
run slice_tests $PY -m pytest -q -p no:cacheprovider tests/test_fetch_data.py tests/test_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_build_site.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_fetch_vendor.py tests/test_koning_spot.py tests/test_figure_kernels.py tests/js
run mypy_nocache_all_twins $R/.venv/bin/mypy --no-incremental
