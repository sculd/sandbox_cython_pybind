def fib(int n):
    cdef int a = 0, b = 1, i
    for i in range(n):
        a, b = a + b, a
    return a
