"""Round 11: card-level delta of course/modules/E/E4/cards.json between the round-10 pin and HEAD (11d7077).

Reads the two versions from git (argv: old-rev new-rev) and prints, per card id, whether it is
new, removed, changed (which fields), or byte-identical. Run from the checkout root."""
import json, subprocess, sys

PATH = "course/modules/E/E4/cards.json"

def load(rev):
    raw = subprocess.run(["git", "show", f"{rev}:{PATH}"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)

old = {c["id"]: c for c in load(sys.argv[1])}
new_list = load(sys.argv[2])
new = {c["id"]: c for c in new_list}
print(f"old cards {len(old)} new cards {len(new)}")
for cid in sorted(set(old) | set(new)):
    if cid not in old:
        print(f"NEW {cid} lesson={new[cid]['lesson']}")
    elif cid not in new:
        print(f"REMOVED {cid} lesson={old[cid]['lesson']}")
    else:
        fields = [k for k in sorted(set(old[cid]) | set(new[cid])) if old[cid].get(k) != new[cid].get(k)]
        if fields:
            print(f"CHANGED {cid} lesson={new[cid]['lesson']} fields={','.join(fields)}")
print("order of ids in new file:", " ".join(c["id"] for c in new_list if c["id"] in ("E4-c055", "E4-c236", "E4-c248", "E4-c249", "E4-c250")))
