import json, re, subprocess, sys
R = '/Users/billyribeiro/.fanout/wt/verifyF31-SC1-b'
BASE = '8e5751c9'
FILES = {
    'L01': 'course/modules/SC/SC1/L01.html', 'L02': 'course/modules/SC/SC1/L02.html',
    'L03': 'course/modules/SC/SC1/L03.html', 'L04': 'course/modules/SC/SC1/L04.html',
    'L05': 'course/modules/SC/SC1/L05.html', 'L06': 'course/modules/SC/SC1/L06.html',
    'index': 'course/modules/SC/SC1/index.html', 'project': 'course/modules/SC/SC1/project.html',
    'rulings': 'plans/FINAL-ARCHITECT-RULINGS.md', 'plan': 'plans/SC1-build-plan.md',
    'open': 'plans/SC1-open-items.md',
}
def changed_lines(path):
    out = subprocess.run(['git', 'diff', '-U0', f'{BASE}..HEAD', '--', path], capture_output=True, text=True, cwd=R).stdout
    s = set()
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', out, re.M):
        a = int(m.group(1)); ca = int(m.group(2) or 1); b = int(m.group(3)); cb = int(m.group(4) or 1)
        # old-side lines changed/removed (ca lines) and new-side lines (cb lines)
        for i in range(a, a + max(ca, 1)): s.add(('old', i))
        for i in range(b, b + max(cb, 1)): s.add(('new', i))
    return s, out
if __name__ == '__main__':
    for k, p in FILES.items():
        s, out = changed_lines(p)
        nums = sorted(i for side, i in s if side == 'new')
        print(k, len(nums), nums[:80])
