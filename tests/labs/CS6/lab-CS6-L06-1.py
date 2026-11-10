"""CS6 Lab L06-1: Profiling Hotspots, Little's Law, and Latency vs Throughput Trade-offs.

Standard library only. Simulates statistical profiling sample distribution,
M/M/1 queuing dynamics under Little's Law (L = lambda * W), and batching latency trade-offs.
"""

from __future__ import annotations


def run_profiling_and_queuing_model() -> None:
    print("=== CS6 Lab 6: Profiling, Queuing Dynamics & Little's Law ===")

    # 1. Statistical Sampling Profiler Model (10,000 timer interrupts)
    total_samples = 10000
    sample_distribution = {
        "market_data_ingest": 620,
        "book_depth_update": 1150,
        "monte_carlo_var_kernel": 6840,
        "regulatory_reporting": 430,
        "json_serialization": 960,
    }

    print(f"1. Statistical CPU Profiling Flame Graph Analysis ({total_samples:,} samples):")
    print(f"{'Routine Name':<28} | {'Samples':>8} | {'CPU Share':>10} | {'Verdict'}")
    print("-" * 62)
    for routine, count in sample_distribution.items():
        share = count / total_samples
        verdict = "CRITICAL HOTSPOT" if share > 0.50 else ("Secondary" if share > 0.10 else "Minor")
        print(f"{routine:<28} | {count:8d} | {share * 100:9.1f}% | {verdict}")
    print()

    # 2. Little's Law and Queuing Theory Simulation (M/M/1 Queue)
    # Service rate mu = 20,000 orders/sec -> Mean service time W_s = 50 microseconds
    mu = 20000.0  # orders / sec
    mean_service_us = (1.0 / mu) * 1e6  # 50 microseconds

    utilizations = [0.20, 0.50, 0.80, 0.90, 0.95]

    print("2. Queuing Pipeline Under Little's Law (L = lambda * W):")
    print(f"   Service Capacity mu:         {mu:,.0f} orders/sec (Service time: {mean_service_us:.1f} us)\n")
    header = (
        f"{'Arrival (lambda)':>16} | {'Util (rho)':>10} | {'Queue (L)':>10} | "
        f"{'Wait Time (Wq)':>15} | {'Total Time (W)':>15}"
    )
    print(header)
    print("-" * 75)

    for rho in utilizations:
        lam = rho * mu
        # Little's Law & M/M/1 formulas:
        # L = rho / (1 - rho) total customers in system
        # W = 1 / (mu * (1 - rho)) total time in system (seconds)
        # W_q = rho / (mu * (1 - rho)) waiting time in queue (seconds)
        l_system = rho / (1.0 - rho)
        w_total_us = (1.0 / (mu * (1.0 - rho))) * 1e6
        w_queue_us = (rho / (mu * (1.0 - rho))) * 1e6

        print(f"{lam:14,.0f}/s | {rho * 100:9.1f}% | {l_system:10.2f} | {w_queue_us:12.1f} us | {w_total_us:12.1f} us")
    print()

    # 3. Batching Trade-offs: Latency vs Throughput
    # Batching amortizes per-packet overhead (4 us fixed) over B items (0.5 us marginal)
    batch_sizes = [1, 4, 16, 64, 256]
    fixed_overhead_us = 4.0
    item_compute_us = 0.5

    print("3. Batching Trade-offs (Microsecond Latency vs Million Orders/sec):")
    print(f"{'Batch Size (B)':>14} | {'Batch Time':>12} | {'Per-Item Latency':>16} | {'Throughput':>18}")
    print("-" * 67)

    for b in batch_sizes:
        batch_latency_us = fixed_overhead_us + b * item_compute_us
        per_item_latency_us = batch_latency_us / b
        throughput_orders_s = b / (batch_latency_us * 1e-6)

        m_orders = throughput_orders_s / 1e6
        print(f"{b:14d} | {batch_latency_us:9.1f} us | {per_item_latency_us:13.2f} us | {m_orders:14.2f} M/s")


run_profiling_and_queuing_model()
