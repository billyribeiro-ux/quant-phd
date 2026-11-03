"""FC2-d r2: print the lesson passage that each sampled card cites (first occurrence of its label, tags stripped).
usage: python -I card_sample_context.py <repo-root> <card-id> [<card-id> ...]"""
import html, json, os, re, sys
root = sys.argv[1]
base = os.path.join(root, "course/modules/FC/FC2")
cards = {c["id"]: c for c in json.load(open(os.path.join(base, "cards.json"), encoding="utf-8"))}
def text_of(lesson):
    raw = open(os.path.join(base, lesson + ".html"), encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(re.sub(r"\s+", " ", raw))
for cid in sys.argv[2:]:
    c = cards[cid]
    t = text_of(c["lesson"])
    print("=== ", cid, c["lesson"], "| FRONT:", c["front"])
    print("    BACK:", c["back"])
    labels = re.findall(r"\b(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Problem|Assumption|Section)\s+([A-Z]?\d+(?:\.\d+)?\w*)", c["back"] + " " + c["front"])
    seen = set()
    for kind, num in labels:
        lab = f"{kind} {num}"
        if lab in seen:
            continue
        seen.add(lab)
        m = re.search(re.escape(lab) + r"(?![\d.])", t)
        if m:
            # prefer a block-title occurrence (the statement), else the first occurrence
            idx = [x.start() for x in re.finditer(re.escape(lab) + r"(?![\d.])", t)]
            pick = idx[0]
            print("  [%s] ..." % lab, t[pick:pick + 700])
        else:
            print("  [%s] NOT FOUND as text" % lab)
