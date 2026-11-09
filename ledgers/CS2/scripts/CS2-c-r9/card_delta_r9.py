# Round 9 delta check for CS2 cards.json: 4540351d (round-8 pin) vs HEAD (95f3f8cb).
import json, re, subprocess, sys, html
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS9-CS2-c"
def git_show(rev, path):
    return subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
P = "course/modules/CS/CS2/cards.json"
old = json.loads(git_show("4540351d", P))
new = json.loads(git_show("HEAD", P))
oi = {c["id"]: c for c in old}; ni = {c["id"]: c for c in new}
print("counts old/new", len(old), len(new), "unique new", len(ni))
print("added", sorted(set(ni) - set(oi)))
print("removed", sorted(set(oi) - set(ni)))
changed = sorted(k for k in oi if k in ni and oi[k] != ni[k])
print("changed", changed)
print("order preserved", [c["id"] for c in old] == [c["id"] for c in new])
# duplicate scan on whole deck
fb = {}
for c in new:
    fb.setdefault((c["front"], c["back"]), []).append(c["id"])
print("exact duplicate pairs", [v for v in fb.values() if len(v) > 1])
fr = {}
for c in new:
    fr.setdefault(c["front"], []).append(c["id"])
print("duplicate fronts", [v for v in fr.values() if len(v) > 1])
# numeric tokens of L09-L11 cards occur in their lesson
def lesson_text(lid):
    raw = open(f"{ROOT}/course/modules/CS/CS2/{lid}.html", encoding="utf-8").read()
    txt = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(txt)
lt = {l: lesson_text(l) for l in ("L09", "L10", "L11")}
missing = []
n49 = 0
for c in new:
    if c["lesson"] not in lt:
        continue
    n49 += 1
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", c[field]):
            if tok in ("0", "1", "2", "3"):
                continue
            if tok not in lt[c["lesson"]]:
                missing.append((c["id"], field, tok))
print("L09-L11 cards", n49, "numeric tokens missing from lesson:", missing)
# process words (case-sensitive) across deck
pw = re.compile(r"\b(we|our|you|I|note|recall|round|verifier|builder|orchestrator|TODO|TBD|placeholder)\b")
hits = [(c["id"], m.group(0)) for c in new for f in ("front", "back") for m in pw.finditer(c[f])]
print("process-word hits", hits)
# scope words in changed cards and in c231
sw = re.compile(r"\b(all|every|only|same|any|always|never|exact|exactly|stable|optimal)\b")
for cid in changed + ["CS2-c231"]:
    c = ni[cid]
    print("scope", cid, [(f, m.group(0)) for f in ("front", "back") for m in sw.finditer(c[f])])
for cid in ("CS2-c231", "CS2-c132"):
    print(json.dumps(ni[cid], ensure_ascii=False))
# grade / basis consistency
bad = [c["id"] for c in new if (c["grade"] == "C") != ("basis" in c)]
print("grade/basis inconsistencies", bad)
