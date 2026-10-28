import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
muts = {
 "c17_L06_01_population_sd_for_se": ("se_n = sd_n / math.sqrt(n)", "se_n = statistics.pstdev(sample) / math.sqrt(n)"),
 "c17_L06_02_quantile_rank_floor_plus_one": ("rank = max(1, math.ceil(p * len(sorted_values)))", "rank = max(1, int(p * len(sorted_values)) + 1)"),
 "c17_L06_03_discount_exponent_off_by_one": ("x / (1.0 + RATE) ** (t + 1)", "x / (1.0 + RATE) ** t"),
 "c17_L06_04_share_counts_zero_npv_as_negative": ("if x < 0) / N_MAX", "if x <= 0) / N_MAX"),
 "c17_L06_05_se_divides_by_n_minus_one": ("se_n = sd_n / math.sqrt(n)", "se_n = sd_n / math.sqrt(n - 1)"),
}
for name,(a,b) in muts.items():
    assert src.count(a) == 1, (name, src.count(a))
    pathlib.Path(sys.argv[2], name + ".py").write_text(src.replace(a, b))
    print("wrote", name)
