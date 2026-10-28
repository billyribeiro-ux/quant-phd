import math, itertools, random
# L02 Prop 1.4 modular identity
M=2654435761
bad=[j for j in range(0,20001) if ((64*j*M)%2**32)%64!=0]
print("L02 Prop1.4 h(64j)=0 counterexamples j<=20000:", bad[:5], len(bad))
# L02 Prop 1.4 all keys in bucket 0 for n=50 and probes
def h(x): return ((x*M)%2**32)%64
print("buckets of 64*j for j=1..50:", sorted({h(64*j) for j in range(1,51)}), "absent 3264 bucket", h(3264))
# L02 Prop 2.2 exact check by brute force: m=3,n=3 averages over all assignments
def avg_check(m,n):
    ok=True
    assigns=list(itertools.product(range(m),repeat=n))
    # unsuccessful for absent key x: probes = number of stored keys in bucket of x
    for b in range(m):
        tot=sum(sum(1 for a in asg if a==b) for asg in assigns)/len(assigns)
        pass
    # unsuccessful average over assignments with absent key bucket uniform over m
    un=[]
    for asg in assigns:
        for bx in range(m):
            un.append(sum(1 for a in asg if a==bx))
    ok &= abs(sum(un)/len(un)-n/m)<1e-12
    # successful average for position i (1-based): 1 + #earlier keys same bucket
    for i in range(1,n+1):
        vals=[1+sum(1 for k in range(i-1) if asg[k]==asg[i-1]) for asg in assigns]
        ok &= abs(sum(vals)/len(vals)-(1+(i-1)/m))<1e-12
    return ok
print("Prop 2.2(a),(b) brute force m=3,n=3 and m=4,n=3:", avg_check(3,3), avg_check(4,3))
# Corollary 2.2 / log2 n! ceiling
print("ceil log2(1024!) =", math.ceil(math.log2(math.factorial(1024))) if False else (math.factorial(1024).bit_length()-1 if False else None))
# exact: ceil(log2(N)) for big N: compare 2^k >= N
N=math.factorial(1024); k=0
while 2**k < N: k+=1
print("ceil log2(1024!) exact =", k, " 2^(k-1)<N:", 2**(k-1) < N)
# L04 Lemma 1.2: max merge comparisons over sorted lists with distinct keys a,b<=4 equals a+b-1?
def merge_count(l,r):
    i=j=c=0
    while i<len(l) and j<len(r):
        c+=1
        if l[i]<=r[j]: i+=1
        else: j+=1
    return c
res={}
for a in range(1,5):
    for b in range(1,5):
        mx=0
        for S in itertools.combinations(range(a+b),a):
            L=list(S); R=[x for x in range(a+b) if x not in S]
            mx=max(mx,merge_count(L,R))
        res[(a,b)]=(mx,a+b-1)
print("Lemma 1.2 max merge vs a+b-1:", all(v[0]<=v[1] for v in res.values()), {k:v for k,v in res.items() if v[0]!=v[1]})
# Prop 3.2 M2: 13 keys above all
def probes(vals,key):
    lo,hi=0,len(vals)-1;p=0
    while lo<=hi:
        mid=(lo+hi)//2;p+=1
        if vals[mid]==key:return p
        if vals[mid]<key: lo=mid+1
        else: hi=mid-1
    return p
print("M2 probes 13 keys above:", probes(list(range(13)),99), " L04 misc: 0,2,4,6 key 7:", probes([0,2,4,6],7))
# L04 R1 modified midpoint worst case for n 1..200
def probes2(vals,key):
    lo,hi=0,len(vals)-1;p=0
    while lo<=hi:
        mid=(lo+hi+1)//2;p+=1
        if vals[mid]==key:return p
        if vals[mid]<key: lo=mid+1
        else: hi=mid-1
    return p
print("R1 worst (new midpoint) == bit_length for n<=300:", all(max(probes2([2*i for i in range(n)],k) for k in [-1]+[2*i+1 for i in range(n-1)]+[2*n-1])==n.bit_length() for n in range(1,301)))
# L03 Remark numbers
print("6*4096*12=",6*4096*12," 2N(N+1)=",2*4096*4097, " 4378444/33562624=", round(4378444/33562624,5), " 166912/294912", round(166912/294912,4))
print("262431/8886=",round(262431/8886,6)," 8886*29=",8886*29, " 5120/8770=",round(5120/8770,5))
print("L01 1/511=",1/511, " 1023/511=",1023/511, " 1048576 == 1024**2", 1024**2)
print("L02 257/128=",257/128," 193/64=",193/64," 772/256=",772/256," 1+127/128=",1+127/128, " 2.0078-1.9921875",2.0078125-1.9921875)
print("L02 unsucc: 134/500",134/500," 270/500",270/500," 548/500",548/500," 1016/500",1016/500," 2014/500",2014/500)
print("L02 E1 successful gaps", 1.0-(1+15/128), 37/32-(1+31/128), 97/64-(1+63/128), 257/128-(1+127/128), 772/256-(1+255/128), "193/64-257/128=",193/64-257/128)
print("L04 Cor2.2 margin n=2..1000 min at 2:", min((math.lgamma(n+1)/math.log(2)-(n/2)*math.log2(n/2), n) for n in range(2,1001)))
