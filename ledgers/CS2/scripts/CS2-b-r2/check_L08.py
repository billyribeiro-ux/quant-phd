import math
M=1103515245;I=12345;MOD=2**31
class G:
    def __init__(s,seed): s.s=seed%MOD
    def below(s,n):
        s.s=(M*s.s+I)%MOD; return (s.s>>16)%n
g=G(20261029)
orders={}   # oid -> dict(side, price, qty, arrival)
levels={'B':{}, 'S':{}}  # price -> dict(list=[oids in arrival], head=0)
searches=[]  # (L, tests)
created=removed=0; queue_steps=0; trades_total=0; traded_msgs=0; cancels=0; new=0
def halving(sorted_prices, p):
    lo,hi=0,len(sorted_prices); t=0
    while lo<hi:
        mid=(lo+hi)//2; t+=1
        if sorted_prices[mid]<p: lo=mid+1
        else: hi=mid
    return t
def best(side):
    ps=[p for p in levels[side] if any(orders[o]['qty']>0 for o in levels[side][p]['list'])]
    if not ps: return None
    return max(ps) if side=='B' else min(ps)
def live_at(side,p):
    return any(orders[o]['qty']>0 for o in levels[side][p]['list'])
def drop_empty(side,p):
    global removed
    if p in levels[side] and not live_at(side,p):
        L=len(levels[side]); sp=sorted(levels[side]); searches.append((len(sp), halving(sp,p))); del levels[side][p]; removed+=1
arrival=0
def submit(side,price,qty,oid):
    global queue_steps,created,trades_total
    opp='S' if side=='B' else 'B'; trades=[]; rem=qty
    while rem>0:
        cand=[p for p in levels[opp] if live_at(opp,p) and ((side=='B' and p<=price) or (side=='S' and p>=price))]
        if not cand: break
        p=min(cand) if side=='B' else max(cand)
        lv=levels[opp][p]
        # head passes dead entries
        while lv['head']<len(lv['list']) and orders[lv['list'][lv['head']]]['qty']==0:
            lv['head']+=1; queue_steps+=1
        o=lv['list'][lv['head']]
        f=min(rem,orders[o]['qty']); orders[o]['qty']-=f; rem-=f
        trades.append((p,f,o))
    if rem>0:
        if price not in levels[side]:
            sp=sorted(levels[side]); searches.append((len(sp), halving(sp,price))); levels[side][price]={'list':[],'head':0}; created+=1
        levels[side][price]['list'].append(oid); orders[oid]={'side':side,'price':price,'qty':rem}
    for p in list(levels[opp]):
        drop_empty(opp,p)
    return trades
# message loop mirroring the lab's stated stream rules
MID=10000;HALF=20;MAXQ=20;CANCEL=25
live=[]
for step in range(400):
    live_ids=sorted(o for o in orders if orders[o]['qty']>0)
    if live_ids and g.below(100)<CANCEL:
        oid=live_ids[g.below(len(live_ids))]
        side=orders[oid]['side']; p=orders[oid]['price']; orders[oid]['qty']=0
        drop_empty(side,p); cancels+=1
    else:
        side='B' if g.below(2)==0 else 'S'
        price=MID-HALF+g.below(2*HALF+1); qty=1+g.below(MAXQ)
        oid=new+1 if False else (new_id:=globals().get('new_id',0)+1); globals()['new_id']=new_id
        tr=submit(side,price,qty,oid); new+=1
        if tr: traded_msgs+=1; trades_total+=len(tr)
print("cancels",cancels,"new",new,"traded msgs",traded_msgs,"executions",trades_total)
print("created",created,"removed",removed,"levels left",created-removed, "levels dict", len(levels['B'])+len(levels['S']))
print("live orders", sum(1 for o in orders.values() if o['qty']>0))
print("best bid",best('B'),"best ask",best('S'))
print("binary searches",len(searches),"max tests",max(t for _,t in searches), "bound ok", all(t<=math.floor(math.log2(L))+1 if L>=1 else t==0 for L,t in searches))
print("queue steps",queue_steps)
print("102/400",102/400,"4 tests => L>=8:", 2**3)
