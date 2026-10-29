"""Compare each E5 slice lab twin with the code block embedded in its page, and the embedded expected block with a fresh run."""
import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
pages = {"L01": "lab-E5-L01-1", "L02": "lab-E5-L02-1", "L03": "lab-E5-L03-1"}
for page, lab in pages.items():
    text = (root / "course/modules/E/E5" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="%s".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, text, re.S)
    code, expected = html.unescape(m.group(1)), html.unescape(m.group(2))
    twin = (root / "tests/labs/E5" / f"{lab}.py").read_text(encoding="utf-8")
    print(page, "embedded code == twin:", code.strip() == twin.strip(), "| lines", len(code.splitlines()))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/E5" / f"{lab}.py")], capture_output=True, text=True, cwd="/")
    print(page, "expected == fresh run:", expected.strip() == run.stdout.strip(), "exit", run.returncode)
