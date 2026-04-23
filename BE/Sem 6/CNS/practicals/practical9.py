import math
import statistics
import time


BIT_MASK_32 = 0xFFFFFFFF
MAX_32 = 2**32


def init_lcg_state(seed: int) -> int:
    return seed & BIT_MASK_32


def next_lcg_32bit(state: int, a: int = 1664525, c: int = 1013904223, m: int = MAX_32) -> tuple[int, int]:
    # GeeksforGeeks formula:
    # X(n+1) = (a * X(n) + c) mod m
    next_state = (a * state + c) % m
    return next_state, next_state


def init_bbs_state(seed: int, p: int = 383, q: int = 503) -> tuple[int, int]:
    # GeeksforGeeks / standard BBS setup:
    # 1) p % 4 == 3, q % 4 == 3
    # 2) n = p * q
    # 3) gcd(seed, n) == 1
    # 4) x0 = (seed^2) mod n
    n = p * q
    s = seed % n
    if s == 0:
        s = 3
    while math.gcd(s, n) != 1:
        s += 1
    x0 = (s * s) % n
    return x0, n


def next_bbs_32bit(state: tuple[int, int]) -> tuple[tuple[int, int], int]:
    # BBS step: x(n+1) = x(n)^2 mod n
    # Output bit: x(n) mod 2
    x, n = state
    value = 0
    for _ in range(32):
        x = (x * x) % n
        value = (value << 1) | (x & 1)
    return (x, n), value


def generate_samples(initial_state, next_value_fn, count: int) -> list[int]:
    values = []
    state = initial_state
    for _ in range(count):
        state, value = next_value_fn(state)
        values.append(value)
    return values


def uniformity_test(values: list[int], bins: int = 16) -> float:
    if not values:
        return 0.0

    counts = [0] * bins
    for value in values:
        bucket = min((value * bins) // MAX_32, bins - 1)
        counts[bucket] += 1

    expected = len(values) / bins
    chi_square = sum(((observed - expected) ** 2) / expected for observed in counts)

    # Convert to bounded score in [0, 100]: lower chi-square -> higher score.
    return 100.0 / (1.0 + chi_square)


def scalability_test(initial_state, next_value_fn, sizes: list[int]) -> float:
    # Measure average time per generated value at each scale.
    per_item_times = []
    for size in sizes:
        state = initial_state
        start = time.perf_counter()
        for _ in range(size):
            state, _ = next_value_fn(state)
        elapsed = time.perf_counter() - start
        per_item_times.append(elapsed / size)

    # Scalability should reward both:
    # 1) lower per-item generation cost (faster algorithm),
    # 2) stable performance as workload grows.
    mean_time = statistics.fmean(per_item_times)
    if mean_time == 0:
        return 100.0

    spread = statistics.pstdev(per_item_times)
    relative_spread = spread / mean_time

    # Speed score: microsecond-level scaling keeps values readable.
    speed_score = 100.0 / (1.0 + mean_time * 1_000_000.0)
    stability_score = 100.0 / (1.0 + 10.0 * relative_spread)
    return 0.7 * speed_score + 0.3 * stability_score


def consistency_test(initial_state, next_value_fn, sample_count: int, runs: int = 5) -> float:
    # Generate multiple runs and compare run-level means.
    run_means = []
    for _ in range(runs):
        values = generate_samples(initial_state, next_value_fn, sample_count)
        run_means.append(statistics.fmean(values))

    grand_mean = statistics.fmean(run_means)
    if grand_mean == 0:
        return 100.0
    relative_std = statistics.pstdev(run_means) / grand_mean
    return 100.0 / (1.0 + 50.0 * relative_std)


def evaluate_generator(name: str, initial_state, next_value_fn) -> dict:
    uniform_values = generate_samples(initial_state, next_value_fn, 50000)
    uniformity_score = uniformity_test(uniform_values)
    scalability_score = scalability_test(initial_state, next_value_fn, sizes=[1000, 10000, 50000, 100000])
    consistency_score = consistency_test(initial_state, next_value_fn, sample_count=10000, runs=5)

    return {
        "name": name,
        "uniformity_score": uniformity_score,
        "scalability_score": scalability_score,
        "consistency_score": consistency_score,
        "total_score": uniformity_score + scalability_score + consistency_score,
    }


def print_result(result: dict) -> None:
    print(f"\n{result['name']}")
    print("-" * len(result["name"]))
    print(f"Uniformity Score : {result['uniformity_score']:.2f}/100")
    print(f"Scalability Score: {result['scalability_score']:.2f}/100")
    print(f"Consistency Score: {result['consistency_score']:.2f}/100")
    print(f"Total Score      : {result['total_score']:.2f}/300")


def main() -> None:
    print("=== 32-bit Random Number Generation Comparison ===")
    print("\nAlgorithms:")
    print("1) Linear Congruential Generator (LCG)")
    print("   X(n+1) = (aX(n) + c) mod m")
    print("2) Blum Blum Shub (BBS)")
    print("   x(n+1) = x(n)^2 mod n, output bit = x(n) mod 2")

    lcg_seed = 123456789
    bbs_seed = 987654321

    lcg_result = evaluate_generator("LCG", init_lcg_state(lcg_seed), next_lcg_32bit)
    bbs_result = evaluate_generator("Blum Blum Shub", init_bbs_state(bbs_seed), next_bbs_32bit)

    print_result(lcg_result)
    print_result(bbs_result)

    winner = lcg_result if lcg_result["total_score"] >= bbs_result["total_score"] else bbs_result
    print(f"\nBest method (based on these 3 tests): {winner['name']}")

    # Show one sample 32-bit output from each generator.
    _, lcg_sample = next_lcg_32bit(init_lcg_state(lcg_seed))
    _, bbs_sample = next_bbs_32bit(init_bbs_state(bbs_seed))
    print(f"\nExample 32-bit number from LCG: {lcg_sample}")
    print(f"Example 32-bit number from BBS: {bbs_sample}")


if __name__ == "__main__":
    main()
