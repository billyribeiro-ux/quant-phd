"""Word counts for the two exemplars: a word is a run of characters between spaces (brief, project.html Length).

Reads the blind extract written by blind_exemplars_r14.py. Body = the five brief sections; Summary separately.
"""
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
parts = re.split(r"^=== (Exemplar [AB]) ===$", text, flags=re.M)
heads = {"Summary", "Setup and conventions", "The checks", "Discretization", "Limitations", "Appendix · Proofs"}
for i in range(1, len(parts), 2):
    name, body = parts[i], parts[i + 1]
    sections = re.split(r"^(Summary|Setup and conventions|The checks|Discretization|Limitations|Appendix · Proofs|Assumptions for P\d\.|P\d\. .*)$", body, flags=re.M)
    cur = None
    counts = {}
    for chunk in sections:
        s = chunk.strip()
        if s in heads:
            cur = s
            counts.setdefault(cur, 0)
            continue
        if cur is None:
            continue
        counts[cur] += len(s.split(" ")) if s else 0
        counts[cur] = counts[cur]
    # recount with explicit whitespace tokens
    tokens = {k: 0 for k in counts}
    cur = None
    for chunk in sections:
        s = chunk.strip()
        if s in heads:
            cur = s
            continue
        if cur is not None and s:
            tokens[cur] += len([t for t in re.split(r"\s+", s) if t])
    body_words = sum(v for k, v in tokens.items() if k in {"Summary", "Setup and conventions", "The checks", "Discretization", "Limitations"})
    print(name, "per-section words:", tokens)
    print(name, "body (five sections) words:", body_words, " Summary words:", tokens.get("Summary"))
