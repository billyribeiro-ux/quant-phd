"""Round 10 text scans for BK4 slice b (L04, L05, both twins, cards.json, index card lines, notation).

Run as: python3 -I -W error ledgers/BK4/scripts/BK4-b-r10/scan_r10.py  (from the checkout root). Prints every hit.
"""

import collections
import html
import json
import re

ROOT = "."
L4 = "course/modules/BK/BK4/L04.html"
L5 = "course/modules/BK/BK4/L05.html"
T4 = "tests/labs/BK4/lab-BK4-L04-1.py"
T5 = "tests/labs/BK4/lab-BK4-L05-1.py"
CARDS = "course/modules/BK/BK4/cards.json"


def read(path):
    with open(f"{ROOT}/{path}", encoding="utf-8") as fh:
        return fh.read()


def prose(path):
    t = read(path)
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


print("== cards: duplicate scan (all cards)")
cards = json.loads(read(CARDS))
norm = lambda s: " ".join(s.lower().split())  # noqa: E731
print("cards", len(cards))
print("dup ids", [k for k, v in collections.Counter(c["id"] for c in cards).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(norm(c["front"]) for c in cards).items() if v > 1])
print("dup backs", [k for k, v in collections.Counter(norm(c["back"]) for c in cards).items() if v > 1])
print("lesson counts", dict(collections.Counter(c["lesson"] for c in cards)))
print("== cards: L04 and L05 grade/basis/cite")
for c in cards:
    if c["lesson"] in ("L04", "L05"):
        print(c["id"], c["lesson"], "grade", c.get("grade"), "| basis", c.get("basis"), "| cite", c.get("cite"))

print("== process words and banned phrases (prose and twins and cards)")
pat = re.compile(
    r"\b(build|builder|round|verifier|REQUESTS?|unit report|fixer|architect|ruling|plan)\b|TODO|TBD|lorem|"
    r"for brevity|details omitted|beyond the scope|left as an exercise|you can add more|important to note|"
    r"studies show|experts agree|well known|obviously|clearly|\.\.\.",
    re.I,
)
for path in (L4, L5):
    for m in pat.finditer(prose(path)):
        print(path, "HIT", m.group(0))
for path in (T4, T5, CARDS):
    for i, line in enumerate(read(path).splitlines(), 1):
        if pat.search(line) and not re.search(r"\bpattern\b|round\(|rounding", line, re.I):
            print(path, i, "HIT", line.strip()[:100])
print("process/banned scan done")

print("== scope words in prose (L04, L05)")
scope = re.compile(r"\b(every|all|any|always|never|each|only|exactly|same|drives?|the market|systemic|none|no source|must)\b", re.I)
for path in (L4, L5):
    print(path, "scope-word hits:", len(scope.findall(prose(path))))

print("== TeX macros used in L04, L05 (math only, from the raw HTML)")
for path in (L4, L5):
    macros = collections.Counter(re.findall(r"\\([A-Za-z]+)", read(path)))
    print(path, sorted(macros))

print("== T+1, SEC, sec.gov, Securities in slice pages and twins")
for path in (L4, L5, T4, T5):
    hits = [m.group(0) for m in re.finditer(r"T\+1|\bSEC\b|sec\.gov|Securities", read(path))]
    print(path, hits)

print("== citation attributes")
for path in (L4, L5):
    print(path, "data-cite:", re.findall(r'data-cite="([^"]+)"', read(path)))

print("== why-it-matters word counts")
for path in (L4, L5):
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', read(path), re.S)
    print(path, len(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split()))

print("== item and problem counts")
for path in (L4, L5):
    t = read(path)
    print(path, "quiz items", len(re.findall(r'<li class="item"', t)),
          "misconceptions", len(re.findall(r'class="misconception"', t)),
          "problems", re.findall(r'class="problem" id="([A-Z]\d)"', t))

print("== hub card titles and page h1")
idx = read("course/modules/BK/BK4/index.html")
for name in ("L04", "L05"):
    print(name, "h1:", re.findall(r"<h1>(.*?)</h1>", read(f"course/modules/BK/BK4/{name}.html")))
    print(name, "hub card:", re.findall(r'href="%s\.html"[^>]*>.*?card-title">(.*?)</span>' % name, idx))

print("== asserts in twins")
print("assert statements:", [m.group(0) for m in re.finditer(r"^\s*assert\b.*$", read(T4) + read(T5), re.M)])
print("assert word in docstrings/comments:", [m.group(0) for m in re.finditer(r".{0,25}\bassert\b.{0,10}", read(T4) + read(T5))])
print("== notation symbols registered")
nt = json.loads(read("notation/notation.json"))
print("macros", len(nt["macros"]), "symbols", [s["symbol"] for s in nt["symbols"]])
print("scan done")
