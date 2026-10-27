"""Re-derive the page numbers of the numeric rows R17-numbers-derived-L03/L04, L03-num-P4, L04-num-M4-quiz,
L04-num-E4 and R14-derivations from their stated inputs (standard library, pin 49def2c).
Each line prints the derived value and the value printed in the page, for a direct comparison.
Usage: .venv/bin/python ledgers/S7/scripts/L03-L04-r27/numeric_rows.py
"""

from __future__ import annotations

import math
from statistics import NormalDist

N = NormalDist()
Phi = N.cdf
Phinv = N.inv_cdf


def phi_pdf(x: float) -> float:
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def show(label: str, value: float, printed: str) -> None:
    print(f"{label:58s} derived {value:.6f}   page {printed}")


print("== L03 Problem P4 (Deflated Sharpe ratio), inputs: N = 500, T = 1260 days, B = 0.337, winner 2.261 annualised")
sigma = 1 / math.sqrt(1260)
show("sigma = 1/sqrt(1260)", sigma, "0.028172")
s_x = sigma / math.sqrt(1 - 0.337)
show("s_X = sigma/sqrt(1 - B)", s_x, "0.034599 (0.549 annualised)")
show("s_X annualised x sqrt(252)", s_x * math.sqrt(252), "0.549")
gamma = 0.57722
c500 = (1 - gamma) * Phinv(1 - 1 / 500) + gamma * Phinv(1 - 1 / (500 * math.e))
show("c_500 = (1-g) Phi^-1(1-1/N) + g Phi^-1(1-1/(Ne))", c500, "3.05253 (page: 0.42278 x 2.87816 + 0.57722 x 3.18024)")
show("  page bracket terms 0.42278*2.87816", 0.42278 * 2.87816, "1.21683")
show("  page bracket terms 0.57722*3.18024", 0.57722 * 3.18024, "1.83570")
sr0 = s_x * c500
show("SR_0 = s_X c_500 per day", sr0, "0.10561")
show("SR_0 annualised", sr0 * math.sqrt(252), "1.677")
winner = 2.261 / math.sqrt(252)
show("winner per day 2.261/sqrt(252)", winner, "0.14243")
dsr = Phi(((winner - sr0) * math.sqrt(1259)) / math.sqrt(1 + winner**2 / 2))
show("DSR with s_X (Phi of the page's expression)", dsr, "0.903 (argument 1.300)")
arg = ((winner - sr0) * math.sqrt(1259)) / math.sqrt(1 + winner**2 / 2)
show("  argument", arg, "1.300")
sr0_null = sigma * c500
show("SR_0 with null dispersion sigma", sr0_null, "0.08600 (1.365 annualised)")
show("  annualised", sr0_null * math.sqrt(252), "1.365")
dsr_null = Phi(((winner - sr0_null) * math.sqrt(1259)) / math.sqrt(1 + winner**2 / 2))
show("DSR with sigma (argument 1.992)", dsr_null, "0.977")
show("  argument", ((winner - sr0_null) * math.sqrt(1259)) / math.sqrt(1 + winner**2 / 2), "1.992")

print("\n== L03 Problem M4 (two-group rates at z = 2.5), pi0 = 0.9, f0 = N(0,1), f1 = N(3,1)")
show("phi(2.5)", phi_pdf(2.5), "0.017528")
show("phi(-0.5)", phi_pdf(-0.5), "0.352065")
pi0f0 = 0.9 * phi_pdf(2.5)
pi1f1 = 0.1 * phi_pdf(-0.5)
show("pi0 f0 = 0.9 x 0.017528", pi0f0, "0.015775")
show("pi1 f1 = 0.1 x 0.352065", pi1f1, "0.035207")
show("lfdr(2.5)", pi0f0 / (pi0f0 + pi1f1), "0.309 (quoted in the row as 0.309432)")
S0 = 1 - Phi(2.5)
S1 = 1 - Phi(-0.5)
show("S0(2.5) = 1 - Phi(2.5)", S0, "0.00621")
show("S1(2.5) = 1 - Phi(-0.5)", S1, "0.69146")
show("pi0 S0", 0.9 * S0, "0.005589")
show("pi1 S1", 0.1 * S1, "0.069146")
S = 0.9 * S0 + 0.1 * S1
show("S(z) = pi0 S0 + pi1 S1", S, "0.074735")
show("Fdr(2.5) = pi0 S0 / S", 0.9 * S0 / S, "0.0748")
show("N S0 / R -> S0/S", S0 / S, "0.0831")

print("\n== L04 Problem M4 (Diebold-Mariano by hand), T = 250, dbar = 0.15, g0 = 1.0, g1 = 0.40, g2 = 0.15")
T = 250
dbar = 0.15
show("naive t = sqrt(T) dbar / sqrt(g0)", math.sqrt(T) * dbar, "2.372 (0.15/0.063246)")
show("  sqrt(1/250)", math.sqrt(1 / 250), "0.063246")
show("  two-sided p of 2.372", 2 * (1 - Phi(2.372)), "0.0177")
sig2 = 1 + 2 * ((2 / 3) * 0.40 + (1 / 3) * 0.15)
show("sigma^2_LR (Bartlett, l = 2)", sig2, "1.6333")
se = math.sqrt(sig2 / T)
show("SE of dbar", se, "0.080829")
dm = dbar / se
show("DM = dbar / SE", dm, "1.856")
show("  two-sided p of DM", 2 * (1 - Phi(dm)), "0.0635")
show("  one-sided p of DM", 1 - Phi(dm), "0.0317")
show("  sqrt(sigma^2_LR) = naive-SE factor", math.sqrt(sig2), "1.278")
flat = 1 + 2 * (0.40 + 0.15)
show("flat weights 1 + 2(0.40+0.15)", flat, "2.1")
show("DM with flat weights", dbar / math.sqrt(flat / T), "1.637")

print("\n== L03 Remark 3.5 / L04 Remark 3.5 and E3 (lines 259, 626)")
show("2(1 - Phi(1.96/sqrt3))", 2 * (1 - Phi(1.96 / math.sqrt(3))), "0.258 (0.2578)")
show("1.96/sqrt3", 1.96 / math.sqrt(3), "1.132")
show("1.96/sqrt(1.857)", 1.96 / math.sqrt(1.857), "1.438")
show("2(1 - Phi(1.96/sqrt(1.857)))", 2 * (1 - Phi(1.96 / math.sqrt(1.857))), "0.150")
show("E3 1 - Phi(2.618/5)", 1 - Phi(2.618 / 5), "0.30")

print("\n== L04 Problem E4 (size of normal tests at phi = 0.5, from the printed variance ratios)")
# Rejection probability of a two-sided 5% normal test whose variance estimate is ratio x the true variance.
def size(ratio_est_over_true: float) -> float:
    return 2 * (1 - Phi(1.96 * math.sqrt(ratio_est_over_true)))
TVAR_NW = 2.992  # T Var(mean) in units of gamma(0), printed
TVAR_SB = 2.992
show("test (iii) size: E[sigma^2_LR]=2.502 g0 vs T Var 2.992 g0", size(2.502 / 2.992), "0.073")
show("test (iv)  size: 2.803 g0 vs 2.992 g0", size(2.803 / 2.992), "0.058")
show("test (iii) size at exact mean 2.446", size(2.446 / 2.992), "0.076")
show("test (iv) size at exact mean 2.561", size(2.561 / 2.992), "0.069")
show("test (iv) weight sum 1 + 2 sum_{h=1}^{499} (1-h/500) 0.95^h", 1 + 2 * sum((1 - h / 500) * 0.95**h for h in range(1, 500)), "37.480")
show("test (iii) weight sum 1 + 2 sum_{j=1}^{7} (1-j/8) 0.5^j", 1 + 2 * sum((1 - j / 8) * 0.5**j for j in range(1, 8)), "2.502 (plain, gamma(0) units)")
show("E4 MC SE sqrt(0.05*0.95/2000)", math.sqrt(0.05 * 0.95 / 2000), "0.00487")
for d in (0.060, 0.059, 0.063):
    show(f"  standardised ({d} - 0.05)/SE", (d - 0.05) / math.sqrt(0.05 * 0.95 / 2000), "2.05 / 1.85 / 2.67 (order as the page)")
print("DONE")
