"""For every card: numeric tokens and cross-reference labels (Lemma/Proposition/Theorem/Corollary/Remark/Definition/Problem/Assumption/Lab) must occur in the card's own lesson text.
Usage: python -I scan_refs_r12.py <cards.json> <out_dir>   (out_dir holds L01.txt..L08.txt rendered by html_to_text.py)"""
import json, re, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
texts = {f"L0{i}": open(f"{out}/L0{i}.txt", encoding="utf-8").read() for i in range(1, 9)}
norm = lambda s: re.sub(r"\s+", " ", s.replace("\\", "").replace("(", " ").replace(")", " ")).lower()
ntexts = {k: norm(v) for k, v in texts.items()}
num_re = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:[eE]-?\d+)?")
ref_re = re.compile(r"(Lemma|Proposition|Theorem|Corollary|Remark|Definition|Problem|Assumption|Assumptions|Section|Lab|Hypothesis) ?([A-Z]?\d+(?:\.\d+)?|[A-Z]\d*)")
absent = []; n_num = 0; n_ref = 0; refs_absent = []
for c in cards:
    lesson = c["lesson"]
    text = ntexts[lesson]
    card_text = c["front"] + " " + c["back"]
    for tok in set(num_re.findall(card_text)):
        if tok in ("1", "0", "2"):
            continue
        n_num += 1
        if norm(tok) not in text and norm(tok) not in norm(card_text.replace(tok, "")):
            absent.append((c["id"], tok))
    for m in set(ref_re.findall(card_text)):
        label = " ".join(x for x in m if x)
        n_ref += 1
        if norm(label) not in text:
            refs_absent.append((c["id"], label))
print("numeric tokens checked", n_num, "absent from own lesson text", len(absent), absent[:40])
print("reference labels checked", n_ref, "absent from own lesson text", len(refs_absent), refs_absent[:60])
