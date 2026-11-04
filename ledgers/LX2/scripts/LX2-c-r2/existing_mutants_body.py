import html, re, subprocess, sys, glob, os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-LX2-c"
page = open(f"{ROOT}/course/modules/LX/LX2/project.html", encoding="utf-8").read()
expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)[1]).strip().splitlines()
for f in sorted(glob.glob(f"{ROOT}/ledgers/LX2/mutants/*.py")):
    p = subprocess.run([sys.executable, "-I", "-W", "error", f], capture_output=True, text=True)
    got = p.stdout.strip().splitlines()
    header_ok = got[:1] == expected[:1]
    body_diff = [i for i, (a, b) in enumerate(zip(got[1:], expected[1:]), start=2) if a != b] + ([] if len(got) == len(expected) else ["len"])
    print(f"{os.path.basename(f)}: header_matches_page={header_ok} body_differing_lines={body_diff}")
