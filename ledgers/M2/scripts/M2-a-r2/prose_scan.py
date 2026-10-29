# Visible-text scan of the M2-a slice: banned phrases, process words, scope words, and word counts (pin 1817191).
# Usage: .venv/bin/python -I ledgers/M2/scripts/M2-a-r2/prose_scan.py
import html, re
PAGES = ["index.html"] + [f"L0{i}.html" for i in range(1, 7)]
BANNED = [r"roughly half", r"about 6%", r"historically", r"\.\.\.", "…", r"studies show", r"well known",
          r"important to note", r"for brevity", r"beyond the scope", r"left as an exercise", r"\bTODO\b", r"\bTBD\b",
          r"lorem", r"typically", r"in practice", r"\bmost\b", r"\bsmall\b", r"\bfast\b", r"\bsmooth\b", r"\boften\b",
          r"\bgenerally\b", r"\busually\b", r"\bclearly\b", r"obvious", r"trivial", r"of course", r"easy to see",
          r"\bbuild", r"\bbuilder", r"\bround\b", r"\bverif", r"REQUEST", r"unit report", r"\bledger", r"\bonly\b",
          r"\ball\b", r"\balways\b", r"\bevery\b", r"\bany\b", r"\bsame\b", r"\bdrives?\b", r"\boffsets?\b", r"\braises?\b",
          r"\bas much as\b", r"\bsimply\b", r"\bjust\b", r"\bhistor", r"\bhence\b"]
def visible(src):
    src = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
    src = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", src)))
for p in PAGES:
    raw = open(f"course/modules/M/M2/{p}", encoding="utf-8").read()
    t = visible(raw)
    print(f"== {p}: visible words {len(t.split())}")
    for pat in BANNED:
        hits = [m.start() for m in re.finditer(pat, t, flags=re.I)]
        if hits:
            print(f"  {pat!r}: {len(hits)}")
            for h in hits[:12]:
                print("     ...", t[max(0, h - 70):h + 60].replace("\n", " "), "...")
    # why-it-matters word count
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    if wim:
        print("  why-it-matters words:", len(visible(wim.group(1)).split()))
