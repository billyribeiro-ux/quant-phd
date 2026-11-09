import json, re, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
pages = {"L07": open(sys.argv[2], encoding="utf-8").read(), "L08": open(sys.argv[3], encoding="utf-8").read()}
tok = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
missing_total = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    nums = []
    for t in tok.findall(text):
        digits = t.replace(".", "").lstrip("0")
        if len(digits) < 2 and "." not in t:
            continue  # skip single digits such as 1, 2, 0
        nums.append(t)
    lesson = pages[c["lesson"]].replace(",", "")
    miss = [t for t in nums if t not in lesson and t.replace(",", "") not in lesson]
    print(c["id"], c["lesson"], "numbers:", nums, "missing from lesson:", miss)
    missing_total += len(miss)
print("total missing numeric tokens:", missing_total)
