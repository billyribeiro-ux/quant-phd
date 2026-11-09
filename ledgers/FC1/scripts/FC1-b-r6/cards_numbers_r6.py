import json, re, html, pathlib
D = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b/course/modules/FC/FC1")
cards = json.loads((D / "cards.json").read_text(encoding="utf-8"))
def text(p):
    t = (D / p).read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)
T = {"L04": text("L04.html"), "L05": text("L05.html"), "L03": text("L03.html")}
for c in cards:
    if c["lesson"] not in T:
        continue
    lt = T[c["lesson"]]
    nums = set(re.findall(r"\d[\d,\.]*\d|\d", c["front"] + " " + c["back"]))
    missing = [n for n in sorted(nums) if n.replace(",", "") not in lt.replace(",", "")]
    if missing:
        print(c["id"], c["lesson"], "numbers not in lesson text:", missing)
print("scan complete")
