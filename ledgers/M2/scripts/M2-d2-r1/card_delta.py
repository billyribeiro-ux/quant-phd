"""Round 1, slice d2: card delta check for course/modules/M/M2/cards.json.
Usage: card_delta.py <repo_root>. Pins: previous 47a36d8c (round-10 pin), head = worktree HEAD.
Blocks are split on the file's own layout (a line ' {' opens a card, ' }' or ' },' closes it),
so cards whose text contains braces are compared too. Reports byte-level changed, added and
removed cards per lesson, duplicate ids/fronts/backs, and process words in changed or added cards."""
import collections, json, re, subprocess, sys

root = sys.argv[1]
prev = subprocess.run(["git", "-C", root, "show", "47a36d8c:course/modules/M/M2/cards.json"],
                      capture_output=True, text=True, check=True).stdout
head = subprocess.run(["git", "-C", root, "show", "HEAD:course/modules/M/M2/cards.json"],
                      capture_output=True, text=True, check=True).stdout
assert head == open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8").read(), "worktree differs from HEAD"

def blocks(txt):
    out, cur = {}, None
    for line in txt.split("\n"):
        if line == " {":
            cur = []
        elif cur is not None and line in (" }", " },"):
            blk = "\n".join(cur)
            out[re.search(r'"id": "(M2-c\d{3})"', blk).group(1)] = blk
            cur = None
        elif cur is not None:
            cur.append(line)
    return out

P, H = blocks(prev), blocks(head)
print("blocks prev", len(P), "head", len(H), "json prev", len(json.loads(prev)), "json head", len(json.loads(head)))
added, removed = sorted(set(H) - set(P)), sorted(set(P) - set(H))
changed = sorted(i for i in set(P) & set(H) if P[i] != H[i])
print("added", added)
print("removed", removed)
print("changed", changed)
for les in ("L22", "L23", "L24"):
    pl = [i for i in P if f'"lesson": "{les}"' in P[i]]
    hl = [i for i in H if f'"lesson": "{les}"' in H[i]]
    same = [i for i in pl if i in H and P[i] == H[i]]
    touched = sorted(set(pl) ^ set(hl)) + sorted(i for i in pl if i in H and P[i] != H[i])
    print(les, "prev", len(pl), "head", len(hl), "byte-identical", len(same), "touched", touched)
objs = json.loads(head)
print("dup ids", [k for k, v in collections.Counter(c["id"] for c in objs).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(c["front"].strip().lower() for c in objs).items() if v > 1])
print("dup backs", [k[:50] for k, v in collections.Counter(c["back"].strip().lower() for c in objs).items() if v > 1])
bad = re.compile(r"\b(round|fixer|verifier|ledger|ruling|slice|mutant|revis\w*|previous version)\b", re.I)
hits = [(c["id"], m.group(0)) for c in objs if c["id"] in set(changed) | set(added)
        for m in [bad.search(c["front"] + " " + c["back"])] if m]
print("process-word hits in changed/added cards", hits)
