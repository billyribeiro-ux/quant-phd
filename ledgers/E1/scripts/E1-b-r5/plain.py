# Verifier-written: print lines [a,b] of a page as plain text, decoding entities and stripping only real tags.
import html, re, sys, pathlib
path, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
for i in range(a - 1, min(b, len(lines))):
    t = re.sub(r"</?[a-zA-Z][^>]*>", "", lines[i])
    t = html.unescape(t).strip()
    if t:
        print(f"{i+1}: {t}")
