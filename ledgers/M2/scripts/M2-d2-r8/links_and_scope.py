"""Internal href/anchor resolution for L22-L24 (file ids checked), and scope-word context listing."""
import html
import re
from pathlib import Path

base = Path("course/modules/M/M2")
broken = []
for pg in ["L22", "L23", "L24"]:
    raw = (base / f"{pg}.html").read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', raw):
        if href.startswith("http"):
            broken.append((pg, href, "external"))
            continue
        file, _, frag = href.partition("#")
        p = base / (file or f"{pg}.html")
        if not p.exists():
            broken.append((pg, href, "missing file"))
            continue
        if frag and frag not in set(re.findall(r'id="([^"]+)"', p.read_text(encoding="utf-8"))):
            broken.append((pg, href, "missing anchor"))
print("broken internal links or anchors in L22-L24:", broken)
TAG = re.compile(r"<[^>]+>")
for pg in ["L22", "L23", "L24"]:
    raw = (base / f"{pg}.html").read_text(encoding="utf-8")
    text = html.unescape(TAG.sub(" ", re.sub(r"<pre[^>]*>.*?</pre>", " ", raw, flags=re.S)))
    text = re.sub(r"\s+", " ", text)
    for w in ["only", "all", "always", "same", "exactly", "never", "none", "any"]:
        for m in re.finditer(r"\b" + w + r"\b", text):
            print(f"{pg} [{w}]: ...{text[max(0, m.start() - 90):m.end() + 60]}...")
