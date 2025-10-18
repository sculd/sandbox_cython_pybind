import time
import parallel_py
import parallel_cy

# Python 버전 (GIL 있음)
start = time.time()
parallel_py.run_python()
t_python = time.time() - start

# Cython 버전 (GIL 없음, 진짜 병렬)
start = time.time()
parallel_cy.run_cython()
t_cython = time.time() - start

print(f"\nPython (GIL): {t_python:.3f} sec")
print(f"Cython (nogil, prange): {t_cython:.3f} sec")
