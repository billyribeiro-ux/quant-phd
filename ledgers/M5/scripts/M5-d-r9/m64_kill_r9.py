import sys, math, importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/Users/billyribeiro/.fanout/wt/verifyB9-M5-d/course/modules/M/M5/grader/reference.py", "ref")
mut = load("/Users/billyribeiro/.fanout/wt/verifyB9-M5-d/ledgers/M5/mutants/m64_change_measured_at_the_last_point_only.py", "mut")
grid=[0.23, 0.24, 0.98, 1.46]; beta=0.8535397019795181; alpha=0.3276562928132905
params={"beta":beta,"alpha":alpha}
f=beta/(1-beta)
# walk the correct iteration and find a sweep where last-point certified < sup certified
v=[0.0]*4
for n in range(1,400):
    new=ref.bellman_operator(params,grid,v)
    d=[abs(a-b) for a,b in zip(new,v)]
    cl=f*d[-1]; cm=f*max(d)
    if cl < cm*0.999 and cm>1e-12:
        print("sweep",n,"last",repr(cl),"max",repr(cm)); break
    v=new
tol=cl  # at this tol the mutant's stop test passes at sweep n, the correct one does not
r=ref.solve(params,grid,tol,400); m=mut.solve(params,grid,tol,400)
print("tol",repr(tol))
print("reference iterations",r["iterations"],"converged",r["converged"],"certified",repr(r["certified_error"]))
print("mutant    iterations",m["iterations"],"converged",m["converged"],"certified",repr(m["certified_error"]))
