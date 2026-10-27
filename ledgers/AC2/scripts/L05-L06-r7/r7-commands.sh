# Round-7 commands run for L05-L06 (checkout /tmp/verify-ac2r7-l56, pin 6adfd01). Outputs are in this directory or /tmp/ac2-v/L05-L06-r7.
cd /tmp/verify-ac2r7-l56
.venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L05-1.py   # lab05.out
.venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L06-1.py   # lab06.out
.venv/bin/python tools/check_pages.py --unit AC2 --page L05; .venv/bin/python tools/check_pages.py --unit AC2 --page L06
.venv/bin/python tools/check_dag.py --unit AC2
.venv/bin/python tools/run_labs.py --unit AC2                  # 11/11
.venv/bin/python tools/page_smoke.py --unit AC2 --pages L05 L06
.venv/bin/python tools/verify_refs.py --offline                # 560 entries, 0 problems
.venv/bin/python tools/verify_refs.py --unit AC2               # live: 7 of 560, 0 problems
.venv/bin/python -m pytest tests/test_labs.py -k "AC2 or A" -q
.venv/bin/ruff check tests/labs/AC2/lab-AC2-L05-1.py tests/labs/AC2/lab-AC2-L06-1.py
.venv/bin/ruff format --check tests/labs/AC2/lab-AC2-L05-1.py tests/labs/AC2/lab-AC2-L06-1.py
.venv/bin/mypy tests/labs/AC2/lab-AC2-L05-1.py tests/labs/AC2/lab-AC2-L06-1.py
# plain curl, no bypass; Crossref API (no personal data in the request)
curl -s "https://api.crossref.org/works/10.2308/tar-9505096112" -o dechow.json
curl -s "https://api.crossref.org/works/10.2308/tar-9608042309" -o sloan.json
# access statements (status only)
curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" https://doi.org/10.2308/tar-9505096112
curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" https://doi.org/10.2469/faj.v55.n5.2296
curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" https://www.sec.gov/os/webmaster-faq
curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" https://www.sec.gov/os/accessing-edgar-data
