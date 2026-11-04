"""Round-6 slice checks for M2-d2 (L22, L23, L24, cards with lesson L22-L24, later-module concept names).
Usage: python3 -I slice_checks_r6.py <repo-root>. Prints: banned/process-word hits, scope-word counts with the
context of each scope word, raw external references, cards summary and duplicate scan, and later-module concept names
found in the visible text of the three pages."""
import html
import json
import re
import sys
from html.parser import HTMLParser

root = sys.argv[1]
PAGES = ["L22", "L23", "L24"]


class Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):  # type: ignore[no-untyped-def]
        if tag in ("script", "style", "pre"):
            self.skip += 1

    def handle_endtag(self, tag):  # type: ignore[no-untyped-def]
        if tag in ("script", "style", "pre") and self.skip:
            self.skip -= 1

    def handle_data(self, data):  # type: ignore[no-untyped-def]
        if not self.skip:
            self.parts.append(data)


def visible(page: str) -> tuple[str, str]:
    raw = open(f"{root}/course/modules/M/M2/{page}.html", encoding="utf-8").read()
    v = Visible()
    v.feed(raw)
    return raw, re.sub(r"\s+", " ", html.unescape(" ".join(v.parts)))


HARD = [r"TODO", r"TBD", r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise",
        r"you can add more", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
        r"obviously", r"clearly", r"\.\.\.", r"…", r"\bbuilder\b", r"\bverifier\b", r"\bround \d", r"\bfixed in\b",
        r"\bcorrected\b", r"\brevision\b", r"\berratum\b", r"previous draft", r"\bprerequisite calculus\b",
        r"\bhistorically\b", r"\bin practice\b", r"\btypically\b", r"\bcertainly\b", r"\bwe\b", r"\byou\b"]
SCOPE = r"\b(only|all|always|every|any|same|exactly|small|smooth|most|roughly|guarante\w*|about)\b"
print("== banned and process-word hits (visible text)")
for p in PAGES:
    _, text = visible(p)
    hits = {h: len(re.findall(h, text, flags=re.I)) for h in HARD}
    print(p, "chars", len(text), "hits", {k: v for k, v in hits.items() if v} or "none")
print("== scope words with counts (context printed by page)")
for p in PAGES:
    _, text = visible(p)
    counts: dict[str, int] = {}
    for m in re.finditer(SCOPE, text, flags=re.I):
        counts[m.group(0).lower()] = counts.get(m.group(0).lower(), 0) + 1
    print(p, dict(sorted(counts.items())))
print("== raw external references")
for p in PAGES:
    raw, _ = visible(p)
    print(p, "src/href http:", re.findall(r'(?:src|href)="https?:[^"]*"', raw), "http strings:", raw.count("http"))
print("== dfn elements in slice pages")
for p in PAGES:
    raw, _ = visible(p)
    print(p, re.findall(r'<dfn[^>]*id="([^"]+)"', raw))
print("== cards")
cards = json.load(open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("total", len(cards), "dup ids", len(ids) - len(set(ids)),
      "dup fronts", len(cards) - len({c["front"] for c in cards}), "dup backs", len(cards) - len({c["back"] for c in cards}))
for c in cards:
    if c["lesson"] in ("L22", "L23", "L24"):
        print(c["id"], c["lesson"], c.get("grade"), "|", c["front"][:90])
print("slice cards:", sum(1 for c in cards if c["lesson"] in ("L22", "L23", "L24")))
print("== later-module concept names found in visible text of L22-L24")
cur = json.load(open(f"{root}/curriculum/curriculum.json", encoding="utf-8"))["concepts"]
pre = {"P0.1", "M1", "M2"}
later = [k for k, v in cur.items() if v.get("module") not in pre]
blob = " ".join(visible(p)[1] for p in PAGES).lower()
for k in sorted(later):
    key = k.replace("-", " ").lower()
    if len(key) >= 5 and (key in blob or k in blob):
        print("  ", k, cur[k].get("module"), blob.count(key))
