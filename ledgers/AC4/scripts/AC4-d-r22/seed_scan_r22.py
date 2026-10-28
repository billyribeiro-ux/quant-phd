import re, subprocess, sys, tempfile, pathlib
root = pathlib.Path(sys.argv[1])
for t, pat in (("L07", r"cases with q <= K and an empty range: (\d+)"), ("L08", r"pairs ranked differently by RI and by OI/C: (\d+) of (\d+)")):
    src = (root / f"tests/labs/AC4/lab-AC4-{t}-1.py").read_text(encoding="utf-8")
    base = re.search(r"^SEED = (\d+)$", src, re.M).group(1)
    res = {}
    for s in range(1, 41):
        code = re.sub(r"^SEED = \d+$", f"SEED = {s}", src, count=1, flags=re.M)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir="/tmp/AC4-d-v22") as f:
            f.write(code)
        out = subprocess.run([sys.executable, "-I", "-W", "error", f.name], capture_output=True, text=True, timeout=60)
        m = re.search(pat, out.stdout)
        res[s] = (out.returncode, m.group(1) if m else None)
    counts = {}
    for s, (rc, v) in res.items():
        counts.setdefault(v, []).append(s)
    print(t, "shipped seed", base, "exit codes:", sorted({rc for rc, _ in res.values()}))
    for v, seeds in counts.items():
        print(f"  value {v}: {len(seeds)} seeds of 40 {seeds if len(seeds) < 12 else ''}")
