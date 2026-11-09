# DAG check for M2 lessons L07-L12 (python -I from checkout root): every concept link, its owner module,
# whether the link target exists in the file it names, and whether any later-module concept is linked.
import json, re
d = json.load(open("curriculum/curriculum.json", encoding="utf-8"))
owner = {k: v["module"] for k, v in d["concepts"].items()}
order = [m for m in d["topological_order"]] if isinstance(d.get("topological_order"), list) else None
for n in range(7, 13):
    src = open(f"course/modules/M/M2/L{n:02d}.html", encoding="utf-8").read()
    for m in re.finditer(r'<a class="concept" data-concept="([^"]+)" href="([^"]+)">([^<]*)</a>', src):
        cid, href, text = m.groups()
        target = href.split("#")[-1]
        local = href.split("#")[0] in ("", f"L{n:02d}.html")
        print(f"L{n:02d} concept={cid} owner={owner.get(cid)} text={text!r} href={href} anchor_in_file={'def-'+cid in src if local else 'external'}")
print("M2-owned concepts:", sorted(k for k, v in owner.items() if v == "M2"))
