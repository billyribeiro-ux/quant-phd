"""Verifier round 15, slice e: scripted checks behind rows E3e-r15-* and the carried notation rows.

Run as: python -I ledgers/E3/scripts/E3-e-r15/checks_r15.py   (from the checkout root)
Prints: data-cite counts, footer texts, symbol occurrence lines for a and W, the lab twin/page
comparison, the hub claims (concept index status, project rung 1, project z formula), and the
references-changed line count since the previous pin.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
E3 = ROOT / "course/modules/E/E3"
PAGES = ["index.html"] + [f"L0{n}.html" for n in range(1, 9)]

print("== data-cite count per page")
for p in PAGES:
    t = (E3 / p).read_text(encoding="utf-8")
    print(p, t.count("data-cite="), "T-graded spans:", len(re.findall(r'data-grade="T"', t)))

print("== footers")
for n in range(1, 9):
    t = (E3 / f"L0{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<footer class="site-footer">(.*?)</footer>', t, re.S)
    print(f"L0{n}:", html.unescape(m.group(1).split("·")[-1]).strip())

print("== symbol a (EZ exponent and affine constant and generic exponent)")
for p, pat in [("L01.html", r"\\\(a \+ b|real constants \\\(a\\\)|\\\(a = 0\\\)"),
               ("L03.html", r"real number \\\(a\\\)|real \\\(a\\\)|w\^\{?a"),
               ("L05.html", r"Let \\\(a := 1 - 1/\\psi"),
               ("L08.html", r"Let \\\(a = 1 - 1/\\psi")]:
    t = (E3 / p).read_text(encoding="utf-8")
    print(p, "matches:", len(re.findall(pat, t)))

print("== symbol W (wealth lottery vs prospect value)")
for p, pat in [("L02.html", r"wealth lottery \\\(W\\\)"), ("L06.html", r"W := \\sum_i p_i")]:
    t = (E3 / p).read_text(encoding="utf-8")
    print(p, "matches:", len(re.findall(pat, t)))

print("== lab twin code and expected block")
for n in range(1, 9):
    page = (E3 / f"L0{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code_page = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/E3/lab-E3-L0{n}-1.py").read_text(encoding="utf-8")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1)).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"tests/labs/E3/lab-E3-L0{n}-1.py"],
                         capture_output=True, text=True).stdout.strip()
    print(f"L0{n}: code==twin {code_page.strip() == twin.strip()}; expected==output {expected == out}")

print("== hub claims")
concepts = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
print("concepts.html 'not yet released' count:", concepts.count("not yet released"),
      "; 'defined here' count:", concepts.count("defined here"))
proj = (E3 / "project.html").read_text(encoding="utf-8")
print("project.html rung 1 says SIMULATED participant:", "one SIMULATED participant" in proj)
print("project.html z formula:", "z = kappa (CE_A - CE_B) / 10000" in proj)
print("project.html at least 12 pairs:", "at least 12 pairs" in proj)
idx = (E3 / "index.html").read_text(encoding="utf-8")
print("index rung 1 wording:", "one SIMULATED participant whose answers are written into the lab" in idx)

print("== references and notation registry unchanged since previous pin (diff lines)")
d = subprocess.run(["git", "diff", "1431aa1d", "dde0486b", "--", "references", "notation"],
                   capture_output=True, text=True).stdout
print("diff lines:", len(d.splitlines()))

print("== quiz item counts per lesson (requirement 8-15)")
for n in range(1, 9):
    t = (E3 / f"L0{n}.html").read_text(encoding="utf-8")
    quiz = t[t.find('<section class="quiz"'):]
    quiz = quiz[:quiz.find("</section>")]
    print(f"L0{n}: items {quiz.count('<li class=\"item\"')}")

print("== registry symbols and raw macros in lesson prose (must be none)")
pats = [r"\\mathbb\{E\}", r"\\mathbb\{R\}", r"\\mathbb\{Q\}", r"\\Phi", r"\\gamma_\{?3", r"\\gamma_\{?4",
        r"R_f", r"R\^\\ast", r"\\operatorname\{Var\}", r"\\operatorname\{Cov\}"]
for n in range(1, 9):
    t = (E3 / f"L0{n}.html").read_text(encoding="utf-8")
    hits = {p: len(re.findall(p, t)) for p in pats}
    print(f"L0{n}:", {p: h for p, h in hits.items() if h})
print("(no output line above means zero hits in that page)")

print("== anchors used by cross-lesson links exist as ids")
ids = set()
for n in range(1, 9):
    t = (E3 / f"L0{n}.html").read_text(encoding="utf-8")
    ids |= set(re.findall(r'id="([^"]+)"', t))
for lesson, anchor in [("L01", "def-expected-utility"), ("L02", "def-certainty-equivalent"),
                       ("L02", "def-arrow-pratt-risk-aversion"), ("L03", "def-crra-utility"),
                       ("L04", "def-first-order-stochastic-dominance"),
                       ("L05", "def-epstein-zin-preferences"),
                       ("L05", "def-elasticity-of-intertemporal-substitution"),
                       ("L06", "def-prospect-theory"), ("L06", "def-loss-aversion"),
                       ("L07", "def-probability-weighting"), ("L08", "def-ambiguity-aversion")]:
    t = (E3 / f"{lesson}.html").read_text(encoding="utf-8")
    print(f"{lesson}#{anchor} defined:", f'id="{anchor}"' in t)

print("== L02 Proposition 3.1 proof: symbol q absent, z used")
t = (E3 / "L02.html").read_text(encoding="utf-8")
print("L02 q(eps) occurrences:", len(re.findall(r"q\(\\\\varepsilon\)", t)), "; z(eps) limit line present:",
      "z(\\varepsilon) \\to" in t)

print("== banned strings, process words, DAG-sensitive terms, strong scope words (index and L01-L08 prose and code)")
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "important to note", "studies show", "experts agree", "well known", "obviously", "clearly"]
process = ["builder", "verifier", "REQUESTS", "ledger", "fanout"]
dag = ["convex", "Bellman", "martingale", "maximum likelihood", "estimator", "confidence", "Fisher", "Hessian",
       "equity risk premium", "risk-neutral"]
scope = ["always", "never", "in general", "for all", "every nondecreasing", "every concave", "every utility",
         "every lottery", "every finite", "every gamble", "every person", "every investor", "every decision"]
for label, words in [("banned", banned), ("process", process), ("dag", dag), ("scope", scope)]:
    for w in words:
        hits = []
        for p in PAGES:
            t = (E3 / p).read_text(encoding="utf-8")
            n = len(re.findall(re.escape(w), t, re.I))
            if n:
                hits.append(f"{p}:{n}")
        print(f"{label} '{w}': {', '.join(hits) if hits else 0}")
