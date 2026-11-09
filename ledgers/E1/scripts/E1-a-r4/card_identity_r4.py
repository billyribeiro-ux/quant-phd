"""Compare slice-a cards (lessons L01-L03) between the round-3 pin and the current pin, object by object (round 4)."""
import json
import subprocess
import sys

ROOT = sys.argv[1]
OLD = "8196077d5f56c3919d33e69888176d197d378ad4"
PATH = "course/modules/E/E1/cards.json"
old = {c["id"]: c for c in json.loads(subprocess.run(["git", "-C", ROOT, "show", f"{OLD}:{PATH}"], capture_output=True, text=True, check=True).stdout)}
new_list = json.load(open(f"{ROOT}/{PATH}", encoding="utf-8"))
new = {c["id"]: c for c in new_list}
slice_a = [c for c in new_list if c["lesson"] in ("L01", "L02", "L03")]
changed = [c["id"] for c in slice_a if old.get(c["id"]) != c]
print("slice-a cards at current pin:", len(slice_a), "| with lesson L01:", sum(c["lesson"] == "L01" for c in slice_a),
      "L02:", sum(c["lesson"] == "L02" for c in slice_a), "L03:", sum(c["lesson"] == "L03" for c in slice_a))
print("slice-a cards differing from round-3 pin:", changed)
print("slice-a cards absent at round-3 pin:", [c["id"] for c in slice_a if c["id"] not in old])
print("cards in round-3 pin but not now:", [i for i in old if i not in new])
print("all cards changed vs round-3 pin:", [c["id"] + "/" + c["lesson"] for c in new_list if old.get(c["id"]) != c and c["id"] in old])
print("new ids:", [i for i in new if i not in old])
