import html, pathlib, re, subprocess, sys
root = pathlib.Path("/tmp/verify32-AC4-b")
PY = str(root / ".venv/bin/python")
exp = {}
for unit in ("L03", "L04"):
    page = (root / f"course/modules/AC/AC4/{unit}.html").read_text(encoding="utf-8")
    exp[unit] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).rstrip("\n")
for d in ("AC4-b-r30", "AC4-b-r32"):
    for f in sorted((root / "ledgers/AC4/mutants" / d).glob("*.py")):
        unit = "L03" if "_L03_" in f.name else "L04"
        r = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True)
        print(d, f.name, "exit", r.returncode, "stdout_matches_expected", r.stdout.rstrip("\n") == exp[unit], "stderr_tail", r.stderr.strip()[-90:].replace("\n", " | "))
