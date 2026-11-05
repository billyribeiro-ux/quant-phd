"""Card-level delta of course/modules/FC/FC2/cards.json between two JSON files (argv[1] previous, argv[2] current)."""
import json
import sys

prev = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
now_list = json.load(open(sys.argv[2], encoding="utf-8"))
now = {c["id"]: c for c in now_list}
changed = sorted(i for i in now if i in prev and now[i] != prev[i])
added = sorted(i for i in now if i not in prev)
removed = sorted(i for i in prev if i not in now)
print("changed:", changed)
print("added:", added)
print("removed:", removed)
for i in changed:
    for k in sorted(set(prev[i]) | set(now[i])):
        if prev[i].get(k) != now[i].get(k):
            print(i, k, "| prev:", prev[i].get(k), "| now:", now[i].get(k))
