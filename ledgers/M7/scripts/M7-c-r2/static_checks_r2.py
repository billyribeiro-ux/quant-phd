"""Round-2 static checks for M7 L07 and L08: notation tokens against notation/notation.json, scope-word listing,
concept links and dfn ids, structure counts, and the why-it-matters word counts.

Run: python3 -I ledgers/M7/scripts/M7-c-r2/static_checks_r2.py
"""
import html
import json
import re

notation = json.load(open("notation/notation.json", encoding="utf-8"))
registered = [s["symbol"] for s in notation["symbols"]]
macros = sorted(notation["macros"].keys())
print("registered symbols:", registered)
print("registered macros:", macros)

for f in ("course/modules/M/M7/L07.html", "course/modules/M/M7/L08.html"):
    raw = open(f, encoding="utf-8").read()
    print("\n=====", f)
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
    toks = set()
    for a, b in maths:
        m = a or b
        toks.update(re.findall(r"\\[A-Za-z]+", m))
        toks.update(re.findall(r"(?<![\\A-Za-z])[A-Za-z](?![A-Za-z])", re.sub(r"\\[A-Za-z]+", "", m)))
    print("math tokens:", sorted(toks))
    print("registered macros used:", [m for m in macros if m in toks])
    print("registered symbol fragments in math:", [x for x in ["\\Phi", "\\gamma", "R^", "\\mathbb{Q}", "\\SR", "\\PSR", "T"]
                                                 if any(x in (a or b) for a, b in maths)])
    print("concept links:", sorted(set(re.findall(r'data-concept="([^"]+)"', raw))))
    print("dfn ids:", re.findall(r'<dfn id="([^"]+)" data-concept="([^"]+)"', raw))
    print("link targets:", sorted(set(re.findall(r'href="([^"]*#[^"]+)"', raw))))
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    print("banned/process words:", re.findall(r"\b(TODO|TBD|lorem|builder|verifier|architect|round \d)\b", txt, re.I))
    print("scope-word count:", len(re.findall(r"\b(every|always|all|never|any|for each|only|same|exactly|drives|whole)\b", txt, re.I)))
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S).group(1)
    print("why-it-matters words:", len(html.unescape(re.sub(r"<[^>]+>", " ", wim)).split()))
    sols = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
    print("solutions:", len(sols), "min words:", min(len(html.unescape(re.sub(r"<[^>]+>", " ", s)).split()) for s in sols))
    print("problem ids:", re.findall(r'class="problem" id="([A-Z]\d)"', raw))
    print("quiz items:", len(re.findall(r'<li class="item"', raw)), "misconceptions:", len(re.findall(r'class="misconception"', raw)))
    print("data-hours:", re.findall(r'data-hours="(\d+)"', raw))
