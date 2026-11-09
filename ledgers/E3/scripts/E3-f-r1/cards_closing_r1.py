"""Closing delta (round 1) card checks for E3 slice f. Run from the checkout root."""
import difflib
import html
import json
import re
import subprocess
import sys

PIN = "4540351d"
HEAD = "HEAD"
CARDS = "course/modules/E/E3/cards.json"


def at(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout


old = json.loads(at(PIN, CARDS))
new = json.loads(open(CARDS, encoding="utf-8").read())
refs = json.load(open("references/references.json", encoding="utf-8"))
ref_keys = set(refs.keys()) if isinstance(refs, dict) else {r.get("key") or r.get("id") for r in refs}

print("n_cards", len(new), "distinct_ids", len({c["id"] for c in new}), "same_order_ids", [c["id"] for c in old] == [c["id"] for c in new])
bad = []
for c in new:
    if set(c) - {"id", "lesson", "front", "back", "grade", "basis", "cite"}:
        bad.append((c["id"], "extra keys", set(c)))
    if c.get("grade") not in (None, "T", "C"):
        bad.append((c["id"], "grade", c.get("grade")))
    if c.get("grade") == "C" and not c.get("basis") and not c.get("cite"):
        bad.append((c["id"], "C without basis or cite"))
    for k in c.get("cite", []):
        if k not in ref_keys:
            bad.append((c["id"], "cite key not in registry", k))
print("integrity_problems", bad)

changed = [c["id"] for c in new if c != next(o for o in old if o["id"] == c["id"])]
print("changed_ids", changed)
for cid in changed:
    o = next(x for x in old if x["id"] == cid)
    n = next(x for x in new if x["id"] == cid)
    for k in sorted(set(o) | set(n)):
        if o.get(k) != n.get(k):
            print(f"  {cid} field {k}: OLD={o.get(k)!r}\n  {'':{len(cid)}} NEW={n.get(k)!r}")

pages = {}
def page(L):
    if L not in pages:
        pages[L] = html.unescape(open(f"course/modules/E/E3/{L}.html", encoding="utf-8").read())
    return pages[L]

xref_miss = []
for c in new:
    src = page(c["lesson"])
    text = c["front"] + " " + c["back"]
    for kind, num in re.findall(r"\b(Definition|Proposition|Theorem|Lemma|Example|Remark|Corollary) (\d+\.\d+)", text):
        if not re.search(rf"{kind} {re.escape(num)}\b", src):
            xref_miss.append((c["id"], f"{kind} {num}"))
print("xref_missing_all_cards", xref_miss)

num_miss = []
for cid in changed:
    n = next(x for x in new if x["id"] == cid)
    src = page(n["lesson"])
    text = n["front"] + " " + n["back"]
    for num in set(re.findall(r"(?<![\w.])\d[\d,./]*\d|(?<![\w.])\d(?![\w.])", text)):
        if num not in src:
            num_miss.append((cid, num))
print("numbers_in_changed_cards_not_in_lesson", num_miss)

scores = []
for cid in changed:
    n = next(x for x in new if x["id"] == cid)
    for o in new:
        if o["id"] == cid:
            continue
        rf = difflib.SequenceMatcher(None, n["front"], o["front"]).ratio()
        rb = difflib.SequenceMatcher(None, n["back"], o["back"]).ratio()
        if rf > 0.8 or rb > 0.85:
            scores.append((cid, o["id"], round(rf, 3), round(rb, 3)))
print("near_duplicate_pairs_changed_vs_all", scores)

banned = re.compile(r"\b(round|ruling|verifier|fixer|TODO|placeholder|we fixed|this round|ledger)\b", re.I)
print("banned_hits_changed", [(cid) for cid in changed if banned.search(next(x for x in new if x["id"] == cid)["back"] + next(x for x in new if x["id"] == cid)["front"])])
