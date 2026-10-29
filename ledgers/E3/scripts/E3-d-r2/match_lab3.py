import sys, json, re
sys.path.insert(0, "/tmp/verifyC2-E3-d/course/modules/E/E3/grader")
from instance import make_instance
src = open("/tmp/verifyC2-E3-d/course/modules/E/E3/project.html", encoding="utf-8").read()
import html
src = html.unescape(src)
block = src.split('data-run>"""Rung 3 reference case')[1].split("</code></pre>")[0]
ns = {}
start = block.index("ANSWERS")
end = block.index("]\n\n\ndef value")
exec("from fractions import Fraction\n" + block[start:end+1].replace("ANSWERS: list[tuple[int, str, list[int], list[str], list[int], list[str]]] = ", "ANSWERS = "), ns)
lab = ns["ANSWERS"]
print("lab answers:", len(lab))
hits = []
for s in range(0, 200):
    inst = make_instance(s)
    resp = json.loads(inst["responses_json"])
    if len(resp) != 12:
        continue
    ok = True
    for (pid, ch, pa, qa, pb, qb), r in zip(lab, resp):
        if r["choice"] != ch or [int(x) for x in r["prizes_a"]] != pa or r["probs_a"] != qa or [int(x) for x in r["prizes_b"]] != pb or r["probs_b"] != qb:
            ok = False; break
    if ok: hits.append(s)
print("seeds whose responses equal the lab data (0..199, 12 answers):", hits)
print("first seed responses sample:", json.loads(make_instance(0)["responses_json"])[0])
