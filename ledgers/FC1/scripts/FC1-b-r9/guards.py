import json, subprocess
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
OLD, NEW = "4540351dc664559cdfd371b908f2b4e644cf4297", "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
def changed(paths):
    r = subprocess.run(["git", "-C", W, "diff", "--name-only", OLD, NEW, "--", *paths], capture_output=True, text=True)
    return [x for x in r.stdout.split("\n") if x]
def card_map(rev):
    raw = subprocess.run(["git", "-C", W, "show", f"{rev}:course/modules/FC/FC1/cards.json"], capture_output=True, text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(raw)}
OLDC, NEWC = card_map(OLD), card_map(NEW)
def cards_identical(ids):
    return {i: (i in NEWC and OLDC.get(i) == NEWC.get(i)) for i in ids}
if __name__ == "__main__":
    files = ["course/modules/FC/FC1/L01.html", "course/modules/FC/FC1/L03.html", "course/modules/FC/FC1/L04.html",
             "course/modules/FC/FC1/L05.html", "course/modules/FC/FC1/index.html", "course/modules/FC/FC1/project.html",
             "tests/labs/FC1", "references", "notation", "course/assets/js", "course/assets/data", "tools", "curriculum",
             "course/modules/FC/FC2", "course/assets/data/market"]
    for f in files:
        print("changed", f, "->", changed([f]))
    print("cards.json changed hunks ids removed:", sorted(set(OLDC) - set(NEWC)), "added:", sorted(set(NEWC) - set(OLDC)))
    modified = [i for i in NEWC if OLDC.get(i) != NEWC[i]]
    print("cards with modified object:", modified)
    print("identical check, all entries except c173:", all(v for k, v in cards_identical(list(NEWC)).items()))
    ids = ["FC1-c016","FC1-c050","FC1-c052","FC1-c053","FC1-c054","FC1-c061","FC1-c062","FC1-c064","FC1-c066","FC1-c067","FC1-c069","FC1-c072","FC1-c075","FC1-c082","FC1-c089","FC1-c090","FC1-c097","FC1-c098","FC1-c099","FC1-c100","FC1-c101","FC1-c103","FC1-c105","FC1-c142","FC1-c153","FC1-c154","FC1-c155","FC1-c156","FC1-c169","FC1-c170","FC1-c171","FC1-c172"]
    print("selected cited cards identical:", cards_identical(ids))
    print("c125 absent, c173 absent, c174 absent:", [i not in NEWC for i in ("FC1-c125","FC1-c173","FC1-c174")])
