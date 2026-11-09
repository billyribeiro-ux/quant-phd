"""Verifier check (round 2): page code equals twin, expected block equals twin output, twin runs under python -I -W error."""
import html, re, subprocess, sys, pathlib

ROOT = pathlib.Path(sys.argv[1]).resolve()
PAGES = {"L08": "course/modules/M/M4/L08.html", "L09": "course/modules/M/M4/L09.html", "L10": "course/modules/M/M4/L10.html"}
for lesson, page in PAGES.items():
    text = (ROOT / page).read_text(encoding="utf-8")
    lab_id = f"lab-M4-{lesson}-1"
    twin = ROOT / "tests/labs/M4" / f"{lab_id}.py"
    m = re.search(r'<section class="lab" id="%s".*?</section>' % re.escape(lab_id), text, re.S)
    assert m, lab_id
    sec = m.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1)
    code = html.unescape(code)
    twin_src = twin.read_text(encoding="utf-8")
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    print(f"{lesson}: code_equals_twin={code.rstrip() == twin_src.rstrip()} code_len={len(code)} twin_len={len(twin_src)}")
    if code.rstrip() != twin_src.rstrip():
        import difflib
        for line in list(difflib.unified_diff(twin_src.splitlines(), code.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd="/tmp", capture_output=True, text=True)
    print(f"{lesson}: twin exit={r.returncode} stderr_bytes={len(r.stderr)} stdout_lines={len(r.stdout.splitlines())}")
    print(f"{lesson}: expected_equals_output={exp.strip() == r.stdout.strip()}")
    if exp.strip() != r.stdout.strip():
        import difflib
        for line in list(difflib.unified_diff(exp.strip().splitlines(), r.stdout.strip().splitlines(), lineterm=""))[:40]:
            print("   ", line)
    out_file = ROOT / "ledgers/M4/scripts/M4-c-r2" / f"twin_{lesson}_r2.txt"
    out_file.write_text(r.stdout, encoding="utf-8")
