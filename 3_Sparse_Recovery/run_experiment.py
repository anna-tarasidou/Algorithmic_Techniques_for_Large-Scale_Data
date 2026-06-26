import random
from nonzero_sampler import NonZeroSampler

N = 10000
P = 1048583


def run_experiment_1():
    print("--- Starting Experiment 1 (Random Deletion) ---")
    sampler = NonZeroSampler(N=N, L=14, T=80, P=P)

    # Generate true vector (75% ones, 25% zeros)
    true_vector = [1 if random.random() < 0.75 else 0 for _ in range(N)]
    non_zeros = []

    # Populate the sampler
    for i, val in enumerate(true_vector):
        if val == 1:
            sampler.update(i + 1, 1)  # 1-based indexing
            non_zeros.append(i + 1)

    total_queries = len(non_zeros)
    error_occurred = False

    # Query and delete randomly
    while non_zeros:
        res = sampler.query()
        if res == -1:
            print("error")
            error_occurred = True
            break

        # Delete a uniformly random element from the ground truth
        idx_to_remove = random.choice(non_zeros)
        sampler.update(idx_to_remove, -1)
        non_zeros.remove(idx_to_remove)

    if not error_occurred:
        print(f"Success! Answered {total_queries} queries correctly.")


def run_experiment_2():
    print("\n--- Starting Experiment 2 (Adversarial Deletion) ---")
    sampler = NonZeroSampler(N=N, L=14, T=80, P=P)

    true_vector = [1 if random.random() < 0.75 else 0 for _ in range(N)]
    non_zeros = []

    for i, val in enumerate(true_vector):
        if val == 1:
            sampler.update(i + 1, 1)
            non_zeros.append(i + 1)

    error_occurred = False

    # Query and delete the exact element returned
    while non_zeros:
        res = sampler.query()
        if res == -1:
            print("error")
            error_occurred = True
            break

        # We delete exactly what the sampler found
        idx_to_remove = res
        sampler.update(idx_to_remove, -1)
        non_zeros.remove(idx_to_remove)

    if not error_occurred:
        print("Success!")


run_experiment_1()
run_experiment_2()
