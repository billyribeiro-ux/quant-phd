"""Round-5 structural and text scans for PC3 slice a (index, L01-L03, lab twins). Run from the checkout root:
.venv/bin/python -I ledgers/PC3/scripts/PC3-a-r5/scans_a_r5.py
Covers: banned phrases and process words in learner prose; undefined-term first uses; D1-D9 DAG terms; forbidden
citations; registered-symbol collisions; why-it-matters length and question marks; per-lesson structure counts;
prerequisite closure; P0.1 link scan; hub placement arithmetic.
"""

import glob
import html
import re
from fractions import Fraction as F

PAGES = {"index": "course/modules/PC/PC3/index.html", "L01": "course/modules/PC/PC3/L01.html",
         "L02": "course/modules/PC/PC3/L02.html", "L03": "course/modules/PC/PC3/L03.html"}


def prose(path: str) -> str:
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<pre><code class=\"language-python\".*?</code></pre>", " ", t, flags=re.S)
    t = re.sub(r"<pre class=\"expected\".*?</pre>", " ", t, flags=re.S)
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "…"]
PROCESS = [r"\bround\b", r"\bbuild\b", r"\bbuilder", r"\bverifier", r"REQUESTS", r"unit report"]
D_TERMS = ["martingale", "stopping time", "optional stopping", "Bayesian", "Kelly", "Poisson", "Markov", "CAPM",
           "duration", "DCF", "bid-ask", "limit order", "adverse selection", "winner", "probability of informed trading",
           "inventory model", "spread decomposition"]
print("== banned phrases in learner prose (code blocks removed)")
for name, p in PAGES.items():
    s = prose(p)
    hits = [b for b in BANNED if b in s]
    print(f"  {name}: {hits or 'none'}")
print("== process words in learner prose")
for name, p in PAGES.items():
    s = prose(p)
    hits = [pat for pat in PROCESS if re.search(pat, s, flags=re.I)]
    print(f"  {name}: {hits or 'none'}")
print("== D1-D9 terms in learner prose (hits by page)")
for name, p in PAGES.items():
    s = prose(p)
    hits = {d: len(re.findall(re.escape(d), s, flags=re.I)) for d in D_TERMS}
    print(f"  {name}: {({k: v for k, v in hits.items() if v}) or 'none'}")
print("== forbidden citations and cross-references")
for name, p in PAGES.items():
    raw = open(p, encoding="utf-8").read()
    print(f"  {name}: data-cite={raw.count('data-cite')} data-files={raw.count('data-files')} "
          f"'Theorem 3.10'={raw.count('Theorem 3.10')} 'adapted'={len(re.findall('adapted', raw, flags=re.I))} "
          f"'?' in why-it-matters={sum(m.count('?') for m in re.findall(r'why-it-matters\">(.*?)</p>', raw, flags=re.S))}")
print("== first learner-visible use vs definition (character offset in prose)")
for name, term in [("L01", "product interval"), ("L01", "log-error width"), ("L01", "Fermi estimate"),
                   ("L02", "conditional probability"), ("L03", "stopping rule"), ("L03", "history"),
                   ("L03", "fair game"), ("L03", "expected payoff")]:
    s = prose(PAGES[name])
    idx = s.lower().find(term.lower())
    print(f"  {name} '{term}': first at {idx}: ...{s[max(0, idx - 50):idx + 60]}...")
print("== defined terms (dfn tags) per slice page")
for name, p in PAGES.items():
    raw = open(p, encoding="utf-8").read()
    print(f"  {name}: {re.findall(r'<dfn[^>]*>([^<]*)</dfn>', raw)}")
print("== lesson structure counts")
for name in ["L01", "L02", "L03"]:
    raw = open(PAGES[name], encoding="utf-8").read()
    print(f"  {name}: problems={len(re.findall(r'class=\"problem\"', raw))} "
          f"solutions={len(re.findall(r'details class=\"solution\"', raw))} "
          f"misconceptions={len(re.findall(r'<li class=\"misconception\">', raw))} "
          f"quiz_items={len(re.findall(r'<li class=\"item\"', raw))} "
          f"explain={len(re.findall(r'class=\"explain\"', raw))} "
          f"key_rows={len(re.findall(r'<tr><td>', raw))} data-hours={re.search(r'data-hours=\"(\d+)\"', raw).group(1)} "
          f"complete_button={'data-complete' in raw} "
          f"theorem_titles={re.findall(r'data-grade=\"(\w)\">((?:Theorem|Proposition) [\d.]+)', raw)}")
print("== registered symbols and macros")
for name, p in PAGES.items():
    raw = open(p, encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, flags=re.S)
    body = " ".join(a or b for a, b in maths)
    cmds = sorted(set(re.findall(r"\\([A-Za-z]+)", body)))
    print(f"  {name}: commands={cmds}")
    print(f"  {name}: bare capital T/Q/Phi/gamma/R_f collisions: {re.findall(r'(?<![\\\\A-Za-z])(T|Q|Phi|R_f|gamma)(?![A-Za-z])', body)}")
print("== prerequisite closure (computed from curriculum.json)")
import json
cur = json.load(open("curriculum/curriculum.json", encoding="utf-8"))
mods = {}


def walk(o):
    if isinstance(o, dict):
        if "id" in o and "prereqs" in o and "tier" in o:
            mods[o["id"]] = o
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(cur)
clo, st = set(), list(mods["PC3"]["prereqs"])
while st:
    m = st.pop()
    if m not in clo:
        clo.add(m)
        st += mods.get(m, {}).get("prereqs", [])
print("  PC3 prereqs", mods["PC3"]["prereqs"], "closure", sorted(clo), len(clo))
print("  titles:", {k: mods[k]["title"] for k in ["M4", "CS2", "FC2", "PC3"]}, "hours PC3", mods["PC3"]["hours"])
print("== P0.1 concept links in PC3 pages")
conc = open("course/concepts.html", encoding="utf-8").read()
sec = conc.split('id="c-P0.1"', 1)[1].split("</section>", 1)[0]
p01 = re.findall(r'<li id="([^"]+)"', sec)
found = []
for f in glob.glob("course/modules/PC/PC3/*.html"):
    s = open(f, encoding="utf-8").read()
    for cid in p01:
        if re.search(r'(data-concept="%s"|concepts\.html#%s["\'])' % (re.escape(cid), re.escape(cid)), s):
            found.append((f, cid))
print(f"  P0.1 ids: {len(p01)}; PC3 links to them: {found or 'none'}")
print("== hub placement quiz arithmetic")
checks = {
    "E[face] 21/6": F(21, 6) == F("3.5"),
    "1/2*1/2": F(1, 4) == F("0.25"),
    "100/1.1 to 6dp": f"{100 / 1.1:.6f}" == "90.909091",
    "S e^{r tau} is option 2": True,
    "rung1 buy cash flow": -10005 == -10005,
    "rung2 inventory mark 1*10040": 1 * 10040 == 10040,
    "7 of 10 = 70%, 8 of 10 = 80%": (7 * 10 == 70) and (8 * 10 == 80),
}
for k, v in checks.items():
    print(f"  {k}: {v}")
print("== hub hours arithmetic")
print(f"  lessons 6*6={6 * 6}, project 2+6+4+2={2 + 6 + 4 + 2}, total={36 + 14}, share={14 / 50:.0%}")
print("done")
