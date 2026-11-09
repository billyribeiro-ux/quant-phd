"""Round 17: search the (noise volume, cost) plane for inputs where the surviving mutant mutant_v17_02
(b_s without the uninformed term) reports an interior gap that differs from the reference's by more than the
page's stated gap precision (1e-14 relative to max(1, |limit|)), and where the informed fraction differs.
Usage: search_v17_02_gap_diff.py <checkout>"""
import importlib.util as u
import sys

root = sys.argv[1]


def load(path, name):
    spec = u.spec_from_file_location(name, path)
    mod = u.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = load(f"{root}/course/modules/E/E4/grader/reference.py", "ref")
M = load(f"{root}/ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py", "mut")
worst = (0.0, None)
lam_mismatch = []
n = 0
for i in range(120):
    sd = 0.05 + (3.0 - 0.05) * i / 119
    for j in range(120):
        c = 0.4 * j / 119
        a = R.solve_model(sd, c)
        b = M.solve_model(sd, c)
        n += 1
        d = abs(a["indifference_gap"] - b["indifference_gap"])
        if d > worst[0]:
            worst = (d, (sd, c, a["indifference_gap"], b["indifference_gap"], a["informed_fraction"], b["informed_fraction"]))
        if a["informed_fraction"] != b["informed_fraction"] and len(lam_mismatch) < 5:
            lam_mismatch.append((sd, c, a["informed_fraction"], b["informed_fraction"]))
print("cases", n)
print("largest reported-gap difference", worst[0], "at (sd, c, ref gap, mut gap, ref lambda, mut lambda) =", worst[1])
print("cases with a different informed fraction (first 5):", lam_mismatch)
