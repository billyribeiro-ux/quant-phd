#!/bin/bash
cd "$(dirname "$0")/../../../.." || exit 1
S=ledgers/E4/scripts/E4-d-r21
O=$S/out
run() { name=$1; shift; { "$@" ; echo "EXIT=$?"; } > "$O/$name.txt" 2>&1; }
run run_labs_E4_all .venv/bin/python tools/run_labs.py --unit E4
run verify_refs_offline_all .venv/bin/python tools/verify_refs.py --offline
run verify_refs_E4_live .venv/bin/python tools/verify_refs.py --unit E4
run labs_twin_check_r21 python3 -I $S/labs_twin_check_r21.py "$(pwd)"
run collect_count_r21 bash $S/collect_count_r21.sh
run mutate_list_E4 .venv/bin/python tools/mutate_graders.py --help
echo done > $O/more_done
