#!/bin/sh
# Byte-identity of every slice-b subject between the base pin dde0486b and HEAD.
cd /Users/billyribeiro/.fanout/wt/verifyF31-LX1-b || exit 1
BASE=dde0486b
for p in course/modules/LX/LX1/L01.html course/modules/LX/LX1/L03.html course/modules/LX/LX1/L04.html \
  course/modules/LX/LX1/cards.json course/modules/LX/LX1/index.html course/modules/LX/LX1/project.html \
  tests/labs/LX1 plans/LX1-build-plan.md plans/LX1-open-items.md plans/KNOWN-ISSUES.md \
  references tools curriculum notation course/assets/data course/concepts.html course/index.html \
  tools/data_sources.yaml tests/test_labs.py tests/test_lx1_project_lab3.py; do
  if git diff --quiet $BASE HEAD -- "$p"; then echo "IDENTICAL $p"; else echo "CHANGED   $p"; fi
done
echo "--- FINAL-ARCHITECT-RULINGS hunks:"; git diff -U0 $BASE HEAD -- plans/FINAL-ARCHITECT-RULINGS.md | grep '^@@'
echo "--- rulings 14,16,26 bytes (sha1 of line ranges at base vs HEAD):"
for r in "32,37" "38,41" "74,80"; do
  a=$(git show $BASE:plans/FINAL-ARCHITECT-RULINGS.md | sed -n "${r}p" | shasum | cut -c1-12)
  b=$(git show HEAD:plans/FINAL-ARCHITECT-RULINGS.md | sed -n "${r}p" | shasum | cut -c1-12)
  echo "lines $r base=$a head=$b"
done
echo "--- all changed non-ledger paths touching LX1 or shared gates:"
git diff --name-only $BASE HEAD | grep -v '^ledgers/' | grep -E 'LX1|LX/|tools/|notation|references/|curriculum|course/assets|concepts|index.html|CURRICULUM|\.yaml|requirements|pyproject' || echo none
