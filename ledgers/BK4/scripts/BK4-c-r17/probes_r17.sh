#!/bin/bash
# Round 17 (BK4 slice c) probes on the pin. Usage: probes_r17.sh <checkout-root>
ROOT="$1"; S="$ROOT/ledgers/BK4/scripts/BK4-c-r17"; G="$ROOT/course/modules/BK/BK4/grader"; PY="$ROOT/.venv/bin/python"
O="$S/out"; mkdir -p "$O"
# P1: collect-only count on the reference (scratch copy; the suite imports clearing_house beside it)
W=$(mktemp -d /tmp/bk4c_r17_collect.XXXXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/reference.py" "$W/clearing_house.py"
(cd "$W" && "$PY" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py > "$O/P1_collect_only.txt" 2>&1; echo "exit=$?" >> "$O/P1_collect_only.txt")
rm -rf "$W"
# P2: the failure text of the float-index mutant (r12b) and of the r16 mutant set, seed 0 and seed 3
for m in r12b_sizing_index_float; do
  W=$(mktemp -d /tmp/bk4c_r17_p2.XXXXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$ROOT/ledgers/BK4/mutants/$m.py" "$W/clearing_house.py"
  (cd "$W" && QF_SEED=0 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$O/P2_$m.txt" 2>&1; echo "exit=$?" >> "$O/P2_$m.txt")
  rm -rf "$W"
done
# P3: a student module that raises an unexpected exception with arguments in its message (not a named refusal),
# to test the page sentence "When your code raises an exception, pytest also prints that exception and the arguments of your function."
W=$(mktemp -d /tmp/bk4c_r17_p3.XXXXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"
cat > "$W/clearing_house.py" <<'PYEOF'
from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict
    uncovered_cents: int


def waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents):
    raise KeyError(f"probe-secret-{loss_cents}")


def margin_for_cover(losses_cents, target_bps):
    raise KeyError(f"probe-margin-secret-{target_bps}")


def cover_bps(losses_cents, margin_cents):
    raise KeyError(f"probe-cover-secret-{margin_cents}")
PYEOF
(cd "$W" && QF_SEED=0 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$O/P3_raises_with_args.txt" 2>&1; echo "exit=$?" >> "$O/P3_raises_with_args.txt")
rm -rf "$W"
# P4: starter (all NotImplementedError) under the page's local command, seed 0
W=$(mktemp -d /tmp/bk4c_r17_p4.XXXXXX); cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/starter.py" "$W/clearing_house.py"
(cd "$W" && QF_SEED=0 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$O/P4_starter_seed0.txt" 2>&1; echo "exit=$?" >> "$O/P4_starter_seed0.txt")
rm -rf "$W"
echo probes-done
