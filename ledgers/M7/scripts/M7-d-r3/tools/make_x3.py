import sys, pathlib
ref = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])
def patch(name, doc, pairs, tail=""):
    text = ref
    for old, new in pairs:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    # the one-line docstring names the error, then the reference body
    head, rest = text.split('"""', 2)[0], text.split('"""', 2)
    body = rest[2]
    text = '"""' + doc + '\n\nMutant of grader/reference.py: one change, as the first line states.\n"""' + body + tail
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
patch("x3_01_solution_memoised_by_asset_count.py",
      "Student error x3-01: allocate caches its first answer per number of assets and returns it for any later case with the same count.",
      [],
      tail='''

_CACHE: dict[int, dict[str, Any]] = {}
_allocate_plain = allocate


def allocate(instance: dict[str, Any]) -> dict[str, Any]:  # noqa: F811
    key = len(instance["mu"]) if isinstance(instance, Mapping) and "mu" in instance else -1
    if key not in _CACHE:
        _CACHE[key] = _allocate_plain(instance)
    return _CACHE[key]
''')
patch("x3_02_sector_cap_sign_reversed_as_a_floor.py",
      "Student error x3-02: the sector cap is written with the wrong sign, so each sector sum must be at least its cap.",
      [("rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap, (\"sector\", k)))",
        "rows.append(([Fraction(-1) if problem.sector[j] == k else Fraction(0) for j in range(n)], -cap, (\"sector\", k)))")])
patch("x3_03_box_upper_bounds_relaxed_by_1e-7.py",
      "Student error x3-03: every upper weight bound is loosened by 1e-7, a tolerance applied to the bound rather than to the check.",
      [("rows.append(([Fraction(1) if j == i else Fraction(0) for j in range(n)], problem.upper[i], (\"upper\", i)))",
        "rows.append(([Fraction(1) if j == i else Fraction(0) for j in range(n)], problem.upper[i] + Fraction(1, 10**7), (\"upper\", i)))")])
patch("x3_04_dual_residual_reported_without_the_floor.py",
      "Student error x3-04: the dual residual is reported as the negative of the smallest inequality multiplier, without the floor at zero.",
      [("dual = max(Fraction(0), -min(mult_ineq))", "dual = -min(mult_ineq)")])
