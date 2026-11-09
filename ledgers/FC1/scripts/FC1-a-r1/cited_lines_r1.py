"""Round-1: compare every cited line of the slice (and its cross-lesson pointers) between dde0486b and HEAD."""
import subprocess
import sys

root = sys.argv[1]
D = "course/modules/FC/FC1/"

def show(rev, path):
    return subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, text=True,
                          check=True).stdout.split("\n")

cites = {
    "L02.html": [270],
    "L04.html": [57, 84],
    "L05.html": [58, 63],
    "project.html": list(range(42, 48)),
    "L01.html": [59, 81, 117, 132, 137, 310, 318, 455, 456, 457, 459, 460, 51],
    "L02.html#2": [50, 58, 92, 133, 246, 253, 256, 270],
    "L03.html": [51, 57, 61, 97, 100, 150, 158, 81],
    "index.html": [35, 59, 62, 69, 106, 120, 149, 154, 159, 162, 164, 166, 171],
}
for key, lines in cites.items():
    f = key.split("#")[0]
    a = show("dde0486b", D + f)
    b = show("HEAD", D + f)
    same_len = len(a) == len(b)
    diff = [n for n in lines if a[n - 1] != b[n - 1]]
    print(f"{key}: {len(lines)} cited lines, line count identical={same_len}, changed cited lines={diff}")
for f in ("L04.html", "L05.html"):
    a = show("dde0486b", D + f)
    b = show("HEAD", D + f)
    print(f, "L04/L05 changed line numbers:", [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y])
for pair in (("L04.html", 57), ("L04.html", 84), ("L05.html", 58), ("L05.html", 63)):
    line = show("HEAD", D + pair[0])[pair[1] - 1]
    print(pair, "HEAD text:", line.strip()[:110])
