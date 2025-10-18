# Python 런타임용 import (np.zeros, np.arange 등)
import numpy as np

# C 레벨 타입 선언용 cimport
cimport numpy as cnp

# 함수 정의
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
