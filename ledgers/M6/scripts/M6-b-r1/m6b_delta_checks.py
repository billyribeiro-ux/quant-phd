"""M6-b round 1 closing-delta checks (run with python -I from the checkout root).

1. Grade-attribute counts on L05-L08 at the base pin and at HEAD (data-grade values must be unchanged).
2. Locator scan: every '01-foundations.yaml:' locator on L05-L08 and its line range in the curriculum file at HEAD.
3. Process-word grep on L05-L08 at HEAD.
4. Registered notation symbols (notation/notation.json) searched in L05-L08 at HEAD.
5. Recomputation of every number in the changed L05 prose and of the card and quiz numbers.
"""
import json
import math
import re
import subprocess

ROOT = "."
PAGES = [f"course/modules/M/M6/{p}.html" for p in ("L05", "L06", "L07", "L08")]


def git_show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout


print("== 1 grade attributes (base 95f3f8cb vs HEAD)")
for p in PAGES:
    base = git_show("95f3f8cb", p)
    head = open(p, encoding="utf-8").read()
    gb = re.findall(r'data-grade="([A-DTX]|not graded)"', base)
    gh = re.findall(r'data-grade="([A-DTX]|not graded)"', head)
    print(p, "base", len(gb), "head", len(gh), "same sequence" if gb == gh else "DIFFERENT sequence")

print("== 2 locator scan")
curr = open("curriculum/01-foundations.yaml", encoding="utf-8").read().splitlines()
for n in (287, 288, 289):
    print("curriculum line", n, repr(curr[n - 1].strip()[:70]))
for p in PAGES:
    text = open(p, encoding="utf-8").read()
    locs = re.findall(r"01-foundations\.yaml:(?:<wbr>)?(\d+)(?:-(?:<wbr>)?(\d+))?", text)
    print(p, "locators", locs)

print("== 3 process words (HEAD)")
banned = re.compile(r"\b(round|verifier|ledger|fixer|reviewer|previous round|the fix|rev\w*)\b", re.I)
for p in PAGES:
    text = open(p, encoding="utf-8").read()
    hits = [(i + 1, m.group(0)) for i, line in enumerate(text.splitlines()) for m in banned.finditer(line)]
    print(p, "hits", hits)

print("== 4 registered notation symbols in L05-L08 (HEAD)")
notation = json.load(open("notation/notation.json", encoding="utf-8"))
needles = ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\Prob"]
for p in PAGES:
    text = open(p, encoding="utf-8").read()
    print(p, {n: text.count(n) for n in needles})
print("T as a bare symbol in math:", {p: len(re.findall(r"\\\(([^\\]|\\[^)])*\bT\b", open(p, encoding="utf-8").read())) for p in PAGES})
print("registered symbols:", [s["symbol"] for s in notation["symbols"]])

print("== 5 recomputed numbers")
pi4 = math.pi / 4
c = math.atan(2) - math.atan(1)
print("pi/4", f"{pi4:.10f}", "-pi/4", f"{-pi4:.10f}")
print("c = arctan2 - pi/4", f"{c:.12f}", "c - pi/4 check", f"{c - (math.atan(2) - pi4):.2e}")
print("quadrature error printed 0.7853982936 - pi/4", f"{0.7853982936 - pi4:+.4e}")
print("printed closed block 0.3217505544 vs c", f"{0.3217505544 - c:+.4e}")
print("9*c", f"{9 * 0.3217505544:.10f}", "10*c", f"{10 * 0.3217505544:.9f}")
print("integral 1/(1+t^2) on [1,2] >= 1/5:", 1 / 5 <= min(1 / (1 + t * t) for t in [1 + i / 1000 for i in range(1001)]) + 1e-15)
# numeric check of c_k for k=0,1,2 by midpoint quadrature of the block integral with the closed inner integral
def inner(x, a):
    return a / (x * x + a * a)
for k in range(3):
    a = 0.5 ** (k + 1)
    n = 20000
    h = a / n
    ck = sum(inner(a + (i + 0.5) * h, a) for i in range(n)) * h
    print("block", k, "a", a, "c_k midpoint", f"{ck:.10f}", "c", f"{c:.10f}", "diff", f"{ck - c:+.2e}")
# direct check of inner integral formula: integral over y in [0,a] of f(x,y) equals a/(x^2+a^2) for x=0.75, a=0.5
x, a = 0.75, 0.5
n = 20000
h = a / n
direct = sum(((x * x - (j + 0.5) * h * (j + 0.5) * h) / ((x * x + ((j + 0.5) * h) ** 2) ** 2)) for j in range(n)) * h
print("inner y-integral direct", f"{direct:.10f}", "closed", f"{a / (x * x + a * a):.10f}")
print("1/3-residual check: 2p-1 for p=1/3", 2 / 3 - 1)
print("L07 Part D values 10/9 and 6/7 as floats", f"{10 / 9:.10f}", f"{6 / 7:.10f}")
