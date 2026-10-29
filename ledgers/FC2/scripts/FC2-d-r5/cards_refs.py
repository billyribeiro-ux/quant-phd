"""Round 5 FC2-d: for each card, check every cited label exists in the card's lesson text, and every decimal number
on the card (front or back) appears in that lesson's text or in the lab output of that lesson."""
import json, re, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d")
cards = json.load(open(ROOT / "course/modules/FC/FC2/cards.json", encoding="utf-8"))
txt = {}
for L in ["L01","L02","L03","L04","L05","L06","L07","L08"]:
    txt[L] = (pathlib.Path("/tmp/fc2d-r5-txt") / f"{L}.html.txt").read_text(encoding="utf-8")
    txt[L] = txt[L].replace("\\(", "").replace("\\)", "")
label_re = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Assumption|Problem|Section|Lab|Solution)\s+([A-Z]?\d+(?:\.\d+)?(?:\([a-z]\))?)")
bad = []
for c in cards:
    L = c["lesson"]; T = txt[L]
    srcs = " ".join(str(c.get(k, "")) for k in ("back", "front", "basis"))
    for kind, num in label_re.findall(srcs):
        base = num.split("(")[0]
        pat = re.compile(re.escape(kind) + r"\s+" + re.escape(base) + r"(?![\d.])")
        if not pat.search(T):
            bad.append((c["id"], L, f"{kind} {num}", "not found in lesson"))
    for num in set(re.findall(r"(?<![\w/])\d+\.\d+", srcs)):
        if num not in T:
            bad.append((c["id"], L, num, "decimal not in lesson text"))
for b in bad: print(b)
print("checked", len(cards), "cards; findings", len(bad))
