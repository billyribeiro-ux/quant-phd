"""Round-4 verifier (E3-d): text scans of project.html and the grader files.

(1) curriculum concept names on the page, with owners (DAG, plan section 7); (2) process words; (3) BUILDER_RULES 1.3-1.4
banned strings; (4) 'kink'; (5) external and network references in the page; (6) figures and data files on the page;
(7) first use of zeta and kappa on the page; (8) in-page anchors and linked targets.
"""
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
src = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", src, flags=re.S)))
text = re.sub(r"\s+", " ", text)
low = text.lower()

cj = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))["concepts"]
print("(1) concept names found on the page (owner from curriculum.json):")
for cid, meta in sorted(cj.items()):
    names = {cid.replace("-", " ")}
    if isinstance(meta, dict) and meta.get("name"):
        names.add(str(meta["name"]).lower())
    for n in names:
        if len(n) >= 5 and re.search(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])", low):
            print("   ", cid, "| owner", meta.get("module") if isinstance(meta, dict) else meta, "| matched", repr(n))
            break

print("(2) process words:", [w for w in ["verif", "builder", "fixer", "round", "audit", "planner", "architect",
                                       "ledger", "todo", "placeholder"] if w in low] or "none")
banned = ["todo", "tbd", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "roughly", "historically", "...", "…", "it can be shown"]
print("(3) BUILDER_RULES banned strings found:", [b for b in banned if b in low] or "none")
print("(4) 'kink' on page:", bool(re.search("kink", src, re.I)),
      "| in grader/*.py:", any(re.search("kink", p.read_text(encoding="utf-8"), re.I)
                              for p in (ROOT / "course/modules/E/E3/grader").glob("*.py")))
ext = re.findall(r"(?:https?:)?//[^\s\"')]+", src)
print("(5) external URLs:", ext or "none", "| network APIs:",
      [w for w in ["fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon", "window.open", "import("] if w in src] or "none",
      "| Blob/createObjectURL:", "Blob(" in src and "URL.createObjectURL" in src)
print("(6) figures or data files on the page:", len(re.findall(r"<svg|<figure|<img|data-files", src)))
print("(7) first zeta on page:", repr(text[max(0, text.find("zeta") - 60):text.find("zeta") + 40]))
print("    first kappa on page:", repr(text[max(0, text.find("kappa") - 40):text.find("kappa") + 20]))
ids = set(re.findall(r'\sid="([^"]+)"', src))
hrefs = set(re.findall(r'href="#([^"]+)"', src))
print("(8) in-page anchors:", len(hrefs), "| unresolved:", sorted(h for h in hrefs if h not in ids) or "none")
