import sys, pathlib
ref = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-M4-d/course/modules/M/M4/grader/reference.py").read_text()
old_loop = "    for _ in range(n_draws):\n"
old_chi = "            chi_square = rng.gammavariate(nu / 2, 2.0)\n"
assert ref.count(old_loop) == 1 and ref.count(old_chi) == 1
def variant(name, cond_reuse, source_expr):
    src = ref.replace(old_loop, "    chi_by_draw: dict[int, float] = {}\n    shared_even: list[float] = []\n    for d in range(n_draws):\n")
    new_chi = (
        "            if " + cond_reuse + ":\n"
        "                chi_square = " + source_expr + "\n"
        "            else:\n"
        "                chi_square = rng.gammavariate(nu / 2, 2.0)\n"
        "            chi_by_draw[d] = chi_square\n"
    )
    src = src.replace(old_chi, new_chi)
    pathlib.Path(f"/tmp/M4-d-r7-chk/{name}.py").write_text(src)
variant("lag1_2k_2k1", "d % 2 == 1", "chi_by_draw[d - 1]")
variant("lag2_4j_4j2", "d % 4 == 2", "chi_by_draw[d - 2]")
variant("lag3_6j_6j3", "d % 6 == 3", "chi_by_draw[d - 3]")
variant("even_all_share", "d % 2 == 0 and d > 0", "chi_by_draw[0]")
print("ok")
