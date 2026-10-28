import pathlib
p = pathlib.Path("/tmp/M4-v/d/scratch/altC_crout_cholesky_column_order.py")
src = pathlib.Path("/tmp/verifyB3-M4-d/course/modules/M/M4/grader/reference.py").read_text()
start = src.index("    factor = [[0.0] * n for _ in range(n)]")
end = src.index("    return factor\n", start)
new = '''    factor = [[0.0] * n for _ in range(n)]
    for j in range(n):
        inner_diag = sum(factor[j][k] * factor[j][k] for k in range(j))
        pivot = cov[j][j] - inner_diag
        if not pivot > 0.0:
            raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
        factor[j][j] = math.sqrt(pivot)
        for i in range(j + 1, n):
            factor[i][j] = (cov[i][j] - sum(factor[i][k] * factor[j][k] for k in range(j))) / factor[j][j]
'''
p.write_text(src[:start] + new + src[end:])
