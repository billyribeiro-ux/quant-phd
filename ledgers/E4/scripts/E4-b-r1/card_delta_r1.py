import json, subprocess, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-E4-b"
PATH = "course/modules/E/E4/cards.json"
def load(rev):
    txt = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{PATH}"], capture_output=True, text=True, check=True).stdout
    return json.loads(txt)
old = load("e919577b"); new = load("HEAD")
oid = {c["id"]: c for c in old}; nid = {c["id"]: c for c in new}
print("counts old/new:", len(old), len(new))
print("ids unique old/new:", len(oid) == len(old), len(nid) == len(new))
removed = sorted(set(oid) - set(nid)); added = sorted(set(nid) - set(oid))
print("REMOVED:", [(i, oid[i]["lesson"]) for i in removed])
print("ADDED:", [(i, nid[i]["lesson"]) for i in added])
changed = [i for i in sorted(set(oid) & set(nid)) if oid[i] != nid[i]]
print("CHANGED:", [(i, nid[i]["lesson"]) for i in changed])
print("ORDER old==new minus removed/added:", [c["id"] for c in old if c["id"] in nid] == [c["id"] for c in new if c["id"] in oid])
print("UNCHANGED count:", len(set(oid) & set(nid)) - len(changed))
print("--- field diffs for changed cards")
for i in changed:
    a, b = oid[i], nid[i]
    keys = sorted(set(a) | set(b))
    diffk = [k for k in keys if a.get(k) != b.get(k)]
    print(i, b["lesson"], "fields:", diffk, "grade old/new:", a.get("grade"), b.get("grade"), "basis old/new:", a.get("basis"), "|", b.get("basis"))
print("--- new cards lacking grade or basis")
for i in added:
    c = nid[i]; print(i, c["lesson"], "grade" in c, "basis" in c, c.get("grade"), c.get("basis"))
