"""Lab 3: Replication package manifest verification and bit-for-bit audit."""

from __future__ import annotations

import hashlib


def audit_replication_package(
    manifest: dict[str, str],
    file_contents: dict[str, bytes],
) -> tuple[bool, list[str]]:
    logs: list[str] = []
    all_ok = True

    # Check completeness
    for filename, expected_digest in manifest.items():
        if filename not in file_contents:
            logs.append(f"MISSING: {filename} listed in manifest but not produced.")
            all_ok = False
            continue

        actual_digest = hashlib.sha256(file_contents[filename]).hexdigest()
        if actual_digest.lower() == expected_digest.lower():
            logs.append(f"VERIFIED: {filename} SHA-256 {actual_digest[:12]}... matches.")
        else:
            logs.append(
                f"CORRUPT: {filename} digest mismatch: expected {expected_digest[:12]}..., got {actual_digest[:12]}..."
            )
            all_ok = False

    return all_ok, logs


def main() -> None:
    data_clean = b"date,permno,ret\n199001,10001,0.045\n199001,10002,-0.012\n"
    table_1 = b"Factor,Alpha,Beta_Mkt,t_stat\nMOM,0.0078,0.12,3.14\n"
    table_2 = b"Decile,VW_Ret,EW_Ret\n1,-0.002,0.001\n10,0.012,0.018\n"

    manifest = {
        "data/cleaned_panel.csv": hashlib.sha256(data_clean).hexdigest(),
        "tables/table1_baseline.csv": hashlib.sha256(table_1).hexdigest(),
        "tables/table2_deciles.csv": hashlib.sha256(table_2).hexdigest(),
    }

    test_bundle = {
        "data/cleaned_panel.csv": data_clean,
        "tables/table1_baseline.csv": table_1,
        "tables/table2_deciles.csv": table_2,
    }

    success, report = audit_replication_package(manifest, test_bundle)
    print("Replication Package Audit Report:")
    print(f"Status: {'PASS' if success else 'FAIL'}")
    for line in report:
        print(f"  {line}")


main()
