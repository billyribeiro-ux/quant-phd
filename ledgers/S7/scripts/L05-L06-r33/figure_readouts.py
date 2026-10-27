"""Independent Python recomputation of the L05 and L06 figure readouts (round 33, S7 L05-L06 verifier).

L05: a port of stats.js rng (xoshiro128** seeded by splitmix32, Marsaglia polar normal) and of
multitest.js stationaryBootstrap, studentizedBootstrap, upperCritical, stepdown, correlation, used by
figures-L05.js. L06: closed forms and an independent normal CDF (scipy.special.ndtr / ndtri), no JS code.
Run as: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r33/figure_readouts.py
"""

from __future__ import annotations

import math

import numpy as np
from scipy.special import ndtr, ndtri

M32 = 0xFFFFFFFF


def imul(a: int, b: int) -> int:
    return (a * b) & M32


def rotl(x: int, k: int) -> int:
    return ((x << k) | (x >> (32 - k))) & M32


class Rng:
    def __init__(self, seed: int) -> None:
        self.a = seed & M32
        self.s = [self._splitmix() for _ in range(4)]
        self.spare: float | None = None

    def _splitmix(self) -> int:
        self.a = (self.a + 0x9E3779B9) & M32
        t = self.a ^ (self.a >> 16)
        t = imul(t, 0x21F0AAAD)
        t ^= t >> 15
        t = imul(t, 0x735A2D97)
        return (t ^ (t >> 15)) & M32

    def _next(self) -> int:
        s0, s1, s2, s3 = self.s
        result = imul(rotl(imul(s1, 5), 7), 9)
        t = (s1 << 9) & M32
        s2 ^= s0
        s3 ^= s1
        s1 ^= s2
        s0 ^= s3
        s2 ^= t
        s3 = rotl(s3, 11)
        self.s = [s0, s1, s2, s3]
        return result

    def uniform(self) -> float:
        hi = self._next() >> 5
        lo = self._next() >> 6
        return (hi * 67108864 + lo) / 9007199254740992

    def integer(self, n: int) -> int:
        return math.floor(self.uniform() * n)

    def normal(self) -> float:
        if self.spare is not None:
            v = self.spare
            self.spare = None
            return v
        while True:
            u = 2 * self.uniform() - 1
            v = 2 * self.uniform() - 1
            s = u * u + v * v
            if not (s >= 1 or s == 0):
                break
        scale = math.sqrt((-2 * math.log(s)) / s)
        self.spare = v * scale
        return u * scale


def stationary_bootstrap(n: int, mean_block: float, gen: Rng) -> np.ndarray:
    p = 1 / mean_block
    idx = np.zeros(n, dtype=np.int64)
    idx[0] = gen.integer(n)
    for t in range(1, n):
        if gen.uniform() < p:
            idx[t] = gen.integer(n)
        else:
            idx[t] = (idx[t - 1] + 1) % n
    return idx


def upper_critical(values: list[float], alpha: float) -> float:
    s = sorted(values)
    rank = math.ceil((1 - alpha) * len(s))
    return s[min(len(s), max(1, rank)) - 1]


def column_moments(rows: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    T = rows.shape[0]
    mean = rows.sum(axis=0) / T
    sd = np.sqrt(((rows - mean) ** 2).sum(axis=0) / (T - 1))
    return mean, sd


def studentized_bootstrap(d: np.ndarray, draws: list, joint: bool = True) -> tuple[np.ndarray, list[np.ndarray]]:
    T, K = d.shape
    mean, sd = column_moments(d)
    root = math.sqrt(T)
    t = mean / (sd / root)
    boot = []
    for draw in draws:
        if joint:
            rows = d[draw]
        else:
            rows = np.column_stack([d[draw[k], k] for k in range(K)])
        m, s = column_moments(rows)
        constant = [bool(np.all(rows[:, k] == rows[0, k])) for k in range(K)]
        boot.append(np.array([(m[k] - mean[k]) / ((sd[k] if constant[k] else s[k]) / root) for k in range(K)]))
    return t, boot


def stepdown(t_obs: np.ndarray, t_boot: list[np.ndarray], alpha: float) -> dict:
    K = len(t_obs)
    active = list(range(K))
    mask = [False] * K
    steps = []
    while active:
        maxima = [max(row[k] for k in active) for row in t_boot]
        critical = upper_critical(maxima, alpha)
        rejected = [k for k in active if t_obs[k] > critical]
        steps.append({"active": list(active), "critical": critical, "rejected": rejected})
        if not rejected:
            break
        for k in rejected:
            mask[k] = True
        active = [k for k in active if not mask[k]]
    return {"mask": mask, "steps": steps}


T5, K5, GENUINE = 250, 20, 8


def simulate_universe(seed: int) -> np.ndarray:
    g = Rng(seed)
    d = np.zeros((T5, K5))
    for i in range(T5):
        common = g.normal()
        for k in range(K5):
            d[i, k] = math.sqrt(0.3) * common + math.sqrt(0.7) * g.normal() + (0.19 if k < GENUINE else 0)
    return d


def boot_draws(T: int, B: int, mean_block: int, gen: Rng, K: int = 0, joint: bool = True) -> list:
    if joint:
        return [stationary_bootstrap(T, mean_block, gen) for _ in range(B)]
    return [[stationary_bootstrap(T, mean_block, gen) for _ in range(K)] for _ in range(B)]


def study(seed: int) -> dict:
    d = simulate_universe(seed)
    draws = boot_draws(T5, 500, 5, Rng(seed + 1000))
    t, boot = studentized_bootstrap(d, draws, True)
    return {"t": t, "result": stepdown(t, boot, 0.05), "seed": seed}


def stepm_readout(seed: int) -> str:
    s = study(seed)
    res, t = s["result"], s["t"]
    single = len(res["steps"][0]["rejected"])
    total = sum(res["mask"])
    found = sum(1 for k in range(GENUINE) if res["mask"][k])
    parts = [f"step {j + 1}: c = {st['critical']:.3f} over {len(st['active'])}, rejects {len(st['rejected'])}" for j, st in enumerate(res["steps"])]
    return (
        f"Study {seed}: " + "; ".join(parts) + f". Single-step rejects {single}; StepM rejects {total} "
        f"({found} of {GENUINE} true alphas, {total - found} false)"
        + ("; a later step added a rejection." if total > single else "; no later step added one.")
    ), t, res


def joint_vs_independent() -> dict:
    T, rho = 250, 0.8
    g = Rng(77)
    d = np.zeros((T, 10))
    for i in range(T):
        c = g.normal()
        for k in range(10):
            d[i, k] = math.sqrt(rho) * c + math.sqrt(1 - rho) * g.normal()
    _, joint = studentized_bootstrap(d, boot_draws(T, 600, 5, Rng(78), joint=True), True)
    _, indep = studentized_bootstrap(d, boot_draws(T, 600, 5, Rng(79), K=10, joint=False), False)

    def corr(boot: list) -> float:
        x = np.array([r[0] for r in boot])
        y = np.array([r[1] for r in boot])
        return float(np.corrcoef(x, y)[0, 1])

    def crit(boot: list) -> float:
        return upper_critical([float(max(r)) for r in boot], 0.05)

    return {
        "corr_joint": corr(joint),
        "corr_indep": corr(indep),
        "crit_joint": crit(joint),
        "crit_indep": crit(indep),
    }


def l06_readouts() -> dict:
    out: dict = {}
    # hurdle-growth at alpha = 5% (default), and alpha = 1%, 10%
    for alpha in (0.01, 0.05, 0.10):
        hurdle = {m: float(ndtri(1 - alpha / (2 * m))) for m in (1, 10, 100, 1000, 10**6)}
        crossing = math.ceil(alpha / (2 * float(ndtr(-3.0))))
        out[f"hurdle_alpha_{alpha}"] = {"hurdle": hurdle, "crossing": crossing}
    # forking-paths: P(min of K two-sided p <= 0.05) = 1 - integral phi(z) (P(|Z|<=c | z))^K dz, Simpson 1200 steps
    alpha = 0.05
    c = float(ndtri(1 - alpha / 2))
    z = np.linspace(-9, 9, 1201)
    h = 18 / 1200
    w = np.ones_like(z)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    simpson_w = w * h / 3
    phi = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)

    def fpr(K: int, rho: float) -> float:
        if rho == 0:
            return 1 - (1 - alpha) ** K
        a, b = math.sqrt(rho), math.sqrt(1 - rho)
        inside = ndtr((c - a * z) / b) - ndtr((-c - a * z) / b)
        return float(1 - np.sum(simpson_w * phi * inside**K))

    out["fpr_K10"] = {rho: fpr(10, rho) for rho in (0, 0.5, 0.8, 0.95)}
    # bayes-posterior at t = 3 (default) and the p-value
    def post(t: float, pi0: float) -> float:
        odds = pi0 / (1 - pi0)
        mbf = math.exp(-t * t / 2)
        return odds * mbf / (1 + odds * mbf)

    out["bayes_t3"] = {p: post(3.0, p) for p in (0.5, 0.8, 0.95, 0.99)}
    out["p_t3"] = 2 * float(ndtr(-3.0))
    out["mbf_t3"] = math.exp(-4.5)
    return out


if __name__ == "__main__":
    text, t, res = stepm_readout(101)
    print("L05 default study readout (seed 101):")
    print(text)
    print("t (first 4):", [round(float(v), 4) for v in t[:4]], "max t:", round(float(max(t)), 4))
    print("L05 joint vs independent:", joint_vs_independent())
    print("L06:")
    for k, v in l06_readouts().items():
        print(k, v)
