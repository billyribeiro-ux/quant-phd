import html, re, subprocess, sys, glob, os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-LX2-c"
page = open(f"{ROOT}/course/modules/LX/LX2/project.html", encoding="utf-8").read()
expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)[1]).strip()
for f in sorted(glob.glob(f"{ROOT}/ledgers/LX2/mutants/*.py")):
    p = subprocess.run([sys.executable, "-I", "-W", "error", f], capture_output=True, text=True)
    same = p.stdout.strip() == expected and p.returncode == 0
    print(f"{os.path.basename(f)}: exit={p.returncode} {'PASSES (same as expected block)' if same else 'KILLED (output differs or error)'}")
