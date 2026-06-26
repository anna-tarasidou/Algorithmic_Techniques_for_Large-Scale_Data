from sparse_recovery import *

# Stream and mechanism parameters
N = 1000000  # Vector size
TOTAL_UPDATES = 10000000
P = 2000003  # Prime number > 2N
T_ITERATIONS = 1  # T=30 guarantees 99% theoretical certainty


def run_stream():
    recovery = OneSparseRecovery(N, P, T_ITERATIONS)

    # Data structures for fast ground truth tracking
    true_vector = [0] * (N + 1)
    non_zero_indices = set()

    phase = 'A'
    errors = 0
    negative_ab_queries = 0

    for command_num in range(1, TOTAL_UPDATES + 1):
        # Command Generation
        if phase == 'A':
            c = random.choice([x for x in range(-100, 101) if x != 0])
            i = random.randint(1, N)

            # 1% chance to switch to Phase B
            if len(non_zero_indices) > 0 and random.random() < 0.01:
                phase = 'B'
        else:
            # Phase B: Fast selection using set to avoid O(N) scans
            i = random.sample(list(non_zero_indices), 1)[0]
            c = -true_vector[i]

        # Apply Command to Ground Truth
        true_vector[i] += c

        if true_vector[i] == 0:
            non_zero_indices.discard(i)
        else:
            non_zero_indices.add(i)

        # Switch back to Phase A if vector becomes completely empty
        if phase == 'B' and len(non_zero_indices) == 0:
            phase = 'A'

        # Update Sketch Mechanism
        recovery.update(i, c)

        # Query & Verification
        is_sparse, predicted_index, rejected_by_ab = recovery.query()

        if rejected_by_ab:
            negative_ab_queries += 1

        true_is_sparse = (len(non_zero_indices) == 1)
        true_index = next(iter(non_zero_indices)) if true_is_sparse else -1

        # Log false positives, false negatives, or wrong index predictions
        if is_sparse != true_is_sparse:
            errors += 1
        elif is_sparse and true_is_sparse and predicted_index != true_index:
            errors += 1

        # Print output periodically (e.g., every 100,000 commands)
        if command_num % 100000 == 0 or command_num == TOTAL_UPDATES:
            print(f"{command_num} {errors} {negative_ab_queries}")


run_stream()
