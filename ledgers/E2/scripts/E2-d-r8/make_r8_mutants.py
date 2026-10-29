import pathlib, sys
ref = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
subs = {
 "r8_m1_uniform_pays_lowest_winning_bid": ("clearing = bids[order[units]]", "clearing = bids[order[units - 1]]"),
 "r8_m2_discriminatory_pays_clearing": ("result[i] = clearing if format == \"uniform\" else bids[i]", "result[i] = clearing"),
 "r8_m3_round_half_down": ("return math.floor(exact + Fraction(1, 2))", "return math.ceil(exact - Fraction(1, 2))"),
 "r8_m4_units_upper_bound_inclusive": ("not 1 <= units < bidders", "not 1 <= units <= bidders"),
 "r8_m5_efficiency_best_from_bids": ("best = sum(sorted(values, reverse=True)[:units])", "best = sum(values[i] for i in _ranking(bids)[:units])"),
 "r8_m6_revenue_sums_winning_bids": ("return sum(payments(format, bids, units))", "return sum(b for b, p in zip(bids, payments(format, bids, units)) if p)"),
 "r8_m7_float_clearing": ("result[i] = clearing if format == \"uniform\" else bids[i]", "result[i] = float(clearing) if format == \"uniform\" else bids[i]"),
}
for name, (old, new) in subs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    (out / f"{name}.py").write_text(ref.replace(old, new))
# correct alternative: stable reverse sort on bids (ties keep lower index first)
alt = ref.replace("return sorted(range(len(bids)), key=lambda i: (-bids[i], i))",
                  "return sorted(range(len(bids)), key=lambda i: bids[i], reverse=True)")
assert alt != ref
(out / "r8_alt_stable_reverse_sort.py").write_text(alt)
print("written", len(subs) + 1)
