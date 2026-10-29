import subprocess, sys, pathlib, html, re
root = pathlib.Path("/tmp/verifyB3-M3-c")
py = str(root / ".venv/bin/python")
for lab, page in [("L07-1", "L07"), ("L08-1", "L08"), ("L09-1", "L09")]:
    out = subprocess.run([py, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lab}.py")],
                         capture_output=True, text=True, check=True).stdout
    text = html.unescape(re.sub(r"<[^>]+>", "", (root / f"course/modules/M/M3/{page}.html").read_text()))
    missing = [ln for ln in out.splitlines() if ln.strip() and ln.strip() not in text]
    print(page, "lines", len(out.splitlines()), "missing from page text:", missing)
