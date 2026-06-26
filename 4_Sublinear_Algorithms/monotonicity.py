import random

# The size of the array (10^100)
ARRAY_SIZE = 10 ** 100


def get_A_value(i):
    # Returns the value A[i] of the virtual array
    if i % 2 != 0:
        return i + 1
    else:
        return i - 1


# Implements the natural sampling algorithm.
def natural_algorithm(N):
    # 1. Sample N random numbers between 1 and 10^100
    indices = [random.randint(1, ARRAY_SIZE) for _ in range(N)]

    # 2. Sort the sampled indices in ascending order
    indices.sort()

    # 3. & 4. Check the inequality A[i_k] <= A[i_{k+1}]
    for k in range(N - 1):
        if get_A_value(indices[k]) > get_A_value(indices[k + 1]):
            # The array is not monotonically increasing.
            return True

            # Sorted based on the sample
    return False


def binary_search_tester():
    # 1. Pick a random index x and query its value
    x = random.randint(1, ARRAY_SIZE)
    target_value = get_A_value(x)

    # 1 query made for get_A_value(x)
    queries = 1

    # 2. Perform binary search for target_value
    low = 1
    high = ARRAY_SIZE

    while low <= high:
        mid = (low + high) // 2
        mid_value = get_A_value(mid)
        queries += 1

        # 3. Check for monotonicity violation
        if mid < x and mid_value > target_value:
            return True, queries
        if mid > x and mid_value < target_value:
            return True, queries

        # 4. Standard binary search routing
        if target_value < mid_value:
            high = mid - 1
        elif target_value > mid_value:
            low = mid + 1
        else:
            break

    # No violation found in this run
    return False, queries


def monte_carlo_simulation(iterations=10000):
    # Estimates success probability and expected queries
    success_count = 0
    total_queries = 0

    for _ in range(iterations):
        found_violation, queries = binary_search_tester()
        total_queries += queries
        if found_violation:
            success_count += 1

    probability = success_count / iterations
    expected_queries = total_queries / iterations

    return probability, expected_queries


def get_B_value(i):
    # Array B: B[i] = 0 if i mod 100 == 20, else floor(i/100) + 1

    if i % 100 == 20:
        return 0
    else:
        return (i // 100) + 1


def get_C_value(i):
    # Array C: C[i] = floor(i/100) if i mod 100 == 20, else floor(i/100) + 1

    if i % 100 == 20:
        return i // 100
    else:
        return (i // 100) + 1


def get_D_value(i, p):
    # Array D: Depends on probability parameter p (0 <= p <= 1).

    if i % 100 == 20:
        # Generate a random float between 0.0 and 1.0
        if random.random() < p:
            return i // 100  # Violation occurs with probability p
        else:
            return (i // 100) + 1  # No violation with probability 1-p
    else:
        return (i // 100) + 1


def empirical_distance(oracle_func, sample_size=1000000, p=None):
    # Estimates the distance to monotonicity by checking a continuous sample of elements
    violations = 0

    for i in range(1, sample_size + 1):
        if p is not None:
            val = oracle_func(i, p)
        else:
            val = oracle_func(i)

        # The ideal monotone sequence: is (i // 100) + 1.
        ideal_val = (i // 100) + 1

        if val != ideal_val:
            violations += 1

    # Calculate the fraction of elements that need to be changed
    distance = violations / sample_size
    return distance
