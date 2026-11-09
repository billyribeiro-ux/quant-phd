# Rebuilds the standing lab-claim mutant set (the base round's five, ruling 37) as one-line edits of the twins.
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
TW = ROOT / "tests/labs/FC1"
OUT = ROOT / "ledgers/FC1/mutants/fc1a-r1"
OUT.mkdir(parents=True, exist_ok=True)
EDITS = {
    "lab-mut-r5-L01-half-limit-comparison-flipped": ("lab-FC1-L01-1.py",
        "print(\"the full-redeposit limit exceeds the half-redeposit limit:\", full_limit > half_limit)",
        "print(\"the full-redeposit limit exceeds the half-redeposit limit:\", full_limit < half_limit)"),
    "lab-mut-r5-L01-closed-form-exponent-short": ("lab-FC1-L01-1.py",
        "return (1 - q ** (n + 1)) / reserve_ratio",
        "return (1 - q ** n) / reserve_ratio"),
    "lab-mut-r5-L02-well-formed-accepts-two-values": ("lab-FC1-L02-1.py",
        "all(len(values[axis]) == 1 and values[axis][0] in allowed",
        "all(len(values[axis]) >= 1 and values[axis][0] in allowed"),
    "lab-mut-r5-L03-tie-pays-full-profit": ("lab-FC1-L03-1.py",
        "    if ask == rival:\n        return (ask - cost) * shares",
        "    if ask == rival:\n        return 2 * (ask - cost) * shares"),
    "lab-mut-r5-L03-spread-capture-doubled": ("lab-FC1-L03-1.py",
        "    return half * sum(t.shares for t in trades)",
        "    return 2 * half * sum(t.shares for t in trades)"),
}
for name, (src, old, new) in EDITS.items():
    text = (TW / src).read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{name}: pattern found {count} times in {src}")
    (OUT / f"{name}__{src}").write_text(text.replace(old, new), encoding="utf-8")
    print(f"wrote {name}__{src}")
