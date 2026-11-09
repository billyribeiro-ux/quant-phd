"""LX1-c round 20: scores criterion C1 of the page's rubric (course/modules/LX/LX1/project.html, tr[data-criterion=C1],
cells td1..td4 = levels 4..1) under the highest-level rule of line 467, for essays that name both the episode and the
condition, each with one or two dates, and each date with or without a locator. Reports which levels are reachable.
Predicates are transcribed from the cell texts as they stand at d1083bf1 (cd4dd7df text in brackets for comparison)."""
from itertools import product

def level(dates_e, dates_c, loc):  # dates_e/dates_c: number of dates; loc: tuple of booleans, one per date
    all_dates = dates_e + dates_c
    has_date_e, has_date_c = dates_e >= 1, dates_c >= 1
    L4 = has_date_e and has_date_c and all(loc)  # "gives a locator for each date"
    # td2 (level 3) as it now reads: "gives a locator for each date" (identical predicate to td1)
    L3_now = has_date_e and has_date_c and all(loc)
    # td2 as it read at cd4dd7df: "gives a locator for all but one date"
    L3_old = has_date_e and has_date_c and sum(loc) >= all_dates - 1
    # td3 (level 2): "a date or a locator is missing for one or both of them" (items: episode, condition)
    missing_e = (not has_date_e) or not any(loc[:dates_e])
    missing_c = (not has_date_c) or not any(loc[dates_e:])
    L2 = missing_e or missing_c
    return {"now": 4 if L4 else (3 if L3_now else (2 if L2 else 1)),
            "old": 4 if L4 else (3 if L3_old else (2 if L2 else 1))}

reach = {"now": {}, "old": {}}
for de, dc in product([1, 2], repeat=2):
    n = de + dc
    for loc in product([False, True], repeat=n):
        s = level(de, dc, loc)
        for k in ("now", "old"):
            reach[k].setdefault(s[k], []).append((de, dc, loc))
for k in ("now", "old"):
    print(f"page text variant {k}: levels reachable {sorted(reach[k], reverse=True)}; "
          f"essays scoring 3: {len(reach[k].get(3, []))}")
print("example essay with one date (episode) and no locator, condition dated with locator (pattern 10):",
      level(1, 1, (False, True)))
