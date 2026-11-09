# Independent re-derivation of Lab 1 L04 numbers from the prose rules (not the lab code).
import random
from fractions import Fraction

SEED, MID, OFF, N = 2026, 10000, 20, 300

class Book:
    def __init__(self):
        self.rest = []          # resting limit orders: dict(side, px, qty, t)
        self.pend = []          # pending stops in arrival order
        self.last = None
        self.fills = []
        self.G = 0; self.X = 0; self.C = 0
        self.t = 0

    def best(self):
        bids = [o['px'] for o in self.rest if o['side'] > 0]
        asks = [o['px'] for o in self.rest if o['side'] < 0]
        return (max(bids) if bids else None, min(asks) if asks else None)

    def R(self):
        return sum(o['qty'] for o in self.rest)

    def take(self, side, kind, qty, px):
        # incoming order: side +1 buy; meets opposite side best price first then earliest t
        self.G += qty
        rem = qty
        while rem > 0:
            opp = [o for o in self.rest if o['side'] == -side]
            if not opp:
                break
            if side > 0:
                best = min(opp, key=lambda o: (o['px'], o['t']))
                if kind == 'limit' and best['px'] > px:
                    break
            else:
                best = min(opp, key=lambda o: (-o['px'], o['t']))
                if kind == 'limit' and best['px'] < px:
                    break
            q = min(rem, best['qty'])
            best['qty'] -= q
            rem -= q
            self.X += q
            self.last = best['px']
            self.fills.append((best['px'], q))
            if best['qty'] == 0:
                self.rest.remove(best)
        if rem > 0:
            if kind == 'limit':
                self.rest.append({'side': side, 'px': px, 'qty': rem, 't': self.t})
            else:
                self.C += rem
        self.t += 1

    def run_stops(self):
        n = 0
        while self.last is not None:
            hit = None
            for i, s in enumerate(self.pend):
                if s['side'] > 0 and self.last >= s['stop']:
                    hit = i; break
                if s['side'] < 0 and self.last <= s['stop']:
                    hit = i; break
            if hit is None:
                break
            s = self.pend.pop(hit)
            self.take(s['side'], 'market', s['qty'], None)
            n += 1
        return n

def fixtures():
    b = Book()
    b.take(-1, 'limit', 60, 1000); b.take(-1, 'limit', 100, 1100); b.take(1, 'market', 150, None)
    cost = sum(p * q for p, q in b.fills)
    print("A fills", b.fills, "cost", cost, "avg", Fraction(cost, 150), "ask1100 left", sum(o['qty'] for o in b.rest if o['side'] < 0))
    b = Book()
    b.take(-1, 'limit', 100, 990); b.take(1, 'limit', 100, 985); b.take(1, 'limit', 100, 980)
    b.pend.append({'side': -1, 'stop': 990, 'qty': 100})
    a0 = b.run_stops()
    b.take(1, 'market', 100, None)
    a1 = b.run_stops()
    print("B fills", b.fills, "activations", a0 + a1)

fixtures()
rng = random.Random(SEED)
b = Book()
kinds = {'limit': 0, 'market': 0, 'stop': 0}
crossed = 0; cons = 0; act = 0
trace = []
for seq in range(N):
    side = rng.choice((1, -1))
    qty = 10 * rng.randint(1, 10)
    roll = rng.random()
    if roll < 0.6:
        kind = 'limit'; px = MID - side * rng.randint(0, OFF); stop = None
    elif roll < 0.85:
        kind = 'market'; px = None; stop = None
    else:
        kind = 'stop'; px = None; stop = MID + side * rng.randint(0, OFF)
    kinds[kind] += 1
    if kind == 'stop':
        b.pend.append({'side': side, 'stop': stop, 'qty': qty})
        b.G += 0
    else:
        b.take(side, kind, qty, px)
    act += b.run_stops()
    bid, ask = b.best()
    if bid is not None and ask is not None and bid >= ask:
        crossed += 1
    if b.G != b.R() + 2 * b.X + b.C:
        cons += 1
    if seq < 8:
        trace.append((seq, kind, side, bid, ask, b.last))
print("counts", kinds, "trades", len(b.fills), "traded", b.X, "activated", act, "pending", len(b.pend))
print("cancelled", b.C, "resting", b.R(), "crossed", crossed, "conservation_fail", cons)
print("end best", b.best())
for t in trace:
    print("trace", t)
print("Fraction 5600/173 =", float(Fraction(5600, 173)))
