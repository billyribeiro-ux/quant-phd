"""Classify each changed line of the round-5 -> round-6 delta as escape-only or substantive."""
import difflib
import html
import subprocess
import sys

PIN_OLD = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
PIN_NEW = "e896b7a4"
FILES = sys.argv[1:]


def show(rev, path):
    return subprocess.run(
        ["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True
    ).stdout.splitlines()


for path in FILES:
    old = show(PIN_OLD, path)
    new = show(PIN_NEW, path)
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    esc_only = 0
    subst = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        o = "\n".join(old[i1:i2])
        n = "\n".join(new[j1:j2])
        if html.unescape(o) == html.unescape(n):
            esc_only += 1
            continue
        subst.append((i1 + 1, i2, j1 + 1, j2, o, n))
    print(f"== {path}: escape-only hunks={esc_only}, substantive hunks={len(subst)}")
    for i1, i2, j1, j2, o, n in subst:
        print(f"-- old {i1}-{i2} / new {j1}-{j2}")
        print("OLD:", o[:1200])
        print("NEW:", n[:1200])
