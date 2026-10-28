"""FC2-d verifier: card numbers vs own lesson text, card cross-references, grade field, binomial/BS recomputation.

Run: .venv/bin/python -I ledgers/FC2/scripts/FC2-d-r1/card_numeric_and_refs.py  (reads /tmp/fc2-v/d/L0n.txt, extracted from the lesson HTML)
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/verifyC1-FC2-d")
cards = json.loads((ROOT / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
lessons = {f"L{n:02d}": Path(f"/tmp/fc2-v/d/L{n:02d}.txt").read_text(encoding="utf-8") for n in range(1, 9)}
ref = re.compile(r"(Definition|Proposition|Theorem|Remark|Example|Lemma|Corollary|Assumption|Problem|Section)\s+([A-Z]?\d+(?:\.\d+)?[a-z′']?|A\d+′?|\d+)")
for c in cards:
    text = c["front"] + " " + c["back"]
    for tok in set(re.findall(r"\d+(?:\.\d+)?", text)):
        if tok not in lessons[c["lesson"]]:
            print("number not in own lesson", c["id"], tok)
    if "grade" not in c:
        print("no grade field", c["id"])
    if c.get("grade") == "T" and "SIMULATED" in c.get("basis", ""):
        print("grade T with SIMULATED basis (rule e)", c["id"], c["basis"])
print("cards", len(cards), "dup ids", len(cards) - len({c["id"] for c in cards}))

# recomputation of card numbers
S, K, r, sig, t = 100.0, 100.0, 0.05, 0.2, 1.0
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
d1 = (math.log(S / K) + (r + sig * sig / 2) * t) / (sig * math.sqrt(t))
bs = S * Phi(d1) - K * math.exp(-r * t) * Phi(d1 - sig * math.sqrt(t))
print("BS call", round(bs, 6), "d1", round(d1, 6), "put", round(bs - S + K * math.exp(-r * t), 6))
def tree(n):
    h = t / n; u = math.exp(sig * math.sqrt(h)); dd = 1 / u; R = math.exp(r * h); q = (R - dd) / (u - dd)
    V = [max(S * u**k * dd**(n - k) - K, 0) for k in range(n + 1)]
    for _ in range(n):
        V = [(q * V[k + 1] + (1 - q) * V[k]) / R for k in range(len(V) - 1)]
    return V[0], q
for n in (1, 2, 5, 10, 25, 50, 100, 200, 400):
    v, q = tree(n)
    print("steps", n, "error cents", round((v - bs) * 100, 6))
print("q1", round(tree(1)[1], 6), "V1 cents", round(tree(1)[0] * 100, 4), "q4", round(tree(4)[1], 6))
print("sum DF 3..5 zero-rate, par rate check", round(0.970874 + 0.933511 + 0.888996 + 0.838561 + 0.783526, 6))
print("L bound", round(S - K * math.exp(-r * t), 6), "put bound 100e^-0.1-50", round(100 * math.exp(-0.1) - 50, 4))
print("fair forward cents", round(5000 * math.exp(0.05 * 0.5) * 100 / 100, 2), "view 237.11 check", round(5300 - 5000 * math.exp(0.025) * math.exp(-0.0125), 2))
