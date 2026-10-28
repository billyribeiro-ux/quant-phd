# Checks that each lab twin's non-blank lines appear in the lesson page (tags stripped, whitespace removed),
# and that the page's embedded `part ` output lines equal a fresh run of the twin.
import html
import re
import subprocess
import sys

root = sys.argv[1]
for page, twin in (("L07", "lab-E3-L07-1"), ("L08", "lab-E3-L08-1")):
    raw = open(f"{root}/course/modules/E/E3/{page}.html", encoding="utf-8").read()
    text = html.unescape(re.sub(r"<[a-zA-Z/!][^>]*>", "", raw))
    norm = lambda s: re.sub(r"\s+", "", s)
    lines = [ln for ln in open(f"{root}/tests/labs/E3/{twin}.py", encoding="utf-8").read().split("\n") if ln.strip()]
    missing = [ln for ln in lines if norm(ln) not in norm(text)]
    emb = [ln.strip() for ln in text.split("\n") if ln.strip().startswith("part ")]
    run = subprocess.run([f"{root}/.venv/bin/python", "-I", "-W", "error", f"{root}/tests/labs/E3/{twin}.py"],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    print(page, "twin lines", len(lines), "missing from page", len(missing),
          "| embedded part-lines", len(emb), "run lines", len(run), "identical", emb == run)
