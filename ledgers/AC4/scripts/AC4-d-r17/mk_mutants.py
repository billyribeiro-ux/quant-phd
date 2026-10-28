"""Write lab-level student-error mutants of the L07 and L08 twins; each is a one-line change to the twin."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
L07 = (root / "tests/labs/AC4/lab-AC4-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/AC4/lab-AC4-L08-1.py").read_text(encoding="utf-8")
muts = {
    "r17_L07_m01_displaced_ignores_external.py": (L07, "return max(0, c.q + c.external - c.capacity)",
                                                  "return max(0, c.q - c.capacity)"),
    "r17_L07_m02_floor_no_division_by_q.py": (L07, "return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v), c.q)",
                                              "return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v))"),
    "r17_L07_m03_strict_nonempty.py": (L07, "empty = [c for c in fits if t_min(c) > t_max(c)]",
                                       "empty = [c for c in fits if t_min(c) >= t_max(c)]"),
    "r17_L07_m04_buyer_gain_sign.py": (L07, "return c.q * (Fraction(c.r_net) - t)",
                                       "return c.q * (t - Fraction(c.r_net))"),
    "r17_L07_m05_firm_surplus_uses_price.py": (L07, "return c.q * (c.r_net - c.v) - displaced(c) * (c.p_m - c.v)",
                                               "return c.q * (c.r_net - c.v) - displaced(c) * (c.p_m - c.v) + c.v"),
    "r17_L08_m01_eva_no_tax.py": (L08, "nopat = Fraction(d.oi) * (10_000 - TAX_BP) / 10_000",
                                  "nopat = Fraction(d.oi)"),
    "r17_L08_m02_ratio_ge_strict.py": (L08, "sign_ok = [(residual_income(d) >= 0) == (return_ratio(d) >= Fraction(RATE_BP, 10_000)) for d in divisions]",
                                       "sign_ok = [(residual_income(d) > 0) == (return_ratio(d) > Fraction(RATE_BP, 10_000)) for d in divisions]"),
    "r17_L08_m03_capitalized_no_amortization_credit.py": (L08, "return replace(d, invested=d.invested + SPEND - first_year, oi=d.oi + SPEND - first_year)",
                                                          "return replace(d, invested=d.invested + SPEND, oi=d.oi + SPEND)"),
    "r17_L08_m04_discord_ignores_ties.py": (L08, "if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:",
                                            "if (by_ri > 0) != (by_ratio > 0):"),
}
for name, (src, old, new) in muts.items():
    assert src.count(old) == 1, (name, src.count(old))
    out = name and src.replace(old, new, 1)
    (dst / name).write_text(out, encoding="utf-8")
    print("wrote", name)
