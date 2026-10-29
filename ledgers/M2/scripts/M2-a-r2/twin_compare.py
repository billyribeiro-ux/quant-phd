# Compares each slice lab's embedded code and expected output with its twin and with a real run (pin 1817191).
# Usage (from checkout root): .venv/bin/python -I ledgers/M2/scripts/M2-a-r2/twin_compare.py
import html, re, subprocess, sys
root = "."
for n in ["01", "02", "03", "04", "05", "06"]:
    src = open(f"{root}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    blocks = re.findall(r'<code class="language-python"[^>]*>(.*?)</code>', src, re.S)
    code = html.unescape(blocks[0]) if blocks else ""
    twin = open(f"{root}/tests/labs/M2/lab-M2-L{n}-1.py", encoding="utf-8").read()
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(exp[0]).strip() if exp else ""
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/M2/lab-M2-L{n}-1.py"],
                         capture_output=True, text=True, check=False)
    print(f"L{n} code_blocks={len(blocks)} expected_blocks={len(exp)} embedded==twin: {code.strip() == twin.strip()} "
          f"exit={run.returncode} printed==expected: {run.stdout.strip() == expected}")
    if code.strip() != twin.strip():
        print("  first differing line:", next((i for i, (a, b) in enumerate(zip(code.splitlines(), twin.splitlines())) if a != b), None))
