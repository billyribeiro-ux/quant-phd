"""Strip tags from the M7 slice pages and scan for banned phrases, process words and out-of-closure terms."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "course/modules/M/M7"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
PATTERNS = {
    "banned": r"roughly|about |historically|typically|usually|generally|often|mostly|\.\.\.|…|etc\.|in general|almost",
    "process": r"builder|verifier|\bround\b|unit report|requests|pinned|fragment",
    "outside-closure": r"covariance|correlation|multivariate|dynamic programming|contraction|efficient frontier|newton|convexity|variance",
    "scope": r"\bonly\b|\ball\b|\balways\b|\bevery\b|\bany\b|\bsame\b|\bdrives\b|\boffsets\b|\braises\b|\bas much as\b",
}
for name in PAGES:
    raw = (ROOT / name).read_text(encoding="utf-8")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text)
    for label, pat in PATTERNS.items():
        hits = [m.start() for m in re.finditer(pat, text, flags=re.I)]
        for pos in hits:
            print(f"{name} [{label}] ...{text[max(0, pos - 70):pos + 60]}...")
    print(f"{name}: scanned {len(text)} characters")
