"""FC2-d r2: instance validity and material difference over seeds 0..49 (uses the reference scanner).
usage: python -I instances_check.py <repo-root>"""
import sys, importlib.util
from fractions import Fraction
root = sys.argv[1]
g = f"{root}/course/modules/FC/FC2/grader"
sys.path.insert(0, g)
import instance as I  # noqa: E402
spec = importlib.util.spec_from_file_location("ref", f"{g}/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
PPM = 1_000_000
seen_answers = {}
kinds = {}
bad = []
for seed in range(50):
    x = I.make_instance(seed)
    s, c, p, k, df = x["strikes_cents"], x["call_cents"], x["put_cents"], x["spot_cents"], x["df_ppm"]
    ok = all(a < b for a, b in zip(s, s[1:])) and 1 <= df <= PPM and s[0] > 0 and len(s) == len(c) == len(p) == 6
    ok &= x["fee_cents_per_contract"] >= 0 and x["half_spread_cents"] >= 0
    sec = [c[j - 1] + c[j + 1] - 2 * c[j] for j in range(1, 5)]
    ok &= all(d >= 0 for d in sec)  # calls convex on an even grid before planting
    gaps = [Fraction(c[i]) - Fraction(p[i]) - (Fraction(k) - Fraction(s[i] * df, PPM)) for i in range(6)]
    res = [abs(g_) for g_ in gaps]
    kind = x["planted_kind"]
    kinds[kind] = kinds.get(kind, 0) + 1
    findings = tuple((r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in ref.scan({
        "spot_cents": k, "df_ppm": df, "strikes_cents": s, "call_cents": c, "put_cents": p,
        "cost": {"fee_cents_per_contract": x["fee_cents_per_contract"], "half_spread_cents": x["half_spread_cents"]}}))
    seen_answers.setdefault(findings, []).append(seed)
    if not ok:
        bad.append(seed)
print("planted kinds over seeds 0-49:", kinds)
print("invalid or non-convex seeds:", bad)
print("distinct findings sets over 50 seeds:", len(seen_answers), "; largest group size:", max(len(v) for v in seen_answers.values()))
print("seeds 0-19 findings counts:", [len(next(f for f, v in seen_answers.items() if sd in v)) for sd in range(20)])
