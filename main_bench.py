import time
import numpy as np
import pandas as pd
import cProfile
import pstats
from pstats import SortKey

import bench_py
import bench_cy
import bench_pure_cy
import bench_cpp
import bench_nb


def benchmark(label, func, *args):
    t0 = time.time()
    for _ in range(2):
        func(*args)
    elapsed = time.time() - t0
    print(f"{label:<16}: {elapsed:6.3f} sec")


def main():
    df = pd.DataFrame({"x": np.random.rand(30_000_000)})
    arr = df["x"].to_numpy()

    benchmark("Python", bench_py.sum_array, arr)
    benchmark("Cython", bench_cy.sum_array, arr)
    benchmark("Cython (Python)", bench_cy.sum_array_python_ver, arr)
    benchmark("Cython Pure-Py", bench_pure_cy.sum_array, arr)
    benchmark("PyBind11", bench_cpp.sum_array, arr)
    # numba is delayed by ~0.15 sec due to the initial compilation.
    benchmark("Numba", bench_nb.sum_array, arr)
    benchmark("NumPy", np.sum, arr)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    # Save profile data for snakeviz
    profile_file = "main_bench.prof"
    profiler.dump_stats(profile_file)
    print(f"\nProfile data saved to: {profile_file}")
    print(f"To visualize, run: snakeviz {profile_file}")

    print("\n" + "="*80)
    print("PROFILING RESULTS")
    print("="*80)

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(SortKey.CUMULATIVE)
