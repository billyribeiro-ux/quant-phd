"""CS6 Lab L02-1: Execution Models, CPython GIL Contention, and Process Isolation.

Standard library only. Deterministic microarchitectural and runtime model simulating
CPython GIL serialization on CPU-bound workloads, multi-process IPC memory overhead,
and native C++ nogil shared-memory multithreading.
"""

from __future__ import annotations


def run_concurrency_model() -> None:
    n_assets = 10
    n_obs = 10000
    n_cores = 4

    # Covariance computation: dot products across asset pairs: (M * (M + 1) / 2) * N operations
    pairs = (n_assets * (n_assets + 1)) // 2  # 55 pairs
    total_flops = pairs * n_obs * 2  # 1,100,000 floating point operations
    base_cpu_time_ms = 100.0  # Normalized single-core execution time in ms

    print("=== CS6 Lab 2: Concurrency Models & Python GIL Simulation ===")
    print(f"Task: Asset covariance ({n_assets} assets, {n_obs} obs, {pairs} unique pairs)")
    print(f"Compute workload: {total_flops:,} FLOPs, Baseline serial runtime: {base_cpu_time_ms:.1f} ms\n")

    # Model 1: Multithreaded Python under CPython GIL
    # All threads serialize on bytecode execution + context switch penalty
    gil_switch_interval_ms = 5.0  # sys.getswitchinterval() default 5ms
    thread_switch_overhead_ms = 0.05  # Context switch and lock contention penalty
    n_switches = int(base_cpu_time_ms / gil_switch_interval_ms) * (n_cores - 1)
    gil_total_switch_overhead = n_switches * thread_switch_overhead_ms
    t_threads = base_cpu_time_ms + gil_total_switch_overhead
    speedup_threads = base_cpu_time_ms / t_threads

    print("1. Multi-threaded CPython (GIL Contention):")
    print(f"   Worker threads:              {n_cores}")
    print("   GIL status:                  HELD (bytecode execution serialized)")
    print(f"   Forced thread switches:      {n_switches}")
    print(f"   Switch & contention delay:   {gil_total_switch_overhead:.2f} ms")
    print(f"   Simulated execution time:    {t_threads:.2f} ms")
    print(f"   Effective parallel speedup:  {speedup_threads:.3f}x (SLOWER than serial)\n")

    # Model 2: Multi-processing with IPC
    # True parallelism, but must serialize inputs and outputs across IPC pipes
    ipc_bytes_per_asset = n_obs * 8  # 80 KB per asset series
    total_ipc_input = n_assets * ipc_bytes_per_asset  # 800 KB
    total_ipc_output = pairs * 8  # 440 bytes
    ipc_transfer_rate_mb_s = 500.0  # Pipe/shm transfer bandwidth (500 MB/s)
    ipc_overhead_ms = ((total_ipc_input + total_ipc_output) / (ipc_transfer_rate_mb_s * 1024 * 1024)) * 1000.0
    process_spawn_overhead_ms = 8.0  # Fork/exec runtime initialization cost
    t_process = (base_cpu_time_ms / n_cores) + ipc_overhead_ms + process_spawn_overhead_ms
    speedup_process = base_cpu_time_ms / t_process

    print("2. Multi-process Isolation (IPC & Memory Overhead):")
    print(f"   Worker processes:            {n_cores}")
    print("   Process memory spaces:       ISOLATED (independent GIL per process)")
    print(f"   IPC serialization traffic:   {total_ipc_input + total_ipc_output:,} bytes")
    print(f"   Process spawn & IPC latency: {ipc_overhead_ms + process_spawn_overhead_ms:.2f} ms")
    print(f"   Simulated execution time:    {t_process:.2f} ms")
    print(f"   Effective parallel speedup:  {speedup_process:.3f}x\n")

    # Model 3: Native Shared-Memory C++ Extension (Pybind11 / nogil)
    # Threads share memory space directly with zero IPC and GIL released
    thread_sync_overhead_ms = 0.5  # Minimal barrier synchronization
    t_native = (base_cpu_time_ms / n_cores) + thread_sync_overhead_ms
    speedup_native = base_cpu_time_ms / t_native

    print("3. Native C++ Shared-Memory Extension (GIL Released):")
    print(f"   Native worker threads:       {n_cores}")
    print("   GIL status:                  RELEASED (Py_BEGIN_ALLOW_THREADS)")
    print("   Memory space:                SHARED (zero IPC copies)")
    print(f"   Barrier sync latency:        {thread_sync_overhead_ms:.2f} ms")
    print(f"   Simulated execution time:    {t_native:.2f} ms")
    print(f"   Effective parallel speedup:  {speedup_native:.3f}x")


run_concurrency_model()
