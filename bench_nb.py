import numba as nb

@nb.njit
def sum_array(arr):
    s = 0.0
    for x in arr:
        s += x
    return s
