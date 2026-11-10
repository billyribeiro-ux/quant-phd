"""CS5 Lab L01: Multi-translation unit compilation and One Definition Rule (ODR) linker model.

Standard library only. Deterministic integer symbol tracking. Simulates separate compilation
of translation units into object symbol tables, testing strong vs weak/inline symbol linkage
and detecting One Definition Rule violations.
"""

from __future__ import annotations

from typing import NamedTuple


class Symbol(NamedTuple):
    name: str
    is_inline: bool
    is_internal: bool
    signature_hash: int


class LinkerError(Exception):
    pass


class TranslationUnit:
    def __init__(self, name: str) -> None:
        self.name = name
        self.symbols: dict[str, Symbol] = {}

    def add_definition(self, name: str, is_inline: bool = False, is_internal: bool = False, body_id: int = 1) -> None:
        sig_hash = hash((name, body_id))
        self.symbols[name] = Symbol(name, is_inline, is_internal, sig_hash)


class Linker:
    def __init__(self) -> None:
        self.global_table: dict[str, tuple[str, Symbol]] = {}

    def link(self, units: list[TranslationUnit]) -> dict[str, str]:
        resolved: dict[str, str] = {}
        for tu in units:
            for name, sym in tu.symbols.items():
                if sym.is_internal:
                    # Internal linkage: scoped to TU, never conflicts globally
                    continue
                if name in self.global_table:
                    prev_tu, prev_sym = self.global_table[name]
                    if not sym.is_inline or not prev_sym.is_inline:
                        raise LinkerError(
                            f"ODR violation: duplicate strong symbol '{name}' defined in both {prev_tu} and {tu.name}"
                        )
                    if sym.signature_hash != prev_sym.signature_hash:
                        msg = (
                            f"ODR ill-formed violation: inline symbol '{name}' "
                            f"has conflicting definitions between {prev_tu} and {tu.name}"
                        )
                        raise LinkerError(msg)
                    # Inline duplicate is deduplicated
                    resolved[name] = f"deduplicated (kept from {prev_tu})"
                else:
                    self.global_table[name] = (tu.name, sym)
                    resolved[name] = f"defined in {tu.name}"
        return resolved


def run_odr_experiments() -> None:
    print("CS5 L01: Translation Unit Linkage and ODR Resolution Model")

    # Experiment 1: Valid multi-unit program with inline functions and internal linkage
    tu1 = TranslationUnit("engine.cpp")
    tu1.add_definition("calculate_delta", is_inline=False, is_internal=False, body_id=101)
    tu1.add_definition("inline_vol_helper", is_inline=True, is_internal=False, body_id=202)
    tu1.add_definition("local_seed_state", is_inline=False, is_internal=True, body_id=303)

    tu2 = TranslationUnit("pricer.cpp")
    tu2.add_definition("price_option", is_inline=False, is_internal=False, body_id=404)
    tu2.add_definition("inline_vol_helper", is_inline=True, is_internal=False, body_id=202)
    tu2.add_definition("local_seed_state", is_inline=False, is_internal=True, body_id=505)

    linker = Linker()
    resolved = linker.link([tu1, tu2])
    print(f"Valid link: {len(resolved)} global symbols resolved:")
    for sym_name, status in sorted(resolved.items()):
        print(f"  {sym_name}: {status}")

    # Experiment 2: Duplicate non-inline strong definition (ODR violation)
    tu3 = TranslationUnit("analytics.cpp")
    tu3.add_definition("calculate_delta", is_inline=False, is_internal=False, body_id=606)

    try:
        linker_fail = Linker()
        linker_fail.link([tu1, tu3])
        print("Linker: Unexpected success")
    except LinkerError as err:
        print(f"Detected expected link collision: {err}")

    # Experiment 3: Inline definition with mismatched tokens across TUs
    tu4 = TranslationUnit("mismatched_header.cpp")
    tu4.add_definition("inline_vol_helper", is_inline=True, is_internal=False, body_id=999)

    try:
        linker_odr_diff = Linker()
        linker_odr_diff.link([tu1, tu4])
        print("Linker: Unexpected success on mismatched inline")
    except LinkerError as err:
        print(f"Detected inline definition mismatch: {err}")


def main() -> None:
    run_odr_experiments()


main()
