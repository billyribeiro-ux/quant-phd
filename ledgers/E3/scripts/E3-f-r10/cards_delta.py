"""Round 10 card delta for E3 slice f: compare cards.json at the round-8 pin with the current pin.

Usage: python3 -I -W error cards_delta.py <checkout_root>
Prints the ids added, removed or changed, and the ids of cards in lessons L01-L04 that are unchanged.
"""
import json
import subprocess
import sys

root = sys.argv[1]
OLD = "2d755599d8d74df292e3e43025f0458c4053802e"
PATH = "course/modules/E/E3/cards.json"


def load(text: str) -> dict[str, dict]:
    data = json.loads(text)
    out: dict[str, dict] = {}
    for card in data:
        if card["id"] in out:
            raise SystemExit(f"DUPLICATE ID {card['id']}")
        out[card["id"]] = card
    return out


old_text = subprocess.run(["git", "-C", root, "show", f"{OLD}:{PATH}"], capture_output=True, text=True, check=True).stdout
with open(f"{root}/{PATH}", encoding="utf-8") as fh:
    new_text = fh.read()
old = load(old_text)
new = load(new_text)
added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))
changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
unchanged = sorted(k for k in set(old) & set(new) if old[k] == new[k])
print("old count", len(old), "new count", len(new))
print("added", added)
print("removed", removed)
print("changed", changed)
print("unchanged count", len(unchanged))
for k in changed:
    print("CHANGED", k, "lesson", new[k]["lesson"])
