"""
Cython Pure Python Mode - Array Summation Benchmark
Pure Python mode version of bench_cy.pyx
Uses PEP 526 inline type annotations

Note: Pure Python mode in Cython 0.29.x has limitations with typed arrays.
For best performance, use .pyx syntax (bench_cy.pyx)
"""

import cython


@cython.boundscheck(False)
@cython.wraparound(False)
def sum_array(arr):
    """
    Equivalent to bench_cy.pyx sum_array but with .py syntax.
    Sum array elements using Cython pure Python mode

    In Cython 0.29.x pure Python mode, we cannot easily declare
    typed memoryviews as function parameters, so performance
    will be limited compared to .pyx syntax.
    """
    i: cython.Py_ssize_t
    n: cython.Py_ssize_t
    s: cython.double
    arr_view: cython.double[:]

    # Cast to typed memoryview for faster access
    arr_view = arr
    n = arr_view.shape[0]
    s = 0.0

    for i in range(n):
        s += arr_view[i]

    return s
