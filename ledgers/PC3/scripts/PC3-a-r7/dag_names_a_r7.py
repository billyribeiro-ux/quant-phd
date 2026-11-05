"""Round 7: concept names (curriculum.json concepts) that occur in slice prose, with owner and closure membership (run with -I)."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, "tools")
import coursekit  # noqa: E402

ROOT = Path(".").resolve()
closure = set(coursekit.prerequisite_closure("PC3")) | {"PC3"}
cur = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))
concepts = cur["concepts"]


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.p, self.k = [], 0

    def handle_starttag(self, t, a):
        if t in ("script", "style"):
            self.k += 1

    def handle_endtag(self, t):
        if t in ("script", "style"):
            self.k -= 1

    def handle_data(self, d):
        if not self.k:
            self.p.append(d)


text = ""
for pg in ["index.html", "L01.html", "L02.html", "L03.html"]:
    t = T()
    t.feed((ROOT / "course/modules/PC/PC3" / pg).read_text(encoding="utf-8"))
    text += " " + " ".join(t.p)
low = " " + re.sub(r"\s+", " ", text).lower() + " "
for cid, meta in sorted(concepts.items()):
    name = meta["name"].lower()
    core = re.sub(r"\s*\(.*?\)", "", name).strip()
    if len(core) < 6:
        continue
    if re.search(r"(?<![a-z])" + re.escape(core) + r"(?![a-z])", low):
        mod = meta["module"]
        print(f"{cid} | '{meta['name']}' | owner {mod} | in closure: {mod in closure}")
