"""E3 slice g round 11 checks, run from the checkout root (python3 -I ledgers/E3/scripts/E3-g-r11/checks_r11.py).

1. per-id card diff for the slice (L05..L08) against 2d755599 and 47a36d8c (git show).
2. cross-reference scan: 'Remark/Proposition/Theorem/Corollary/Definition/Example/Problem/Model/Observation/Section x' on the
   L05..L08 cards against the lesson text (strip.py output in this directory).
3. full-unit duplicate scan of all cards (ids, fronts, backs).
4. quiz correct options: the data-correct label text per quiz question in L05..L08.
5. hub hours: data-hours-lessons and data-hours-project against 8 lessons x 7 study hours.
"""
import collections
import json
import html as htmllib
import re
import subprocess

ROOT = "."
D = "ledgers/E3/scripts/E3-g-r11"
CARDS = "course/modules/E/E3/cards.json"


def load_rev(rev):
    raw = subprocess.run(["git", "show", f"{rev}:{CARDS}"], capture_output=True, text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(raw)}


cur = {c["id"]: c for c in json.load(open(CARDS, encoding="utf-8"))}
print("== 1. slice card diffs")
for label, rev in (("vs 2d755599", "2d755599d8d74df292e3e43025f0458c4053802e"), ("vs 47a36d8c", "47a36d8c78633793ccc762ae19dcd5e19b780d19")):
    ref = load_rev(rev)
    out = []
    for i in sorted(set(ref) | set(cur)):
        if ref.get(i) != cur.get(i):
            lesson = (cur.get(i) or ref.get(i))["lesson"]
            if lesson in ("L05", "L06", "L07", "L08"):
                state = "added" if i not in ref else "removed" if i not in cur else "changed"
                out.append(f"{i}({lesson}:{state})")
    print(label, out)

print("== 2. cross-references on slice cards")
texts = {L: open(f"{D}/{L}.txt", encoding="utf-8").read() for L in ("L05", "L06", "L07", "L08")}
pat = re.compile(r"\b(Remark|Proposition|Theorem|Corollary|Definition|Example|Problem|Model|Observation|Lemma|Section)\s+([0-9]+(?:\.[0-9]+)?|[MPERA][0-9]+)")
n = 0
miss = []
for c in cur.values():
    if c["lesson"] not in texts:
        continue
    for m in pat.finditer(c["front"] + " " + c["back"]):
        n += 1
        kind, num = m.group(1), m.group(2)
        t = texts[c["lesson"]]
        if kind == "Section":
            ok = re.search(rf"^{re.escape(num)}[A-Za-z]", t, re.M) is not None
        else:
            ok = f"{kind} {num}" in t
        if not ok:
            miss.append(f"{c['id']}:{m.group(0)}")
print("mentions", n, "not in own lesson text:", miss)

print("== 3. unit duplicate scan")
ids = [c["id"] for c in cur.values()]
fronts = collections.Counter(re.sub(r"\s+", " ", c["front"].strip().lower()) for c in cur.values())
backs = collections.Counter(re.sub(r"\s+", " ", c["back"].strip().lower()) for c in cur.values())
print("cards", len(ids), "dup ids", len(ids) - len(set(ids)), "dup fronts", sum(1 for v in fronts.values() if v > 1), "dup backs", sum(1 for v in backs.values() if v > 1))

print("== 4. quiz correct options")
for L in ("L05", "L06", "L07", "L08"):
    src = open(f"course/modules/E/E3/{L}.html", encoding="utf-8").read()
    for m in re.finditer(r'<label class="option" data-correct>(.*?)</label>', src, re.S):
        body = re.sub(r"<input[^>]*>", "", m.group(1))
        body = htmllib.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        print(L, "|", body[:140])

print("== 5. hub hours")
hub = open("course/modules/E/E3/index.html", encoding="utf-8").read()
hl = re.search(r'data-hours-lessons="(\d+)"', hub).group(1)
hp = re.search(r'data-hours-project="(\d+)"', hub).group(1)
hdr = [re.search(r"· (\d+) study hours", texts[L]) for L in ("L05", "L06", "L07", "L08")]
print("hub lessons", hl, "project", hp, "lesson study hours (L05..L08)", [h.group(1) if h else None for h in hdr], "8x7 =", 8 * 7)
