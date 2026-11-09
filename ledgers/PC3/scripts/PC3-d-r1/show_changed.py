import json, subprocess
P = "course/modules/PC/PC3/cards.json"
old = {c["id"]: c for c in json.loads(subprocess.check_output(["git", "show", f"5db69a9b:{P}"]))}
new = json.loads(open(P, encoding="utf-8").read())
changed = {"PC3-c005","PC3-c050","PC3-c053","PC3-c055","PC3-c062","PC3-c067","PC3-c081","PC3-c090","PC3-c091","PC3-c096","PC3-c097","PC3-c110","PC3-c112","PC3-c116","PC3-c123","PC3-c124","PC3-c148","PC3-c174","PC3-c175","PC3-c178"}
for c in new:
    if c["id"] in changed or c["id"] not in old:
        print(json.dumps(c, ensure_ascii=False))
