# sandbox_cython_pybind

## for benchmark
```
$ python setup_bench.py build_ext --inplace
$ c++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes)     bench_cpp.cpp -o bench_cpp$(python3.10-config --extension-suffix)
```

## for parallel benchmark
```
$ python setup_parallel.py build_ext --inplace
```
