import pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB18-M3-d")
src = (ROOT / "course/modules/M/M3/grader/reference.py").read_text()
mut = ROOT / "ledgers/M3/mutants"
def write(name, doc, old, new, count=1):
    assert src.count(old) == count, (name, src.count(old))
    text = src.replace(old, new)
    lines = text.split("\n")
    # replace module docstring with the one-line mutant description
    start = text.index('"""'); end = text.index('"""', start + 3) + 3
    text = text[:start] + '"""' + doc + '"""' + text[end:]
    (mut / name).write_text(text)
write("v18_m01_is_psd_cholesky_refuses_singular.py",
      "is_psd decides by a Cholesky factorisation without tolerance, so a PSD matrix with a zero eigenvalue is refused.",
      "    return min_eigenvalue(matrix) >= -tol",
      """    n = len(matrix)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = matrix[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    return False
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return True""")
write("v18_m02_projection_loop_cap_ignores_small_max_iter.py",
      "projection_repair runs max(max_iter, 500) iterations, so an argument of max_iter=1 gives the converged answer.",
      "    for _ in range(max_iter):", "    for _ in range(max(max_iter, 500)):")
write("v18_m03_clip_skips_rescale_on_unit_diagonal.py",
      "clip_repair skips the rescaling when the input diagonal is already all ones, so the clipped output keeps a diagonal that is not unit.",
      "    return _rescale(x)",
      "    if all(matrix[i][i] == 1.0 for i in range(len(matrix))):\n        return x\n    return _rescale(x)")
print("ok")
