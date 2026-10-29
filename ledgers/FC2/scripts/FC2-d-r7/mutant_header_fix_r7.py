from pathlib import Path
M = Path("/Users/billyribeiro/.fanout/wt/verifyC7-FC2-d/ledgers/FC2/mutants")
fix = {
    "r7_a_duplicate_strikes_accepted.py": "# Student error: the strike check accepts equal neighbouring strikes (b < a instead of b <= a).",
    "r7_c_discounted_strike_floored.py": "# Student error: the discounted strike is truncated to whole cents before the parity gap.",
}
for name, line in fix.items():
    p = M / name
    lines = p.read_text().split("\n")
    lines[1] = line
    p.write_text("\n".join(lines))
print("ok")
