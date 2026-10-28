import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
alts = {
 "alt_r18_a_plain_sum_not_fsum": ("math.fsum(sample) / n", "sum(sample) / n"),
 "alt_r18_b_fmean_for_mean": ("mean_n = math.fsum(sample) / n", "mean_n = statistics.fmean(sample)"),
 "alt_r18_c_direct_power_discount": ("x / (1.0 + RATE) ** (t + 1)", "x * (1.0 + RATE) ** -(t + 1)"),
}
for name,(a,b) in alts.items():
    assert src.count(a) == 1, (name, src.count(a))
    pathlib.Path(sys.argv[2], name + ".py").write_text(src.replace(a, b))
    print("wrote", name)
