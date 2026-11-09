import json, re, subprocess, sys
ROOT = sys.argv[1]
PAGES = ["L05", "L06", "L07", "L08"]
base = "course/modules/M/M6/"
def pagetext(rev, lesson):
    return subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{base}{lesson}.html"], capture_output=True, text=True, check=True).stdout
# 1 grade sequence
for lesson in PAGES:
    old = re.findall(r'data-grade="([A-Z]|X)"', pagetext("2a805c83", lesson))
    new = re.findall(r'data-grade="([A-Z]|X)"', pagetext("HEAD", lesson))
    print("grades", lesson, "old", len(old), "new", len(new), "identical_sequence", old == new, "".join(new))
# 2 process words in learner text (strip tags)
pat = re.compile(r"\b(round|verifier|ledger|fixer|reviewer|the fix|previous round|ruling|pin|fragment)\b", re.I)
for lesson in PAGES:
    txt = re.sub(r"<[^>]+>", " ", pagetext("HEAD", lesson))
    hits = [m.group(0) for m in pat.finditer(txt)]
    print("process_words", lesson, hits)
# 3 notation: registered symbols count in L05..L08 at HEAD
nj = json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))
flat = json.dumps(nj)
syms = re.findall(r'"(\\\\[A-Za-z]+\{?[^"]*|[A-Za-z]_\{?[^"]*)"\s*:', flat)
print("notation keys sample", list(nj.keys())[:5] if isinstance(nj, dict) else type(nj))
