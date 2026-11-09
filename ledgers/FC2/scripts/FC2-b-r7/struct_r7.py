import subprocess, re
from collections import Counter
root = "/Users/billyribeiro/.fanout/wt/verifyS7-FC2-b"
def show(rev, path):
    return subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, text=True).stdout
def tags(s):
    return Counter(re.findall(r"<(/?[a-zA-Z][a-zA-Z0-9]*)[ >/]", s))
def ids(s):
    return sorted(re.findall(r'id="([^"]+)"', s))
def classes(s):
    return Counter(c for m in re.findall(r'class="([^"]+)"', s) for c in m.split())
for lid in ("L04", "L05", "L06"):
    p = f"course/modules/FC/FC2/{lid}.html"
    a, b = show("e896b7a4", p), show("aa659725", p)
    print(lid, "tag counts equal:", tags(a) == tags(b), "| id list equal:", ids(a) == ids(b),
          "| class counts equal:", classes(a) == classes(b), "| bytes", len(a), len(b),
          "| lines", a.count("\n"), b.count("\n"))
    # every changed line must be a single-line text edit inside one <p>/<li>/<span> element
    import difflib
    al, bl = a.splitlines(), b.splitlines()
    sm = difflib.SequenceMatcher(None, al, bl, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    print("  non-equal opcodes:", [(o[0], o[1]+1, o[2], o[3]-o[2]+0) for o in ops])
