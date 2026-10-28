"""Check that every printed line of a twin run appears verbatim in its page text dump.

Usage: python -I lines_in_page.py <run-output-file> <page-text-dump>
"""
import sys


def main() -> None:
    run_path, page_path = sys.argv[1], sys.argv[2]
    with open(run_path, encoding="utf-8") as fh:
        run_lines = [ln.rstrip("\n") for ln in fh if ln.strip()]
    with open(page_path, encoding="utf-8") as fh:
        page = fh.read()
    missing = [ln for ln in run_lines if ln not in page]
    print(f"{len(run_lines)} printed lines; {len(run_lines) - len(missing)} verbatim in page; missing {len(missing)}")
    for ln in missing:
        print("MISSING:", ln)


if __name__ == "__main__":
    main()
