from cython.parallel cimport prange
from libc.math cimport sin
cimport cython
import time

@cython.boundscheck(False)
@cython.wraparound(False)
def run_prange(int n=50000000):
    t_start = time.time()
    cdef double s = 0
    cdef int i

    for i in prange(n, nogil=True, num_threads=4):
        s += sin(i * 0.0001)

    print(f"(Cyton) Computation complete! Result: {s:.2f}")
    print(f"Cython (nogil, prange): {time.time() - t_start:.3f} sec")
    return s

# Alternative implementation using parallel block with manual thread management
from cython.parallel cimport parallel, threadid
from openmp cimport omp_get_thread_num, omp_get_num_threads

cdef double[:] thread_sums

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def run_parallel(int n=50_000_000, int num_threads=4):
    global thread_sums
    import numpy as np
    thread_sums = np.zeros(num_threads, dtype=np.float64)

    t_start = time.time()
    cdef int i, j, tid, start_idx
    cdef double partial_sum, total_sum

    total_sum = 0.0

    with nogil, parallel(num_threads=num_threads):
        tid = threadid()
        partial_sum = 0.0
        i = tid

        # Use C-level while loop (not Python range)
        while i < n:
            partial_sum = partial_sum + sin(i * 0.0001)
            i = i + num_threads

        thread_sums[tid] = partial_sum

    # Sum up all thread results
    for j in range(num_threads):
        total_sum = total_sum + thread_sums[j]

    print(f"Cython (nogil, parallel): {time.time() - t_start:.3f} sec")
    return total_sum
