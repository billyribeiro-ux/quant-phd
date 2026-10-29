"""Write three round-25 alternative correct engines (different algorithms or grids) from the reference, each edit must match once."""
import pathlib
ROOT = pathlib.Path("/tmp/verify25-CF1-d")
REF = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
ALTS = {
    "r25_a_multiplicative_grid_accumulation.py": (
        "    xs = [\n"
        "        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))\n"
        "        for k in range(_GRID_POINTS)\n"
        "    ]\n"
        "    xs[0], xs[-1] = _X_LOW, _X_HIGH\n",
        "    step = math.exp((math.log(_X_HIGH) - math.log(_X_LOW)) / (_GRID_POINTS - 1))\n"
        "    xs = [_X_LOW]\n"
        "    for _ in range(_GRID_POINTS - 2):\n"
        "        xs.append(xs[-1] * step)\n"
        "    xs.append(_X_HIGH)\n",
    ),
    "r25_b_horner_npv_reversed.py": (
        "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))\n",
        "    acc = 0.0\n"
        "    for cf in reversed(list(flows)):\n"
        "        acc = acc / (1.0 + rate) + cf\n"
        "    return acc\n",
    ),
    "r25_c_payback_fsum_prefix.py": (
        "        if cumulative + discounted[t] >= 0.0:\n"
        "            return (t - 1) + (-cumulative) / discounted[t]\n"
        "        cumulative += discounted[t]\n",
        "        if math.fsum(discounted[: t + 1]) >= 0.0:\n"
        "            return (t - 1) + (-cumulative) / discounted[t]\n"
        "        cumulative = math.fsum(discounted[: t + 1])\n",
    ),
}
for name, edits in ALTS.items():
    text = REF
    old, new = edits[0], edits[1]
    assert text.count(old) == 1, (name, text.count(old))
    text = text.replace(old, new)
    (ROOT / "ledgers/CF1/scripts/CF1-d-r25/alts" / name).write_text(text, encoding="utf-8")
    print("wrote", name)
