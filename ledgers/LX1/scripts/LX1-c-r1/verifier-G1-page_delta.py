"""Verifier G1: delta of project.html between pin 95f3f8cb (old copy) and the checkout (new copy): TeX spans, href and id
attributes, banned strings, process words and scope words, computed on the changed lines only and on the whole page."""
import re
import sys
from pathlib import Path

old = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
new = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
changed = [(i + 1, o, n) for i, (o, n) in enumerate(zip(old, new)) if o != n]
print("line count old/new:", len(old), len(new), "| differing lines (same index):", [c[0] for c in changed])


def tex(text):
    return re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)


def learner(text):
    text = re.sub(r"<pre.*?</pre>", " ", text, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


old_tex = [t for line in old for t in tex(line)]
new_tex = [t for line in new for t in tex(line)]
print("TeX spans old/new:", len(old_tex), len(new_tex), "identical sequence:", old_tex == new_tex)
print("href/id attributes identical:", re.findall(r'(?:href|id)="[^"]*"', "\n".join(old)) == re.findall(r'(?:href|id)="[^"]*"', "\n".join(new)))
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "roughly", "historically", "About 6", "it can be shown", "round 1", "fixer", "verifier",
          "ruling", "builder", "agent"]
scope = r"\b(only|all|every|any|same|always|exactly|drives|never|each)\b"
process = r"\b(round|fixer|verifier|ruling|builder|agent|pin|ledger|audit)\b"
for lineno, o, n in changed:
    ln = learner(n)
    print(f"line {lineno}: banned hits {[b for b in banned if b.lower() in ln.lower()]}")
    print(f"line {lineno}: process hits {re.findall(process, ln, re.I)}")
    print(f"line {lineno}: scope hits {re.findall(scope, ln, re.I)} (old line: {re.findall(scope, learner(o), re.I)})")
whole_new = learner("\n".join(new))
print("whole page learner-prose banned hits:", [b for b in banned if b.lower() in whole_new.lower()])
print("whole page process-word hits:", [m.group(0) for m in re.finditer(process, whole_new, re.I)])
