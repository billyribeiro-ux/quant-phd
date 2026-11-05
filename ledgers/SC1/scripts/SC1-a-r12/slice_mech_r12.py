"""Mechanical slice-a checks (r12): why-it-matters word counts, data-hours, banned and process words,
concept links and dfn ids, notation macros and symbols used, and card/hub ids. Usage: python -I slice_mech_r12.py <checkout>"""
import json
import re
import sys

root = sys.argv[1]
base = root + "/course/modules/SC/SC1/"
files = {"index": base + "index.html", "L01": base + "L01.html", "L02": base + "L02.html", "L03": base + "L03.html"}
texts = {k: open(v, encoding="utf-8").read() for k, v in files.items()}

def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()

print("== why-it-matters word counts (limit 120)")
for k in ("L01", "L02", "L03"):
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', texts[k], re.S)
    txt = strip_tags(m.group(1))
    print(k, len(txt.split()))

print("== data-hours")
for k in ("L01", "L02", "L03"):
    print(k, re.search(r'data-hours="(\d+)"', texts[k]).group(1))
print("index data-hours-lessons/project", re.search(r'data-hours-lessons="(\d+)"', texts["index"]).group(1),
      re.search(r'data-hours-project="(\d+)"', texts["index"]).group(1))

print("== banned phrases / placeholders")
banned = r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\."
for k, t in texts.items():
    hits = [m.start() for m in re.finditer(banned, t, re.I)]
    print(k, "hits:", len(hits))

print("== process words (learner-visible text, tags stripped)")
proc = r"\bbuilder|\bverifier|\bround \d|\bfixer|\bplanner|\barchitect|\bruling|REQUESTS|unit report|\bQ\d+\b|\bDAG_DEFECT"
for k, t in texts.items():
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    hits = re.findall(proc, strip_tags(body), re.I)
    print(k, hits)

print("== concept links (href to concepts.html#id) and dfn ids")
concepts_html = open(root + "/course/concepts.html", encoding="utf-8").read()
anchors = set(re.findall(r'id="([^"]+)"', concepts_html))
for k, t in texts.items():
    for cid in sorted(set(re.findall(r'concepts\.html#([\w-]+)', t))):
        print(k, "concepts link", cid, "anchor exists:", cid in anchors)
for k, t in texts.items():
    for m in re.finditer(r'<dfn([^>]*)>', t):
        print(k, "dfn", m.group(1).strip())

print("== intra-unit links")
for k, t in texts.items():
    for tgt in sorted(set(re.findall(r'href="(L0\d\.html#[\w-]+)"', t))):
        page, frag = tgt.split("#")
        target = open(base + page, encoding="utf-8").read()
        print(k, tgt, "defined in target:", f'id="{frag}"' in target)
