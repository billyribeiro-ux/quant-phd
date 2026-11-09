"""Find every '<' followed by a letter whose tag name is not followed by a space, '>' or '/' (a raw comparison in math or prose)."""
import re
from pathlib import Path
for name in ("L05", "L06", "L07"):
    text = Path(f"course/modules/M/M5/{name}.html").read_text(encoding="utf-8")
    hits = []
    for m in re.finditer(r"<([A-Za-z][A-Za-z0-9]*)(.?)", text):
        nxt = m.group(2)
        if nxt not in (" ", ">", "/", "\n", "\t", ""):
            line = text.count("\n", 0, m.start()) + 1
            hits.append((line, text[max(0, m.start()-25):m.end()+15].replace("\n", " ")))
    print(name, "suspicious '<' hits:", len(hits))
    for h in hits:
        print("  ", h)
    # also '<' followed by a digit, space or '=' inside math spans
    math_lt = [(text.count("\n", 0, m.start()) + 1) for m in re.finditer(r"\\\((?:(?!\\\)).)*?<\s*[0-9=\\ ]", text)]
    print(name, "math '<' followed by digit/space/backslash (unescaped in tag-free text):", math_lt[:20])
