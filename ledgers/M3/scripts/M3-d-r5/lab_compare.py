"""Run each project lab twin under python -I -W error and diff its stdout against the page's expected block."""
import html, re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/M/M3/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-M3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in labs:
    code = html.unescape(code)
    expected = html.unescape(expected)
    out_dir = Path(sys.argv[2]) / lab_id
    out_dir.mkdir(parents=True, exist_ok=True)
    src = out_dir / "page_code.py"
    src.write_text(code, encoding="utf-8")
    twin = root / "tests/labs/M3" / f"{lab_id}.py"
    twin_text = twin.read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(src)], capture_output=True, text=True, timeout=60)
    run_twin = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, timeout=60)
    same_code = twin_text.strip() == code.strip()
    print(lab_id, "page_rc", run.returncode, "twin_rc", run_twin.returncode, "stdout==expected", run.stdout.strip() == expected.strip(),
          "twin_stdout==expected", run_twin.stdout.strip() == expected.strip(), "code==twin", same_code)
    if run.stderr: print("stderr:", run.stderr[:300])
    if run_twin.stderr: print("twin stderr:", run_twin.stderr[:300])
    print(run.stdout)
