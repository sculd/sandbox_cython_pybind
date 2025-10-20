import cProfile
import pstats
from pstats import SortKey

import parallel_py
import parallel_cy
import parallel_nb
import parallel_np


def main():
    parallel_py.run_python()
    parallel_cy.run_prange()
    parallel_cy.run_parallel_np_zeroes()
    parallel_cy.run_parallel_malloc()
    parallel_nb.run_prange()
    parallel_nb.run_prange_private()
    parallel_nb.run_vectorize()
    parallel_nb.run_guvectorize()
    parallel_nb.run_manual_threading()
    parallel_np.run_numpy_threading()
    parallel_np.run_numpy_threadpool()
    parallel_np.run_python_loop_threading()


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    # Save profile data for snakeviz
    profile_file = "main_parallel.prof"
    profiler.dump_stats(profile_file)
    print(f"\nProfile data saved to: {profile_file}")
    print(f"To visualize, run: snakeviz {profile_file}")

    print("\n" + "="*80)
    print("PROFILING RESULTS")
    print("="*80)

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(SortKey.CUMULATIVE)
