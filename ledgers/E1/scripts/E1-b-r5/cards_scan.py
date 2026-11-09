# Verifier-written: (1) every labelled citation in a slice card exists in its own lesson page;
# (2) every number token in a slice card appears in that lesson page; (3) duplicate ids/fronts over all cards.
import json, pathlib, re, html, collections
REPO = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS5-E1-b")
cards = json.loads((REPO / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
def plain(p):
    t = (REPO / f"course/modules/E/E1/{p}.html").read_text(encoding="utf-8")
    t = re.sub(r"</?[a-zA-Z][^>]*>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))
pages = {p: plain(p) for p in ("L04", "L05", "L06")}
pages_full = pages  # labs' expected output lives in the same page text
slice_ids = {c["id"] for c in cards if c["lesson"] in ("L04", "L05", "L06")} | {"E1-c133", "E1-c143", "E1-c144", "E1-c145", "E1-c146", "E1-c147", "E1-c148", "E1-c153", "E1-c154", "E1-c155", "E1-c156"}
cite_re = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Assumption|Problem)\s+([A-Z]?\d*(?:\.\d+)?[A-Z]?\d*)\b")
bad = []
n_cards = 0
number_re = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
nums_missing = []
for c in cards:
    if c["id"] not in slice_ids:
        continue
    n_cards += 1
    text = c["front"] + " " + c["back"]
    lesson = c["lesson"]
    pg = pages[lesson]
    for kind, lab in cite_re.findall(text):
        if kind == "Problem":
            ok = re.search(rf"\b{re.escape(lab)} ·", pg) is not None
        else:
            ok = re.search(rf"\b{kind} {re.escape(lab)}\b", pg) is not None
        if not ok:
            bad.append((c["id"], lesson, f"{kind} {lab}"))
    for tok in number_re.findall(text):
        if tok not in pg:
            nums_missing.append((c["id"], lesson, tok))
print("slice cards scanned:", n_cards)
print("citation misses (id, lesson, citation):", bad)
print("number tokens not in own lesson page (id, lesson, token):", nums_missing)
ids = collections.Counter(c["id"] for c in cards)
fr = collections.Counter(re.sub(r"[^a-z0-9]+", " ", c["front"].lower()).strip() for c in cards)
print("total", len(cards), "dup ids", [k for k, v in ids.items() if v > 1], "dup fronts", [k for k, v in fr.items() if v > 1])
