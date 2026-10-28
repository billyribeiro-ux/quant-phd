import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
muts = {
 "r18_L06_06_quantile_zero_based_index": ("return sorted_values[rank - 1]", "return sorted_values[rank]"),
 "r18_L06_07_receipt_range_excludes_high": ("rng.randint(LOW, HIGH)", "rng.randint(LOW, HIGH - 1)"),
 "r18_L06_08_expected_uses_low_plus_high": ("mean_receipt = (LOW + HIGH) / 2.0", "mean_receipt = (LOW + HIGH) / 1.0"),
 "r18_L06_09_quantile_uses_round_not_ceil": ("rank = max(1, math.ceil(p * len(sorted_values)))", "rank = max(1, round(p * len(sorted_values)) + 1)"),
 "r18_L06_10_share_uses_pstdev_style_se": ("se_negative = math.sqrt(negative * (1.0 - negative) / N_MAX)", "se_negative = math.sqrt(negative * (1.0 - negative) / (N_MAX - 1))"),
}
for name,(a,b) in muts.items():
    assert src.count(a) == 1, (name, src.count(a))
    pathlib.Path(sys.argv[2], name + ".py").write_text(src.replace(a, b))
    print("wrote", name)
