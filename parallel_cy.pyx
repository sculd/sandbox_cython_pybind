from cython.parallel cimport prange
from libc.math cimport sin
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def run_cython(int n=50000000):
    cdef double s = 0
    cdef int i

    for i in prange(n, nogil=True, num_threads=4):
        s += sin(i * 0.0001)

    print(f"(Cyton) Computation complete! Result: {s:.2f}")
    return s
