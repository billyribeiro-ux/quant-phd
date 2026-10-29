"""Flag round-20 rows whose cited text touches a changed line or changed card (delta fd9a9b7..f95243f)."""
import json, re, sys
rows = json.load(open('/tmp/fanout-frags/AC1-b.round20.json'))['rows']
CHANGED_NUM = {52, 121, 331, 347, 357, 360}
CHANGED_CARDS = {'AC1-c057', 'AC1-c069', 'AC1-c071', 'AC1-c087'}
for r in rows:
    text = r['location'] + ' ' + r['evidence']
    nums = set()
    for a, b in re.findall(r'lines? (\d+)\s*(?:-|to|–)\s*(\d+)', text):
        nums |= set(range(int(a), int(b) + 1))
    for a in re.findall(r'(?<![\d,.])(\d{2,3})(?![\d,])', text):
        nums.add(int(a))
    cards = set(re.findall(r'AC1-c\d{3}', text))
    hit_nums = sorted(n for n in nums if n in CHANGED_NUM)
    hit_cards = sorted(cards & CHANGED_CARDS)
    if hit_nums or hit_cards or any(k in text for k in ('misconception 1', 'misconception 2', 'Remark 2.4', 'bullet', 'why-it-matters', 'Section 3', 'Section 4', 'card')):
        print(r['id'], r['status'], 'nums', hit_nums, 'cards', hit_cards, '|', r['location'][:90])
