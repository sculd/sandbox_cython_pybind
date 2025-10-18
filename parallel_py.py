import math
import threading
import time

N = 50_000_000

def worker(start, end, results, index):
    s = 0
    for i in range(start, end):
        s += math.sin(i * 0.0001)
    results[index] = s

def run_python():
    threads = []
    results = [0.0] * 4  # List to store results from each thread
    chunk = N // 4
    
    for t in range(4):
        th = threading.Thread(target=worker, args=(t*chunk, (t+1)*chunk, results, t))
        threads.append(th)
        th.start()
    
    for th in threads:
        th.join()
    
    # Sum all results from threads
    total_sum = sum(results)
    print(f"(Python) Computation complete! Result: {total_sum:.2f}")
    return total_sum