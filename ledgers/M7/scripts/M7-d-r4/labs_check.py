"""Extract each project lab's code and expected block from project.html; compare with the twin and run the twin."""
import html, re, subprocess, sys
root = sys.argv[1]
page = open(root + "/course/modules/M/M7/project.html", encoding="utf-8").read()
PY = root + "/.venv/bin/python"
for n in (1, 2, 3):
    sec = page[page.index(f'id="lab-M7-project-{n}"'):]
    sec = sec[: sec.index("</section>")]
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = open(f"{root}/tests/labs/M7/lab-M7-project-{n}.py", encoding="utf-8").read()
    print(f"lab {n}: page code == twin: {code.strip() == twin.strip()} (len page {len(code)}, twin {len(twin)})")
    if n == 2:
        print("  page blanks:", code.count("___"), "; twin has blanks:", twin.count("___"))
    out = subprocess.run([PY, "-I", "-W", "error", root + f"/tests/labs/M7/lab-M7-project-{n}.py"], capture_output=True, text=True)
    print(f"  twin run exit {out.returncode}, stderr bytes {len(out.stderr)}")
    print("  twin output == expected block:", out.stdout.strip() == expected.strip())
    if out.stdout.strip() != expected.strip():
        print("  OUTPUT:\n" + out.stdout + "\n  EXPECTED:\n" + expected)
    if n == 2:
        # the page's blank-filled completion must equal lab 1's expected output when the twin is run
        pass
