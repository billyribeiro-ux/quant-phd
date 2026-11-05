"""Notation registry scan for M2 (project math and cards) and grep for references to removed card ids."""
import html, json, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); m2 = root / "course/modules/M/M2"
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered = [s["symbol"] for s in reg["symbols"]]
raw = (m2 / "project.html").read_text(encoding="utf-8")
math = " ".join(re.findall(r"\\\((.*?)\\\)", raw, flags=re.S) + re.findall(r"\\\[(.*?)\\\]", raw, flags=re.S))
cards = json.loads((m2 / "cards.json").read_text(encoding="utf-8"))
ctext = " ".join(c["front"] + " " + c["back"] for c in cards)
checks = {"T": r"(?<![A-Za-z\\])T(?![A-Za-z])", "\\Phi": r"\\Phi", "\\gamma_3/\\gamma_4": r"\\gamma_[34]", "R^\\ast": r"R\^\\ast",
          "R^{e\\ast}": r"R\^\{e\\ast\}", "R_f": r"R_f", "\\mathbb{Q}": r"\\mathbb\{Q\}", "\\mathbb{R}": r"\\mathbb\{R\}",
          "\\Prob": r"\\Prob", "\\E": r"\\E(?![a-zA-Z])"}
for name, pat in checks.items():
    print(f"{name:14s} project math hits={len(re.findall(pat, math))} card text hits={len(re.findall(pat, ctext))}")
print("registered symbols:", registered)
print("single-letter identifiers in project math:", sorted(set(re.findall(r"(?<![\\a-zA-Z])([A-Za-z])(?![a-zA-Z])", math))))
print("plain-text Q in cards (partition or difference quotient, not \\mathbb{Q}):", len(re.findall(r"\bQ\b", ctext)))
out = subprocess.run(["git", "grep", "-l", "-E", "M2-c408|M2-c411|M2-c412", "--", "course", "tests", "tools", "plans", "curriculum", "notation", "atlas"], cwd=root, capture_output=True, text=True)
print("references to removed ids (working tree, git grep):", repr(out.stdout.strip()), "exit", out.returncode)
