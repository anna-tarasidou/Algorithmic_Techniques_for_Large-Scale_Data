from monotonicity import *


def main():
    # Test the algorithm for various sample sizes N
    test_Ns = [100, 1000, 10000, 100000]

    print("--- Testing Natural Algorithm ---")
    for n in test_Ns:
        found_violation = natural_algorithm(n)
        if found_violation:
            print(f"Test with N = {n:<7}: Non-monotonicity revealed!")
        else:
            print(f"Test with N = {n:<7}: Failed to find violation (expected)")

    # Test the Binary Search Algorithm
    print("\n--- Running Monte Carlo Simulation for Binary Search Tester ---")
    iterations = 10000
    prob, exp_queries = monte_carlo_simulation(iterations)

    print(f"Estimated Probability of finding non-monotonicity: {prob * 100:.2f}%")
    print(f"Expected number of queries per run: {exp_queries:.2f}")

    SAMPLE_SIZE = 1_000_000
    print(f"--- Theoretical vs Empirical Distances (Sample = {SAMPLE_SIZE}) ---\n")

    # 1. Array B
    dist_B = empirical_distance(get_B_value, SAMPLE_SIZE)
    print(f"Array B - Theoretical Distance: 0.01000 (1/100)")
    print(f"Array B - Empirical Distance  : {dist_B:.5f}\n")

    # 2. Array C
    dist_C = empirical_distance(get_C_value, SAMPLE_SIZE)
    print(f"Array C - Theoretical Distance: 0.01000 (1/100)")
    print(f"Array C - Empirical Distance  : {dist_C:.5f}\n")

    # 3. Array D (Testing different values of p)
    test_ps = [0.0, 0.25, 0.5, 0.75, 1.0]
    for p in test_ps:
        dist_D = empirical_distance(get_D_value, SAMPLE_SIZE, p=p)
        theoretical_D = p / 100
        print(f"Array D (p={p:<4}) - Theoretical Distance: {theoretical_D:.5f} ({p}/100)")
        print(f"Array D (p={p:<4}) - Empirical Distance  : {dist_D:.5f}")
        print("-" * 65)


main()
