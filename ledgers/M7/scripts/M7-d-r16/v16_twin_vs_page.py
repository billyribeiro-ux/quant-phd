"""Round-15: page code blocks and expected blocks vs the lab twins (run under python -I -W error)."""
import html, re, subprocess, sys
ROOT = sys.argv[1]
page = open(ROOT + "/course/modules/M/M7/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks:", len(blocks), "expected blocks:", len(expected))
for idx, lab in enumerate(["lab-M7-project-1", "lab-M7-project-2", "lab-M7-project-3"]):
    twin = open(f"{ROOT}/tests/labs/M7/{lab}.py", encoding="utf-8").read()
    code = html.unescape(blocks[idx])
    same_code = code.strip() == twin.strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/M7/{lab}.py"], capture_output=True, text=True)
    exp = html.unescape(expected[idx]).strip()
    out = run.stdout.strip()
    print(lab, "page code == twin:", same_code, "| twin exit", run.returncode, "| stderr bytes", len(run.stderr), "| expected == output:", exp == out)
    if not same_code:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:20]))
    if exp != out:
        print("EXPECTED:\n" + exp + "\nOUTPUT:\n" + out)
