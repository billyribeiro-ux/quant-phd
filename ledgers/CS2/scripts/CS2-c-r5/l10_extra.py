from collections import deque
def run(series,w):
    dq=deque(); s3=0; per=[]
    for i,x in enumerate(series):
        rem1=0
        while dq and series[dq[-1]]>=x:
            dq.pop(); rem1+=1
        dq.append(i); rem3=0
        while dq[0]<=i-w:
            dq.popleft(); s3+=1; rem3+=1
        per.append((rem1,rem3))
    return s3, per
for n in (6,10,25):
    for w in (1,2,3,5):
        if n<w: continue
        s3,_=run(list(range(n)),w)
        assert s3==n-w,(n,w,s3)
print("R3 increasing: step-3 total == n-w for all tested (n,w): OK")
for w in range(1,8):
    series=[float(i) for i in range(w)]+[-1.0]
    s3,per=run(series,w)
    assert per[-1][0]==w, (w,per[-1])
print("Cor 2.5(c) series removes w entries at the last insertion for w=1..7: OK")
