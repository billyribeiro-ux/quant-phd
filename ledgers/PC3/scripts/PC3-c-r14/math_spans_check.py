"""Compare the math spans of the changed project.html lines (407, 432, 696) before and after the round-13 pin."""
import re
import subprocess
import sys

root = sys.argv[1]
pin_old = "e919577"
pin_new = "8e5751c"
path = "course/modules/PC/PC3/project.html"
old = subprocess.run(["git", "-C", root, "show", f"{pin_old}:{path}"], capture_output=True, text=True).stdout.split("\n")
new = subprocess.run(["git", "-C", root, "show", f"{pin_new}:{path}"], capture_output=True, text=True).stdout.split("\n")
spans = lambda s: re.findall(r"\\\((.*?)\\\)", s)
for n in (407, 432, 696):
    o, w = old[n - 1], new[n - 1]
    print(f"line {n}: math spans identical={spans(o) == spans(w)}; old spans={len(spans(o))} new spans={len(spans(w))}")
    print(f"  old words: {re.sub(r'<[^>]+>', '', o)[:0]}")
diff_lines = [i + 1 for i in range(len(old)) if old[i] != new[i]]
print("changed line numbers in project.html:", diff_lines)
