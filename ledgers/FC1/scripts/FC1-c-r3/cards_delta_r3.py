"""Round-3 card delta (verifier D3): which cards changed between the round-2 pin and the round-3 pin, and whether the
round-2 sample cards and lesson files are byte-identical. Usage: cards_delta_r3.py <old cards.json> <new cards.json> <checkout root>."""
import hashlib
import json
import subprocess
import sys

old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
changed = sorted(i for i in old if i in new and old[i] != new[i])
removed = sorted(set(old) - set(new))
added = sorted(set(new) - set(old))
print("changed:", changed)
print("removed:", removed)
print("added:", added)
sample = ["FC1-c001", "FC1-c011", "FC1-c021", "FC1-c031", "FC1-c041", "FC1-c051", "FC1-c061", "FC1-c071", "FC1-c081",
          "FC1-c091", "FC1-c101", "FC1-c111", "FC1-c010", "FC1-c012", "FC1-c016", "FC1-c037", "FC1-c043", "FC1-c054",
          "FC1-c089", "FC1-c029", "FC1-c030", "FC1-c033", "FC1-c034", "FC1-c095", "FC1-c096", "FC1-c097", "FC1-c098",
          "FC1-c067", "FC1-c068", "FC1-c082", "FC1-c083", "FC1-c084", "FC1-c092", "FC1-c093"]
print("round-2 sample and numeric cards unchanged:", all(old[i] == new[i] for i in sample if i in old and i in new),
      "missing:", [i for i in sample if i not in new])
root = sys.argv[3]
for f in ["course/modules/FC/FC1/L01.html", "course/modules/FC/FC1/L02.html", "course/modules/FC/FC1/L03.html",
          "course/modules/FC/FC1/L04.html", "course/modules/FC/FC1/L05.html"]:
    prev = subprocess.run(["git", "-C", root, "show", f"c737272f5bdef4a027417989cd52254555e8a0bb:{f}"],
                          capture_output=True, check=True).stdout
    cur = open(f"{root}/{f}", "rb").read()
    print(f, "byte-identical since round-2 pin:", prev == cur, hashlib.sha256(cur).hexdigest()[:16])
