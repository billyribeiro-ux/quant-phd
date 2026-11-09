import json, subprocess, sys
R = sys.argv[1]
base = json.loads(subprocess.run(["git", "show", "329c1d7f:course/modules/M/M4/cards.json"], capture_output=True, text=True, cwd=R, check=True).stdout)
head = json.load(open(R + "/course/modules/M/M4/cards.json", encoding="utf-8"))
bm = {c["id"]: c for c in base}
hm = {c["id"]: c for c in head}
def ser(c): return json.dumps(c, ensure_ascii=False, sort_keys=False)
for L in ("L05", "L06", "L07"):
    bl = [c["id"] for c in base if c["lesson"] == L]
    hl = [c["id"] for c in head if c["lesson"] == L]
    same = [i for i in hl if i in bm and ser(bm[i]) == ser(hm[i])]
    print(L, "base", len(bl), "head", len(hl), "removed", [i for i in bl if i not in hl], "records byte-identical", len(same), "of", len(hl), "changed", [i for i in hl if i in bm and ser(bm[i]) != ser(hm[i])])
ids = ["M4-c088", "M4-c089", "M4-c092", "M4-c093", "M4-c097", "M4-c101", "M4-c105", "M4-c107", "M4-c108", "M4-c191"]
print("B6-26 ids identical:", all(ser(bm[i]) == ser(hm[i]) for i in ids), ids)
allc = [c["id"] for c in head if c["lesson"] in ("L05", "L06", "L07")]
print("ids in L05-L07 whose record differs from base:", [i for i in allc if i in bm and ser(bm[i]) != ser(hm[i])])
print("duplicate ids in head:", len(head) - len(hm))
