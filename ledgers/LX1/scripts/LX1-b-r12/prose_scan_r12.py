"""LX1-b round 12 prose scan of L03.html and L04.html: banned phrases (BUILDER_RULES 1.3-1.4, check_pages BANNED),
process words, registered notation (notation/notation.json), out-of-closure concept names (plan section 4),
duplicate dfn terms across the unit's pages, and the symbols ell and kappa used on each page.
Run: .venv/bin/python -I <this file> <checkout>
"""
import glob
import html
import os
import re
import sys

root = sys.argv[1]
banned = [r"\bTODO\b", r"\bTBD\b", r"\blorem\b", r"for brevity", r"details omitted", r"beyond the scope",
          r"left as an exercise", r"you can add more", r"it is important to note", r"studies show",
          r"experts agree", r"it is well known", r"\bobviously\b", r"\bclearly\b", r"\.\.\."]
process = r"\b(builder|builders|verifier|verifiers|architect|fixer|planner|campaign|checkout|ledger|build plan|open item|DATA_REQUEST|REFERENCE_REQUEST|round|REQUESTS|unit report)\b"
registered = [r"\Phi", r"\gamma", r"R^\ast", r"R^{e\ast}", r"R_f", r"\mathbb{Q}", r"\E", r"\Prob", r"\Var", r"\Cov",
              r"\Corr", r"\R", r"\N", r"\indic", r"\Normal", r"\iid", r"\dto", r"\pto", r"\argmax", r"\argmin", r"\tr",
              r"\diag", r"\SR", r"\hSR", r"\PSR", r"\DSR", r"\PBO", r"\FWER", r"\FDR", r"\FDP", r"\se", r"\emgamma"]
outside = ["bank run", "fire sale", "leverage cycle", "banking crisis", "currency crisis", "covered interest",
           "uncovered interest", "efficient market", "moral hazard", "Fisher", "bank reserve", "credit default",
           "contagion", "term spread", "expected inflation", "sovereign", "deposit insurance"]


def prose(path):
    t = open(path, encoding="utf-8").read()
    maths = [a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)]
    t = re.sub(r"<pre[^>]*>.*?</pre>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)), maths


for name in ("L03", "L04"):
    path = f"{root}/course/modules/LX/LX1/{name}.html"
    text, maths = prose(path)
    print(f"== {name}: math segments {len(maths)}")
    for pat in banned:
        for m in re.finditer(pat, text, re.I):
            print("BANNED", repr(m.group(0)), "|", text[max(0, m.start() - 60): m.end() + 40])
    for m in re.finditer(process, text, re.I):
        print("PROCESS", repr(m.group(0)), "|", text[max(0, m.start() - 60): m.end() + 40])
    for sym in registered:
        for s in maths:
            if re.search(re.escape(sym) + r"(?![a-zA-Z])", s):
                print("REGISTERED", sym, "|", s[:80])
    for s in maths:
        if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", s):
            print("REGISTERED bare T |", s[:80])
    for term in outside:
        n = len(re.findall(re.escape(term), text, re.I))
        if n:
            print("OUTSIDE-CLOSURE NAME", repr(term), n)
    print("ell in math:", sum(1 for s in maths if r"\ell" in s), "| kappa in math:", sum(1 for s in maths if r"\kappa" in s))
    print("banned/process/registered/outside scan done")

print("== dfn terms across the unit pages")
for p in sorted(glob.glob(f"{root}/course/modules/LX/LX1/*.html")):
    raw = open(p, encoding="utf-8").read()
    for m in re.finditer(r"<dfn([^>]*)>([^<]*)</dfn>", raw):
        print(os.path.basename(p), m.group(2).strip(), "|", m.group(1).strip())
