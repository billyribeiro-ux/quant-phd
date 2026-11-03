"""Scan L05-L08 cards and lesson text for process words and banned phrases (BUILDER_RULES 1.3-1.4 subset),
and list the registry macros and symbols used. Usage: python -I process_words_g3.py <checkout> <scripts_dir>
"""
import json
import re
import sys

root, scripts = sys.argv[1], sys.argv[2]
cards = json.load(open(f"{root}/course/modules/E/E3/cards.json", encoding="utf-8"))
pw = re.compile(r"\b(build|builder|round|verifier|REQUEST|unit report|audit|ledger|pinned|fragment)\b", re.I)
hits = [(c["id"], m.group(0)) for c in cards if c["lesson"] in ("L05", "L06", "L07", "L08")
        for m in [pw.search(c["front"] + " " + c["back"])] if m]
print("process-word hits in L05-L08 cards:", hits)
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|"
                    r"you can add more|it is important to note|studies show|experts agree|it is well known|"
                    r"obviously|clearly", re.I)
for L in ("L05", "L06", "L07", "L08"):
    text = open(f"{scripts}/text/{L}.txt", encoding="utf-8").read()
    print(f"banned phrases in {L} text:", [m.group(0) for m in banned.finditer(text)])
    macros = sorted(set(re.findall(r"\\(E|R|Prob|Var|Cov|indic|Normal)(?![A-Za-z])", text)))
    raw = sorted(set(re.findall(r"\\mathbb\{[A-Za-z]\}|\\Phi|\\gamma_[34]|R_f|R\^\\ast|\\mathbb\{Q\}", text)))
    print(f"  registered macros used in {L}: {macros}; registered symbols used raw in {L}: {raw}")

v_hits = [c["id"] for c in cards if c["lesson"] == "L06" and re.search(r"\bV\b", c["front"] + " " + c["back"])]
print("L06 cards with a bare V (prospect value must be W):", v_hits)
