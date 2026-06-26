import random
import math

ARRAY_SIZE = 10 ** 100


def get_B_value(i):
    if i % 100 == 20:
        return 0
    return (i // 100) + 1


def get_C_value(i):
    if i % 100 == 20:
        return i // 100
    return (i // 100) + 1


def get_D_value(i, p, test_seed):
    if i % 100 == 20:
        rng = random.Random(f"{test_seed}_{i}")
        if rng.random() < p:
            return i // 100
        else:
            return (i // 100) + 1

    return (i // 100) + 1


def binary_search_tester(array_name, epsilon, p=None, test_seed=None):
    if epsilon <= 0:
        return False

    iterations_needed = math.ceil(math.log(1 - 0.75) / math.log(1 - epsilon))

    for _ in range(iterations_needed):
        x = random.randint(1, ARRAY_SIZE)

        if array_name == 'B':
            target_value = get_B_value(x)
        elif array_name == 'C':
            target_value = get_C_value(x)
        elif array_name == 'D':
            target_value = get_D_value(x, p, test_seed)
        else:
            raise ValueError("Invalid array name")

        low = 1
        high = ARRAY_SIZE

        while low <= high:
            mid = (low + high) // 2

            if array_name == 'B':
                mid_value = get_B_value(mid)
            elif array_name == 'C':
                mid_value = get_C_value(mid)
            elif array_name == 'D':
                mid_value = get_D_value(mid, p, test_seed)
            else:
                raise ValueError("Invalid array name")

            if mid < x:
                if mid_value > target_value:
                    return True
                low = mid + 1
            elif mid > x:
                if mid_value < target_value:
                    return True
                high = mid - 1
            else:
                break

    return False


def run_experiments():
    print("--- Testing Efficient Algorithm (Binary Search) ---")

    success_B = sum(1 for _ in range(100) if binary_search_tester('B', 0.01))
    print(f"Array B | Runs: 100 | Success Rate: {(success_B / 100) * 100:.2f}%")

    success_C = sum(1 for _ in range(100) if binary_search_tester('C', 0.01))
    print(f"Array C | Runs: 100 | Success Rate: {(success_C / 100) * 100:.2f}%")

    print("\n--- Testing Stochastic Array D ---")
    p_values = [0.5, 0.25, 0.10, 0.01, 0.001]

    for p in p_values:
        eps_D = p / 100.0

        if p == 0.01:
            runs = 20
        elif p == 0.001:
            runs = 5
        else:
            runs = 100

        success_D = sum(1 for seed in range(runs) if binary_search_tester('D', eps_D, p, seed))
        print(
            f"Array D (p={p:<5}) | eps = {eps_D:<7} | Runs: {runs:<3} | Success Rate: {(success_D / runs) * 100:.2f}%")


run_experiments()
