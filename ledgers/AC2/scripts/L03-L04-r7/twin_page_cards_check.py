import html, json, re, subprocess
root = "/tmp/verify-ac2r7-l34"
for n in ("03", "04"):
    page = open(f"{root}/course/modules/AC/AC2/L{n}.html", encoding="utf-8").read()
    tw = open(f"{root}/tests/labs/AC2/lab-AC2-L{n}-1.py", encoding="utf-8").read().splitlines()
    miss = [l for l in tw if l.strip() and html.escape(l, quote=False) not in page and l not in page]
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip()
    print("L" + n, "twin lines", len(tw), "missing from page", len(miss), "expected block lines", len(exp.splitlines()))
new = json.load(open(f"{root}/course/modules/AC/AC2/cards.json"))
old = json.loads(subprocess.check_output(["git", "-C", root, "show", "ff9284f:course/modules/AC/AC2/cards.json"]))
print("cards", len(new), "contiguous", [c["id"] for c in new] == [f"AC2-c{i:03d}" for i in range(1, 141)])
print("unique fronts", len({c["front"] for c in new}) == 140, "unique backs", len({c["back"] for c in new}) == 140)
ob = {c["id"]: c for c in old}
print("changed vs ff9284f", [c["id"] for c in new if ob.get(c["id"]) != c])
mine = [c for c in new if c["lesson"] in ("L03", "L04")]
print("L03/L04 cards", len(mine), "byte-identical to ff9284f", all(ob[c["id"]] == c for c in mine))
