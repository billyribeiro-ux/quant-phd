import math
p = {"beta": 0.8535397019795181, "alpha": 0.3276562928132905}
grid = [0.23, 0.24, 0.98, 1.46]
tol = 1.0119307470200622e-11
b, a = p["beta"], p["alpha"]
factor = b / (1 - b)
def sweep(vals):
    out = []
    for k in grid:
        r = k ** a
        out.append(max(math.sqrt(r - kp) + b * v for kp, v in zip(grid, vals) if kp <= r))
    return out
def run(measure):
    vals = [0.0] * len(grid)
    for n in range(1, 401):
        new = sweep(vals)
        ch = measure([x - y for x, y in zip(new, vals)])
        vals = new
        if factor * ch <= tol:
            return n, vals
    return None, vals
sup_n, _ = run(lambda d: max(abs(x) for x in d))
last_n, _ = run(lambda d: abs(d[-1]))
print("sup-norm stop sweep", sup_n, "last-point-only stop sweep", last_n)
