# Round-2 checks for E1 slice b (L04-L06): card duplicate scan, card-text claims, quiz tolerance, Prop 5.4 multiplier.
import json
from fractions import Fraction as F

ROOT = "/tmp/verifyB2-E1-b"
cards = json.load(open(f"{ROOT}/course/modules/E/E1/cards.json", encoding="utf-8"))
fronts = [c["front"].strip().lower() for c in cards]
backs = [c["back"].strip().lower() for c in cards]
print("cards", len(cards), "duplicate fronts", len(fronts) - len(set(fronts)), "duplicate backs", len(backs) - len(set(backs)))
ids = [c["id"] for c in cards]
print("duplicate ids", len(ids) - len(set(ids)))
for c in cards:
    n = int(c["id"].split("c")[-1])
    if n == 62:
        print("c062 back has 'For linear demand' qualifier:", "For linear demand" in c["back"], "| says 'Unit elasticity maximizes revenue':", "Unit elasticity maximizes revenue" in c["back"])
    if n == 90:
        print("c090 back states unrestricted (d-x)/2:", "the reaction is (d - x)/2" in c["back"])

# Lemma 2.4 is R(x) = max(0, (d-x)/2). Reference case d = 100 and rival x = 120 (x > d):
d = F(100); x = F(120)
print("reaction at x=120 by Lemma 2.4:", max(F(0), (d - x) / 2), "| formula (d-x)/2 gives", (d - x) / 2)

# Proposition 5.4 step, reference monopoly case a=120, b=1, c=20 at p*=70 (Q=a-bp)
a, b, c, p = 120, 1, 20, F(70)
Q = a - b * p; Qp = -b
eps = p * Qp / Q
print("FOC identity (p-c)Q'/Q =", (p - c) * Qp / Q)
print("multiply by p*  -> ((p-c)/p) * eps =", (p - c) / p * eps)
print("multiply by 1/p* -> value", (p - c) * Qp / Q / p, "(should be -1 for the stated identity)")

# Quiz numeric grading as in course/assets/js/quiz.js: |value - answer| <= tol
for ans, tol in ((F(5333333, 100000), F(1, 1000)),):
    pass
exact = F(160, 3)
for typed in (F(5333, 100), F(53333, 1000)):
    print("L06 Q2 typed", float(typed), "accepted with tolerance 0.001 against 53.3333:", abs(float(typed) - 53.3333) <= 0.001)
exact4 = F(200, 3)
print("L06 Q4 typed 66.67 accepted with tolerance 0.001 against 66.6667:", abs(66.67 - 66.6667) <= 0.001)
