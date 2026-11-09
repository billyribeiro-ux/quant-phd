"""Round-2 prose and structure scans for M2 slice a (index.html, L01-L06 and their lab twins).

Covers: banned phrases (BUILDER_RULES 1.3-1.4), process words, rhetorical questions in visible prose, LaTeX macro
inventory against notation/notation.json, registry-symbol usage, later-module concept names, why-it-matters word counts,
data-hours, quiz item counts, and data-answer attributes. Run from the checkout root with -I.
"""

from __future__ import annotations

import html
import json
import re

ROOT = "course/modules/M/M2/"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html"]


def visible(name: str) -> str:
    t = open(ROOT + name, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<pre[^>]*>.*?</pre>", " ", t, flags=re.S)  # lab code and expected blocks: checked by run_labs
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t))


BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "motivational", "in practice", "typically", "fast", "smooth"]
PROCESS = ["builder", "verifier", "fixer", "round ", "slice", "ledger", "fragment", "orchestrat", "subagent"]
LATER = ["Fubini", "Lagrange", "multiplier", "Riemann-Stieltjes", "Lebesgue", "duration", "convexity", "Taylor's theorem",
         "gradient", "Jacobian", "Hessian", "envelope", "implicit-function", "automatic differentiation"]

print("== banned phrase and process-word hits (visible prose)")
for name in PAGES:
    s = visible(name)
    hits = {w: len(re.findall(re.escape(w), s, flags=re.I)) for w in BANNED + PROCESS}
    print(name, {k: v for k, v in hits.items() if v})

print("== rhetorical questions in visible prose (outside quiz and problem prompts)")
for name in PAGES:
    t = open(ROOT + name, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>|<pre[^>]*>.*?</pre>", " ", t, flags=re.S)
    t = re.sub(r'<p class="prompt">.*?</p>|<p class="wrong">.*?</p>|<p>(?:(?!</p>).)*?Show that|<label.*?</label>', " ", t, flags=re.S)
    s = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
    for m in re.finditer(r"[^.!?]{0,140}\?", s):
        print(f"  {name}: ...{m.group(0).strip()[-120:]}")

print("== LaTeX macros used (visible code paths: pages incl. math) vs notation.json")
notation = json.load(open("notation/notation.json", encoding="utf-8"))
registered = set(notation["macros"].keys())
used: dict[str, int] = {}
for name in PAGES:
    t = open(ROOT + name, encoding="utf-8").read()
    for mac in re.findall(r"\\[a-zA-Z]+", t):
        used[mac] = used.get(mac, 0) + 1
std = {m for m in used if m not in registered}
print("registered macros used:", sorted(m for m in used if m in registered))
print("non-registered TeX commands used (standard KaTeX/LaTeX commands):", sorted(std))
print("\\mathbb occurrences:", sum(open(ROOT + n, encoding='utf-8').read().count('\\mathbb') for n in PAGES))
sym = [s["symbol"] for s in notation["symbols"]]
print("registry symbols:", sym)
for name in PAGES:
    t = open(ROOT + name, encoding="utf-8").read()
    for pat in [r"\\Phi", r"\\gamma", r"R\^\\ast", r"R_f", r"\\mathbb\{Q\}", r"R\^\{e"]:
        n = len(re.findall(pat, t))
        if n:
            print("  registry-symbol pattern", pat, "in", name, n)

print("== later-module concept names in slice prose")
for name in PAGES:
    s = visible(name)
    for w in LATER:
        n = len(re.findall(re.escape(w), s))
        if n:
            print(f"  {name}: {w!r} x{n}")

print("== why-it-matters word counts, data-hours, quiz items, data-answer attributes")
for n in range(1, 7):
    name = f"L0{n}.html"
    t = open(ROOT + name, encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, flags=re.S)
    words = len(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split())
    hrs = re.search(r'data-hours="(\d+)"', t).group(1)
    quiz = t[t.find('class="quiz"'):]
    quiz = quiz[: quiz.find("</section>")]
    items = quiz.count('<li class="item"')
    answers = re.findall(r'data-kind="numeric" data-answer="([^"]+)" data-tolerance="([^"]+)"', quiz)
    print(f"{name}: why_words={words} data-hours={hrs} quiz_items={items} numeric_answers={answers}")
hub = open(ROOT + "index.html", encoding="utf-8").read()
print("index numeric items:", re.findall(r'data-skill data-answer="([^"]+)" data-tolerance="([^"]+)"', hub))
print("index data-hours-lessons/project:", re.findall(r'data-hours-(lessons|project)="(\d+)"', hub))
print("data-cite in index:", re.findall(r'data-cite="([^"]+)"', hub))
print("data-cite/data-files in L01-L06:", sum(open(ROOT + f"L0{n}.html", encoding="utf-8").read().count("data-cite") + open(ROOT + f"L0{n}.html", encoding="utf-8").read().count("data-files") for n in range(1, 7)))
print("data-chart/figure in slice pages:", sum(open(ROOT + n, encoding="utf-8").read().count("data-chart") for n in PAGES))
