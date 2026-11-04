"""LX1-a r1: concept owners (curriculum.json concepts dict), module titles, and page concept links for hub, L01, L02."""
import json, re, pathlib
cur = json.load(open("curriculum/curriculum.json", encoding="utf-8"))
mods = {m["id"]: m for part in cur["parts"] for m in part["modules"]}
for mid in ["FC1", "E5", "E1", "M1", "M2", "P0.1", "LX1"]:
    m = mods[mid]
    print("MODULE", mid, repr(m["title"]), m["tier"], m["hours"], m["prereqs"], "introduces", m["introduces"])
concepts = cur["concepts"]
pages = ["course/modules/LX/LX1/index.html", "course/modules/LX/LX1/L01.html", "course/modules/LX/LX1/L02.html"]
for page in pages:
    text = pathlib.Path(page).read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r'data-concept="([^"]+)"', text)))
    anchors = sorted(set(re.findall(r'concepts\.html#([^"]+)"', text)))
    print("PAGE", page)
    for i in ids:
        c = concepts.get(i)
        print("   data-concept", i, "owner", c and c["module"], "name", c and c["name"], "| anchor-linked:", i in anchors)
    print("   anchors without data-concept:", [a for a in anchors if a not in ids])
    for i in anchors:
        if i not in concepts:
            print("   ANCHOR NOT IN CURRICULUM:", i)
