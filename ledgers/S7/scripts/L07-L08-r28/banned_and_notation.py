"""Round 28: banned-phrase scan (BUILDER_RULES 1.2-1.4 strings, ellipses, 'about half'/'roughly half' and bare
percentages in the visible prose) and notation collisions with the four AP1 symbols added to notation.json
(R_f, \\mathbb{Q}, R^\\ast, R^{e\\ast}) for the two lessons. Visible text = HTML with tags and <script> removed."""

import html
import json
import re
from pathlib import Path

ROOT = Path("/tmp/verify-s7-r1-l78")
PAGES = [ROOT / "course/modules/S/S7/L07.html", ROOT / "course/modules/S/S7/L08.html"]
BANNED = ["roughly half", "about half", "beyond this lesson", "...", "…", "obviously", "clearly", "simply", "trivially", "it is easy", "as we saw"]
for page in PAGES:
    raw = page.read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    print(page.name, "visible words", len(text.split()))
    for phrase in BANNED:
        hits = [m.start() for m in re.finditer(re.escape(phrase), text, flags=re.I)]
        if hits:
            print(f"  banned phrase {phrase!r}: {len(hits)} hit(s); first context: {text[max(0, hits[0]-60):hits[0]+60]!r}")
    for m in re.finditer(r"(about|roughly|nearly|around|some)\s+\d+(\.\d+)?\s*%", text):
        print("  bare approximate percentage:", repr(text[max(0, m.start()-40):m.end()+20]))
    for m in re.finditer(r"about\s+(half|one half|a half)", text, flags=re.I):
        print("  'about half' form:", repr(text[max(0, m.start()-60):m.end()+30]))
    for sym in ["R_f", "R_{f}", "\\mathbb{Q}", "\\Q", "R^\\ast", "R^{e\\ast}", "R^{e*}", "R^*"]:
        n = raw.count(sym)
        if n:
            print(f"  notation {sym!r} occurs {n} time(s)")
    for sym in ["\\Prob", "\\E", "\\Var"]:
        pass
notation = json.loads((ROOT / "course/assets/data/notation.json").read_text(encoding="utf-8"))
print("notation entries:", len(notation.get("entries", notation.get("symbols", []))) if isinstance(notation, dict) else len(notation))
macros = notation.get("macros", {})
print("macro names matching Q / Rf / Rstar:", [k for k in macros if k in ("\\Q", "\\Rf", "\\Rstar", "\\Re", "\\Rstarstar", "\\Ree")])
print("keys with 'SR' in name:", [k for k in macros if "SR" in k][:10])
print("AP1 entries:", [e["symbol"] for e in notation.get("symbols", []) if e.get("module") == "AP1"] if "symbols" in notation else "n/a")
