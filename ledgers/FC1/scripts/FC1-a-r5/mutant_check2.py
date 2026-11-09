import html, re, subprocess
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS5-FC1-a"
cases = [("L01", "ledgers/FC1/mutants/fc1a_r5_lab_L01_closed_form_exponent_short.py"),
         ("L03", "ledgers/FC1/mutants/fc1a_r5_lab_L03_spread_capture_doubled.py")]
for lesson, mut in cases:
    src = open(f"{ROOT}/course/modules/FC/FC1/{lesson}.html", encoding="utf-8").read()
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)).rstrip("\n").splitlines()
    r = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", f"{ROOT}/{mut}"], capture_output=True, text=True)
    got = r.stdout.rstrip("\n").splitlines()
    diffs = [(i, e, g) for i, (e, g) in enumerate(zip(expected, got)) if e != g]
    print(f"{lesson} {mut.split('/')[-1]} exit={r.returncode} stderr_bytes={len(r.stderr)} mismatches={len(diffs)}")
    for d in diffs[:2]:
        print("   ", d)
