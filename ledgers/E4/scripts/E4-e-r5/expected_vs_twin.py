"""For each E4 lab section on a lesson page: compare the <pre class="expected"> block with the twin's output,
and compare the page's <pre><code data-run> code with the twin file. Token-level comparison (whitespace-insensitive)."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
for page in sorted((ROOT / "course/modules/E/E4").glob("L0*.html")):
    src = page.read_text(encoding="utf-8")
    for m in re.finditer(r'<section class="lab" id="(lab-E4-[^"]+)" data-runtime="python">(.*?)</section>', src, re.S):
        lab_id, body = m.group(1), m.group(2)
        code_m = re.search(r"<pre><code class=\"language-python\" data-run>(.*?)</code></pre>", body, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        twin = ROOT / "tests/labs/E4" / f"{lab_id}.py"
        out_path = OUT / f"{lab_id}.out"
        twin_code = twin.read_text(encoding="utf-8")
        page_code = html.unescape(code_m.group(1)) if code_m else None
        code_eq = page_code is not None and page_code.split() == twin_code.split()
        exp = html.unescape(re.sub(r"<[^>]+>", "", exp_m.group(1))) if exp_m else None
        actual = out_path.read_text(encoding="utf-8")
        exp_eq = exp is not None and exp.split() == actual.split()
        print(f"{page.name} {lab_id}: page_code_equals_twin={code_eq} expected_equals_output={exp_eq} "
              f"(expected tokens {len(exp.split()) if exp else None}, output tokens {len(actual.split())})")
        if not exp_eq and exp is not None:
            import difflib
            for line in difflib.unified_diff(exp.split("\n"), actual.split("\n"), lineterm="", n=0):
                print("   ", line[:200])
