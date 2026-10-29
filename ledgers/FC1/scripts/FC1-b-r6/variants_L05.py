import re, subprocess, sys
src = open("tests/labs/FC1/lab-FC1-L05-1.py").read()
base = subprocess.run([sys.executable, "-I", "-W", "error", "tests/labs/FC1/lab-FC1-L05-1.py"], capture_output=True, text=True).stdout.splitlines()
for c, s in [(0, 0), (0, 1), (0, 3), (3, 2), (2, 2), (1, 2), (2, 0)]:
    v = re.sub(r"^CLEARING_OFFSET = \d+", f"CLEARING_OFFSET = {c}", src, flags=re.M)
    v = re.sub(r"^SETTLEMENT_LAG = \d+", f"SETTLEMENT_LAG = {s}", v, flags=re.M)
    path = f"/Users/billyribeiro/.fanout/wt/verifyC6-FC1-b/ledgers/FC1/scripts/FC1-b-r6/variant_c{c}_s{s}.py"
    open(path, "w").write(v)
    r = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True)
    out = r.stdout.splitlines()
    print(f"== clearing={c} lag={s} rc={r.returncode} stderr={r.stderr.strip()[:200]!r}")
    for a, b in zip(base, out):
        if a != b:
            print("  base:", a[:120]); print("  var :", b[:120])
    if len(base) != len(out):
        print("  line count differs", len(base), len(out))
