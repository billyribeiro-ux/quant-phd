"""Round-1 closing-delta checks on cards.json and the changed lesson/index text (run with -I from the checkout root).
Prints: card ids and duplicates, cited Definition/Proposition/Remark/Assumption/Problem labels absent from the card's
own lesson, and every whole numeric token of each card absent from its own lesson text."""
import html, json, re, collections, sys, os
root = sys.argv[1]
cards = json.load(open(os.path.join(root, "course/modules/E/E5/cards.json"), encoding="utf-8"))
ids = [c["id"] for c in cards]
nums = sorted(int(i.split("c")[-1]) for i in ids)
print("cards", len(cards), "unique ids", len(set(ids)), "missing in 1..max", sorted(set(range(1, max(nums) + 1)) - set(nums)))
print("dup fronts", [k for k, v in collections.Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("dup backs", [k[:60] for k, v in collections.Counter(c["back"].strip().lower() for c in cards).items() if v > 1])
def plain(p):
    t = open(os.path.join(root, p), encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))
L = {f"L0{n}": plain(f"course/modules/E/E5/L0{n}.html") for n in range(1, 9)}
bad = []
for c in cards:
    text = c["back"] + " " + c["front"] + " " + c.get("basis", "")
    for a, b in re.findall(r"(Remark|Definition|Proposition|Theorem|Assumption|Problem|Lemma|Example) (\d+\.\d+|[A-Z]\d+|\d+)", text):
        if f"{a} {b}" not in L[c["lesson"]]:
            bad.append((c["id"], c["lesson"], f"{a} {b}"))
print("cited labels absent from own lesson:", bad)
tok = re.compile(r"(?<![A-Za-z_\\])\d+(?:[./]\d+)*(?:\.\d+)?")
miss = []
for c in cards:
    for m in set(tok.findall(c["front"] + " " + c["back"] + " " + c.get("basis", ""))):
        pat = r"(?<![\d.])" + re.escape(m) + r"(?![\d])"
        if not re.search(pat, L[c["lesson"]]) and not re.search(pat, L[c["lesson"]].replace(",", "")):
            miss.append((c["id"], c["lesson"], m))
print("numeric tokens absent from own lesson (whole-token):", miss)
