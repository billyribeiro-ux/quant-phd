from fractions import Fraction as F
# L02 R3 sum bound, beta in (0,1): sum_{k=n}^{m-1} beta^k <= beta^n/(1-beta)
import random
random.seed(5)
bad=0
for _ in range(20000):
    b=F(random.randint(1,999),1000); c=F(random.randint(1,50)); n=random.randint(0,30); m=n+random.randint(1,30)
    s=sum(b**k for k in range(n,m)); assert s==b**n*(1-b**(m-n))/(1-b)
    if s> b**n/(1-b): bad+=1
    # Bernoulli: (1+h)^N >= 1+Nh with beta=1/(1+h)
    h=1/b-1
    N=random.randint(1,40)
    if not ((1+h)**N >= 1+N*h): bad+=1
print("R3 checks failures:", bad)
# L03 y_n = 2/(2n+1) <= 1/n and not of form 1/k
for n in range(1,500):
    y=F(2,2*n+1)
    assert 0<y<=F(1,n)
    assert not (1/y).denominator==1 or True
    assert (1/y).denominator!=1
print("y_n bounds ok; 1/y_n noninteger for n=1..499 ->", all((F(2*n+1,2)).denominator==2 for n in range(1,500)))
# L03 Lemma 1.3 proof: |x^2-4|<=5|x-2| when |x-2|<=1, and x^2->4 epsilon step
for k in range(-200,201):
    x=F(2)+F(k,200)
    assert abs(x-2)<=1 and abs(x*x-4)<=5*abs(x-2)
print("Lemma 1.3 bound ok on 401 grid points")
