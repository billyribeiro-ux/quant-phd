"""Round-28 part C: today's OpenCitations index counts for the counter-evidence screens (r24-counter-cz-screen,
r24-counter-jkp-screen, r24-counter-jiang-lu-screen, counter-ggm1997). One request per DOI, 2 s apart, no personal data.
Counts the citing rows and those whose creation date (the 'creation' field, YYYY-MM-DD) is 2024-2026.
Run: python -I opencitations_count_C.py"""
import json
import time
import urllib.error
import urllib.request

DOIS = {
    "10.1093/rapstu/raz011": "r24-counter-cz-screen: recorded 83 citing rows, 32 created 2024-2026",
    "10.1111/jofi.13249": "r24-counter-jkp-screen: recorded 408 citing rows, 297 created 2024-2026",
    "10.1214/24-aoas1983": "r24-counter-jiang-lu-screen (Jiang): recorded 0 citing rows",
    "10.1016/j.frl.2025.108491": "r24-counter-jiang-lu-screen (Lu): recorded 0 citing rows",
    "10.1214/aop/1024404523": "counter-ggm1997: recorded 183 citing rows (181 with a DOI)",
}
for i, (doi, note) in enumerate(DOIS.items()):
    if i:
        time.sleep(2)
    url = "https://api.opencitations.net/index/v2/citations/doi:" + doi
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            status = r.status
            rows = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"{doi}: HTTP {e.code} ({note})")
        continue
    recent = sum(1 for row in rows if str(row.get("creation", ""))[:4] in ("2024", "2025", "2026"))
    with_doi = sum(1 for row in rows if "doi:" in str(row.get("citing", "")))
    print(f"{doi}: HTTP {status}, citing rows {len(rows)}, created 2024-2026 {recent}, with a DOI {with_doi} ({note})")
