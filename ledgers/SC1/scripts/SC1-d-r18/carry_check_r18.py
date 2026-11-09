"""For each round-17 row, list the repository files its location/evidence cite and whether any of them changed in
700bf33f..50559266 (from delta_files_r18.txt). Usage: python3 -I carry_check_r18.py <frag.json> <delta.txt>"""
import json
import re
import sys

frag = json.load(open(sys.argv[1]))
changed = set(line.strip() for line in open(sys.argv[2]) if line.strip())
pat = re.compile(r"((?:course|tests|plans|ledgers|references|tools|curriculum|notation|atlas|benchmarks)/[A-Za-z0-9_./\-]+|CURRICULUM\.md|BLUEPRINT\.md|BUILDER_RULES\.md|VERIFIER_RULES\.md|L0[0-9]\.html|project\.html|cards\.json)")
for r in frag["rows"]:
    text = " ".join([r.get("location", ""), r.get("evidence", "")])
    files = sorted(set(m.group(1).rstrip(".,;:)") for m in pat.finditer(text)))
    hit = [f for f in files if any(c == f or c.endswith("/" + f) or f.endswith(c) for c in changed)]
    print(f"{r['status']:4} {r['id']:48} changed={'Y' if hit else 'n'} files={len(files)} hit={hit[:4]}")
