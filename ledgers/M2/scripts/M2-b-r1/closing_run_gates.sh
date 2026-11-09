#!/bin/bash
# Closing-delta (round 1, pin d9de2fe5) gate record for M2 slice b. Run from the verifier checkout.
cd /Users/billyribeiro/.fanout/wt/verifyH1-M2-b || exit 1
S=ledgers/M2/scripts/M2-b-r1
PY=.venv/bin/python
run() { local name=$1; shift; "$@" > $S/$name.out 2>&1; echo "exit=$?" >> $S/$name.out; echo "$name: $(tail -1 $S/$name.out)"; }
run closing_check_pages_M2      $PY tools/check_pages.py --unit M2
run closing_check_dag_M2        $PY tools/check_dag.py --unit M2
run closing_check_projects_M2   $PY tools/check_projects.py --unit M2
run closing_run_labs_M2         $PY tools/run_labs.py --unit M2
run closing_page_smoke_L07_L12  $PY tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12
run closing_build_site_check    $PY tools/build_site.py --check
run closing_verify_refs_offline $PY tools/verify_refs.py --offline
run closing_pytest_cards_pages  $PY -m pytest tests/test_page_checks.py tests/test_labs.py tests/test_refs.py -k 'M2 or card or page or refs' -q
