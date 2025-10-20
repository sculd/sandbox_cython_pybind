import math
import time
import numpy as np
from numba import njit, prange

N = 50_000_000


@njit(parallel=True)
def compute_prange(n):
    """Numba parallel computation using prange"""
    s = 0.0
    for i in prange(n):
        s += math.sin(i * 0.0001)
    return s


@njit
def compute_strided_worker(start, n, stride):
    """Worker function that processes strided indices"""
    local_sum = 0.0
    i = start
    while i < n:
        local_sum += math.sin(i * 0.0001)
        i += stride
    return local_sum


@njit(parallel=True)
def compute_prange_private(n, num_threads=4):
    """Numba parallel computation with manual thread partitioning"""
    thread_sums = np.zeros(num_threads, dtype=np.float64)

    # Each thread processes strided indices
    for tid in prange(num_threads):
        thread_sums[tid] = compute_strided_worker(tid, n, num_threads)

    return np.sum(thread_sums)


def run_prange(n=N):
    """Run Numba parallel computation with prange"""
    # Warm-up JIT compilation
    _ = compute_prange(100)

    t_start = time.time()
    result = compute_prange(n)
    elapsed = time.time() - t_start

    print(f"Numba (parallel prange) Computation complete! Result: {result:.2f}")
    print(f"Numba (parallel prange): {elapsed:.3f} sec")
    return result


def run_prange_private(n=N, num_threads=4):
    """Run Numba parallel computation with private accumulators"""
    # Warm-up JIT compilation
    _ = compute_prange_private(100, num_threads)

    t_start = time.time()
    result = compute_prange_private(n, num_threads)
    elapsed = time.time() - t_start

    print(f"Numba (parallel private) Computation complete! Result: {result:.2f}")
    print(f"Numba (parallel private): {elapsed:.3f} sec")
    return result
