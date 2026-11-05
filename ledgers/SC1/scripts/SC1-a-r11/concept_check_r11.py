"""Hub prerequisite list versus the concepts used by the SC1 module (round 11).

Prints the data-concept targets used on index, L01-L08 and project that are neither in the hub prerequisite
list (index.html From-list section) nor defined by SC1 itself, and the hub targets that no SC1 page uses.
Also prints the data-hours of each lesson.
"""

import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a/course/modules/SC/SC1/"
hub = open(ROOT + "index.html", encoding="utf-8").read()
section = hub[hub.index('id="prerequisites"') : hub.index('id="placement"')]
hub_list = set(re.findall(r'data-concept="([^"]+)"', section))
own = {
    "brownian-motion",
    "brownian-motion-construction",
    "quadratic-variation",
    "continuous-time-martingale",
    "markov-property",
    "reflection-principle",
    "running-maximum-distribution",
    "first-passage-time",
}
used = set()
for f in ["index.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html", "L07.html", "L08.html", "project.html"]:
    used |= set(re.findall(r'data-concept="([^"]+)"', open(ROOT + f, encoding="utf-8").read()))
print("used, not in hub list, not SC1-defined:", sorted(used - hub_list - own))
print("hub list, not used anywhere in module:", sorted(hub_list - used))
print("hub list size:", len(hub_list), "| SC1-defined concepts used:", len(used & own))
for n in range(1, 9):
    t = open(ROOT + f"L0{n}.html", encoding="utf-8").read()
    print(f"L0{n} data-hours:", re.findall(r'data-hours="(\d+)"', t))
