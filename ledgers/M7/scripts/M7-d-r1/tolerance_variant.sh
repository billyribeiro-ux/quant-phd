#!/bin/sh
# Start-portfolio tolerance check: the reference with TOL 1e-7 (the page states 1e-9) run through the suite on seeds 0-9.
# Usage: sh ledgers/M7/scripts/M7-d-r1/tolerance_variant.sh <checkout-root> <scratch-dir>
set -e
root="$1"; scratch="$2"
mkdir -p "$scratch"
cp "$root/course/modules/M/M7/grader/instance.py" "$root/course/modules/M/M7/grader/test_project.py" "$scratch/"
sed 's/^TOL = Fraction(1, 10\*\*9)/TOL = Fraction(1, 10**7)/' "$root/course/modules/M/M7/grader/reference.py" > "$scratch/constrained_allocator.py"
cd "$scratch"
fails=0
for s in 0 1 2 3 4 5 6 7 8 9; do
  QF_SEED=$s "$root/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1 || fails=$((fails+1))
done
echo "tolerance 1e-7 variant: seeds failing of 10 = $fails"
