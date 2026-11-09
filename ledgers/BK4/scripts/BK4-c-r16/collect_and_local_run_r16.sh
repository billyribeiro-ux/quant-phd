#!/bin/bash
# Round-16 verifier, slice c. (1) collect-only count on the reference in a scratch copy (the suite imports
# clearing_house, which exists only beside the suite at run time); (2) the page's local command (project.html :399)
# run with QF_SEED=3 against each named candidate, output kept under out/. Usage: collect_and_local_run_r16.sh <checkout-root>
ROOT="$1"; S="$ROOT/ledgers/BK4/scripts/BK4-c-r16"; G="$ROOT/course/modules/BK/BK4/grader"; PY="$ROOT/.venv/bin/python"
W=$(mktemp -d /tmp/bk4c_r16_collect.XXXXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/reference.py" "$W/clearing_house.py"
(cd "$W" && "$PY" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py > "$S/out/collect_only.txt" 2>&1; echo "exit=$?" >> "$S/out/collect_only.txt")
(cd "$W" && QF_SEED=0 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$S/out/reference_seed0.txt" 2>&1; echo "exit=$?" >> "$S/out/reference_seed0.txt")
rm -rf "$W"
for m in r16a_target_message_omits_target_bps r16c_default_fund_ignores_the_margin_already_paid r16e_cover_sorts_the_callers_list_in_place r15b_default_fund_capped_at_full_loss; do
  W=$(mktemp -d /tmp/bk4c_r16_local.XXXXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$ROOT/ledgers/BK4/mutants/$m.py" "$W/clearing_house.py"
  (cd "$W" && QF_SEED=3 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$S/out/local_run_$m.txt" 2>&1; echo "exit=$?" >> "$S/out/local_run_$m.txt")
  rm -rf "$W"
done
echo done
