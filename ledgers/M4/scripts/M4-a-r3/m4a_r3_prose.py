"""Round-3 verifier scans for M4 slice a: visible-text scans, macros, word counts, card numbers.

Usage: python -I -W error m4a_r3_prose.py <repo_root>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
M4 = ROOT / "course" / "modules" / "M" / "M4"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html"]
REGISTERED = {
    "E",
    "Prob",
    "Var",
    "Cov",
    "Corr",
    "R",
    "N",
    "indic",
    "Normal",
    "iid",
    "dto",
    "pto",
    "argmax",
    "argmin",
    "tr",
    "diag",
    "SR",
    "hSR",
    "PSR",
    "DSR",
    "PBO",
    "FWER",
    "FDR",
    "FDP",
    "se",
    "emgamma",
}


def visible(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<pre class=\"expected\".*?</pre>", " ", text, flags=re.S)  # output blocks reported separately
    text = re.sub(r"<code class=\"language-python\" data-run>.*?</code>", " ", text, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", text))


banned = re.compile(
    r"\b(TODO|TBD|lorem|clearly|obviously|for brevity|details omitted|beyond the scope|left as an exercise|"
    r"you can add more|it is important to note|studies show|experts agree|it is well known|well known)\b|\.\.\.",
    re.I,
)
process = re.compile(
    r"\b(builder|verifier|verif\w*|ledger|round \d|open item|architect|plan \w+|draft|Q\d+|REFERENCE_REQUESTS)\b", re.I
)
scope = re.compile(r"\b(always|every|all|only|exactly|any|same|drives|never)\b", re.I)

out: list[str] = []
for name in PAGES:
    raw = (M4 / name).read_text(encoding="utf-8")
    vis = visible(raw)
    hits_b = [m.group(0) for m in banned.finditer(vis)]
    hits_p = [m.group(0) for m in process.finditer(vis)]
    out.append(f"{name}: banned_hits={hits_b} process_hits={hits_p}")
    # macros used anywhere in page math (inside \( \) and \[ \] and in <td>/<p> text)
    cmds = sorted(set(re.findall(r"\\([A-Za-z]+)", html.unescape(raw))))
    out.append(f"{name}: latex_commands={' '.join(cmds)}")
    # why-it-matters word count
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    if wim:
        words = len(visible(wim.group(1)).split())
        out.append(f"{name}: why_it_matters_words={words} (limit 120)")
    out.append(
        f"{name}: data-chart count={raw.count('data-chart')} data-files count={raw.count('data-files')} script-src non-local={re.findall(r'src=\"(https?://[^\"]+)\"', raw)}"
    )

# registered-symbol usage check: \T, \Phi, \gamma_3, \gamma_4, \varphi, \mathbb, \R
for name in PAGES:
    raw = html.unescape((M4 / name).read_text(encoding="utf-8"))
    for pat in [
        r"\\mathbb\{",
        r"\\Phi",
        r"\\varphi",
        r"\\gamma_\{?[34]",
        r"\\operatorname\{Var\}",
        r"\\operatorname\{Cov\}",
        r"\\R\b",
        r"\\E\b",
        r"\\Var\b",
        r"\\Cov\b",
    ]:
        n = len(re.findall(pat, raw))
        if n:
            out.append(f"{name}: pattern {pat} count={n}")

# card numbers appear in their lesson (visible text plus lab output blocks)
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))
missing = []
lessons = {f"L0{i}": (M4 / f"L0{i}.html").read_text(encoding="utf-8") for i in range(1, 5)}
for card in cards:
    if card["lesson"] not in lessons:
        continue
    lesson_text = html.unescape(lessons[card["lesson"]])
    for tok in set(re.findall(r"\d+(?:\.\d+)?", card["back"] + " " + card["front"])):
        if tok in ("1", "0", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            continue
        if tok not in lesson_text:
            missing.append((card["id"], tok))
out.append(
    f"cards L01-L04 count={sum(1 for c in cards if c['lesson'] in ('L01', 'L02', 'L03', 'L04'))}; numbers (>=11 or decimal) absent from lesson: {missing}"
)

dups = {}
for card in cards:
    dups.setdefault(card["front"].strip().lower(), []).append(card["id"])
out.append(f"duplicate fronts across deck: {[k for k, v in dups.items() if len(v) > 1]}")
for card in cards:
    if card["lesson"] in ("L01", "L02", "L03", "L04") and card["grade"] not in ("T", "C"):
        out.append(f"card {card['id']} grade {card['grade']}")
    if card["grade"] == "C" and not card.get("basis"):
        out.append(f"card {card['id']} grade C without basis")
    if card["grade"] == "T" and card.get("basis"):
        out.append(f"card {card['id']} grade T with basis")
print("\n".join(out))
