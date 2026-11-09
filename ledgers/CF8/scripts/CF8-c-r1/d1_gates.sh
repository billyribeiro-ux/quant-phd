#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyG1-CF8-c || exit 1
run() { echo "== $*"; "$@" > /tmp/cf8c-closing-r1/last.out 2>&1; rc=$?; tail -n 4 /tmp/cf8c-closing-r1/last.out; echo "exit $rc"; }
run .venv/bin/python tools/check_pages.py --unit CF8
run .venv/bin/python tools/check_dag.py --unit CF8
run .venv/bin/python tools/check_projects.py --unit CF8
run .venv/bin/python tools/build_site.py --check
run .venv/bin/python tools/verify_refs.py --offline
