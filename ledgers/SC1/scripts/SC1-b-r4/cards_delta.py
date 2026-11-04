# Usage: python -I cards_delta.py <prev_cards.json> <cur_cards.json>
# Lists card ids whose content changed between two pins, with lesson tags.
import json
import sys

prev = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
cur_list = json.load(open(sys.argv[2], encoding="utf-8"))
cur = {c["id"]: c for c in cur_list}
print("prev count", len(prev), "cur count", len(cur_list), "cur unique", len(cur))
print("removed", sorted(set(prev) - set(cur)))
print("added", sorted(set(cur) - set(prev)))
changed = [k for k in sorted(set(prev) & set(cur)) if prev[k] != cur[k]]
print("changed", len(changed))
for k in changed:
    print(k, cur[k]["lesson"], "|", "front_changed" if prev[k]["front"] != cur[k]["front"] else "", "back_changed" if prev[k]["back"] != cur[k]["back"] else "", "cite_changed" if prev[k]["cite"] != cur[k]["cite"] else "")
