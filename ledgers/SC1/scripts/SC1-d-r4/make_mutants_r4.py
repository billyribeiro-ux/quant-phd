"""Verifier r4: write five new student-error mutants as single-change copies of grader/reference.py."""
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE4-SC1-d")
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/mutants"

MUTANTS = {
    "m27_nested_coarse_starts_at_first_step": (
        "Coarse grid off by one step: nested_grid_counts takes the coarse maximum over the points t_1, t_1 + s, ... (values[0::stride]) instead of ending each block at t_{k s}.",
        "    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
        "    coarse = sum(1 for values in paths if max(values[0 :: stride]) >= level)",
    ),
    "m28_paths_redrawn_from_seed_each_path": (
        "Generator reseeded per path: _grid_paths calls random.Random(seed) inside the path loop, so every path repeats the same increments.",
        '''    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths: list[list[float]] = []
    for _ in range(int(instance["n_paths"])):
''',
        '''    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths: list[list[float]] = []
    for _ in range(int(instance["n_paths"])):
        rng = random.Random(int(instance["seed"]))
''',
    ),
    "m29_srw_terminal_drops_the_all_up_walk": (
        "Range error: srw_terminal_count sums j over range(n) and so drops the walk that goes up at every step.",
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
        "    return sum(math.comb(n, j) for j in range(n) if 2 * j - n >= a)",
    ),
    "m30_reflection_identity_shifted_down": (
        "Off-by-one in the identity: srw_max_count returns #{S_n >= a} + #{S_n >= a - 1}, the identity with the level shifted down.",
        "    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)",
        "    return srw_terminal_count(n, a) + srw_terminal_count(n, a - 1)",
    ),
    "m31_coarse_count_on_fresh_paths": (
        "Coarse count on fresh paths: nested_grid_counts draws the coarse grid's paths again with n_coarse steps instead of subsampling the fine paths.",
        "    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
        "    coarse_paths = _grid_paths(instance, n_coarse)\n    coarse = sum(1 for values in coarse_paths if max(values) >= level)",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    body = REF
    if name.startswith("m28"):
        # the reference's first line of _grid_paths body, replaced as a block
        assert body.count(old) == 1, name
        body = body.replace(old, new)
    else:
        assert body.count(old) == 1, (name, body.count(old))
        body = body.replace(old, new)
    # one-line docstring replaces the module docstring's first line; keep the rest of the reference unchanged
    head, sep, rest = body.partition('"""')
    _, sep2, tail = rest.partition('"""')
    module_doc = f'"""{doc}\n\nSingle-change copy of grader/reference.py, written by the verifier (round 4).\n"""'
    out = module_doc + tail
    (OUT / f"{name}.py").write_text(out, encoding="utf-8")
    print("wrote", name)
