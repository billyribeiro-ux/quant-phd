"""Check every same-page href="#id" target exists, and every relative href path exists (project.html only)."""
import os, re
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d"
P = f"{ROOT}/course/modules/E/E4/project.html"
t = open(P, encoding="utf-8").read()
ids = set(re.findall(r'\sid="([^"]+)"', t))
anchors = set(re.findall(r'href="#([^"]+)"', t))
print("same-page anchors:", len(anchors), "missing:", sorted(a for a in anchors if a not in ids))
rel = set(re.findall(r'href="([^"#][^"]*)"', t))
bad = []
for h in sorted(rel):
    path = os.path.normpath(os.path.join(os.path.dirname(P), h.split("#")[0]))
    if not os.path.exists(path):
        bad.append(h)
print("relative hrefs:", len(rel), "missing files:", bad)
frag = [h for h in rel if "#" in h]
for h in sorted(frag):
    file, anchor = h.split("#", 1)
    path = os.path.normpath(os.path.join(os.path.dirname(P), file))
    if os.path.exists(path) and anchor not in open(path, encoding="utf-8").read():
        print("fragment target missing:", h)
print("data-cite keys:", re.findall(r'data-cite="([^"]+)"', t))
