# Compares each slice lab's embedded code and expected output with its twin and with a real run.
# Usage (from checkout root): .venv/bin/python -I ledgers/M2/scripts/M2-a-r1/twin_compare.py
import html, re, subprocess, sys
root = "."
for n in ["01", "02", "03", "04", "05", "06"]:
    src = open(f"{root}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    code = html.unescape(re.search(r'<code class="language-python"[^>]*>(.*?)</code>', src, re.S).group(1))
    twin = open(f"{root}/tests/labs/M2/lab-M2-L{n}-1.py", encoding="utf-8").read()
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)).strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/M2/lab-M2-L{n}-1.py"],
                         capture_output=True, text=True, check=False)
    print(f"L{n} embedded==twin: {code.strip() == twin.strip()} exit={run.returncode} printed==expected: {run.stdout.strip() == expected}")
