"""Round-2 evidence checks for E3-d (run from the checkout root with the checkout's .venv python).

Prints: exemplar word counts, prize range and lottery facts, mixed-pair count, registry data-cite lines,
reading keys, registry symbols vs page math, process-word scan, network grep, hours greps, delta-method/Newton
names with the curriculum owners, and the grader docstring numbers.
"""
import html, json, re
from fractions import Fraction as F
from pathlib import Path

ROOT = Path.cwd()
PAGE = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
TEST = (ROOT / "course/modules/E/E3/grader/test_project.py").read_text(encoding="utf-8")

print("== exemplar word counts (tags stripped, whitespace split)")
for aid in ["exemplar-a", "exemplar-b"]:
    body = re.search(r'<article class="exemplar" id="%s".*?</article>' % aid, PAGE, re.S).group(0)
    paras = re.findall(r'<div class="memo-text">(.*?)</div>', body, re.S)
    txt = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", p)) for p in paras)
    print(aid, len(txt.split()))

print("== lab 3 answers: prize range, prize counts, mixed pairs, sums")
ns = {}
src = (ROOT / "tests/labs/E3/lab-E3-project-3.py").read_text(encoding="utf-8")
exec(compile(src.split("def value(")[0], "answers", "exec"), ns)
A = ns["ANSWERS"]
prizes = [x for a in A for x in a[2] + a[4]]
print("prize min", min(prizes), "max", max(prizes), "answers", len(A))
print("prize counts per lottery", sorted({len(a[2]) for a in A} | {len(a[4]) for a in A}))
def mixed(a):
    for pr, pb in ((a[2], a[3]), (a[4], a[5])):
        if any(x > 0 and F(p) > 0 for x, p in zip(pr, pb)) and any(x < 0 and F(p) > 0 for x, p in zip(pr, pb)):
            return True
    return False
print("mixed pairs", sum(mixed(a) for a in A), "non-mixed pair_ids", [a[0] for a in A if not mixed(a)])
print("probabilities sum to exactly 1 for every lottery:",
      all(sum(F(p) for p in a[3]) == 1 and sum(F(p) for p in a[5]) == 1 for a in A))

print("== data-cite claim spans and reading keys")
for f in ["L05.html", "L06.html", "L07.html", "L08.html", "L02.html"]:
    s = (ROOT / "course/modules/E/E3" / f).read_text(encoding="utf-8")
    for m in re.finditer(r'data-cite="([a-z0-9]+)"', s):
        print(f, m.group(1), "line", s.count("\n", 0, m.start()) + 1)
for m in re.finditer(r"Pratt \(1964\)[^<]{0,80}", (ROOT / "course/modules/E/E3/L02.html").read_text(encoding="utf-8")):
    print("L02 Pratt sentence:", m.group(0)[:90])
reg_all = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
reg = {e["key"] for e in reg_all["entries"]}
print("registry top-level keys", list(reg_all.keys()))
for k in ["pratt1964risk", "kahneman1979prospect", "epstein1989substitution", "ellsberg1961risk", "gilboa1989maxmin"]:
    print("registry", k, k in reg)

print("== notation: registered symbols vs page math")
nota = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
print("registered:", [s["symbol"] for s in nota["symbols"]])
maths = re.findall(r"\\\((.*?)\\\)", PAGE, re.S) + re.findall(r"\\\[(.*?)\\\]", PAGE, re.S)
cmds = sorted({c for m in maths for c in re.findall(r"\\[A-Za-z]+", m)})
print("LaTeX commands on page:", cmds)
print("gamma subscripts:", sum(1 for m in maths if re.search(r"\\gamma\s*_", m)), "| Phi uses:", sum(m.count("\\Phi") for m in maths))

print("== process words in learner text")
txt = re.sub(r"<script.*?</script>", "", PAGE, flags=re.S)
txt = re.sub(r"<[^>]+>", " ", txt)
for w in ["plan", "builder", "architect", "verifier", "fixer", "ledger", "batch", "mutant", "orchestrat", "TODO", "placeholder"]:
    print(w, len(re.findall(r"\b" + w, txt, re.I)))

print("== network and hours")
print("network tokens in page:", len(re.findall(r"fetch\(|XMLHttpRequest|sendBeacon|https?://", PAGE)))
print("data-hours-project:", re.findall(r'data-hours-project="(\d+)"', PAGE))

print("== concept names used by name (curriculum owners)")
cur = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))
owners = {}
for c in (cur["concepts"].values() if isinstance(cur["concepts"], dict) else cur["concepts"]):
    if isinstance(c, dict):
        owners.setdefault(c.get("name", ""), c.get("module"))
for name in ["Delta method", "Newton's method", "Loss aversion", "Probability weighting", "Hessian matrix",
             "Maximum likelihood estimation", "Asymptotic normality of the MLE"]:
    print(name, "->", owners.get(name))
for pat in ["delta method", "Newton", "maximum likelihood", "Hessian", "asymptotic"]:
    print("page", pat, [PAGE.count("\n", 0, m.start()) + 1 for m in re.finditer(pat, PAGE)])

print("== grader docstring numbers and kink wording")
print("kinks lines in test", [TEST.count("\n", 0, m.start()) + 1 for m in re.finditer("kink", TEST)])
print("kinks lines in page", [PAGE.count("\n", 0, m.start()) + 1 for m in re.finditer("kink", PAGE)])
print("every-model comments", [TEST.count("\n", 0, m.start()) + 1 for m in re.finditer("every model", TEST)])
print("1.3% line", [TEST.count("\n", 0, m.start()) + 1 for m in re.finditer(r"1\.3%", TEST)])
print("zeta lines in page", [PAGE.count("\n", 0, m.start()) + 1 for m in re.finditer(r"zeta", PAGE)][:6])
print("'choice-noise' on page:", "choice-noise" in PAGE, "| 'noise scale' on page:", "noise scale" in PAGE)
print("dominan* on page:", len(re.findall("dominan", PAGE, re.I)))
print("'assert=plain turns off' line:", [PAGE.count("\n", 0, m.start()) + 1 for m in re.finditer("turns off", PAGE)])
