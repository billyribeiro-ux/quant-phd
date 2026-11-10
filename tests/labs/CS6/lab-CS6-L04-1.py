"""CS6 Lab L04-1: GPU Warp Divergence, Memory Coalescing, and SIMT Execution Model.

Standard library only. Simulates a CUDA Streaming Multiprocessor (SM) warp of 32 threads
evaluating branchy option payoffs, computing warp execution efficiency and memory coalescing transactions.
"""

from __future__ import annotations


def run_gpu_warp_model() -> None:
    warp_size = 32
    dram_transaction_size = 128  # bytes per GPU memory transaction
    bytes_per_double = 8

    print("=== CS6 Lab 4: GPU Programming Model & Warp Execution Simulation ===")
    print(f"Hardware Warp Size: {warp_size} threads, DRAM Transaction Unit: {dram_transaction_size} bytes\n")

    # 1. Global Memory Coalescing Simulation
    # Scenario A: Coalesced memory access (Thread k reads offset k * 8)
    coalesced_bytes = warp_size * bytes_per_double  # 256 bytes
    coalesced_transactions = (coalesced_bytes + dram_transaction_size - 1) // dram_transaction_size
    coalesced_bus_efficiency = coalesced_bytes / (coalesced_transactions * dram_transaction_size)

    # Scenario B: Strided non-coalesced access (Thread k reads offset k * 128, spanning separate segments)
    uncoalesced_transactions = warp_size  # 32 distinct 128-byte transactions
    uncoalesced_transferred = uncoalesced_transactions * dram_transaction_size
    uncoalesced_bus_efficiency = coalesced_bytes / uncoalesced_transferred

    coalesced_transferred = coalesced_transactions * dram_transaction_size
    print("1. Memory Access Coalescing (32 double-precision reads = 256 bytes payload):")
    print(f"   Coalesced Transactions:      {coalesced_transactions} (transferred {coalesced_transferred}B)")
    print(f"   Coalesced Bus Efficiency:    {coalesced_bus_efficiency:.1%}")
    print(f"   Uncoalesced Transactions:    {uncoalesced_transactions} (transferred {uncoalesced_transferred}B)")
    print(f"   Uncoalesced Bus Efficiency:  {uncoalesced_bus_efficiency:.1%}")
    print(f"   Memory Bandwidth Waste:      {(1.0 - uncoalesced_bus_efficiency) * 100:.1f}%\n")

    # 2. SIMT Warp Divergence Simulation
    # 32 threads evaluate an option payoff: branch A (exercise, 20 cycles), branch B (expire worthless, 5 cycles)
    # Test cases: Divergent (16 exercise, 16 expire) vs Convergent (all 32 exercise)
    divergent_active_a = 16
    divergent_active_b = 16
    cycles_path_a = 20
    cycles_path_b = 5

    # In SIMT, divergent paths are executed serially across the warp:
    divergent_total_cycles = cycles_path_a + cycles_path_b  # 25 cycles
    divergent_useful_thread_cycles = (divergent_active_a * cycles_path_a) + (divergent_active_b * cycles_path_b)
    divergent_total_thread_capacity = warp_size * divergent_total_cycles
    divergent_warp_efficiency = divergent_useful_thread_cycles / divergent_total_thread_capacity

    # Convergent warp: all 32 threads take Path A
    convergent_active_a = 32
    convergent_total_cycles = cycles_path_a  # 20 cycles
    convergent_useful_thread_cycles = convergent_active_a * cycles_path_a
    convergent_total_thread_capacity = warp_size * convergent_total_cycles
    convergent_warp_efficiency = convergent_useful_thread_cycles / convergent_total_thread_capacity

    print("2. SIMT Warp Divergence (Path A = 20 cycles, Path B = 5 cycles):")
    print("   Scenario A: Divergent Warp (50% Exercise / 50% Expire):")
    print(f"     Execution Serialized:      Path A ({cycles_path_a} cyc) + Path B ({cycles_path_b} cyc)")
    print(f"     Warp Execution Latency:    {divergent_total_cycles} cycles")
    print(f"     Useful Thread Work:        {divergent_useful_thread_cycles} thread-cycles")
    print(f"     Warp Execution Efficiency: {divergent_warp_efficiency:.1%}")
    print("   Scenario B: Convergent Warp (100% Exercise):")
    print(f"     Execution Single Pass:     Path A only ({convergent_total_cycles} cyc)")
    print(f"     Warp Execution Latency:    {convergent_total_cycles} cycles")
    print(f"     Useful Thread Work:        {convergent_useful_thread_cycles} thread-cycles")
    print(f"     Warp Execution Efficiency: {convergent_warp_efficiency:.1%}")


run_gpu_warp_model()
