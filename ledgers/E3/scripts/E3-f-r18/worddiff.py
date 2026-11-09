import difflib, subprocess, sys, re
# word-level diff of changed lines between two commits for one file; prints only changed token pairs
old_rev, new_rev, path = sys.argv[1], sys.argv[2], sys.argv[3]
def get(rev):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True).stdout.splitlines()
o, n = get(old_rev), get(new_rev)
sm = difflib.SequenceMatcher(None, o, n, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    a = " ".join(o[i1:i2]); b = " ".join(n[j1:j2])
    ta = re.findall(r"\S+", a); tb = re.findall(r"\S+", b)
    wsm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    pairs = []
    for t, x1, x2, y1, y2 in wsm.get_opcodes():
        if t != "equal":
            pairs.append((" ".join(ta[x1:x2])[:90], " ".join(tb[y1:y2])[:90]))
    print(f"@{i1+1}: " + " | ".join(f"[{x}] -> [{y}]" for x, y in pairs))
