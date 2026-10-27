import math
l = 2*math.log(20)
def norm_b(t, k):
    u = t/k
    return math.sqrt((1+1/u)*(l+math.log(1+u)))  # = b_t/sqrt(t) of (5), u = t/kappa
ts = range(1, 200000)
best = min(ts, key=lambda t: norm_b(t, 252.0))
print("min over integer t=1..199999 at kappa=252:", round(norm_b(best,252.0),6), "at t =", best)
print("continuous optimum t = u*kappa:", round(8.211968*252, 2))
print("b_756/sqrt(756) at kappa=252:", round(norm_b(756,252.0),5), " at kappa=92.1:", round(norm_b(756,92.1),5))
print("b_2520/sqrt(2520) at kappa=92.1:", round(norm_b(2520,92.1),5), " at kappa=252:", round(norm_b(2520,252.0),5))
print("b_36/sqrt(36) at kappa=252:", round(norm_b(36,252.0),3), " 7.0 claimed on page")
print("b_t/sqrt(t) min over t at kappa=92.0608:", round(min(norm_b(t,92.0608) for t in range(1,20000)),6))
