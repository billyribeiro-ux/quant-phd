import html, json, re, subprocess
REPO = "/Users/billyribeiro/.fanout/wt/verifyG1-BK4-b"
BASE, HEAD = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672", "2a805c83"
def show(path, rev):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
P = "course/modules/BK/BK4/cards.json"
old = {c["id"]: c for c in json.loads(show(P, BASE))}
new_raw = show(P, HEAD)
new = {c["id"]: c for c in json.loads(new_raw)}
print("cards base/head:", len(old), len(new), "ids equal:", set(old) == set(new))
changed = [k for k in new if old.get(k) != new[k]]
print("changed objects:", changed)
for k in changed:
    for f in sorted(set(old[k]) | set(new[k])):
        if old[k].get(f) != new[k].get(f):
            print(" ", k, f, "\n    BASE:", json.dumps(old[k].get(f), ensure_ascii=False), "\n    HEAD:", json.dumps(new[k].get(f), ensure_ascii=False))
print("fields:", sorted(next(iter(new.values())).keys()))
bk = {k: v for k, v in new.items() if k.startswith("BK4-")}
print("BK4 cards:", len(bk), "by lesson:", {l: sum(1 for v in bk.values() if v["lesson"] == l) for l in sorted({v["lesson"] for v in bk.values()})})
ids = [c["id"] for c in json.loads(new_raw)]
print("total ids unique:", len(ids) == len(set(ids)), "total cards:", len(ids))
# every L04/L05 card: numbers in front/back must appear in its lesson text
def text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s))
lessons = {l: text(show(f"course/modules/BK/BK4/{l}.html", HEAD)) for l in ["L04", "L05"]}
for k, v in bk.items():
    if v["lesson"] not in lessons:
        continue
    nums = set(re.findall(r"\d[\d,]*(?:\.\d+)?", v["front"] + " " + v["back"]))
    missing = [n for n in nums if n.replace(",", "") not in lessons[v["lesson"]].replace(",", "")]
    print(k, v["lesson"], v.get("grade"), "numbers:", sorted(nums), "missing in lesson:", missing)
