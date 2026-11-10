"""CS6 Lab L03-1: SIMD Vectorization, Register Lane Packing, and Memory Alignment Model.

Standard library only. Simulates x86-64 SIMD execution units (Scalar vs AVX2 vs AVX-512)
evaluating Black-Scholes pricing kernels, analyzing memory alignment penalties and
mask-based branch elimination.
"""

from __future__ import annotations


def run_simd_model() -> None:
    n_options = 1024  # 1024 European options

    # Microarchitectural parameters
    # Scalar: 1 double / 64-bit register
    # AVX2: 4 doubles / 256-bit YMM register (32-byte alignment)
    # AVX-512: 8 doubles / 512-bit ZMM register (64-byte alignment)
    scalar_ops_per_option = 48  # FLOPs per Black-Scholes evaluation
    scalar_total_ops = n_options * scalar_ops_per_option

    print("=== CS6 Lab 3: SIMD Vectorization & Execution Unit Simulation ===")
    print(f"Workload: {n_options} European option pricing evaluations ({scalar_total_ops:,} FLOPs)\n")

    # 1. Scalar Execution (x87 / Scalar SSE)
    # Array-of-Structs (AoS) with branch mispredictions on payoff max()
    branch_mispredict_rate = 0.08  # 8% branch misprediction on near-ATM strikes
    branch_penalty_cycles = 15  # Modern out-of-order CPU branch penalty
    scalar_instructions = scalar_total_ops
    scalar_branch_stalls = int(n_options * branch_mispredict_rate * branch_penalty_cycles)
    scalar_total_cycles = scalar_instructions + scalar_branch_stalls

    print("1. Scalar Baseline (AoS Layout, Branchy Payoff):")
    print("   SIMD Vector Width:           1 double (64 bits)")
    print(f"   Instruction Count:           {scalar_instructions:,} instructions")
    print(f"   Branch Mispredict Stalls:    {scalar_branch_stalls:,} cycles")
    print(f"   Total Execution Cycles:      {scalar_total_cycles:,} cycles")
    print(f"   Throughput:                  {scalar_total_ops / scalar_total_cycles:.3f} FLOPs/cycle\n")

    # 2. AVX2 Vectorization (256-bit, Struct-of-Arrays, 32B aligned)
    # 4 doubles per vector instruction; branch eliminated via blendv_pd (predicated masking)
    avx2_lanes = 4
    avx2_instructions = scalar_total_ops // avx2_lanes
    avx2_branch_stalls = 0  # Zero branch mispredictions via SIMD bitwise blend
    avx2_total_cycles = avx2_instructions + avx2_branch_stalls
    avx2_speedup = scalar_total_cycles / avx2_total_cycles

    print("2. AVX2 Vector Execution (256-bit YMM, SoA Layout, Masked Blend):")
    print(f"   SIMD Vector Width:           {avx2_lanes} doubles (256 bits)")
    print("   Memory Alignment:            32 bytes (Aligned _mm256_load_pd)")
    print(f"   Instruction Count:           {avx2_instructions:,} instructions")
    print("   Branch Mispredict Stalls:    0 cycles (Eliminated via _mm256_blendv_pd)")
    print(f"   Total Execution Cycles:      {avx2_total_cycles:,} cycles")
    print(f"   Speedup vs Scalar:           {avx2_speedup:.3f}x\n")

    # 3. AVX-512 Vectorization (512-bit, Struct-of-Arrays, 64B aligned)
    # 8 doubles per vector instruction; mask registers (k1-k7)
    avx512_lanes = 8
    avx512_instructions = scalar_total_ops // avx512_lanes
    avx512_branch_stalls = 0
    avx512_total_cycles = avx512_instructions + avx512_branch_stalls
    avx512_speedup = scalar_total_cycles / avx512_total_cycles

    print("3. AVX-512 Vector Execution (512-bit ZMM, SoA Layout, Mask Registers):")
    print(f"   SIMD Vector Width:           {avx512_lanes} doubles (512 bits)")
    print("   Memory Alignment:            64 bytes (Aligned _mm512_load_pd)")
    print(f"   Instruction Count:           {avx512_instructions:,} instructions")
    print("   Branch Mispredict Stalls:    0 cycles (AVX-512 opmask k-register)")
    print(f"   Total Execution Cycles:      {avx512_total_cycles:,} cycles")
    print(f"   Speedup vs Scalar:           {avx512_speedup:.3f}x")


run_simd_model()
