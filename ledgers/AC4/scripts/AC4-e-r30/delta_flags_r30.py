"""Flags previous-round rows whose cited subject touches a file or card changed since pin 503d139."""
import json, re, sys
prev = json.load(open("/tmp/fanout-frags/AC4-e.round29.json"))["rows"]
changed_cards = {"AC4-c016", "AC4-c023", "AC4-c026", "AC4-c074", "AC4-c078", "AC4-c135", "AC4-c141"}
hunks = {"L01": [(459, 459)], "L02": [(66, 66), (71, 71), (76, 76), (86, 86), (122, 122), (127, 127), (311, 311), (330, 330), (466, 466)],
         "L03": [(64, 64), (69, 69), (88, 88), (112, 112), (328, 328), (381, 381), (385, 385), (433, 433)],
         "L04": [(51, 51), (133, 133), (350, 350)], "L06": [(72, 72), (79, 79), (86, 86), (88, 88), (140, 140), (404, 404)]}
out = []
for r in prev:
    text = r["location"] + " " + r["evidence"]
    flags = []
    cards = set(re.findall(r"AC4-c\d{3}", text))
    if cards & changed_cards:
        flags.append("changed-card:" + ",".join(sorted(cards & changed_cards)))
    for lesson in hunks:
        for m in re.finditer(rf"{lesson}\.html[^;)]*", text):
            seg = m.group(0)
            nums = [int(x) for x in re.findall(r"\d+", seg.replace(",", " "))]
            rng = []
            for a in re.findall(r"lines? (\d+)(?:\s*(?:-|to|and)\s*(\d+))?", seg):
                lo = int(a[0]); hi = int(a[1]) if a[1] else lo
                rng.append((lo, hi))
            if not rng:
                flags.append(f"{lesson}-unlocated")
            for lo, hi in rng:
                for h0, h1 in hunks[lesson]:
                    if not (hi < h0 - 3 or lo > h1 + 3):
                        flags.append(f"{lesson}-hunk-near-{h0}")
    if re.search(r"tests/labs/AC4/lab-AC4-L0[346]", text):
        flags.append("changed-lab-twin")
    if re.search(r"cards\.json", text) and not cards:
        flags.append("whole-cards-json")
    out.append((r["id"], flags))
for i, f in out:
    if f:
        print(i, f)
print("rows", len(out), "flagged", sum(1 for _, f in out if f))
