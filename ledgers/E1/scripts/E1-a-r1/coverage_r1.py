import json, re, sys
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E1/cards.json", encoding="utf-8"))
for L in ("L01", "L02", "L03"):
    html = open(f"{root}/course/modules/E/E1/{L}.html", encoding="utf-8").read()
    blocks = re.findall(r'block-title[^>]*>((?:(?!</span>).)*?)<span class="name">', html)
    labels = []
    for t in blocks:
        m = re.search(r"(Definition|Proposition|Remark|Example|Theorem|Corollary|Lemma)\s+(\d\.\d)", t)
        if m:
            labels.append(f"{m.group(1)} {m.group(2)}")
    lesson_cards = [c for c in cards if c["lesson"] == L]
    print(f"== {L}: {len(labels)} labelled blocks, {len(lesson_cards)} cards")
    for lab in labels:
        hits = [c["id"] for c in lesson_cards if re.search(r"\(" + re.escape(lab) + r"[)\s,;]", c["back"] + " ") or re.search(re.escape(lab) + r"\b", c["back"] + " " + c["front"])]
        print(f"  {lab}: {hits if hits else 'NO CARD'}")
    unc = [c["id"] for c in lesson_cards if not re.search(r"(Definition|Proposition|Remark|Example|Lemma|Lab|Problem|Section|Misconception|Corollary|Theorem)", c["back"] + c["front"])]
    print("  cards with no label or lab/section citation:", unc)
