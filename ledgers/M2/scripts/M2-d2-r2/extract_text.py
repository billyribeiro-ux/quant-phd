"""Extract visible text (KaTeX source kept, tags stripped) of a slice page and scan banned phrases and scope words."""
import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "well known", "obviously",
          "clearly", "it can be shown", "...", "…", "roughly", "typically", "in practice", "small", "smooth",
          "fast", "most", "always", "every", "any", "only", "exactly", "same", "drives", "all", "generally", "usually",
          "tends", "significant", "robust", "strong", "good", "bad", "builder", "verifier", "ledger", "Round", "round-trip",
          "clearly", "essentially", "naturally", "intuitively", "obvious", "trivially", "without loss", "in general"]
for L in sys.argv[2:]:
    raw = (root / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    text = re.sub(r"<pre.*?</pre>", lambda m: "\n[PRE]\n", body, flags=re.S)
    text = re.sub(r"<br\s*/?>|</p>|</li>|</h[1-6]>|</div>|</tr>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    out = Path(sys.argv[0]).parent / f"text_{L}.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(L, "lines", len(lines), "chars", sum(len(l) for l in lines))
    for i, l in enumerate(lines, 1):
        for b in banned:
            if re.search(r"(?<![A-Za-z])" + re.escape(b) + r"(?![A-Za-z])", l, flags=re.I):
                print(f"  {L} text-line {i} [{b}]: {l[:160]}")
