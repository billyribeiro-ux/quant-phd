# Maps every cited old line range (aa659725) of FC2 files to its new location (95f3f8cb) and proves byte identity.
import difflib, json, re, subprocess, sys
ROOT = sys.argv[1]
OLD, NEW = "aa659725", "95f3f8cb"
FILES = ["course/modules/FC/FC2/project.html", "course/modules/FC/FC2/grader/test_project.py",
         "course/modules/FC/FC2/grader/reference.py", "course/modules/FC/FC2/grader/instance.py",
         "course/modules/FC/FC2/grader/starter.py", "tests/labs/FC2/lab-FC2-project-1.py",
         "tests/labs/FC2/lab-FC2-project-2.py", "tests/labs/FC2/lab-FC2-project-3.py",
         "tests/labs/FC2/lab-FC2-L04-1.py", "tests/labs/FC2/lab-FC2-L06-1.py",
         "course/modules/FC/FC2/L04.html", "course/modules/FC/FC2/index.html", "course/modules/FC/FC2/cards.json"]
def show(rev, path):
    return subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True, text=True).stdout.splitlines()
out = {}
for f in FILES:
    a, b = show(OLD, f), show(NEW, f)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    m = {}  # old 1-based line -> (new 1-based line or None, identical flag)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for k in range(i2 - i1):
            if tag == "equal":
                m[i1 + k + 1] = (j1 + k + 1, True)
            else:
                m[i1 + k + 1] = (None, False)
    out[f] = {"n_old": len(a), "n_new": len(b), "map": {str(k): v for k, v in m.items()}}
json.dump(out, open(sys.argv[2], "w"))
for f in FILES:
    print(f, out[f]["n_old"], out[f]["n_new"], "changed old lines:", sum(1 for v in out[f]["map"].values() if not v[1]))
