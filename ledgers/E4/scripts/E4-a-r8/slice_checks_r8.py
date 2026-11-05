"""E4 slice a (index, L01-L03) round 8 static checks: structure counts, banned and process terms, macros,
registered symbols, concept anchors and owners, and the data-simulated labels of L06-L08. Run as
.venv/bin/python -I ledgers/E4/scripts/E4-a-r8/slice_checks_r8.py (cwd = the checkout root)."""

import html
import json
import pathlib
import re

ROOT = pathlib.Path(".").resolve()
BASE = ROOT / "course/modules/E/E4"
PAGES = ["index", "L01", "L02", "L03"]
text = {p: (BASE / f"{p}.html").read_text(encoding="utf-8") for p in PAGES}


def prose(s: str) -> str:
    s = re.sub(r"<pre.*?</pre>", " ", s, flags=re.S)
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


print("== structure")
for p in ["L01", "L02", "L03"]:
    t = text[p]
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    sols = re.findall(r'<details class="solution">(.*?)</details>', t, re.S)
    print(p, "why_words", len(prose(why.group(1)).split()), "solutions", len(sols),
          "min_solution_words", min(len(prose(s).replace("Solution", "", 1).split()) for s in sols),
          "misconceptions", len(re.findall(r'<li class="misconception"', t)),
          "problems", len(re.findall(r'<div class="problem"', t)),
          "quiz_items", len(re.findall(r'<li class="item"', t)),
          "data_references_entries", len(re.findall(r"<ol data-references>\s*<li", t)),
          "h1", re.findall(r"<h1>(.*?)</h1>", t))
    print(p, "dfn_concepts", re.findall(r'<dfn[^>]*data-concept="([^"]+)"', t))
print("hub_cards", re.findall(r'<span class="card-title">(.*?)</span>', text["index"]))
for n in range(4, 10):
    t = (BASE / f"L0{n}.html").read_text(encoding="utf-8")
    print(f"L0{n}", "h1", re.findall(r"<h1>(.*?)</h1>", t))

print("== banned, process and D-terms (prose, case-insensitive)")
terms = ["state price", "Bayes", "martingale", "common knowledge", "CARA", "informationally efficient",
         "noise trader", "posterior", "intermediate value", "Banach", "law of one price", "risk-neutral",
         "pricing kernel", "stochastic discount", "TODO", "TBD", "lorem", "for brevity", "clearly", "obviously",
         "studies show", "experts agree", "it is important to note", "beyond the scope", "left as an exercise",
         "details omitted", "you can add more", "it is well known", "builder", "verifier", "REQUEST", "unit report"]
for term in terms:
    counts = {p: len(re.findall(re.escape(term), prose(text[p]), flags=re.I)) for p in PAGES}
    print(f"{term!r}", counts)
for p in PAGES:
    s = re.sub(r"<pre.*?</pre>", "", text[p], flags=re.S)
    print("ellipsis outside code", p, s.count("..."), "unicode", s.count("…"))
print("process word 'round' whole-word", {p: len(re.findall(r"\bround\b", prose(text[p]), flags=re.I)) for p in PAGES})

print("== macros and registered symbols")
notation = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
registered = set(notation["macros"].keys())
used = {}
for p in PAGES:
    for m in re.finditer(r"(?<![A-Za-z])\\([A-Za-z]+)", text[p]):
        used.setdefault(m.group(0), set()).add(p)
print("registered macros used", {k: sorted(v) for k, v in used.items() if k in registered})
print("unregistered commands used", sorted(k for k in used if k not in registered))
print("mathbb present", any("mathbb" in k for k in used))
for p in PAGES:
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text[p], re.S)
    flat = [x for pair in maths for x in pair if x]
    hits = [m for m in flat if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", m)]
    print("standalone T in math", p, len(hits))

print("== concept anchors and owners")
concepts_html = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
curriculum = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))["concepts"]
closure = {"E1", "E2", "E3", "M1", "M2", "M3", "M4", "M7", "P0.1", "E4"}
used_concepts = sorted({c for p in PAGES for c in re.findall(r'data-concept="([^"]+)"', text[p])})
for c in used_concepts:
    anchor = f'id="{c}"' in concepts_html
    owner = curriculum.get(c, {}).get("module")
    print(f"{c}: anchor_in_concepts_html={anchor} owner={owner} in_closure_or_E4={owner in closure}")

print("== labs: seeded draws and SIMULATED labels (L04-L09, project)")
for lab in ["L04", "L05", "L06", "L07", "L08", "L09"]:
    tw = (ROOT / f"tests/labs/E4/lab-E4-{lab}-1.py").read_text(encoding="utf-8")
    pg = (BASE / f"{lab}.html").read_text(encoding="utf-8")
    print(lab, "random.Random calls in twin", tw.count("random.Random("), "SIMULATED on page", pg.count("SIMULATED"))
print("project SIMULATED on page", (BASE / "project.html").read_text(encoding="utf-8").count("SIMULATED"))
print("data-files on slice pages", sum(text[p].count("data-files") for p in PAGES))
print("years (1800-2099) in prose", {p: re.findall(r"\b(1[89]\d\d|20\d\d)\b", prose(text[p])) for p in PAGES})
