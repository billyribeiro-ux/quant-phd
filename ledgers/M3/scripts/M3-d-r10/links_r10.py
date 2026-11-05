"""Round-10 verifier (M3 slice d): every relative href/src on project.html resolves on disk, every #fragment exists as an
id in its target page, and every data-cite key is a registry key in references/references.json. Run from the root."""

import json
import os
import re

PAGE = "course/modules/M/M3/project.html"
base = os.path.dirname(PAGE)
text = open(PAGE, encoding="utf-8").read()
refs = {e.get("key") for e in json.load(open("references/references.json", encoding="utf-8"))["entries"]}
targets = re.findall(r'(?:href|src)="([^"]+)"', text)
bad = []
for t in sorted(set(targets)):
    if t.startswith(("http://", "https://", "mailto:", "data:")):
        bad.append(("EXTERNAL", t))
        continue
    path, _, frag = t.partition("#")
    target = os.path.normpath(os.path.join(base, path)) if path else PAGE
    if not os.path.exists(target):
        bad.append(("MISSING", t))
        continue
    if frag and target.endswith(".html"):
        if not re.search(r'id="%s"' % re.escape(frag), open(target, encoding="utf-8").read()):
            bad.append(("NO_ANCHOR", t))
print("distinct href/src:", len(set(targets)), "problems:", bad)
cites = re.findall(r'data-cite="([^"]+)"', text)
print("data-cite keys:", cites, "all in registry:", all(c in refs for c in cites))
