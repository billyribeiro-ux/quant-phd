"""Round-8 verifier (FC1-c): mechanical card checks against the current lesson text (no edits)."""
import json, re, collections, sys, pathlib
ROOT = pathlib.Path(sys.argv[1]); S = pathlib.Path(sys.argv[2])
cards = json.loads((ROOT / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
lessons = {n: (S / "lessons_text" / f"{n}.txt").read_text(encoding="utf-8") for n in ["L01", "L02", "L03", "L04", "L05"]}
alltext = "\n".join(lessons.values())
print("cards", len(cards))
ids = [c["id"] for c in cards]
print("ids unique", len(set(ids)) == len(ids), "gaps:", sorted(set(f"FC1-c{i:03d}" for i in range(1, 143)) - set(ids)))
print("fronts unique", len(set(c["front"] for c in cards)) == len(cards), "backs unique", len(set(c["back"] for c in cards)) == len(cards))
for c in cards:
    lt = lessons[c["lesson"]]
    # citations in parentheses at the end of the back
    cites = re.findall(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)", c["back"])
    for cite in cites:
        for part in [p.strip() for p in cite.split(";")]:
            m = re.match(r"^(Definition|Proposition|Remark|Example|Assumption|Corollary|Lemma|Problem|Section|Lab|misconception|Assumption A|Assumption B|Assumption)\s*([A-Z]?[0-9][0-9.()a-z′']*)?", part)
            if not m:
                continue
            label = part.split(",")[0].split(" (")[0].strip()
            if label.startswith("Lab"):
                ok = "Lab 1" in lt or "Lab 2" in lt or "Lab 3" in lt or "Lab 1" in alltext
                continue
            if label.startswith("misconception"):
                num = re.search(r"\d", label)
                if num and f"misconception {num.group()}" not in lt.lower() and f"Misconception {num.group()}" not in lt:
                    print(f"{c['id']} {c['lesson']}: cite '{part}' not found in {c['lesson']}")
                continue
            key = part.split(",")[0].split(";")[0].strip()
            if key and not re.search(re.escape(key.split(" (")[0].rstrip(")")), alltext):
                print(f"{c['id']} {c['lesson']}: cite label '{key}' absent from all lessons")
            elif key and re.search(re.escape(key.split(" (")[0].rstrip(")")), lt) is None:
                print(f"{c['id']} {c['lesson']}: cite label '{key}' absent from its own lesson {c['lesson']} (present elsewhere)")
    # numbers in the back and front must appear in the card's lesson
    text = c["front"] + " " + c["back"]
    for num in re.findall(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?", text):
        norm = num.replace(",", "")
        if norm in ("1",): continue
        if norm not in lt.replace(",", "") and norm not in lt:
            print(f"{c['id']} {c['lesson']}: number '{num}' not in its lesson")
