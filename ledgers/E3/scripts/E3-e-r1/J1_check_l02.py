"""Verifier J1: L02 expected block equals twin stdout; page sentence equals twin docstring sentence; page code equals twin source."""
import html, re, subprocess, sys
root = sys.argv[1]
page = open(f"{root}/course/modules/E/E3/L02.html", encoding="utf-8").read()
twin = open(f"{root}/tests/labs/E3/lab-E3-L02-1.py", encoding="utf-8").read()
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
exp = html.unescape(exp).rstrip("\n")
out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E3/lab-E3-L02-1.py"], capture_output=True, text=True, check=True)
print("expected == twin stdout:", exp == out.stdout.rstrip("\n"), "| stderr bytes:", len(out.stderr.encode()))
sent = "printed with six decimal places, in the units the lab names (CU, CU squared, per CU or dimensionless for r_R); the"
print("page sentence in page:", sent in " ".join(page.split()), "| in twin:", sent in " ".join(twin.split()))
code = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
print("page code blocks:", len(code))
for c in code:
    c2 = html.unescape(c)
    if "def main" in c2:
        print("page code contains wealth line with :.6f:", "wealth_cu {WEALTH:.6f}" in c2, "| page code == twin body:", c2.strip() == twin.strip())
