# Verifier check: each embedded data-run block in the L09-L11 pages equals its lab twin (after strip).
import html, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
for lab in ("L09", "L10", "L11"):
    src = (root / f"course/modules/CS/CS2/{lab}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r"data-run>(.*?)</code></pre>", src, re.S).group(1))
    twin = (root / f"tests/labs/CS2/lab-CS2-{lab}-1.py").read_text(encoding="utf-8")
    print(lab, "IDENTICAL" if code.strip() == twin.strip() else "DIFFERENT")
