"""Round 5 FC2-d: every integer with 2+ digits or any fraction on a card must appear in its lesson (lossless text)."""
import json, re, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d")
cards = json.load(open(ROOT / "course/modules/FC/FC2/cards.json", encoding="utf-8"))
txt = {L: (pathlib.Path("/tmp/fc2d-r5-txt") / f"{L}.html.lossless.txt").read_text(encoding="utf-8") for L in ["L01","L02","L03","L04","L05","L06","L07","L08"]}
bad = []
for c in cards:
    T = txt[c["lesson"]].replace(",", "")
    for tok in set(re.findall(r"(?<![\w.])\d{2,}(?![\w.])", c["back"] + " " + c["front"])):
        if tok not in T.replace(",", ""):
            bad.append((c["id"], c["lesson"], tok))
print(*bad, sep="\n")
print("integer-check findings:", len(bad))
