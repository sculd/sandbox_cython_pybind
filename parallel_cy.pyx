from cython.parallel cimport prange, parallel, threadid
from libc.math cimport sin
cimport cython
import time

@cython.boundscheck(False)
@cython.wraparound(False)
def run_prange(int n=50000000, bint show_result=False):
    t_start = time.time()
    cdef double s = 0
    cdef int i

    for i in prange(n, nogil=True, num_threads=4):
        s += sin(i * 0.0001)

    if show_result:
        print(f"Cython (nogil, prange) Computation complete! Result: {s:.2f}")
    print(f"Cython (nogil, prange): {time.time() - t_start:.3f} sec")
    return s

# Alternative implementation using parallel block with manual thread management
from libc.stdlib cimport malloc, free

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def run_parallel_np_zeroes(int n=50_000_000, int num_threads=4, bint show_result=False):
    import numpy as np
    cdef double[:] thread_sums = np.zeros(num_threads, dtype=np.float64)

    t_start = time.time()
    cdef int j, tid, i
    cdef double total_sum = 0.0
    cdef double local_sum

    # Each thread computes its portion independently
    with nogil, parallel(num_threads=num_threads):
        tid = threadid()
        local_sum = 0.0  # Thread-private accumulator
        i = tid

        # Accumulate into local variable - self-contained per thread
        while i < n:
            local_sum = local_sum + sin(i * 0.0001)
            i = i + num_threads

        # Write result once at the end
        thread_sums[tid] = local_sum

    # Sum up all thread results
    total_sum = 0.0
    for j in range(num_threads):
        total_sum = total_sum + thread_sums[j]

    if show_result:
        print(f"Cython (nogil, parallel) Computation complete! Result: {total_sum:.2f}")
    print(f"Cython (nogil, parallel): {time.time() - t_start:.3f} sec")
    return total_sum

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def run_parallel_malloc(int n=50_000_000, int num_threads=4, bint show_result=False):
    t_start = time.time()
    cdef int j, tid, i
    cdef double total_sum = 0.0
    cdef double local_sum
    cdef double* thread_sums

    # Allocate C array
    thread_sums = <double*>malloc(num_threads * sizeof(double))
    if thread_sums == NULL:
        raise MemoryError()

    # Initialize to zero
    for j in range(num_threads):
        thread_sums[j] = 0.0

    # Each thread computes its portion independently
    with nogil, parallel(num_threads=num_threads):
        tid = threadid()
        local_sum = 0.0  # Thread-private accumulator
        i = tid

        # Accumulate into local variable - self-contained per thread
        while i < n:
            local_sum = local_sum + sin(i * 0.0001)
            i = i + num_threads

        # Write result once at the end
        thread_sums[tid] = local_sum

    # Sum up all thread results
    total_sum = 0.0
    for j in range(num_threads):
        total_sum = total_sum + thread_sums[j]

    free(thread_sums)

    if show_result:
        print(f"Cython (nogil, parallel malloc) Computation complete! Result: {total_sum:.2f}")
    print(f"Cython (nogil, parallel malloc): {time.time() - t_start:.3f} sec")
    return total_sum
