"""Round-12 structural checks for SC1 slice b (L04-L06, twins, changed cards, hub).

Run: <checkout>/.venv/bin/python -I -W error <this file>. Paths are absolute to the verifier checkout (pin 5db69a9).
Each block prints the observed values that a fragment row cites.
"""

import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE12-SC1-b")
PY = str(ROOT / ".venv" / "bin" / "python")
SC1 = ROOT / "course" / "modules" / "SC" / "SC1"
LABS = ROOT / "tests" / "labs" / "SC1"
PREV_PIN = "11d7077a290f7960b183d3a5a6631af4773888f9"


def git_show(rev: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{rev}:{path}"], capture_output=True, text=True, check=True
    ).stdout


print("== subject byte-identity, 11d7077 vs 5db69a9 (slice files)")
for rel in [
    "course/modules/SC/SC1/L04.html",
    "course/modules/SC/SC1/L05.html",
    "course/modules/SC/SC1/L06.html",
    "course/modules/SC/SC1/index.html",
    "tests/labs/SC1/lab-SC1-L04-1.py",
    "tests/labs/SC1/lab-SC1-L05-1.py",
    "tests/labs/SC1/lab-SC1-L06-1.py",
]:
    old = git_show(PREV_PIN, rel)
    new = (ROOT / rel).read_text(encoding="utf-8")
    print(rel, "byte-identical" if old == new else "CHANGED", len(new.encode()))

print("== twin match (page code == twin; expected == twin stdout; twin under -I -W error)")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1))
    twin = (LABS / f"lab-SC1-{lab}-1.py").read_text(encoding="utf-8")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    run = subprocess.run([PY, "-I", "-W", "error", str(LABS / f"lab-SC1-{lab}-1.py")], capture_output=True, text=True)
    print(
        lab,
        "exit",
        run.returncode,
        "stderr_bytes",
        len(run.stderr.encode()),
        "code==twin",
        code.rstrip("\n") == twin.rstrip("\n"),
        "expected==stdout",
        expected.rstrip("\n") == run.stdout.rstrip("\n"),
    )
    open(ROOT / "ledgers/SC1/scripts/SC1-b-r12/out" / f"twin_{lab}.stdout", "w", encoding="utf-8").write(run.stdout)

print("== why-it-matters word counts (limit 120; math replaced by x)")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    wim = html.unescape(re.sub(r"<[^>]+>", " ", re.search(r'<p class="why-it-matters">(.*?)</p>', page, re.S).group(1)))
    wim = re.sub(r"\\\((.*?)\\\)", "x", wim)
    print(lab, len(wim.split()))

print("== quiz items, explanations, problems, solutions")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    quiz = page[page.index('class="quiz"') :]
    print(
        lab,
        "quiz items",
        quiz.count('<li class="item"'),
        "explanations",
        quiz.count('class="explain" hidden'),
        "problems",
        len(re.findall(r'class="problem-title"', page)),
        "solutions",
        page.count('<details class="solution">'),
    )

print("== cards: slice ids, changed/added/removed vs 11d7077")
cards_now = json.loads((SC1 / "cards.json").read_text(encoding="utf-8"))
cards_prev = json.loads(git_show(PREV_PIN, "course/modules/SC/SC1/cards.json"))
ids = [c["id"] for c in cards_now]
print("cards total", len(cards_now), "duplicate ids", len(ids) - len(set(ids)))
prev = {c["id"]: c for c in cards_prev}
now = {c["id"]: c for c in cards_now}
print("added", sorted(set(now) - set(prev)))
print("removed", sorted(set(prev) - set(now)))
changed = [i for i in now if i in prev and prev[i] != now[i]]
print("changed", changed)
print("slice cards (L04-L06):", sum(1 for c in cards_now if c["lesson"] in ("L04", "L05", "L06")))
print("cards without grade (slice):", [c["id"] for c in cards_now if c["lesson"] in ("L04", "L05", "L06") and "grade" not in c])

print("== hub hours")
hub = (SC1 / "index.html").read_text(encoding="utf-8")
print(re.search(r'data-hours-lessons="\d+" data-hours-project="\d+"', hub).group(0))
print("lesson data-hours:", [re.search(r'data-hours="(\d+)"', (SC1 / f"L0{i}.html").read_text(encoding="utf-8")).group(1) for i in range(1, 9)])

print("== notation scan: T as a math symbol; H; macros used in slice pages")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    macros = sorted(set(re.findall(r"\\([A-Za-z]+)", page)))
    print(lab, "macros", macros)
    print(lab, "T as math symbol:", bool(re.search(r"\\\(\s*T\b", page)), "| '\\\\Phi' uses:", page.count("\\Phi"))
