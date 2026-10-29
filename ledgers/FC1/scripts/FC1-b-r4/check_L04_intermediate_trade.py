import sys, types
src = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()\n", "\n")
mod = types.ModuleType("twin_defs")
sys.modules["twin_defs"] = mod
exec(compile(src, sys.argv[1], "exec"), mod.__dict__)
Order, Book = mod.Order, mod.Book
b = Book()
b.match(Order(0, 1, "limit", 100, 1010))   # bid 100 @1010 rests
b.match(Order(1, 1, "limit", 10, 1000))    # bid 10 @1000 rests
b.pending.append(Order(2, 1, "stop", 5, None, 1005))  # buy stop, trigger 1005
b.match(Order(3, -1, "market", 110))       # sell 110: trades 100 @1010, then 10 @1000
print("fills", b.fills, "last", b.last)
print("any trade of the arriving order at or above 1005:", any(p >= 1005 for p, _ in b.fills))
n = b.activate()
print("activated after match:", n, "pending left:", len(b.pending))
