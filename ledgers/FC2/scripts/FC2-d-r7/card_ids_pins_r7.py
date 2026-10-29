import json, subprocess
P = "course/modules/FC/FC2/cards.json"
for c in ["04626e9", "9fd6aed", "0d2d0f3"]:
    raw = subprocess.run(["git", "show", f"{c}:{P}"], capture_output=True, text=True, cwd="/Users/billyribeiro/.fanout/wt/verifyC7-FC2-d").stdout
    d = json.loads(raw)
    ids = sorted(int(x["id"].split("c")[-1]) for x in d)
    print(c, len(d), "missing", [i for i in range(1, max(ids) + 1) if i not in ids])
