# Recomputes the L04 Lab 1 cumulative check from the printed per-quarter values in L04.html lines 277-284.
import re, sys
rows = {}
txt = open(sys.argv[1], encoding="utf-8").read().splitlines()
for line in txt:
    m = re.match(r"^q(\d) revenue (-?\d+) ni_rule_a (-?\d+) ni_rule_b (-?\d+) cash_change (-?\d+) prepaid_balance_b (-?\d+)", line)
    if m:
        rows[int(m.group(1))] = {k: int(v) for k, v in zip(["rev","a","b","cash","p"], m.group(2,3,4,5,6))}
cum_a = cum_b = 0
for q in sorted(rows):
    cum_a += rows[q]["a"]; cum_b += rows[q]["b"]
    diff = cum_a - cum_b
    print(f"q{q} cumA {cum_a} cumB {cum_b} diff {diff} minus_prepaid {-rows[q]['p']} equal {diff == -rows[q]['p']} prepaid_zero {rows[q]['p']==0}")
