"""Generate the verifier's round-3 student-error mutants from the reference solution (one change each)."""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    "v01_convexity_zero_net_kept": (
        "Convexity finding kept when its net is exactly zero, because the convexity net test uses >= 0 instead of > 0.",
        [('                    "kind": "convexity",\n', '                    "kind": "convexity",\n'),
         ("        net = gross - per_finding\n        if net > 0:\n            findings.append(\n                {\n"
          "                    \"kind\": \"convexity\"",
          "        net = gross - per_finding\n        if net >= 0:\n            findings.append(\n                {\n"
          "                    \"kind\": \"convexity\"")],
    ),
    "v02_parity_explanation_names_P1_only": (
        "Parity explanation names only P1, omitting P2, P3, the supplied discount factor P4 and the cost P6 it depends on.",
        [("f\"put-call parity (P1 European exercise, P2 one expiry, P3 no income, P4 the supplied discount factor): \"",
          "f\"put-call parity (P1 European exercise): \""),
         ("f\"{spread} (P6).\"", "f\"{spread}.\"")],
    ),
    "v03_parity_gross_bankers_round": (
        "Parity gross rounded with Python round(), which sends an exact half cent to the even cent, not up.",
        [("        gross = _half_up(abs(gap))\n        net = gross - per_finding\n        if net > 0:\n            findings.append(\n"
          "                {\n                    \"kind\": \"parity\"",
          "        gross = round(abs(gap))\n        net = gross - per_finding\n        if net > 0:\n            findings.append(\n"
          "                {\n                    \"kind\": \"parity\"")],
    ),
    "v04_convexity_returns_one_based_index": (
        "Convexity indices returned one-based (j + 1), so every convexity finding is attached to the next strike.",
        [("    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]",
          "    return [j + 1 for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]")],
    ),
    "v05_convexity_findings_before_parity": (
        "Findings returned with convexity records first, reversing the required parity-then-convexity order.",
        [("    return findings\n", "    return sorted(findings, key=lambda record: record[\"kind\"] == \"parity\")\n")],
    ),
    "v06_gross_rounds_signed_gap_then_abs": (
        "Parity gross taken as the magnitude of the signed half-up rounding, so a negative half cent rounds down in magnitude.",
        [("        gross = _half_up(abs(gap))\n", "        gross = abs(_half_up(gap))\n")],
    ),
}

for name, (doc, pairs) in MUTANTS.items():
    src = REF
    for old, new in pairs:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    header = f'"""{doc}\n\nMutant of the reference scanner: one change, everything else as in reference.py.\n"""\n'
    body = src.split('"""', 2)[2]
    (OUT / f"{name}.py").write_text(header + body, encoding="utf-8")
    print("wrote", name)
