"""Independent recomputation for AC2 L05-L06 round 2 (verifier-written; does not import the lab twin).

Re-implements the L05 generator from its written spec (quintile sort, long low / short high, t with ddof=1),
reproduces each printed value of the lab, then checks the lesson's explanation of the z-gap gap
(-2.7937 printed vs -2.7996 analytic) against the finite-N expectation, and recomputes Prop 2.3 and E1-E3, R1.
Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L05-L06-r2/recompute_l05.py
"""
import math

import numpy as np

NF, NM, SIG, BASE, BETA, NS, Q = 500, 120, 0.08, 0.005, -0.0008, 200, 100


def phi(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def Phiinv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def one(seed, beta):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((NM, NF))
    e = rng.standard_normal((NM, NF))
    r = BASE + beta * z + SIG * e
    spreads = np.empty(NM)
    gaps = np.empty(NM)
    for t in range(NM):
        o = np.argsort(z[t], kind="stable")
        lo, hi = o[:Q], o[-Q:]
        spreads[t] = r[t, lo].mean() - r[t, hi].mean()
        gaps[t] = z[t, lo].mean() - z[t, hi].mean()
    return spreads, gaps


def tstat(x):
    return x.mean() / (x.std(ddof=1) / math.sqrt(x.size))


def main():
    null_t, eff_t, eff_m, gaps = [], [], [], []
    for s in range(NS):
        s0, _ = one(s, 0.0)
        s1, g = one(s, BETA)
        null_t.append(tstat(s0))
        eff_t.append(tstat(s1))
        eff_m.append(s1.mean())
        gaps.append(g.mean())
    null_t, eff_t, eff_m, gaps = map(np.array, (null_t, eff_t, eff_m, gaps))
    planted = BETA * gaps.mean()
    sd_th = SIG * math.sqrt(2 / Q)
    print("mean_z_gap_simulated %.4f" % gaps.mean())
    print("planted_monthly_spread %.5f" % planted)
    print("spread_sd_theory %.5f" % sd_th)
    print("expected_t_at_planted %.3f" % (planted / (sd_th / math.sqrt(NM))))
    print("recovered_mean_monthly_spread %.5f" % eff_m.mean())
    print("null_mean_t %.3f null_sd_t %.3f" % (null_t.mean(), null_t.std(ddof=1)))
    print("null_false_positive_rate %.3f" % np.mean(np.abs(null_t) > 1.96))
    print("effect_rejection_rate_power %.3f" % np.mean(np.abs(eff_t) > 1.96))
    print("effect_median_t %.3f" % np.median(eff_t))
    print("seed0_spread_mean %.5f seed0_t %.3f" % (eff_m[0], eff_t[0]))
    # Prop 2.3 analytic gap
    q = Phiinv(0.2)
    print("Prop2.3 q %.6f phi(q) %.6f gap %.6f" % (q, phi(q), -2 * phi(q) / 0.2))
    # Explanation test for -2.7937 vs -2.7996: finite-N expectation of the sorted gap
    big = np.array([one(10_000 + s, 0.0)[1].mean() for s in range(2000)])
    print("finite-N gap mean over 2000 seeds (beta 0) %.4f se %.4f" % (big.mean(), big.std(ddof=1) / math.sqrt(big.size)))
    print("lab gap minus analytic %.4f; in SE units of the 2000-seed mean %.2f" % (gaps.mean() + 2.799619, (gaps.mean() + 2.799619) / (big.std(ddof=1) / math.sqrt(big.size))))
    # Hand calculations in the lesson
    print("E2 spread sd", round(0.08 * math.sqrt(2 / 100), 5), "t", round(0.0022350 / (0.01131 / math.sqrt(120)), 3))
    print("E3 z seed0", round((0.00075 - 0.00223) / (0.01131 / math.sqrt(120)), 3))
    print("E1 se", round(math.sqrt(0.05 * 0.95 / 200), 5), "z", round(0.010 / math.sqrt(0.05 * 0.95 / 200), 3))
    print("R1 T", round(2000 * 0 + ((1.96 + Phiinv(0.8)) * 0.01131 / 0.0022350) ** 2, 1))
    print("M3 t", round(0.0020 / (0.0100 / math.sqrt(120)), 4), "se", round(0.0100 / math.sqrt(120), 6))
    print("M2 compound", round(1.008 ** 12 - 1, 5))
    print("null rate z", round((0.060 - 0.05) / math.sqrt(0.05 * 0.95 / 200), 3))
    print("standard error of 120-month mean spread", round(0.01131 / math.sqrt(120), 6))


if __name__ == "__main__":
    main()
