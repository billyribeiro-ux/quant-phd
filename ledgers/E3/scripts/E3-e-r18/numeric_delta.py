"""For each changed lesson: compare the multiset of numeric tokens and of the non-symbol words in removed vs added lines."""
import re, subprocess, sys, collections
pin_old, pin_new = sys.argv[1], sys.argv[2]
files = sys.argv[3:]
for f in files:
    diff = subprocess.run(["git", "diff", "-U0", pin_old, pin_new, "--", f], capture_output=True, text=True).stdout
    rem, add = [], []
    for line in diff.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            rem.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            add.append(line[1:])
    num = re.compile(r"(?<![A-Za-z_\\])\d+(?:\.\d+)?")
    cr = collections.Counter(n for l in rem for n in num.findall(l))
    ca = collections.Counter(n for l in add for n in num.findall(l))
    print(f"{f}: removed lines {len(rem)}, added lines {len(add)}; numeric tokens removed-only {dict(cr - ca)} added-only {dict(ca - cr)}")
