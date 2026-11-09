import json, sys, collections, re
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("records", len(d))
ids = [x["id"] for x in d]
print("dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
fr = collections.Counter(x["front"].strip().lower() for x in d)
print("dup fronts", [k for k, v in fr.items() if v > 1])
bad = []
for x in d:
    keys = set(x)
    if x["grade"] not in ("T", "A", "B", "C", "D", "X"):
        bad.append((x["id"], "grade", x["grade"]))
    if x["grade"] != "T" and "basis" not in x:
        bad.append((x["id"], "missing basis"))
    if x["grade"] == "T" and "basis" in x:
        bad.append((x["id"], "T with basis"))
    if x["lesson"] not in {"L%02d" % i for i in range(1, 12)}:
        bad.append((x["id"], "lesson", x["lesson"]))
    if set(keys) - {"id", "lesson", "front", "back", "grade", "basis"}:
        bad.append((x["id"], "extra keys", sorted(keys)))
print("rule violations", bad)
nums = [int(m) for x in d for m in re.findall(r"CS2-c(\d+)", x["id"])]
print("id number range", min(nums), max(nums), "count", len(nums))
