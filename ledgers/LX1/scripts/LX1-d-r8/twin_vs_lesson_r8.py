"""Round 8: every line of each lab twin's standalone output must appear (whitespace-normalised) in its lesson text."""
import re, sys
base = sys.argv[1]
out_dir = f"{base}/ledgers/LX1/scripts/LX1-d-r8/out"
def norm(s):
    return " ".join(s.split())
for L in ("L01", "L02", "L03", "L04"):
    lesson = norm(open(f"{out_dir}/{L}.txt", encoding="utf-8").read())
    twin = [norm(x) for x in open(f"{out_dir}/twin_lab-LX1-{L}-1.out", encoding="utf-8").read().splitlines() if x.strip()]
    missing = [x for x in twin if x not in lesson]
    print(f"{L}: {len(twin) - len(missing)}/{len(twin)} twin output lines verbatim in lesson text; missing: {missing}")
