"""PC3 slice a, round 8: banned phrases, process words, why-it-matters word counts, structure counts, debate field."""
import json
import re
import sys
from html.parser import HTMLParser

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-a"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
BASE = f"{ROOT}/course/modules/PC/PC3/"


class Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style", "pre"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "pre") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def visible(path: str) -> str:
    p = Visible()
    p.feed(open(path, encoding="utf-8").read())
    return " ".join(p.parts)


BANNED = [
    r"\bTODO\b", r"\bTBD\b", r"lorem", r"for brevity", r"details omitted", r"beyond the scope",
    r"left as an exercise", r"you can add more", r"roughly half", r"historically", r"about 6%",
    r"it is important to note", r"studies show", r"experts agree", r"it is well known", r"obviously",
    r"clearly", r"it can be shown", r"\.\.\.", "…",
]
PROCESS = [r"\bbuilder", r"\bverif", r"\bledger", r"\bagent", r"\bfixer", r"\bround \d", r"\bround\b",
           r"\bfragment", r"\baudit", r"\bmutant", r"\bblocking", r"\bplan\b", r"\barchitect"]

print("== banned and process-word hits (visible text, scripts and pre excluded)")
for name in PAGES:
    txt = visible(BASE + name)
    for pat in BANNED + PROCESS:
        for m in re.finditer(pat, txt, flags=re.IGNORECASE):
            s = max(0, m.start() - 50)
            print(f"{name}: {pat!r} at {m.start()}: ...{txt[s:m.end() + 40]!r}")
print("== end hits")

print("== why-it-matters word counts (limit 120)")
for name in ["L01.html", "L02.html", "L03.html"]:
    html = open(BASE + name, encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', html, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", m.group(1))
    txt = re.sub(r"\s+", " ", txt).strip()
    print(name, len(txt.split()), "rhetorical?", "?" in txt)

print("== structure counts")
for name in ["L01.html", "L02.html", "L03.html"]:
    html = open(BASE + name, encoding="utf-8").read()
    tiers = re.findall(r'<div class="tier" data-tier="([a-z]+)">(.*?)</div>\s*(?=<div class="tier"|</section>)', html, flags=re.S)
    counts = {t: len(re.findall(r'class="problem"', body)) for t, body in tiers}
    sols = len(re.findall(r'<details class="solution">', html))
    items = len(re.findall(r'<li class="item"', html))
    miscs = len(re.findall(r'<li class="misconception">', html))
    print(name, "problems", counts, "solutions", sols, "quiz items", items, "misconceptions", miscs)
    heads = re.findall(r'<h2 id="(s\d+)"><span class="section-number">(\d+)</span>([^<]+)</h2>', html)
    print("  sections:", [(h[1], h[2]) for h in heads])
    print("  data-hours:", re.findall(r'data-hours="(\d+)"', html), "eyebrow:", re.findall(r'eyebrow">([^<]+)<', html))

print("== curriculum PC3 entry")
cur = json.load(open(f"{ROOT}/curriculum/curriculum.json", encoding="utf-8"))
items = cur if isinstance(cur, list) else cur.get("modules", cur.get("units", []))
pc3 = None
def walk(o):  # type: ignore[no-untyped-def]
    global pc3
    if isinstance(o, dict):
        if o.get("id") == "PC3" and pc3 is None:
            pc3 = o
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(cur)
print(json.dumps({k: v for k, v in (pc3 or {}).items() if k not in ("lessons_text",)}, ensure_ascii=False)[:2500])
