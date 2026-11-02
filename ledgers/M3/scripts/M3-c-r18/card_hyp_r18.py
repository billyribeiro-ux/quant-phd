import json, re, sys, pathlib, html
root = pathlib.Path(sys.argv[1]); base = root / "course/modules/M/M3"
cards = json.load(open(base / "cards.json", encoding="utf-8"))
pat = re.compile(r"\((Definition|Theorem|Proposition|Corollary|Lemma|Remark) ([0-9]+(?:\.[0-9]+)?)(\([a-c]\))?\)")
blocks = {}
for L in ["L02","L03","L04","L05","L07","L08","L09"]:
    t = (base / f"{L}.html").read_text(encoding="utf-8")
    for m in re.finditer(r'<span class="block-title[^"]*"[^>]*>(.*?)</span>', t, re.S):
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
        seg = html.unescape(re.sub(r"<[^>]+>", " ", t[m.end(): m.end()+1500])); seg = re.sub(r"\s+", " ", seg)
        blocks[(L, title.split(" (")[0].strip())] = seg
for c in cards:
    L = c["lesson"]; back = c["back"]; front = c["front"]
    txt = front + " " + back
    refs = pat.findall(back)
    need = []
    for kind, n, _ in refs:
        seg = blocks.get((L, f"{kind} {n}"), "")
        if re.search(r"Assuming F1|Assumptions? F1", seg[:400]):
            need.append(f"{kind} {n}")
    has = "F1" in txt
    if need and not has:
        print("NO_HYP", c["id"], L, c.get("grade","-"), need, "|", back[:110])
    if c.get("grade") == "T" and not need and not has and L in ("L07","L08","L09"):
        print("T_NOHYP_CHECK", c["id"], L, "|", back[:110])
