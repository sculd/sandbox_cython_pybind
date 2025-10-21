# C-level type declarations using cimport
cimport numpy as cnp

# Function definitions
def sum_array(cnp.ndarray[cnp.float64_t, ndim=1] arr):
    cdef Py_ssize_t i, n = arr.shape[0]
    cdef double s = 0

    n = arr.shape[0]
    for i in range(n):
        s += arr[i]

    return s

def sum_array_python_ver(arr):
    s = 0.0
    for x in arr:
        s += x
    return s
