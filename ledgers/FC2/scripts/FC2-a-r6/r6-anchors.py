# Round-6: every href/src in the four slice-a pages resolves to a file, and every #anchor to an id in its target.
import os, re, sys
ROOT = sys.argv[1]
BASE = os.path.join(ROOT, "course/modules/FC/FC2")
pages = ["index.html", "L01.html", "L02.html", "L03.html"]
ids_cache = {}
def ids_of(path):
    if path not in ids_cache:
        s = open(path, encoding="utf-8").read()
        ids_cache[path] = set(re.findall(r'\sid="([^"]+)"', s))
    return ids_cache[path]
checked = 0; missing_files = []; missing_anchors = []
for pg in pages:
    src = open(os.path.join(BASE, pg), encoding="utf-8").read()
    for href in re.findall(r'href="([^"]+)"', src):
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        target, _, frag = href.partition("#")
        tpath = os.path.normpath(os.path.join(BASE, target)) if target else os.path.join(BASE, pg)
        checked += 1
        if not os.path.exists(tpath):
            missing_files.append((pg, href)); continue
        if frag and tpath.endswith(".html") and frag not in ids_of(tpath):
            missing_anchors.append((pg, href))
print("hrefs checked", checked, "missing files", len(missing_files), "missing anchors", len(missing_anchors))
for x in missing_files + missing_anchors:
    print("BAD", x)
