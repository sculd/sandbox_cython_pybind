# sandbox_cython_pybind

## for benchmark
```
$ python setup_bench_cy.py build_ext --inplace
$ python setup_bench_pure_cy.py build_ext --inplace
$ c++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes)     bench_cpp.cpp -o bench_cpp$(python3.10-config --extension-suffix)
$ python main_bench.py
```
result:
```
Python          :  2.415 sec
Cython          :  0.022 sec
Cython (Python) :  1.914 sec
Cython Pure-Py  :  0.022 sec
PyBind11        :  0.022 sec
Numba           :  0.247 sec
Numba compiled  :  0.022 sec
NumPy           :  0.013 sec
```

## for parallel benchmark
```
$ python setup_parallel.py build_ext --inplace
$ python main_parallel.py
```
result:
```
Python (GIL): 2.412 sec
Cython (nogil, prange): 0.080 sec
Cython (nogil, parallel): 0.080 sec
Cython (nogil, parallel malloc): 0.079 sec
Numba (parallel prange): 0.038 sec
Numba (parallel private): 0.088 sec
Numba (@vectorize parallel): 0.079 sec
Numba (@guvectorize parallel): 0.090 sec
Numba (manual threading nogil): 0.152 sec
NumPy (threading): 0.134 sec
NumPy (ThreadPoolExecutor): 0.134 sec
Python loop (threading, GIL-bound): 2.188 sec
```

## Verdict

### NumPy
> “If it can be vectorized, use NumPy.”

### Numba

> “When you want C-like performance with minimal code change.”

### Cython

> “When you need integration with C/C++ libraries.”

### PyBind11

> “When you already have (or prefer) C++.”

## Summary Table

| Scenario | Recommended Tool |
|-----------|------------------|
| Vector or matrix computation (simple math) | 🟩 **NumPy** |
| Pure mathematical broadcasting / linear algebra | 🟩 **NumPy** |
| Numeric loops with simple logic | 🟨 **Numba** |
| Quick prototyping and fast iteration | 🟨 **Numba** |
| Performance-critical loops or GIL-free parallelization | 🟦 **Cython** |
| Data-science / ML code mixing NumPy arrays and loops | 🟦 **Cython + NumPy** |
| Need for fine control over memory layout and thread behavior | 🟦 **Cython** |
| Wrapping existing C++ code or libraries | 🟥 **PyBind11** |
| Existing native engine written in C++ | 🟥 **PyBind11** |
