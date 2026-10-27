"""Independent Python recomputation of the L07 and L08 live-figure readouts (round 28 verifier).

Mirrors course/modules/S/S7/figures-L07.js (dsrExplorer) and figures-L08.js (cscvExplorer) from the formulas,
not from the JS. The CSCV history generator is a Python port of stats.js rng() (xoshiro128** seeded by splitmix32,
53-bit uniform, Marsaglia polar normal) so that the SIMULATED histories can be rebuilt without the browser.
Run from the checkout: .venv/bin/python -I <this file> (self-test prints the seed-501 median-history values).
"""

from __future__ import annotations

import math
from statistics import NormalDist

PHI = NormalDist()
GAMMA_E = 0.5772156649015329
M32 = 0xFFFFFFFF
LETTERS = "ABCDEFGH"
S_BLOCKS, BLOCK, N_CONF, VOL = 8, 63, 10, 0.01
TRIALS = [1, 2, 5, 10, 20, 40, 100, 200, 500, 1000]
DAYS = [126, 252, 504, 756, 1260, 2520, 5040]


def expected_max_z(n: int) -> float:
    if n == 1:
        return 0.0
    return (1 - GAMMA_E) * PHI.inv_cdf(1 - 1 / n) + GAMMA_E * PHI.inv_cdf(1 - 1 / (n * math.e))


def benchmark_sharpe(n: int, sd: float) -> float:
    """Formula (3) as figures-L07.js benchmarkSharpe: SR0 = sd * bracket, and 0 for a single trial."""
    if n == 1:
        return 0.0
    return sd * expected_max_z(n)


def se_formula2(sr: float, t: int, skew: float, kurt: float) -> float:
    return math.sqrt((1 - skew * sr + ((kurt - 1) / 4) * sr * sr) / (t - 1))


def l07_readout(sr: float, ti: int, skew: float, kurt: float, ni: int, dispersion: float) -> dict[str, object]:
    """The readout and desc numbers of dsr-explorer for one state; refused when kurt < 1 + skew^2."""
    t, n = DAYS[ti], TRIALS[ni]
    if kurt < 1 + skew * skew:
        return {"refused": True, "bound": f"{1 + skew * skew:.2f}"}
    bracket = 1 - skew * sr + ((kurt - 1) / 4) * sr * sr
    se = se_formula2(sr, t, skew, kurt)
    sr0 = benchmark_sharpe(n, dispersion)
    psr = PHI.cdf(sr / se)
    dsr = PHI.cdf((sr - sr0) / se)
    readout = (
        f"s.e. = √({bracket:.4f}/{t - 1}) = {se:.4f}; PSR(0) = Φ({sr / se:.3f}) = {psr:.3f}; "
        f"SR0 = {sr0:.4f} per day ({sr0 * math.sqrt(252):.2f} annualized) for N = {n}; "
        f"DSR = Φ({(sr - sr0) / se:.3f}) = {dsr:.3f}."
    )
    desc = (
        f"Two normal densities with the standard error {se:.4f} of formula (2): one centred at 0 (the PSR benchmark) "
        f"and one at SR0 = {sr0:.4f}, the expected maximum of {n} null trial{'' if n == 1 else 's'} (the DSR benchmark). "
        f"The area of each to the left of the estimated Sharpe ratio {sr:.3f} is PSR = {psr:.3f} and DSR = {dsr:.3f}."
    )
    return {"refused": False, "readout": readout, "desc": desc, "se": se, "psr": psr, "dsr": dsr, "sr0": sr0}


class Rng:
    """stats.js rng(seed): xoshiro128** with splitmix32 seeding; uniform from two 32-bit draws; Marsaglia polar normal."""

    def __init__(self, seed: int) -> None:
        self.a = seed & M32
        self.s = [self._splitmix() for _ in range(4)]
        self.spare: float | None = None

    def _splitmix(self) -> int:
        self.a = (self.a + 0x9E3779B9) & M32
        t = self.a ^ (self.a >> 16)
        t = (t * 0x21F0AAAD) & M32
        t ^= t >> 15
        t = (t * 0x735A2D97) & M32
        return (t ^ (t >> 15)) & M32

    @staticmethod
    def _rotl(x: int, k: int) -> int:
        return ((x << k) | (x >> (32 - k))) & M32

    def _next(self) -> int:
        s0, s1, s2, s3 = self.s
        result = (self._rotl((s1 * 5) & M32, 7) * 9) & M32
        t = (s1 << 9) & M32
        s2 ^= s0
        s3 ^= s1
        s1 ^= s2
        s0 ^= s3
        s2 ^= t
        s3 = self._rotl(s3, 11)
        self.s = [s0, s1, s2, s3]
        return result

    def uniform(self) -> float:
        hi = self._next() >> 5
        lo = self._next() >> 6
        return (hi * 67108864 + lo) / 9007199254740992

    def normal(self) -> float:
        if self.spare is not None:
            value, self.spare = self.spare, None
            return value
        while True:
            u = 2 * self.uniform() - 1
            v = 2 * self.uniform() - 1
            s = u * u + v * v
            if s < 1 and s != 0:
                break
        scale = math.sqrt(-2 * math.log(s) / s)
        self.spare = v * scale
        return u * scale


def simulate(seed: int, edge: bool) -> list[list[float]]:
    g = Rng(seed)
    return [
        [VOL * (g.normal() + (0.1 if (edge and n == 0) else 0.0)) for n in range(N_CONF)]
        for _ in range(S_BLOCKS * BLOCK)
    ]


def _combinations(n: int, k: int) -> list[tuple[int, ...]]:
    import itertools

    return list(itertools.combinations(range(n), k))


def _sharpe_cols(rows: list[list[float]], n_cols: int) -> list[float]:
    t = len(rows)
    out = []
    for c in range(n_cols):
        m = sum(r[c] for r in rows) / t
        ss = sum((r[c] - m) ** 2 for r in rows)
        out.append(m / math.sqrt(ss / (t - 1)))
    return out


def cscv(matrix: list[list[float]], n_blocks: int) -> dict[str, object]:
    n_cols = len(matrix[0])
    size = len(matrix) // n_blocks
    blocks = [matrix[s * size : (s + 1) * size] for s in range(n_blocks)]
    splits = []
    for in_sample in _combinations(n_blocks, n_blocks // 2):
        out_sample = [s for s in range(n_blocks) if s not in in_sample]
        is_metric = _sharpe_cols([r for s in in_sample for r in blocks[s]], n_cols)
        oos_metric = _sharpe_cols([r for s in out_sample for r in blocks[s]], n_cols)
        best = 0
        for n in range(1, n_cols):
            if is_metric[n] > is_metric[best]:
                best = n
        lower = equal = 0
        for n in range(n_cols):
            if oos_metric[n] < oos_metric[best]:
                lower += 1
            elif n != best and oos_metric[n] == oos_metric[best]:
                equal += 1
        rank = 1 + lower + 0.5 * equal
        omega = rank / (n_cols + 1)
        splits.append(
            {
                "in_sample": in_sample,
                "best": best,
                "rank": rank,
                "omega": omega,
                "logit": math.log(omega / (1 - omega)),
                "oos_metric": oos_metric,
                "is_metric": is_metric,
            }
        )
    logits = [s["logit"] for s in splits]
    pbo = sum(1 for lg in logits if lg <= 0) / len(logits)
    return {"pbo": pbo, "splits": splits}


def l08_readout(seed: int, edge: bool, split_no: int, result: dict[str, object]) -> dict[str, object]:
    splits = result["splits"]
    s = splits[split_no - 1]  # type: ignore[index]
    pbo = result["pbo"]
    prefix = "A median history. " if seed == 501 else ""
    tail = "" if edge else f" (Theorem 4.1 gives E[PBO] = {(math.floor((N_CONF + 1) / 2) / N_CONF):.1f} when nothing works)"
    readout = (
        f"{prefix}Split {split_no}: in-sample blocks {''.join(LETTERS[b] for b in s['in_sample'])}; "  # type: ignore[index]
        f"winner configuration {s['best'] + 1}; out-of-sample rank {s['rank']:g} of {N_CONF}, "  # type: ignore[index]
        f"ω = {s['rank']:g}/{N_CONF + 1} = {s['omega']:.3f}, λ = {s['logit']:.3f}. "  # type: ignore[index]
        f"Over all 70 splits PBO = {pbo:.3f}{tail}."  # type: ignore[operator]
    )
    n_le0 = sum(1 for x in splits if x["logit"] <= 0)  # type: ignore[index,union-attr]
    hist_desc = (
        f"Histogram of the 70 logits λ = ln(ω/(1 − ω)); the {n_le0} at or below zero, where the in-sample winner lands "
        f"at or below the out-of-sample median, give PBO = {pbo:.3f}."  # type: ignore[operator]
    )
    return {"readout": readout, "hist_desc": hist_desc, "split_logit_label": f"λ = {s['logit']:.2f}"}  # type: ignore[index]


if __name__ == "__main__":
    print("seed 501 default (edge off) PBO:", round(cscv(simulate(501, False), 8)["pbo"], 6))  # type: ignore[index]
    print(l08_readout(501, False, 1, cscv(simulate(501, False), 8))["readout"])  # type: ignore[arg-type]
    print(l07_readout(0.09, 3, -1.5, 8.0, 5, 0.03)["readout"])  # type: ignore[index]
