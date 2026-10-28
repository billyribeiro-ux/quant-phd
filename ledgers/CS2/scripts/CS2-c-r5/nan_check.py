import math
from collections import deque
def run(series, w):
    dq=deque(); out=[]
    for i,x in enumerate(series):
        while dq and dq[-1][1] >= x: dq.pop()
        dq.append((i,x))
        while dq[0][0] <= i-w: dq.popleft()
        out.append(dq[0][1])
    return out, list(dq)
s=[1.0, float('nan'), 0.0]
print('deque front values', run(s,3))
s2=[3.0, float('nan'), 1.0, 5.0]
out,dq=run(s2,3); print('front after NaN series', out, 'final deque', dq)
import itertools
print('window min at i=2 over {1,nan,0}:', min([1.0,float('nan'),0.0]))
