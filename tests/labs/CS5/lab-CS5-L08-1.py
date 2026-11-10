"""CS5 Lab L08: C ABI status code mapping and WebAssembly wasm32 binary header validator.

Standard library only. Simulates C ABI foreign function interface status-to-exception translation
and inspects the canonical 8-byte WebAssembly binary module header and section identifiers.
"""

from __future__ import annotations

import math
from typing import NamedTuple

STATUS_SUCCESS = 0
ERR_NON_FINITE_FLOAT = 1
ERR_NON_POSITIVE_PARAM = 2
ERR_INSUFFICIENT_PATHS = 3
ERR_INVALID_SEED = 4

WASM_MAGIC = b"\x00\x61\x73\x6d"  # \0asm
WASM_VERSION = b"\x01\x00\x00\x00"  # Version 1 (little-endian uint32)


class CAbiPricingResult(NamedTuple):
    call: float
    call_se: float
    put: float
    put_se: float


def simulated_c_abi_kernel(
    s0: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int,
    seed: int,
) -> tuple[int, tuple[float, float, float, float] | None]:
    """Models native C++ function exposed via extern 'C' returning integer status code."""
    for val in (s0, strike, rate, vol, maturity):
        if not math.isfinite(val):
            return ERR_NON_FINITE_FLOAT, None
    if s0 <= 0.0 or strike <= 0.0 or vol <= 0.0 or maturity <= 0.0:
        return ERR_NON_POSITIVE_PARAM, None
    if n_paths < 2:
        return ERR_INSUFFICIENT_PATHS, None
    if not (0 <= seed <= (1 << 64) - 1):
        return ERR_INVALID_SEED, None

    # Dummy calculation for boundary testing
    df = math.exp(-rate * maturity)
    call_est = df * max(s0 - strike, 0.0)
    put_est = df * max(strike - s0, 0.0)
    return STATUS_SUCCESS, (call_est, 0.01, put_est, 0.01)


def python_ctypes_wrapper(
    s0: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int,
    seed: int,
) -> CAbiPricingResult:
    """Python ctypes wrapper translating C ABI status codes to Python exceptions."""
    status, payload = simulated_c_abi_kernel(s0, strike, rate, vol, maturity, n_paths, seed)
    if status == STATUS_SUCCESS and payload is not None:
        return CAbiPricingResult(*payload)
    if status == ERR_NON_FINITE_FLOAT:
        raise ValueError("C ABI kernel error: floating-point parameter is not finite")
    if status == ERR_NON_POSITIVE_PARAM:
        raise ValueError("C ABI kernel error: financial parameters must be strictly positive")
    if status == ERR_INSUFFICIENT_PATHS:
        raise ValueError("C ABI kernel error: n_paths must be >= 2")
    if status == ERR_INVALID_SEED:
        raise ValueError("C ABI kernel error: seed out of 64-bit unsigned integer range")
    raise RuntimeError(f"Unknown C ABI status code: {status}")


def validate_wasm32_binary(binary_bytes: bytes) -> dict[str, str]:
    """Validates the 8-byte header of a freestanding wasm32 compiled binary."""
    if len(binary_bytes) < 8:
        raise ValueError(f"WASM binary must be at least 8 bytes; got {len(binary_bytes)}")

    magic = binary_bytes[:4]
    version = binary_bytes[4:8]

    if magic != WASM_MAGIC:
        raise ValueError(f"Invalid WASM magic bytes: {magic.hex()} (expected {WASM_MAGIC.hex()})")
    if version != WASM_VERSION:
        raise ValueError(f"Unsupported WASM version: {version.hex()} (expected {WASM_VERSION.hex()})")

    ver_int = int.from_bytes(version, byteorder="little")
    return {
        "magic": magic.decode("ascii", errors="replace"),
        "magic_hex": magic.hex(),
        "version": str(ver_int),
        "header_valid": "true",
    }


def run_systems_boundary_experiments() -> None:
    print("CS5 L08: Foreign Function Interface (C ABI) and WebAssembly Header Model")

    # Experiment 1: Successful C ABI invocation
    res = python_ctypes_wrapper(100.0, 100.0, 0.05, 0.20, 1.0, 5000, 42)
    print(f"C ABI call successful: call={res.call:.4f}, put={res.put:.4f}")

    # Experiment 2: C ABI error code propagation
    for test_name, params in [
        ("Negative volatility", (100.0, 100.0, 0.05, -0.20, 1.0, 5000, 42)),
        ("Insufficient paths (N=1)", (100.0, 100.0, 0.05, 0.20, 1.0, 1, 42)),
        ("Non-finite spot price (NaN)", (float("nan"), 100.0, 0.05, 0.20, 1.0, 5000, 42)),
    ]:
        try:
            python_ctypes_wrapper(*params)
            print(f"C ABI: Unexpected success on {test_name}")
        except ValueError as err:
            print(f"C ABI status translation ({test_name}): {err}")

    # Experiment 3: WebAssembly wasm32 binary header verification
    synthetic_wasm_module = WASM_MAGIC + WASM_VERSION + b"\x01\x04\x01\x60\x00\x00"  # Header + type section stub
    wasm_info = validate_wasm32_binary(synthetic_wasm_module)
    print(f"WASM binary validation: magic=0x{wasm_info['magic_hex']} (\\0asm), version={wasm_info['version']}")

    # Invalid WASM magic test
    try:
        validate_wasm32_binary(b"\x7fELF" + WASM_VERSION)  # ELF header instead of WASM
        print("WASM: Unexpected success on ELF binary")
    except ValueError as err:
        print(f"WASM header rejection (corrupt magic): {err}")


def main() -> None:
    run_systems_boundary_experiments()


main()
