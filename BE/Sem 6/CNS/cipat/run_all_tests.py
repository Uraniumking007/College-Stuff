"""
Run all tests sequentially with clear section breaks.
Usage:  python run_all_tests.py          # run all
        python run_all_tests.py 1 3 5    # run specific tests
"""

import sys
import os
import time
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS = {
    1: ("Correctness Verification", "tests/test_correctness.py"),
    2: ("Speed Benchmark", "tests/test_speed.py"),
    3: ("Memory Usage", "tests/test_memory.py"),
    4: ("Hybrid RSA+AES vs Pure RSA", "tests/test_hybrid.py"),
    5: ("Key Size Scaling", "tests/test_keysize.py"),
    6: ("Concurrency & Throughput", "tests/test_concurrency.py"),
}

SEP = "=" * 70


def main():
    args = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else list(TESTS.keys())

    print(SEP)
    print("RSA PERFORMANCE EVALUATION — ALL TESTS")
    print(f"Running tests: {args}")
    print(SEP)

    total_start = time.perf_counter()
    results = {}

    for test_id in args:
        if test_id not in TESTS:
            print(f"\n  Unknown test ID: {test_id}")
            continue

        name, script = TESTS[test_id]
        script_path = os.path.join(SCRIPT_DIR, script)
        print(f"\n{'#' * 70}")
        print(f"### TEST {test_id}: {name}")
        print(f"{'#' * 70}\n")

        t0 = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, script_path],
            cwd=SCRIPT_DIR,
            env={**os.environ, "PYTHONPATH": SCRIPT_DIR},
        )
        elapsed = time.perf_counter() - t0
        results[test_id] = {"name": name, "exit_code": proc.returncode, "time_s": elapsed}
        print(f"\n  → Test {test_id} finished in {elapsed:.1f}s (exit: {proc.returncode})")

    total_time = time.perf_counter() - total_start

    print(f"\n{SEP}")
    print("SUMMARY")
    print(SEP)
    print(f"  {'Test':>5s}  {'Name':30s}  {'Time':>8s}  {'Status':>8s}")
    print(f"  {'─'*5}  {'─'*30}  {'─'*8}  {'─'*8}")
    for tid, r in results.items():
        status = "PASS" if r["exit_code"] == 0 else "FAIL"
        print(f"  {tid:>5d}  {r['name']:30s}  {r['time_s']:>7.1f}s  {status:>8s}")
    print(f"\n  Total time: {total_time:.1f}s")
    print(SEP)


if __name__ == "__main__":
    main()
