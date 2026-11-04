import json, re, collections
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b/course/modules/LX/LX1"
cards = json.load(open(f"{ROOT}/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
print("total cards", len(cards), "duplicate ids", [k for k, v in ids.items() if v > 1])
fronts = collections.Counter(c["front"] for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
pages = {"L03": open(f"{ROOT}/L03.html", encoding="utf-8").read(), "L04": open(f"{ROOT}/L04.html", encoding="utf-8").read()}
import html as H
def text(s): return H.unescape(re.sub(r"<[^>]+>", " ", s))
ptext = {k: text(v) for k, v in pages.items()}
ref_pat = re.compile(r"\b(Definition|Proposition|Corollary|Remark|Lemma|Assumption|Problem|Lab|Section|Part|Misconception|Key result|M|P|E|R)\s?(\d+(?:\.\d+)?)\b|\b([MPER]\d)\b")
for c in cards:
    if c["lesson"] not in ("L03", "L04"):
        continue
    print("---", c["id"], c["lesson"], c.get("grade"), "|", c["front"])
    print("    back:", c["back"])
    combined = c["front"] + " " + c["back"]
    for m in re.finditer(r"(Definition|Proposition|Corollary|Remark|Lemma|Assumption|Problem|Lab|Section|Part)\s(\d+(?:\.\d+)?)", combined):
        token = m.group(0)
        found = token in ptext[c["lesson"]] or (m.group(1) in ("Problem",) and m.group(2) in ptext[c["lesson"]])
        if not found:
            print("    NOT FOUND in lesson:", token)
    # numbers in back
    for num in re.findall(r"\d[\d,]*\.?\d*", c["back"]):
        n = num.rstrip(".").replace(",", "")
        if n not in ptext[c["lesson"]] and n not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"):
            print("    NUMBER not in lesson text:", num)
print("L03/L04 cards:", sum(1 for c in cards if c["lesson"] in ("L03","L04")))
