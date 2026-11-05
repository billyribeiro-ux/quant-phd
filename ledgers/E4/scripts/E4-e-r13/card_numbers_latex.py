"""Verifier r13: card numeric tokens vs lesson text, with LaTeX fractions (\\tfrac, \\frac, \\dfrac) normalised to a/b first."""
import json
import re
import sys
from collections import Counter

ROOT = sys.argv[1]
TXT = sys.argv[2]
cards = json.load(open(f"{ROOT}/course/modules/E/E4/cards.json", encoding="utf-8"))
lessons = {}
for n in range(1, 10):
    raw = open(f"{TXT}/L0{n}.txt", encoding="utf-8").read()
    raw = re.sub(r"\\[tdc]?frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", raw)
    raw = re.sub(r"\\[tdc]?frac(\d)(\d)", r"\1/\2", raw)
    raw = re.sub(r"\\[tdc]?frac\{([^{}]*)\}(\d)", r"\1/\2", raw)
    raw = re.sub(r"\\[tdc]?frac(\d)\{([^{}]*)\}", r"\1/\2", raw)
    raw = raw.replace("\\(", "").replace("\\)", "").replace("\\", "").replace("{", "").replace("}", "")
    lessons[f"L0{n}"] = raw
num_re = re.compile(r"\d+(?:\.\d+)?(?:e-?\d+)?(?:/\d+)?")
absent = []
checked = 0
for c in cards:
    text = c["front"] + " " + c["back"]
    lesson_text = lessons[c["lesson"]].replace(" ", "")
    for tok in sorted(set(num_re.findall(text))):
        checked += 1
        if tok in ("0", "1", "2"):
            continue
        if tok.replace(" ", "") not in lesson_text:
            absent.append((c["id"], c["lesson"], tok))
print("numeric tokens checked", checked)
print("absent after LaTeX normalisation (excluding 0,1,2):", len(absent))
for row in absent:
    print("  ", row)
