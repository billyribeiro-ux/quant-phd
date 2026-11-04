"""Round-6 alternative correct implementations for CS2 slice d (VERIFIER_RULES 2.6 / plan 4.1 rule 8).
Each alternative is a complete module written next to this script's alts_v6 folder. Run: python3 v6_make_alts.py <root>"""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
outdir = root / "ledgers/CS2/scripts/CS2-d-r6/alts_v6"


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"anchor not unique or missing: {old[:70]!r}"
    return text.replace(old, new)


def welford_block(src: str, new_cls: str) -> str:
    start = src.index("class WelfordAccumulator:")
    end = src.index("class RollingMinMax:")
    return src[:start] + new_cls + "\n\n" + src[end:]


# B: delta-squared M2 form, M2 += delta * delta * (n - 1) / n, mean updated after
B_CLS = '''class WelfordAccumulator:
    """Welford with the delta-squared form of the M2 update, M2 += delta^2 (n - 1) / n."""

    def __init__(self) -> None:
        self._n = 0
        self._mean = 0.0
        self._m2 = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._n += 1
        delta = x - self._mean
        self._m2 += delta * delta * (self._n - 1) / self._n
        self._mean += delta / self._n

    @property
    def count(self) -> int:
        return self._n

    def mean(self) -> float:
        if self._n == 0:
            raise ValueError("the mean is undefined before the first value")
        return self._mean

    def variance(self, ddof: int = 1) -> float:
        if self._n == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 0:
            return self._m2 / self._n
        if ddof == 1:
            if self._n < 2:
                raise ValueError("the sample variance needs at least two values")
            return self._m2 / (self._n - 1)
        raise TypeError("ddof must be 0 or 1")
'''
b = welford_block(ref, B_CLS)
b = '"""Alternative B (correct): reference with the delta-squared Welford form M2 += delta^2 (n-1)/n."""' + b[b.index('"""', 3) + 3:]
(outdir / "alt_v6_b_delta_squared_welford.py").write_text(b, encoding="utf-8")

# C: rolling min/max whose deques keep TIES (pop only strictly worse values); different internal layout
c = replace_once(ref, "        while self._mins and self._mins[-1][1] >= x:", "        while self._mins and self._mins[-1][1] > x:")
c = replace_once(c, "        while self._maxs and self._maxs[-1][1] <= x:", "        while self._maxs and self._maxs[-1][1] < x:")
c = '"""Alternative C (correct): reference with the deques keeping equal values (pop only strictly worse values)."""' + c[c.index('"""', 3) + 3:]
(outdir / "alt_v6_c_rolling_keeps_ties.py").write_text(c, encoding="utf-8")

# D: sketch that never compresses (stores every value as a tuple with g = 1, delta = 0); exact, zero error
d = replace_once(ref, "        self._compress()\n", "        pass\n")
d = '"""Alternative D (correct): reference sketch with compression removed, so every value is stored with weight 1."""' + d[d.index('"""', 3) + 3:]
(outdir / "alt_v6_d_sketch_never_compresses.py").write_text(d, encoding="utf-8")

# E: GK-style sketch whose compression cap is the exact 2 epsilon n (a Fraction, no floor, no plus one)
e = replace_once(
    ref,
    "        cap = math.floor(2 * self._exact_epsilon * self._n) + 1\n",
    "        cap = 2 * self._exact_epsilon * self._n\n",
)
e = '"""Alternative E (correct?): reference sketch with the compression cap 2 epsilon n as an exact Fraction, no floor."""' + e[e.index('"""', 3) + 3:]
(outdir / "alt_v6_e_sketch_cap_exact_two_epsilon_n.py").write_text(e, encoding="utf-8")

print("wrote alternatives B, C, D, E (alternative A is alts_v6/alt_v6_a_two_pass_exact_list.py, written by hand)")
