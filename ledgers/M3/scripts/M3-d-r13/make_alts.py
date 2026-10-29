import pathlib
ref = pathlib.Path("course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path("/tmp/m3d13_alts"); out.mkdir(exist_ok=True)
alts = {
 "alt1_jacobi_tight_cutoff_200_sweeps": [
   ("for _ in range(100):", "for _ in range(200):"),
   ("if off <= 1e-15 * max(scale, 1e-300):", "if off <= 1e-300 + 1e-17 * scale:")],
 "alt2_is_psd_negated_comparison": [
   ("    return min_eigenvalue(matrix) >= -tol", "    return not (min_eigenvalue(matrix) < -tol)")],
 "alt3_rescale_by_square_roots_separately": [
   ("return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]",
    "s = [math.sqrt(v) for v in d]\n    return [[x[i][j] / (s[i] * s[j]) for j in range(len(x))] for i in range(len(x))]")],
 "alt4_projection_stop_on_gap_and_step_with_max_iter_2000": [
   ("def projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 500) -> list[list[float]]:",
    "def projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 2000) -> list[list[float]]:")],
 "alt5_weights_without_pivoting": [
   ("        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))\n        aug[col], aug[pivot] = aug[pivot], aug[col]\n", "")],
 "alt6_clip_repair_floor_via_max_over_zero": [
   ("    x = _rebuild([max(value, floor) for value in values], vectors)", "    x = _rebuild([max(value, floor, -math.inf) for value in values], vectors)")],
}
for name, reps in alts.items():
    body = ref
    for old, new in reps:
        assert body.count(old) == 1, (name, old[:40], body.count(old))
        body = body.replace(old, new)
    (out / name).mkdir(exist_ok=True)
    (out / name / "covariance_doctor.py").write_text(body, encoding="utf-8")
    print("alt", name)
