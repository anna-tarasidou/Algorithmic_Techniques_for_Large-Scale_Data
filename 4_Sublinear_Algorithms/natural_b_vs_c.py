import random

ARRAY_SIZE = 10 ** 100


def get_B_value(i):
    if i % 100 == 20:
        return 0
    else:
        return (i // 100) + 1


def get_C_value(i):
    if i % 100 == 20:
        return i // 100
    else:
        return (i // 100) + 1


def natural_algorithm(N, oracle_func):
    indices = [random.randint(1, ARRAY_SIZE) for _ in range(N)]
    indices.sort()

    for k in range(N - 1):
        if oracle_func(indices[k]) > oracle_func(indices[k + 1]):
            return True  # Violation found

    return False


def test_algorithm_performance(N, iterations=1000):
    # Runs the natural algorithm multiple times to find the empirical success probability.

    print(f"Testing Natural Algorithm with N = {N} over {iterations} runs...\n")

    # Test for Array C
    success_C = sum(1 for _ in range(iterations) if natural_algorithm(N, get_C_value))
    prob_C = (success_C / iterations) * 100
    print(f"Array C - Success Probability: {prob_C:.2f}% (Expected: ~0.00%)")

    # Test for Array B
    success_B = sum(1 for _ in range(iterations) if natural_algorithm(N, get_B_value))
    prob_B = (success_B / iterations) * 100
    print(f"Array B - Success Probability: {prob_B:.2f}% (Expected: >= 99.00%)")


# We choose N = 1000 based on our theoretical calculation
N_chosen = 1000
test_algorithm_performance(N_chosen, iterations=1000)
