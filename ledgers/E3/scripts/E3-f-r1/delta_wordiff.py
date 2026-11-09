"""Word-level diff of each changed line in the 2a805c83..HEAD delta for the E3 pages (for locating changed sentences)."""
import difflib
import subprocess
import sys

files = sys.argv[1:]
for f in files:
    old = subprocess.run(["git", "show", f"2a805c83:{f}"], capture_output=True, text=True).stdout.splitlines()
    new = subprocess.run(["git", "show", f"HEAD:{f}"], capture_output=True, text=True).stdout.splitlines()
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        print(f"== {f} {tag} old {i1+1}-{i2} new {j1+1}-{j2}")
        for a, b in zip(old[i1:i2], new[j1:j2]):
            wa, wb = a.split(" "), b.split(" ")
            s = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
            for t, a1, a2, b1, b2 in s.get_opcodes():
                if t != "equal":
                    print(f"  {t}: OLD[{' '.join(wa[a1:a2])}] NEW[{' '.join(wb[b1:b2])}]")
