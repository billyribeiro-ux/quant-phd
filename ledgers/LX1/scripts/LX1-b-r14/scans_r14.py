"""Round-14 scans for LX1-b (L03, L04, cards). Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r13/scans_r13.py"""
import html
import json
import os
import re
from collections import Counter

import sys
ROOT = sys.argv[1]
BASE = os.path.join(ROOT, "course/modules/LX/LX1")


def page_text(name):
    s = open(os.path.join(BASE, name + ".html"), encoding="utf-8").read()
    body = re.sub(r"<pre><code.*?</code></pre>", "", s, flags=re.S)
    body = re.sub(r"<pre class=\"expected\".*?</pre>", "", body, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)), s


print("== 1. banned, process and outside-closure words (prose, code and expected blocks removed)")
BANNED = [r"\bTODO\b", r"\bTBD\b", r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise",
          r"you can add more", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
          r"obviously", r"clearly", r"\.\.\."]
PROCESS = [r"\bbuild(er|ers|ing)?\b", r"\bround\b", r"verifier", r"REQUEST", r"unit report", r"fixer", r"planner", r"architect", r"ruling"]
CLOSURE_OUT = [r"bank run", r"fire sale", r"leverage cycle", r"banking crisis", r"currency crisis", r"covered interest",
               r"uncovered interest", r"efficient market", r"moral hazard", r"Fisher", r"bank reserve", r"credit default",
               r"contagion", r"term spread", r"expected inflation", r"sovereign", r"deposit insurance", r"central bank balance"]
for name in ("L03", "L04"):
    body, _ = page_text(name)
    for group, pats in (("banned", BANNED), ("process", PROCESS), ("outside-closure", CLOSURE_OUT)):
        hits = {p: len(re.findall(p, body)) for p in pats}
        print(name, group, {k: v for k, v in hits.items() if v} or "none")

print("== 2. scope words (count only; each hit was read in context in round 13)")
SCOPE = [r"\bevery\b", r"\ball\b", r"\bnever\b", r"\balways\b", r"\bany\b", r"\bonly\b", r"\bsame\b", r"\bexactly\b", r"\bthe first\b", r"\bthe last\b"]
for name in ("L03", "L04"):
    body, _ = page_text(name)
    print(name, {p: len(re.findall(p, body)) for p in SCOPE})

print("== 3. concept links and dfn anchors")
for name in ("L03", "L04"):
    _, s = page_text(name)
    for m in re.finditer(r'<a class="concept" data-concept="([^"]+)" href="([^"]+)"', s):
        href = m.group(2)
        if "#" in href:
            f, frag = href.split("#", 1)
            target = os.path.normpath(os.path.join(BASE, f)) if f else os.path.join(BASE, name + ".html")
            ids = set(re.findall(r'id="([^"]+)"', open(target, encoding="utf-8").read()))
            print(name, "link", m.group(1), href, "OK" if frag in ids else "MISSING")
    print(name, "dfn:", re.findall(r'<dfn[^>]*>', s))

print("== 4. symbols in math segments per lesson")
for name in ("L01", "L02", "L03", "L04"):
    s = open(os.path.join(BASE, name + ".html"), encoding="utf-8").read()
    maths = " ".join(m.group(1) for m in re.finditer(r"\\\((.*?)\\\)", s, re.S))
    letters = sorted(set(re.findall(r"(?<![\\a-zA-Z])([A-Za-z])(?![a-zA-Z])", re.sub(r"\\[a-zA-Z]+", "", maths))))
    greek = Counter(re.findall(r"\\(ell|lambda|psi|varphi|bar\{x\}|kappa|beta|delta|pi|Phi|gamma|E|R|Prob)(?![a-zA-Z])", maths))
    print(name, "letters:", "".join(letters), "| greek/macros:", dict(greek))
print("N in L01 (count parameter, S_N):", re.findall(r"S_N\(t\) = [^\\]{0,30}", open(os.path.join(BASE, 'L01.html'), encoding='utf-8').read())[:2])
print("N in L03 (net worth):", re.findall(r"N_t = N_0 - \(V_t - V_0\)", open(os.path.join(BASE, 'L03.html'), encoding='utf-8').read()))

print("== 5. cards: ids, duplicate fronts and backs, numbers absent from lesson")
cards = json.load(open(os.path.join(BASE, "cards.json"), encoding="utf-8"))
print("cards", len(cards), "lessons", dict(Counter(c["lesson"] for c in cards)))
print("duplicate ids", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate fronts", [k for k, v in Counter(re.sub(r"\W+", " ", c["front"]).strip().lower() for c in cards).items() if v > 1])
print("duplicate backs", [k[:50] for k, v in Counter(re.sub(r"\W+", " ", c["back"]).strip().lower() for c in cards).items() if v > 1])
print("cite non-empty", [c["id"] for c in cards if c["cite"]])
for c in cards:
    if c["lesson"] not in ("L03", "L04"):
        continue
    lesson = open(os.path.join(BASE, c["lesson"] + ".html"), encoding="utf-8").read()
    for n in re.findall(r"\d+\.\d+", c["back"]):
        if n not in lesson:
            print("  number not in lesson:", c["id"], n)
print("number check done")
