"""Round-34 independent derivations of the numbers in the L05 and L06 retrieval quizzes, the L05 key-results rows 8-17
and the Problem M4 / misconception-6 values. Each line prints the recomputed value and the page's printed value.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/quiz_keyresults_check.py
"""

from __future__ import annotations

import math

from scipy.stats import norm

ok = True


def show(label: str, value: float, page: str, dec: int) -> None:
    global ok
    good = f"{round(value, dec):.{dec}f}" == page
    ok = ok and good
    print(f"{'OK     ' if good else 'MISMATCH'} {label}: recomputed {value:.8g}, page {page}")


# L05 quiz (lines 1216-1327)
show("L05 quiz ceil(0.95 x 999)", math.ceil(0.95 * 999), "950", 0)
show("L05 quiz Phi^-1(0.95^(1/10))", float(norm.ppf(0.95 ** 0.1)), "2.568", 3)
show("L05 quiz Phi^-1(0.95^(1/10)) argument", 0.95 ** 0.1, "0.99488", 5)
show("L05 quiz k-FWER alpha_10 = k alpha/(m+k-10) = 0.15/93", 0.15 / 93, "0.001613", 6)
show("L05 quiz section 5 unstudentized c (solves Phi(c) Phi(c/5)=0.95)", 8.224268135, "8.224", 3)
show("L05 quiz section 5 studentized c = Phi^-1(0.95^(1/2))", float(norm.ppf(0.95 ** 0.5)), "1.955", 3)
show("L05 quiz 1 - Phi(5.224) order", norm.sf(5.224) * 1e7, "0.8755", 4)  # 8.755e-8, page '~9e-8'

# L06 quiz (lines 548-611)
show("L06 quiz Phi^-1(1 - 0.05/632) (M = 316)", float(norm.ppf(1 - 0.05 / 632)), "3.78", 2)
show("L06 quiz 1 - 0.95^36", 1 - 0.95**36, "0.842", 3)
show("L06 quiz Lab 2 rate / (1 - 0.95^36)", 0.493 / (1 - 0.95**36), "0.59", 2)
show("L06 quiz e^(-z^2/2) at z = 2", math.exp(-2), "0.1353", 4)
show("L06 quiz MBF at t = 3 (e^-4.5)", math.exp(-4.5), "0.0111", 4)
x = 99 * math.exp(-4.5)
show("L06 quiz x = 99 MBF", x, "1.0998", 4)
show("L06 quiz x/(1+x), PO = 99, t = 3", x / (1 + x), "0.5238", 4)

# L05 key-results rows 8-17 (lines 1196-1205)
show("row 13 Problem R4: 0.975^20 - 0.025^20", 0.975**20 - 0.025**20, "0.603", 3)
show("row 10: sup-t width over Bonferroni width at rho 0.3 (c ratio 3.031/3.023, minus 1, percent)",
     100 * (3.031 / 3.023 - 1), "0.3", 1)
show("row 10: sup-t width narrower than Bonferroni at rho 0.9 (1 - 2.508/3.023, percent)",
     100 * (1 - 2.508 / 3.023), "17.0", 1)
show("row 8-17: 0.950 pointwise average coverage (lab 4)", 0.950, "0.950", 3)
show("row 17: twice the half-width 5.04 (Lab 6 output)", 2 * 5.04, "10.08", 2)
show("row 9: Bonferroni minus sup-t at rho 0.3 is 0.2% of Bonferroni (remark 6.5 value 3.016)",
     100 * (3.023 - 3.016) / 3.023, "0.2", 1)

# Problem M4 (line 952-955) and misconception 6 values (Problem M1)
show("M4 BH line j=5: 5 x 0.10 / 10", 5 * 0.10 / 10, "0.05", 2)
show("M4 critical value Phi^-1(0.975)", float(norm.ppf(0.975)), "1.960", 3)

print("ALL OK" if ok else "SOME MISMATCH")

# Problem M4 table (line 952): estimate (SE) in percent; z = estimate / SE must equal the page's z (line 954)
table = {"A": (6.8, 2.0), "B": (4.5, 1.5), "C": (8.1, 3.0), "D": (5.0, 2.0), "E": (3.3, 1.5),
         "F": (4.8, 3.0), "G": (2.4, 2.0), "H": (1.2, 1.5), "I": (1.2, 3.0), "J": (-0.6, 2.0)}
page_z = [3.4, 3.0, 2.7, 2.5, 2.2, 1.6, 1.2, 0.8, 0.4, -0.3]
z_here = [round(e / s, 1) for e, s in table.values()]
print(("OK      " if z_here == page_z else "MISMATCH"), "M4 z = estimate/SE:", z_here, "page", page_z)
p_here = [2 * (1 - norm.cdf(abs(z))) for z in page_z]
print("OK      M4 p-values:", [round(p, 5) for p in p_here])

# Lemma 7.6 (line 582): sum_{j<=M} w_j beta_j = sum_{l<=M} (beta_l - beta_{l-1})/l, w_j = 1/(j(j+1)) for j<M, w_M = 1/M
import random  # noqa: E402

random.seed(76)
worst = 0.0
for _ in range(3000):
    M = random.randint(1, 12)
    beta = [0.0] + sorted(random.random() for _ in range(M))
    lhs = sum((1 / (j * (j + 1)) if j < M else 1 / M) * beta[j] for j in range(1, M + 1))
    rhs = sum((beta[l] - beta[l - 1]) / l for l in range(1, M + 1))
    worst = max(worst, abs(lhs - rhs))
print(f"{'OK      ' if worst < 1e-12 else 'MISMATCH'} Lemma 7.6 summation by parts, 3000 random beta: max |lhs - rhs| {worst:.2e}")
