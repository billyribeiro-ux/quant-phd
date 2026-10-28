"""Extracts the three project labs' expected blocks and code from project.html and runs each twin (python -I -W error)."""
import html, re, subprocess, sys
from pathlib import Path
page = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
for lab in ("lab-M2-project-1", "lab-M2-project-2", "lab-M2-project-3"):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    (out / f"{lab}.page.py").write_text(code, encoding="utf-8")
    (out / f"{lab}.expected.txt").write_text(exp, encoding="utf-8")
    twin = Path(sys.argv[3]) / f"{lab}.py"
    same_twin = twin.read_text(encoding="utf-8").strip() == code.strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(out / f"{lab}.page.py")], capture_output=True, text=True)
    got = run.stdout.strip()
    print(lab, "twin_equals_page_code:", same_twin, "| stdout==expected:", got == exp.strip(), "| rc:", run.returncode, run.stderr[:200])
    if got != exp.strip():
        print("GOT:\n" + got + "\nEXP:\n" + exp)
