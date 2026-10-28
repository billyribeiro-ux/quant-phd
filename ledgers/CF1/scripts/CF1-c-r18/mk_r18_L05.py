import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
muts = {
 "r18_L05_01_tail_varies_year4": ("tail = (*PROJECT_A[:5], rng.randint(0, 500_000), rng.randint(0, 500_000))", "tail = (*PROJECT_A[:4], rng.randint(0, 500_000), rng.randint(0, 500_000), rng.randint(0, 500_000))"),
 "r18_L05_02_discount_exponent_minus_one": ("f / (1.0 + rate) ** t for t, f in enumerate(flows)", "f / (1.0 + rate) ** (t - 1) for t, f in enumerate(flows)"),
 "r18_L05_03_fraction_over_cumulative": ("return (t - 1) + (-previous) / flows[t]", "return (t - 1) + (-previous) / total"),
 "r18_L05_04_npv_uses_simple_sum": ("return math.fsum(discount(flows, rate))", "return float(sum(flows[:3]))"),
}
for name,(a,b) in muts.items():
    assert src.count(a) == 1, (name, src.count(a))
    pathlib.Path(sys.argv[2], name + ".py").write_text(src.replace(a, b))
    print("wrote", name)
