"""PC3 slice a, round 8: link, anchor, concept-closure and DAG scan over index, L01, L02, L03."""
import json
import os
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-a"
BASE = f"{ROOT}/course/modules/PC/PC3"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
concepts_html = open(f"{ROOT}/course/concepts.html", encoding="utf-8").read()
cids = set(re.findall(r'id="([^"]+)"', concepts_html))
cur = json.load(open(f"{ROOT}/curriculum/curriculum.json", encoding="utf-8"))
mods: dict[str, dict] = {}
def walk(o):  # type: ignore[no-untyped-def]
    if isinstance(o, dict):
        if "id" in o and "prereqs" in o:
            mods.setdefault(o["id"], o)
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(cur)
closure = {"M4", "CS2", "FC2", "M1", "M2", "AC1", "CF1", "CS1", "E1", "FC1", "P0.1"}
intro_by_concept: dict[str, str] = {}
for mid, m in mods.items():
    for c in (m.get("introduces") or {}):
        intro_by_concept[c] = mid
used: set[str] = set()
for name in PAGES:
    html = open(f"{BASE}/{name}", encoding="utf-8").read()
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith("http"):
            print("EXTERNAL", name, href)
            continue
        path, _, frag = href.partition("#")
        if path == "" :
            if frag and frag not in ids:
                print("MISSING local anchor", name, href)
            continue
        target = os.path.normpath(os.path.join(BASE, path))
        if not os.path.exists(target):
            print("MISSING file", name, href, target)
            continue
        if frag:
            tid = open(target, encoding="utf-8").read()
            if path.startswith("../../../concepts.html") or target.endswith("concepts.html"):
                if frag not in cids:
                    print("MISSING concept anchor", name, href)
            elif f'id="{frag}"' not in tid:
                print("MISSING anchor", name, href)
    for cid in re.findall(r'data-concept="([^"]+)"', html):
        used.add(cid)
        if cid not in cids:
            print("UNKNOWN data-concept", name, cid)
        owner = intro_by_concept.get(cid)
        status = "in closure" if owner in closure else f"OUTSIDE closure (owner {owner})"
        print(f"concept {cid} on {name}: introduced by {owner}: {status}")
print("concept ids used:", sorted(used))
print("count of distinct concept-index ids in concepts.html:", len(cids))
hrefs_idx = re.findall(r'href="([^"]+)"', open(f"{BASE}/index.html", encoding="utf-8").read())
print("index hrefs:", hrefs_idx)
