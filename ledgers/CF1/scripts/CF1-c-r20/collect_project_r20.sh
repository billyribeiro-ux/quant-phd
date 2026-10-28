#!/bin/sh
# Round 20: collect-only count of the CF1 project grader (reference copied as capbudget.py, as the grader docstring requires).
# Usage: collect_project_r20.sh <checkout> <scratch>
CK=$1; S=$2; P=$CK/.venv/bin/python
rm -rf "$S" && mkdir -p "$S" && cp "$CK"/course/modules/CF/CF1/grader/* "$S"/ && cp "$S"/reference.py "$S"/capbudget.py
cd "$S" && "$P" -I -m pytest --collect-only -q test_project.py 2>&1 | tail -1
