"""Round 5 verifier (FC1-c): every card's label citations and numeric tokens must occur in its lesson text or lab output."""
import json, pathlib, re

CARDS = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c/course/modules/FC/FC1/cards.json")
TXT = pathlib.Path("/tmp/fc1c_r5_text")
LAB = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c/ledgers/FC1/scripts/FC1-c-r5/out/lesson_labs_output_r5.out")
lessons = {n: (TXT / f"{n}.txt").read_text(encoding="utf-8") for n in ["L01", "L02", "L03", "L04", "L05"]}
lab_text = LAB.read_text(encoding="utf-8")
label_re = re.compile(r"(Definition|Proposition|Remark|Assumptions?|Example|Problem|Corollary|Section|Misconception|misconception|Lab \d, Part [A-D]|Assumption [A-Z]\d|Assumption [0-9.]+|Assumptions [A-Z]\d to [A-Z]\d|Part [A-D])\s?[A-Z]?[0-9][0-9.()]*")
num_re = re.compile(r"(?<![A-Za-z_])-?\d{3,}(?:\.\d+)?")
problems = []
for c in json.loads(CARDS.read_text(encoding="utf-8")):
    L = c["lesson"]
    hay = lessons[L] + "\n" + lab_text
    fields = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    hay_l = hay.lower()
    for tok in sorted(set(m.group(0).rstrip(").,;") for m in label_re.finditer(fields))):
        norm = tok.replace("Assumptions", "Assumption")
        num = tok.split()[-1] if tok.split()[-1][:1].isdigit() else None
        ok = norm.lower() in hay_l or tok.lower() in hay_l
        if not ok and tok.startswith("Section") and num:
            ok = re.search(r"(^|\n)" + re.escape(num) + r"[A-Z]", hay) is not None
        if not ok and "misconception" in tok.lower():
            ok = "misconception" in hay_l
        if not ok:
            problems.append((c["id"], L, "label not in lesson", tok))
    for tok in sorted(set(num_re.findall(fields))):
        t = tok.lstrip("-")
        if t not in hay and t.replace(",", "") not in hay:
            problems.append((c["id"], L, "number not in lesson/lab", tok))
for p in problems:
    print(p)
print("problems:", len(problems))
