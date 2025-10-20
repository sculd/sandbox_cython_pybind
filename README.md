# sandbox_cython_pybind

## for benchmark
```
$ python setup_bench.py build_ext --inplace
$ c++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes)     bench_cpp.cpp -o bench_cpp$(python3.10-config --extension-suffix)
```
result:
```
Python          :  2.393 sec
Cython          :  0.022 sec
Cython (Python) :  1.883 sec
PyBind11        :  0.023 sec
Numba           :  0.239 sec
NumPy           :  0.012 sec
```

## for parallel benchmark
```
$ python setup_parallel.py build_ext --inplace
```
result:
```
(Python) Computation complete! Result: 8453.81
Python (GIL): 2.513 sec
Cython (nogil, prange) Computation complete! Result: 8453.81
Cython (nogil, prange): 0.079 sec
Cython (nogil, parallel) Computation complete! Result: 8453.81
Cython (nogil, parallel): 0.079 sec
Cython (nogil, parallel malloc) Computation complete! Result: 8453.81
Cython (nogil, parallel malloc): 0.079 sec
Numba (parallel prange) Computation complete! Result: 8453.81
Numba (parallel prange): 0.021 sec
Numba (parallel private) Computation complete! Result: 8453.81
Numba (parallel private): 0.084 sec
Numba (@vectorize parallel) Computation complete! Result: 8453.81
Numba (@vectorize parallel): 0.074 sec
Numba (@guvectorize parallel) Computation complete! Result: 8453.81
Numba (@guvectorize parallel): 0.093 sec
Numba (manual threading nogil) Computation complete! Result: 8453.81
Numba (manual threading nogil): 0.152 sec
NumPy (threading) Computation complete! Result: 8453.81
NumPy (threading): 0.134 sec
NumPy (ThreadPoolExecutor) Computation complete! Result: 8453.81
NumPy (ThreadPoolExecutor): 0.130 sec
Python loop (threading, GIL-bound) Computation complete! Result: 8453.81
Python loop (threading, GIL-bound): 2.252 sec
```