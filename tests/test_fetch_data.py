"""tools/fetch_data.py: the Federal Reserve SDMX transform on a fixture, MANIFEST building, and the offline check."""

from __future__ import annotations

import dataclasses
import io
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

import pytest

import fetch_data
from fetch_data import DataError, Dataset, build, check, describe, fed_sdmx, load_manifest, load_spec, save_manifest

KF = "http://www.federalreserve.gov/structure/compact/H10_H10"
FRB = "http://www.federalreserve.gov/structure/compact/common"
MESSAGE = "http://www.SDMX.org/resources/SDMXML/schemas/v1_0/message"
COMMON = "http://www.SDMX.org/resources/SDMXML/schemas/v1_0/common"

# (date, value, status) per series, shaped like the Board's H10_data.xml: an annotated series, holidays as "ND".
SERIES = {
    "RXI$US_N.B.EU": [
        ("1999-12-31", "0.9000", "A"),
        ("2000-01-31", "1.0000", "A"),
        ("2000-02-01", "ND", "ND"),
        ("2000-02-28", "1.1000", "A"),
        ("2000-02-29", "1.2000", "A"),
        ("2000-03-01", "1.3000", "A"),
    ],
    "RXI_N.B.JA": [("2000-01-31", "105.00", "A"), ("2000-02-28", "110.00", "A"), ("2000-02-29", "ND", "ND")],
    "RXI_N.B.SZ": [("2000-01-31", "1.6000", "A")],
}


def sdmx_zip(series: dict[str, list[tuple[str, str, str]]], member: str = "H10_data.xml") -> bytes:
    blocks = []
    for name, observations in series.items():
        obs = "".join(f'<frb:Obs OBS_STATUS="{s}" OBS_VALUE="{v}" TIME_PERIOD="{d}" />' for d, v, s in observations)
        notes = (
            "<frb:Annotations><common:Annotation><common:AnnotationType>Short Description</common:AnnotationType>"
            f"<common:AnnotationText>{name}</common:AnnotationText></common:Annotation></frb:Annotations>"
        )
        blocks.append(f'<kf:Series FREQ="9" SERIES_NAME="{name}">{notes}{obs}</kf:Series>')
    xml = (
        f'<?xml version="1.0" encoding="UTF-8"?><message:MessageGroup xmlns:message="{MESSAGE}" '
        f'xmlns:common="{COMMON}" xmlns:frb="{FRB}"><message:Header><message:ID>H10</message:ID></message:Header>'
        f'<frb:DataSet id="H10" xmlns:kf="{KF}">{"".join(blocks)}</frb:DataSet></message:MessageGroup>'
    )
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        archive.writestr(member, xml)
        archive.writestr("H10_struct.xml", "<structure/>")
    return out.getvalue()


def spec(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "kind": "fed_sdmx",
        "member": "H10_data.xml",
        "sample": "daily",
        "start": "2000-01-01",
        "end": "2000-02-29",
        "series": {"EUR": "RXI$US_N.B.EU", "JPY": "RXI_N.B.JA"},
        "invert": ["JPY"],
    }
    return {**base, **overrides}


def test_daily_keeps_available_observations_in_range_and_inverts() -> None:
    table = fed_sdmx(sdmx_zip(SERIES), spec())
    assert table.csv_bytes().decode() == (
        "date,EUR,JPY\n"
        "2000-01-31,1.0000,0.0095238095\n"
        "2000-02-28,1.1000,0.0090909091\n"
        "2000-02-29,1.2000,\n"  # JPY's ND is dropped, the date stays for EUR; 2000-02-01 has no value at all
    )


def test_month_end_takes_each_columns_last_value_in_the_month() -> None:
    table = fed_sdmx(sdmx_zip(SERIES), spec(sample="month_end"))
    assert table.key == "month"
    assert table.rows == (("2000-01", "1.0000", "0.0095238095"), ("2000-02", "1.2000", "0.0090909091"))


def test_month_end_drops_an_incomplete_final_month() -> None:
    table = fed_sdmx(sdmx_zip(SERIES), spec(sample="month_end", end="2000-02-28"))
    assert [row[0] for row in table.rows] == ["2000-01"]


@pytest.mark.parametrize(
    ("value", "inverse"),
    [
        ("1.25", "0.80000000"),
        ("105.00", "0.0095238095"),
        ("0.5", "2.0000000"),
        ("0.0001", "10000.000"),
        # Just above a power of ten the inverse stays below it: eight digits, not a rounded-up seven.
        ("1.0000000051", "0.99999999"),
        ("10.000000051", "0.099999999"),
        # Rounding that carries into a new leading digit keeps eight significant digits.
        ("0.100000005", "9.9999995"),
        ("0.1000000004", "10.000000"),
        # Quotients that terminate within eight digits.
        ("0.8", "1.2500000"),
        ("1.6", "0.62500000"),
        # Exact ties at the ninth digit go to even: 1/4096 = 0.000244140625, 1/0.4096 = 2.44140625.
        ("4096", "0.00024414062"),
        ("0.4096", "2.4414062"),
        # A tie below 1e-4 and a quotient below 1e-6 stay exact in plain decimal (a float or str() would not).
        ("40960", "0.000024414062"),
        ("20000000", "0.000000050000000"),
    ],
)
def test_inversion_keeps_eight_significant_digits_in_plain_decimal(value: str, inverse: str) -> None:
    assert fetch_data._invert(value) == inverse


def test_a_series_missing_from_the_release_is_an_error() -> None:
    with pytest.raises(DataError, match="series not found"):
        fed_sdmx(sdmx_zip(SERIES), spec(series={"EUR": "RXI$US_N.B.EU", "XYZ": "RXI_N.B.XY"}))


def test_the_transform_description_names_every_choice() -> None:
    text = describe(spec(sample="month_end"))
    for part in ("H10_data.xml", "OBS_STATUS A", "2000-01-01 to 2000-02-29", "month-end", "JPY inverted", "EUR="):
        assert part in text


@pytest.fixture
def market(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    folder = tmp_path / "market"
    monkeypatch.setattr(fetch_data, "MARKET", folder)
    monkeypatch.setattr(fetch_data, "MANIFEST", folder / "MANIFEST.json")
    return folder


def dataset(**overrides: Any) -> Dataset:
    fields: dict[str, Any] = {
        "id": "fx_test",
        "title": "Test FX",
        "issuer": "Board of Governors of the Federal Reserve System",
        "url": "https://www.federalreserve.gov/releases/h10/data/FRB_h10_xml.zip",
        "licence": '"in the public domain"',
        "licence_url": "https://www.federalreserve.gov/disclaimer.htm",
        "citation": "Board of Governors of the Federal Reserve System, H.10",
        "transform": spec(),
    }
    return Dataset(**{**fields, **overrides})


def test_build_writes_the_snapshot_and_a_complete_manifest_entry(market: Path) -> None:
    raw = sdmx_zip(SERIES)
    entry = build(dataset(), raw, "2026-10-17")
    blob = (market / "fx_test.csv").read_bytes()
    assert entry["file"] == "fx_test.csv" and entry["rows"] == 3 and entry["bytes"] == len(blob)
    assert entry["key"] == "date" and entry["columns"] == ["EUR", "JPY"]
    assert (entry["first"], entry["last"], entry["retrieved"]) == ("2000-01-31", "2000-02-29", "2026-10-17")
    assert entry["sha256"] == fetch_data.sha256(blob) and entry["raw_sha256"] == fetch_data.sha256(raw)
    for field in ("source_url", "licence", "licence_url", "citation", "transform", "title", "issuer"):
        assert entry[field], field


def test_build_is_deterministic(market: Path) -> None:
    raw = sdmx_zip(SERIES)
    first = build(dataset(), raw, "2026-10-17")["sha256"]
    assert build(dataset(), raw, "2026-11-01")["sha256"] == first


def built(market: Path) -> tuple[Dataset, dict[str, dict[str, Any]]]:
    ds = dataset()
    save_manifest({ds.id: build(ds, sdmx_zip(SERIES), "2026-10-17")})
    return ds, load_manifest()


def test_a_fresh_build_passes_the_offline_check(market: Path) -> None:
    ds, manifest = built(market)
    assert check([ds], manifest) == []
    assert json.loads((market / "MANIFEST.json").read_text())["schema"] == 1


def test_a_hand_edited_snapshot_is_caught(market: Path) -> None:
    ds, manifest = built(market)
    path = market / "fx_test.csv"
    path.write_text(path.read_text().replace("1.1000", "1.1001"))
    assert any("SHA-256 differs" in p for p in check([ds], manifest))


def test_a_truncated_snapshot_is_caught(market: Path) -> None:
    ds, manifest = built(market)
    path = market / "fx_test.csv"
    path.write_text("".join(path.read_text().splitlines(keepends=True)[:-1]))
    found = check([ds], manifest)
    assert any("2 rows, MANIFEST says 3" in p for p in found)


def test_an_emptied_snapshot_is_reported_not_a_crash(market: Path) -> None:
    ds, manifest = built(market)
    (market / "fx_test.csv").write_bytes(b"")
    assert any("header" in p for p in check([ds], manifest))


def test_a_missing_snapshot_is_caught(market: Path) -> None:
    ds, manifest = built(market)
    (market / "fx_test.csv").unlink()
    assert any("is missing" in p for p in check([ds], manifest))


def test_a_stray_file_in_the_data_folder_is_caught(market: Path) -> None:
    ds, manifest = built(market)
    (market / "ff_factors.csv").write_text("month,MKT\n")
    assert any("ff_factors.csv" in p and "not a dataset" in p for p in check([ds], manifest))


@pytest.mark.parametrize(
    ("change", "field"),
    [
        ({"licence": '"all rights reserved"'}, "licence"),
        ({"licence_url": "https://example.org/terms"}, "licence_url"),
        ({"url": "https://www.federalreserve.gov/releases/h15/data/FRB_h15_xml.zip"}, "source_url"),
        ({"transform": spec(end="2000-01-31")}, "transform"),
        ({"title": "Another title"}, "title"),
        ({"issuer": "Another issuer"}, "issuer"),
        ({"citation": "Another citation"}, "citation"),
    ],
)
def test_a_spec_change_without_a_rebuild_is_caught(market: Path, change: dict[str, Any], field: str) -> None:
    ds, manifest = built(market)
    assert any(f"MANIFEST {field} differs" in p for p in check([dataclasses.replace(ds, **change)], manifest))


def test_manifest_and_spec_must_list_the_same_datasets(market: Path) -> None:
    ds, manifest = built(market)
    assert any("no MANIFEST entry" in p for p in check([ds, dataset(id="fx_other")], manifest))
    extra = {**manifest, "gone": {**manifest[ds.id], "id": "gone"}}
    assert any("MANIFEST lists 'gone'" in p for p in check([ds], extra))


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("datasets:\n  - id: x\n", "is missing"),
        (
            "datasets:\n  - {id: a, title: t, issuer: i, url: u, licence: l, licence_url: v, citation: c,"
            " transform: {kind: scrape}}\n",
            "unknown transform",
        ),
    ],
)
def test_the_spec_is_validated(tmp_path: Path, text: str, message: str) -> None:
    path = tmp_path / "spec.yaml"
    path.write_text(text)
    with pytest.raises(DataError, match=message):
        load_spec(path)


def test_the_committed_snapshots_match_their_manifest() -> None:
    assert check(load_spec(), load_manifest()) == []


def test_every_embedded_dataset_quotes_its_licence_from_the_issuer() -> None:
    for ds in load_spec():
        assert ds.licence.startswith('"') and ds.licence.endswith('"'), f"{ds.id}: licence must be a quotation"
        assert ds.licence_url.startswith("https://"), ds.id
        assert "redistribut" in ds.licence or "distributed" in ds.licence, f"{ds.id}: no redistribution grant"


def test_the_default_mode_is_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_network(url: str, *, attempts: int = 4) -> bytes:
        raise AssertionError(f"--check must not download {url}")

    monkeypatch.setattr(fetch_data, "download", no_network)
    monkeypatch.setattr(sys, "argv", ["fetch_data.py"])
    assert fetch_data.main() == 0


def test_requests_carry_no_personal_data() -> None:
    assert "@" not in fetch_data.USER_AGENT and "mailto" not in fetch_data.USER_AGENT.lower()


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("first", "1999-01-04", "first key is"),
        ("last", "2026-10-30", "last key is"),
        ("bytes", 1, "bytes, MANIFEST says 1"),
        ("title", "Edited", "MANIFEST title differs"),
        ("issuer", "Edited", "MANIFEST issuer differs"),
        ("citation", "Edited", "MANIFEST citation differs"),
    ],
)
def test_a_hand_edited_manifest_field_is_caught(market: Path, field: str, value: object, message: str) -> None:
    ds, manifest = built(market)
    edited = {ds.id: {**manifest[ds.id], field: value}}
    assert any(message in p for p in check([ds], edited))


def document(*blocks: str) -> str:
    """An SDMX message holding the given series blocks, with the namespaces the release files use."""
    return (
        f'<?xml version="1.0" encoding="UTF-8"?><message:MessageGroup xmlns:message="{MESSAGE}" '
        f'xmlns:common="{COMMON}" xmlns:frb="{FRB}"><message:Header><message:ID>H10</message:ID></message:Header>'
        f'<frb:DataSet id="H10" xmlns:kf="{KF}">{"".join(blocks)}</frb:DataSet></message:MessageGroup>'
    )


def series_block(name: str, observations: list[tuple[str, str, str]]) -> str:
    obs = "".join(f'<frb:Obs OBS_STATUS="{s}" OBS_VALUE="{v}" TIME_PERIOD="{d}" />' for d, v, s in observations)
    return f'<kf:Series FREQ="9" SERIES_NAME="{name}">{obs}</kf:Series>'


def zip_with(xml: str, member: str = "H10_data.xml") -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        archive.writestr(member, xml)
    return out.getvalue()


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (b"<html>not a zip</html>", "not a zip archive"),
        (
            zip_with(document(series_block("RXI$US_N.B.EU", [("2000-01-31", "1.0000", "A")])), "H10_struct.xml"),
            "no such member",
        ),
        (zip_with("<message:MessageGroup><unclosed>"), "unreadable"),
        (
            zip_with(document(series_block("RXI$US_N.B.EU", [("2000-01-31", "1,0000", "A")]))),
            "not a plain decimal number",
        ),
        (zip_with(document(series_block("RXI$US_N.B.EU", [("2000-02-30", "1.0000", "A")]))), "not an ISO date"),
        # date.fromisoformat also accepts the basic and week forms; the release files use YYYY-MM-DD only.
        (zip_with(document(series_block("RXI$US_N.B.EU", [("20000131", "1.0000", "A")]))), "not an ISO date"),
        (zip_with(document(series_block("RXI$US_N.B.EU", [("2000-W05-1", "1.0000", "A")]))), "not an ISO date"),
        # \d would accept other scripts' digits, which would then reach the snapshot as text.
        (
            zip_with(document(series_block("RXI$US_N.B.EU", [("2000-01-31", "\u0661.0000", "A")]))),
            "not a plain decimal number",
        ),
        (
            zip_with(
                document(series_block("RXI$US_N.B.EU", [("2000-01-31", "1.0000", "A"), ("2000-01-31", "1.0001", "A")]))
            ),
            "two available observations dated 2000-01-31",
        ),
        (
            zip_with(
                document(
                    series_block("RXI$US_N.B.EU", [("2000-01-31", "1.0000", "A")]),
                    series_block("RXI$US_N.B.EU", [("2000-01-31", "1.0000", "A")]),
                )
            ),
            "appears twice",
        ),
        (
            zip_with(
                document(
                    series_block("RXI$US_N.B.EU", [("2000-01-31", "1.0000", "A")]),
                    series_block("RXI_N.B.JA", [("2000-01-31", "0.0000", "A")]),
                )
            ),
            "cannot be inverted",
        ),
    ],
)
def test_a_malformed_download_is_refused_with_a_data_error(raw: bytes, message: str) -> None:
    with pytest.raises(DataError, match=message):
        fed_sdmx(raw, spec())


def test_negative_rates_are_kept_as_published() -> None:
    raw = zip_with(
        document(series_block("RIFSGFSM03_N.B", [("2000-01-03", "-0.0400", "A"), ("2000-01-04", "4.5000", "A")]))
    )
    table = fed_sdmx(raw, spec(series={"TBILL": "RIFSGFSM03_N.B"}, invert=[]))
    assert table.rows == (("2000-01-03", "-0.0400"), ("2000-01-04", "4.5000"))


def test_bytes_retrieved_again_keep_their_retrieval_date(market: Path) -> None:
    raw = sdmx_zip(SERIES)
    previous = build(dataset(), raw, "2026-10-17")
    assert fetch_data.retrieval_date(previous, raw, "2026-10-19") == "2026-10-17"
    changed = sdmx_zip({**SERIES, "RXI_N.B.SZ": [("2000-01-31", "1.6001", "A")]})
    assert fetch_data.retrieval_date(previous, changed, "2026-10-19") == "2026-10-19"
    assert fetch_data.retrieval_date(None, raw, "2026-10-19") == "2026-10-19"


def test_fetch_downloads_each_dataset_and_keeps_the_date_of_unchanged_bytes(
    market: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ds = dataset()
    raw = sdmx_zip(SERIES)
    save_manifest({ds.id: build(ds, raw, "2026-10-17")})
    fetched: list[str] = []

    def fake_download(url: str, *, attempts: int = 4) -> bytes:
        fetched.append(url)
        return raw

    monkeypatch.setattr(fetch_data, "load_spec", lambda *_args, **_kwargs: [ds])
    monkeypatch.setattr(fetch_data, "download", fake_download)
    monkeypatch.setattr(sys, "argv", ["fetch_data.py", "--fetch"])
    assert fetch_data.main() == 0
    assert fetched == [ds.url]
    assert load_manifest()[ds.id]["retrieved"] == "2026-10-17"


def test_every_dataset_is_read_from_a_board_release_page() -> None:
    for ds in load_spec():
        assert ds.url.startswith("https://www.federalreserve.gov/releases/h"), ds.id
        assert ds.url.endswith("_xml.zip"), ds.id
