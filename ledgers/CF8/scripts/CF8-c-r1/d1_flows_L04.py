L = [2480237, 2466600, 2422927, 2629208, 2268160, 1660095, 1469856, 1066984, 1134718, 1058254, 911360, 1068435, 1282442]
cum = [l - 2400000 for l in L]
prev = 0
nu = []
for c in cum:
    nu.append(c - prev)
    prev = c
for w, (n, c) in enumerate(zip(nu, cum), 1):
    print(w, n, c)
print("min nu week", min(range(13), key=lambda i: nu[i]) + 1, min(nu))
print("min cum week", min(range(13), key=lambda i: cum[i]) + 1, min(cum))
print("5*1234567/7 =", 5 * 1234567 / 7)
