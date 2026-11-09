"""Round 16: scope-word contexts in project.html prose, and in-page / cross-page anchor resolution.

Usage: python -I scope_and_anchors_r16.py <checkout-root>
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
html = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
# keep only element text outside <script>, <style>, <code>, <pre> and math, then split sentences
body = re.sub(r"<(script|style|pre|code)\b.*?</\1>", " ", html, flags=re.S)
text = re.sub(r"\\\((.*?)\\\)", " MATH ", body, flags=re.S)
text = re.sub(r"<[^>]+>", " ", text)
words = r"\b(only|all|every|always|any|same|exactly|drives|whatever|each)\b"
hits = [m for m in re.finditer(words, text, flags=re.I)]
print("scope-word hits in prose:", len(hits))
for m in hits:
    s = max(0, m.start() - 70)
    ctx = " ".join(text[s:m.end() + 60].split())
    print(f"- [{m.group(0)}] ...{ctx}...")
ids = set(re.findall(r'\sid="([^"]+)"', html))
hrefs = re.findall(r'href="#([^"]+)"', html)
print("in-page hrefs:", len(hrefs), "unresolved:", [h for h in hrefs if h not in ids])
cross = sorted(set(re.findall(r'href="([^"#]+\.html)#([^"]+)"', html)))
for page, anchor in cross:
    target = (root / "course/modules/E/E4" / page).resolve() if not page.startswith("../") else (root / "course/modules/E/E4" / page).resolve()
    if not target.exists():
        print("MISSING PAGE", page)
        continue
    ok = f'id="{anchor}"' in target.read_text(encoding="utf-8")
    print("cross-page", page, anchor, "resolves" if ok else "UNRESOLVED")
