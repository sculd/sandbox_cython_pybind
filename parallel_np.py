import time
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor

N = 50_000_000


def worker_numpy(start, end, results, index):
    """Worker using NumPy operations (releases GIL in C code)"""
    chunk = np.arange(start, end, dtype=np.int64)
    # np.sin releases the GIL during computation
    result = np.sin(chunk * 0.0001).sum()
    results[index] = result


def worker_python_loop(start, end, results, index):
    """Worker using pure Python loop (GIL-bound)"""
    import math
    s = 0.0
    for i in range(start, end):
        s += math.sin(i * 0.0001)
    results[index] = s


def run_numpy_threading(n=N, num_threads=4, show_result=False):
    """Run NumPy with threading - GIL released during np.sin"""
    t_start = time.time()

    threads = []
    results = [0.0] * num_threads
    chunk = n // num_threads

    for t in range(num_threads):
        start = t * chunk
        end = n if t == num_threads - 1 else (t + 1) * chunk
        th = threading.Thread(target=worker_numpy, args=(start, end, results, t))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    total_sum = sum(results)
    elapsed = time.time() - t_start

    if show_result:
        print(f"NumPy (threading) Computation complete! Result: {total_sum:.2f}")
    print(f"NumPy (threading): {elapsed:.3f} sec")
    return total_sum


def run_numpy_threadpool(n=N, num_threads=4, show_result=False):
    """Run NumPy with ThreadPoolExecutor"""
    chunk = n // num_threads

    t_start = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for t in range(num_threads):
            start = t * chunk
            end = n if t == num_threads - 1 else (t + 1) * chunk
            # Submit lambda that uses NumPy
            future = executor.submit(
                lambda s, e: np.sin(np.arange(s, e, dtype=np.int64) * 0.0001).sum(),
                start, end
            )
            futures.append(future)

        results = [f.result() for f in futures]

    total_sum = sum(results)
    elapsed = time.time() - t_start

    if show_result:
        print(f"NumPy (ThreadPoolExecutor) Computation complete! Result: {total_sum:.2f}")
    print(f"NumPy (ThreadPoolExecutor): {elapsed:.3f} sec")
    return total_sum


def run_python_loop_threading(n=N, num_threads=4, show_result=False):
    """Run pure Python loop with threading (GIL-bound - for comparison)"""
    t_start = time.time()

    threads = []
    results = [0.0] * num_threads
    chunk = n // num_threads

    for t in range(num_threads):
        start = t * chunk
        end = n if t == num_threads - 1 else (t + 1) * chunk
        th = threading.Thread(target=worker_python_loop, args=(start, end, results, t))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    total_sum = sum(results)
    elapsed = time.time() - t_start

    if show_result:
        print(f"Python loop (threading, GIL-bound) Computation complete! Result: {total_sum:.2f}")
    print(f"Python loop (threading, GIL-bound): {elapsed:.3f} sec")
    return total_sum
