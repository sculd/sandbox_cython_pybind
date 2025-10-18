import time
import numpy as np
import pandas as pd

import bench_py
import bench_cy
import bench_cpp
import bench_nb

df = pd.DataFrame({"x": np.random.rand(30_000_000)})

arr = df["x"].to_numpy()


def benchmark(label, func, *args):
    t0 = time.time()
    func(*args)
    elapsed = time.time() - t0
    print(f"{label:<16}: {elapsed:6.3f} sec")

benchmark("Python", bench_py.sum_array, arr)
benchmark("Cython", bench_cy.sum_array, arr)
benchmark("Cython (Python)", bench_cy.sum_array_python_ver, arr)
benchmark("PyBind11", bench_cpp.sum_array, arr)
benchmark("Numba", bench_nb.sum_array, arr)
benchmark("NumPy", np.sum, arr)
