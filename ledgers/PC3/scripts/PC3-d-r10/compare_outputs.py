import html, re, sys
root = sys.argv[1]
for n in range(1, 7):
    page = open(f"{root}/course/modules/PC/PC3/L0{n}.html", encoding="utf-8").read()
    text = html.unescape(re.sub(r"<[^>]+>", "", page))
    out = open(f"/tmp/pc3d_r10/lab_L0{n}.out", encoding="utf-8").read().splitlines()
    missing = [l for l in out if l.strip() and l.strip() not in text]
    print(f"L0{n}: {len(out)} output lines, {len(missing)} not found verbatim in page text")
    for l in missing:
        print("   MISSING:", l)
