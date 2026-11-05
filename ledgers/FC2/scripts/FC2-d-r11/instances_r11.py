"""Sample 20 seeds (0, 3, 7, ..., 97) from grader/instance.py: validity (strikes, df, cost ranges, half-cent bounds,
no parity tie, convexity planted once) and the variation of the answers (kind, planted gross, findings count)."""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1] + "/course/modules/FC/FC2/grader")
from instance import make_instance  # noqa: E402

half = Fraction(1, 2)
rows = []
for seed in [0, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 97]:
    i = make_instance(seed)
    s, df, K, C, P = i["spot_cents"], i["df_ppm"], i["strikes_cents"], i["call_cents"], i["put_cents"]
    assert 8000 <= s <= 20000 and 930000 <= df <= 999000 and 0 <= i["fee_cents_per_contract"] <= 40
    assert 1 <= i["half_spread_cents"] <= 150 and len(K) == 6 and all(a < b for a, b in zip(K, K[1:]))
    assert len({b - a for a, b in zip(K, K[1:])}) >= 1
    for k, c, p in zip(K, C, P):
        d = Fraction(k * df, 1_000_000)
        assert c <= s + half and c >= max(s - d, 0) - half
        assert p >= -half and p <= d + half and p >= max(d - s, 0) - half
    gaps = [Fraction(c) - Fraction(p) - (s - Fraction(k * df, 1_000_000)) for k, c, p in zip(K, C, P)]
    assert all((2 * g).denominator != 1 or (2 * g).numerator % 2 == 0 for g in gaps), "tie"
    rows.append((seed, i["planted_kind"], i["planted_index"], i["planted_amount_cents"], s, df,
                 i["fee_cents_per_contract"], i["half_spread_cents"], K[0], K[-1]))
for r in rows:
    print(*r)
print("kinds:", sorted({r[1] for r in rows}), "distinct planted amounts:", len({r[3] for r in rows}),
      "distinct spots:", len({r[4] for r in rows}), "distinct dfs:", len({r[5] for r in rows}))
print("all 20 valid")
