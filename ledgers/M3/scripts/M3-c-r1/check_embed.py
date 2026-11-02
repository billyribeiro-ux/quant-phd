# Compares each lab's <code> block and expected block in L07-L09 with its twin (code) and twin output (expected).
import html, re, subprocess, sys
root = sys.argv[1]
for L, lab in [("L07", "lab-M3-L07-1"), ("L08", "lab-M3-L08-1"), ("L09", "lab-M3-L09-1")]:
    txt = open(f"{root}/course/modules/M/M3/{L}.html", encoding="utf-8").read()
    sec = re.search(rf'<section class="lab" id="{lab}".*?</section>', txt, re.S).group(0)
    code = re.search(r'<pre><code[^>]*data-run[^>]*>(.*?)</code></pre>', sec, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
    twin = open(f"{root}/tests/labs/M3/{lab}.py", encoding="utf-8").read()
    print(L, "code == twin:", html.unescape(code).strip() == twin.strip(), "| markers left:", "@@" in sec)
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/M3/{lab}.py"], capture_output=True, text=True, cwd=f"{root}/tests/labs/M3").stdout
    print(L, "expected == twin output:", html.unescape(expected).strip() == out.strip())
