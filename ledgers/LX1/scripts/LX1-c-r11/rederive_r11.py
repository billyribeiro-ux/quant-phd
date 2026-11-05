"""Round-11 independent re-derivation (verifier): exact Fractions for labs 1 and 2, float/statistics for lab 3 from
the committed CSV, and MANIFEST / data-field checks. Argument 1 is the checkout root."""
import csv, hashlib, json, math, statistics, sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
def half(x, p):
    return Decimal(x).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)

# Lab 1 (exact)
D = Fraction(10_000_000)
for name, ps in (("falling", (1, .97, .94, .91, .88, .85)), ("rising", (1, 1.03, 1.06, 1.09, 1.12, 1.15))):
    P = [Fraction(str(p)) for p in ps]
    rd = [D / p for p in P]
    burden = 100 * (P[0] / P[-1] - 1)
    print(f"lab1 {name}: t5 real debt cents exact={float(rd[-1]):.5f} dollars={half(float(rd[-1]/100),2)} "
          f"burden={half(float(burden),2)} (exact {float(burden):.6f})")
diff = (D / Fraction("0.85") - D / Fraction("1.15"))
print(f"lab1 difference cents exact={float(diff):.5f} dollars={half(float(diff/100),2)}")
# Lab 2 (exact)
P2 = [Fraction(str(p)) for p in (1, .99, .98, .96, .95, .93)]
D2 = Fraction(4_000_000)
print("lab2 real dollars:", [str(half(float(D2 / p / 100), 2)) for p in P2])
print("lab2 burden:", half(float(100 * (P2[0] / P2[-1] - 1)), 2), f"exact {float(100*(P2[0]/P2[-1]-1)):.6f}")
print("lab2 inverted burden:", half(float(100 * (P2[-1] / P2[0] - 1)), 2))
# Lab 3 (CSV, independent)
rows = list(csv.DictReader(open(root / "course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("csv header:", list(rows[0].keys()), "rows:", len(rows), "first", rows[0]["month"], "last", rows[-1]["month"])
for col in ("EUR", "GBP"):
    blanks = [r["month"] for r in rows if (r[col] or "").strip() == ""]
    print(f"blank {col}: {len(blanks)}", (blanks[0], blanks[-1]) if blanks else "")
gaps = 0
for a, b in zip(rows, rows[1:]):
    ya, ma = map(int, a["month"].split("-")); yb, mb = map(int, b["month"].split("-"))
    if (yb * 12 + mb) - (ya * 12 + ma) != 1:
        gaps += 1
print("month gaps:", gaps)
gbp = [(r["month"], float(r["GBP"])) for r in rows]
ch = [(m, math.log(v / p)) for (p_, p), (m, v) in zip([(a, b) for a, b in gbp[:-1]], gbp[1:]) for _ in [0]]
ch = []
for (pm, pv), (m, v) in zip(gbp, gbp[1:]):
    ch.append((m, math.log(v / pv)))
def sd(xs):
    mu = sum(xs) / len(xs)
    return math.sqrt(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1))
W1 = [c for m, c in ch]
W2 = [c for m, c in ch if m >= "2000-01"]
W3 = [c for m, c in ch if m >= "2025-10"]
for nm, W in (("w1", W1), ("w2", W2), ("w3", W3)):
    z = sum(1 for x in W if x == 0.0)
    print(f"{nm}: n={len(W)} zeros={z} sd_pct={100*sd(W):.6f} -> {half(100*sd(W),2)} stdev_agree={abs(sd(W)-statistics.stdev(W))<1e-12}")
s1, s2 = sd(W1), sd(W2)
print("ratio", half(s2 / s1, 2), f"{s2/s1:.6f}", "difference", half(100 * (s1 - s2), 2), f"{100*(s1-s2):.6f}")
big = max(ch, key=lambda t: abs(t[1])); print("largest overall", big[0], half(100 * big[1], 2))
big2 = max([t for t in ch if t[0] >= "2000-01"], key=lambda t: abs(t[1])); print("largest w2", big2[0], half(100 * big2[1], 2))
big3 = max([t for t in ch if t[0] >= "2025-10"], key=lambda t: abs(t[1])); print("largest w3", big3[0], half(100 * big3[1], 2))
zeros = [m for m, c in ch if c == 0.0]; print("zero months:", zeros)
# MANIFEST
man = json.loads((root / "course/assets/data/market/MANIFEST.json").read_text(encoding="utf-8"))
ds = man["datasets"]
print("manifest dataset ids:", list(ds.keys()) if isinstance(ds, dict) else [d.get("id") for d in ds])
fx = ds["fx_monthly"] if isinstance(ds, dict) else next(d for d in ds if d.get("id") == "fx_monthly")
for k in ("title", "transform", "columns", "first", "last", "rows", "retrieved", "citation", "licence", "licence_url", "sha256", "bytes"):
    if k in fx:
        print(f"manifest.{k}:", json.dumps(fx[k], ensure_ascii=False)[:400])
raw = (root / "course/assets/data/market/fx_monthly.csv").read_bytes()
print("csv sha256:", hashlib.sha256(raw).hexdigest(), "bytes", len(raw))
