import math
import time
import numpy as np
from numba import njit, prange, vectorize, guvectorize
from concurrent.futures import ThreadPoolExecutor

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


def run_prange(n=N, show_result=False):
    """Run Numba parallel computation with prange"""
    # Warm-up JIT compilation
    _ = compute_prange(100)

    t_start = time.time()
    result = compute_prange(n)
    elapsed = time.time() - t_start

    if show_result:
        print(f"Numba (parallel prange) Computation complete! Result: {result:.2f}")
    print(f"Numba (parallel prange): {elapsed:.3f} sec")
    return result


def run_prange_private(n=N, num_threads=4, show_result=False):
    """Run Numba parallel computation with private accumulators"""
    # Warm-up JIT compilation
    _ = compute_prange_private(100, num_threads)

    t_start = time.time()
    result = compute_prange_private(n, num_threads)
    elapsed = time.time() - t_start

    if show_result:
        print(f"Numba (parallel private) Computation complete! Result: {result:.2f}")
    print(f"Numba (parallel private): {elapsed:.3f} sec")
    return result


# 1. @vectorize with target='parallel'
@vectorize(['float64(int64)'], target='parallel')
def compute_sin_element(i):
    """Vectorized parallel element-wise computation"""
    return math.sin(i * 0.0001)


def run_vectorize(n=N, show_result=False):
    """Run Numba parallel computation using @vectorize"""
    # Warm-up JIT compilation
    _ = compute_sin_element(np.arange(100, dtype=np.int64)).sum()

    t_start = time.time()
    indices = np.arange(n, dtype=np.int64)
    result = compute_sin_element(indices).sum()
    elapsed = time.time() - t_start

    if show_result:
        print(f"Numba (@vectorize parallel) Computation complete! Result: {result:.2f}")
    print(f"Numba (@vectorize parallel): {elapsed:.3f} sec")
    return result


# 2. @guvectorize (Generalized Universal Functions)
@guvectorize(['(int64[:], float64[:])'], '(n)->()', target='parallel')
def compute_gufunc(indices, result):
    """Generalized ufunc for parallel reduction"""
    s = 0.0
    for i in range(indices.shape[0]):
        s += math.sin(indices[i] * 0.0001)
    result[0] = s


def run_guvectorize(n=N, chunk_size=1_000_000, show_result=False):
    """Run Numba parallel computation using @guvectorize"""
    # Warm-up JIT compilation
    test_arr = np.arange(100, dtype=np.int64).reshape(1, -1)
    _ = compute_gufunc(test_arr)

    t_start = time.time()
    # Split indices into chunks for parallel processing
    indices = np.arange(n, dtype=np.int64)
    num_chunks = (n + chunk_size - 1) // chunk_size

    # Pad to make even chunks
    padded_size = num_chunks * chunk_size
    padded_indices = np.zeros(padded_size, dtype=np.int64)
    padded_indices[:n] = indices

    # Reshape into chunks
    chunked = padded_indices.reshape(num_chunks, chunk_size)

    # Apply gufunc and sum results
    results = compute_gufunc(chunked)
    result = results.sum()

    elapsed = time.time() - t_start

    if show_result:
        print(f"Numba (@guvectorize parallel) Computation complete! Result: {result:.2f}")
    print(f"Numba (@guvectorize parallel): {elapsed:.3f} sec")
    return result


# 3. Manual chunking with nogil
@njit(nogil=True)
def compute_chunk(start, end):
    """Worker function with nogil for manual threading"""
    s = 0.0
    for i in range(start, end):
        s += math.sin(i * 0.0001)
    return s


def run_manual_threading(n=N, num_threads=4, show_result=False):
    """Run Numba parallel computation with manual threading"""
    # Warm-up JIT compilation
    _ = compute_chunk(0, 100)

    t_start = time.time()
    chunk_size = n // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = i * chunk_size
            end = n if i == num_threads - 1 else (i + 1) * chunk_size
            futures.append(executor.submit(compute_chunk, start, end))

        results = [f.result() for f in futures]

    result = sum(results)
    elapsed = time.time() - t_start

    if show_result:
        print(f"Numba (manual threading nogil) Computation complete! Result: {result:.2f}")
    print(f"Numba (manual threading nogil): {elapsed:.3f} sec")
    return result
