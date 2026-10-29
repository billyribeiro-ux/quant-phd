import sys, math
ns = {"__name__": "x"}
src2 = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()", "\n")
exec(compile(src2, "p2", "exec"), ns)
v=[0.0,0.0,0.0]; w=[0.1,0.2,0.3]
print("ratio2", repr(ns["sup_distance"](ns["bellman"](v), ns["bellman"](w))/ns["sup_distance"](v,w)))
values=[0.0,0.0,0.0]; n=0; cert=math.inf
while cert>1e-6 and n<300:
    n+=1; new=ns["bellman"](values); change=ns["sup_distance"](new,values); cert=0.9/(1-0.9)*change; values=new
print("sweeps",n,"cert",repr(cert),"change",repr(change))
# lab 1 terms
ns1={"__name__":"y"}
src1=open(sys.argv[2],encoding="utf-8").read().replace("\nmain()","\n")
exec(compile(src1,"p1","exec"),ns1)
values=[0.0,0.0,0.0]; n=0; cert=math.inf
while cert>1e-6:
    n+=1; new=ns1["bellman"](values); change=ns1["sup_distance"](new,values); cert=0.9/(1-0.9)*change; values=new
print("lab1 sweeps",n,"cert",repr(cert),"change",repr(change))
