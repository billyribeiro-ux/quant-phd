"""Round-35 random sample (fixed seeds, 50 per page) of the small numeric tokens classified by small_token_classes.py.
Writes the sample as: page, index, class, line, token, context. Run after small_token_classes.py.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r35/sample_tokens.py <small_tokens.tsv>
"""

import random
import sys

rows = [line.rstrip("\n").split("\t", 4) for line in open(sys.argv[1], encoding="utf-8")]
for page, seed in (("L05", 35), ("L06", 36)):
    pool = [r for r in rows if r[1] == page]
    rng = random.Random(seed)
    sample = rng.sample(range(len(pool)), 50)
    for k, idx in enumerate(sorted(sample), 1):
        cls, pg, line, tok, ctx = pool[idx]
        print(f"{page}\t{k:02d}\t{cls}\t{line}\t{tok}\t{ctx}")
