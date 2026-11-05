"""Round-10: every in-page href="#id" resolves to an id; every data-cite key exists in references/references.json;
every relative href to another page or asset exists on disk. Usage: python anchors_refs_r10.py <repo_root>"""

import html.parser
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = root / "course/modules/BK/BK4/project.html"
text = page.read_text(encoding="utf-8")


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.cites = set(), [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if "data-cite" in a:
            self.cites.append(a["data-cite"])


p = P()
p.feed(text)
bad = []
for h in p.hrefs:
    if h.startswith("#"):
        if h[1:] not in p.ids:
            bad.append(("anchor", h))
    elif not re.match(r"^(https?:|mailto:)", h):
        target = (page.parent / h.split("#")[0]).resolve()
        if not target.exists():
            bad.append(("file", h))
refs = json.loads((root / "references/references.json").read_text(encoding="utf-8"))
keys = {r.get("key") for r in refs["entries"]}
missing_cites = [c for c in p.cites if c not in keys]
print(f"anchors and links: {len(p.hrefs)} hrefs, bad: {bad}")
print(f"data-cite keys: {p.cites}, missing from references.json: {missing_cites}")
print("ANCHORS_REFS PASS" if not bad and not missing_cites else "ANCHORS_REFS FAIL")
