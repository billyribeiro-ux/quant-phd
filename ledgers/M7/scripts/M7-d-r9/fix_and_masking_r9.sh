#!/bin/bash
# Round 9: evidence for PRJ-R9-01..03. (a) the masking of purity and signature checks in the round-9 suite; (b) the proposed fixes, tried in scratch copies only.
CK=/Users/billyribeiro/.fanout/wt/verifyD9-M7-d
S=$CK/ledgers/M7/scripts/M7-d-r9
M=$CK/ledgers/M7/mutants
G=$CK/course/modules/M/M7/grader
PY=$CK/.venv/bin/python
W=/tmp/m7d-r9/masking; rm -rf $W; mkdir -p $W
echo "== (a) round-9 suite, as delivered"
for m in v9_06_prints_before_refusing_a_non_integer_sector_label v9_07_marks_its_argument_before_refusing_text_in_mu v9_08_allocate_takes_an_optional_second_argument; do
  mkdir -p $W/$m; cp $G/instance.py $G/test_project.py $W/$m/; cp $M/$m.py $W/$m/constrained_allocator.py
  echo -n "$m seed 0: "; (cd $W/$m && QF_SEED=0 $PY -I -m pytest -p no:cacheprovider --assert=plain -W error -q test_project.py 2>&1 | grep -E "passed|failed" | tail -1)
done
mkdir -p $W/boolean; cp $G/instance.py $G/test_project.py $W/boolean/; cp $M/v9_06_prints_before_refusing_a_non_integer_sector_label.py $W/boolean/constrained_allocator.py
echo -n "v9_06 with -k boolean (refusal tests only), seed 0: "; (cd $W/boolean && QF_SEED=0 $PY -I -m pytest -p no:cacheprovider --assert=plain -W error -q -k boolean test_project.py 2>&1 | tail -1)
mkdir -p $W/r8suite; cp $CK/.git/../ledgers/M7/scripts/M7-d-r9/pyodide_durations_r9.mjs /dev/null 2>/dev/null
git -C $CK show 2d755599:course/modules/M/M7/grader/test_project.py > $W/r8suite/test_project.py
cp $G/instance.py $W/r8suite/; cp $M/v9_08_allocate_takes_an_optional_second_argument.py $W/r8suite/constrained_allocator.py
echo -n "round-8 test_project.py (pin 2d755599) on v9_08, seed 0: "; (cd $W/r8suite && QF_SEED=0 $PY -I -m pytest -p no:cacheprovider --assert=plain -W error -q test_project.py 2>&1 | grep -E "FAILED|passed|failed" | tr '\n' ' '); echo
echo "== (b) proposed fixes in scratch copies (the repo is not edited)"
F=$W/fix; mkdir -p $F; cp $G/instance.py $F/
/usr/bin/sed 's/raise AssertionError(/_fail(/g' $G/test_project.py | /usr/bin/sed 's/^def _observed_call(/def _fail(message: str) -> None:\n    pytest.fail(message, pytrace=False)\n\n\ndef _observed_call(/' > $F/test_project.py
for pair in "ref:/tmp/m7d_ref_r9.py" "v9_06:$M/v9_06_prints_before_refusing_a_non_integer_sector_label.py" "v9_07:$M/v9_07_marks_its_argument_before_refusing_text_in_mu.py"; do
  name=${pair%%:*}; src=${pair#*:}; cp $src $F/constrained_allocator.py
  echo -n "pytest.fail variant, $name, seed 0: "; (cd $F && QF_SEED=0 $PY -I -m pytest -p no:cacheprovider --assert=plain -W error -q test_project.py 2>&1 | grep -E "passed|failed" | tail -1)
done
F2=$W/fix2; mkdir -p $F2; cp $G/instance.py $F2/
/usr/bin/sed 's/^    def checked(instance: Any) -> Any:/    @functools.wraps(real)\n    def checked(instance: Any) -> Any:/' $G/test_project.py | /usr/bin/sed 's/^import contextlib$/import contextlib\nimport functools/' > $F2/test_project.py
for pair in "ref:/tmp/m7d_ref_r9.py" "v9_08:$M/v9_08_allocate_takes_an_optional_second_argument.py"; do
  name=${pair%%:*}; src=${pair#*:}; cp $src $F2/constrained_allocator.py
  echo -n "functools.wraps variant, $name, seed 0: "; (cd $F2 && QF_SEED=0 $PY -I -m pytest -p no:cacheprovider --assert=plain -W error -q test_project.py 2>&1 | grep -E "passed|failed" | tail -1)
done
echo DONE
