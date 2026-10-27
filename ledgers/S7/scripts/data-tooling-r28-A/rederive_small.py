"""Round-28 part A: small re-derivations used by the decisions (run from the checkout with -I).

Prints one line per check. Sections: (1) closed forms on the cards (maths-cards-closed-forms), (2) the card V identity
(cards-c066), (3) card grade counts (cards-grade-key-empirical), (4) SIMULATED labels in the figure captions
(figures-simulated-labels), read from the lesson HTML.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
from scipy import stats  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[4]

print("(1) closed forms")
print("Phi^-1(0.95^(1/10)) =", round(float(stats.norm.ppf(0.95 ** 0.1)), 5), "-> card c049 says 2.568")
print("0.975^20 - 0.025^20 =", round(0.975 ** 20 - 0.025 ** 20, 6), "-> card c119 says 0.603")
print("Phi^-1(1 - 0.05/40) =", round(float(stats.norm.ppf(1 - 0.05 / 40)), 5), "-> card c173 says 3.023")
print("Phi^-1((1 + 0.95^(1/20))/2) =", round(float(stats.norm.ppf((1 + 0.95 ** (1 / 20)) / 2)), 5), "-> card c173 says 3.016")
print("FDR bound gamma = 0.10/0.2 =", 0.10 / 0.2, "-> card c169 says 0.5")
for n in (2, 3, 5, 10):
    print(f"floor((N+1)/2)/N, N={n}: {math.floor((n + 1) / 2) / n}")
c = 8.224
print("Phi(c)Phi(c/5) at c=8.224:", round(float(stats.norm.cdf(c) * stats.norm.cdf(c / 5)), 6), "-> card c200 says 0.95 at c=8.224")
print("1 - Phi(5.224) =", float(stats.norm.sf(5.224)), "< 1e-7:", float(stats.norm.sf(5.224)) < 1e-7)
root = float(__import__("scipy.optimize", fromlist=["brentq"]).brentq(lambda x: stats.norm.cdf(x) * stats.norm.cdf(x / 5) - 0.95, 5, 12))
print("root of Phi(c)Phi(c/5)=0.95:", round(root, 4), "-> card c200 says 8.224")

print("(2) card c066: V = Var of sqrt(T) SR-hat (delta method), algebra of the printed decomposition")
rng = np.random.default_rng(66)
sr, g3, g4 = rng.uniform(-2, 2, 200_000), rng.uniform(-3, 3, 200_000), rng.uniform(1, 12, 200_000)
v = 1 + sr**2 / 2 - g3 * sr + (g4 - 3) / 4 * sr**2
decomp = (1 + sr**2 / 2) + (-g3 * sr + (g4 - 3) / 4 * sr**2)
print("max |V - decomposition| =", float(np.max(np.abs(v - decomp))))
pos = (sr > 0) & (g3 < 0) & (g4 >= 3)
print("draws with SR>0, gamma3<0, gamma4>=3:", int(pos.sum()), "of which V > 1+SR^2/2:", int(np.sum(v[pos] > 1 + sr[pos] ** 2 / 2)))

print("(3) card grades in cards.json")
cards = json.loads((ROOT / "course/modules/S/S7/cards.json").read_text(encoding="utf-8"))
cards = cards if isinstance(cards, list) else cards.get("cards", cards)
grades = [str(x.get("grade", "")) if isinstance(x, dict) else "" for x in cards]
print("cards:", len(grades), "T:", grades.count("T"), "C:", grades.count("C"), "B:", grades.count("B"), "no grade:", len(grades) - sum(grades.count(g) for g in "TCB"))

print("(4) SIMULATED labels in the figure captions (course/modules/S/S7/*.html)")
for page, lines in (("L05.html", (117, 294)), ("L08.html", (130,))):
    text = (ROOT / "course/modules/S/S7" / page).read_text(encoding="utf-8").splitlines()
    for n in lines:
        line = text[n - 1]
        print(f"{page}:{n} simulated-label={'simulated-label' in line and 'SIMULATED' in line}  {line.strip()[:110]}")
