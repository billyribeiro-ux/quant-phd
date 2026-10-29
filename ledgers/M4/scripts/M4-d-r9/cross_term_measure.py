import sys, importlib.util, statistics
sys.path.insert(0, sys.argv[1])
import tail_risk as sol
def sv(xs):
    m = sum(xs)/len(xs); return sum((x-m)**2 for x in xs)/(len(xs)-1)
w1=w2=1_000_000; cov=[[4e-4,4.8e-4],[4.8e-4,9e-4]]
target=4.0*w1*w2*cov[0][1]
errs=[]
for s in range(int(sys.argv[2]), int(sys.argv[3])):
    p=sol.simulate_losses([w1,w2],cov,100_000,s,"student_t",5)
    m=sol.simulate_losses([w1,-w2],cov,100_000,s,"student_t",5)
    errs.append(abs((sv(p)-sv(m))-target)/target)
print("max %.4f mean %.4f n %d" % (max(errs), statistics.mean(errs), len(errs)))
