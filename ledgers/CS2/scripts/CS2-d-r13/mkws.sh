#!/bin/bash
# usage: mkws.sh <solution.py> <outdir>  -- builds a grader workspace like tools/run_graders.py
set -e
G=/Users/billyribeiro/.fanout/wt/verifyB13-CS2-d/course/modules/CS/CS2/grader
rm -rf "$2"; mkdir -p "$2"
cp "$G/test_project.py" "$G/instance.py" "$2/"
cp "$1" "$2/streamstats.py"
