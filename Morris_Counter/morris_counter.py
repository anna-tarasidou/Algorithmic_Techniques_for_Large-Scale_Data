import random
import statistics
import decimal
from collections import defaultdict

import matplotlib.pyplot as plt


class MorrisCounter:
    def __init__(self, alpha=2.0, c_max=float('inf')):
        # Initialize variable C to 0
        self.c = 0
        self.alpha = alpha
        self.c_max = c_max

    def insert(self):
        # Calculate probability of incrementing C: 1 / ( alpha^C )
        probability = 1.0 / (self.alpha ** self.c)

        # Generate a random float number in [0.0, 0.1)
        if random.random() < probability and self.c < self.c_max:
            self.c += 1

    def query(self):
        # Return the estimated count
        return (1.0 / (self.alpha - 1)) * (self.alpha ** self.c - 1)


def exercise_1a():
    n_insertions = 1000000
    counter = MorrisCounter(alpha=2.0)

    # List to hold the estimations
    estimations = []

    for i in range(1, n_insertions + 1):
        counter.insert()
        current_estimate = counter.query()
        estimations.append(current_estimate)

        # Print to monitor the progress
        if i % 100000 == 0:
            print(f"Insertion {i}: Estimated count = {current_estimate}")

    # Plotting the estimations vs the actual number of insertions
    plt.figure(figsize=(10, 6))

    # Plot the Morris Counter estimation
    plt.plot(range(1, n_insertions + 1), estimations, label='approx counter value', color='orange', linewidth=1.5)

    # Plot the true linear value (y = x) for comparison
    plt.plot(range(1, n_insertions + 1), range(1, n_insertions + 1), label='true value', color='blue', linewidth=1.5)

    plt.xlabel('n')
    plt.ylabel('Counter Value')
    plt.title('Morris Counter Estimation (alpha=2)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def exercise_1b():
    n_insertions = 1000000
    num_counters = 5

    # List with independent Morris Counters
    counters = [MorrisCounter(alpha=2.0) for _ in range(num_counters)]

    # Lists to hold the estimations
    mean_estimations = []
    median_estimations = []

    for i in range(1, n_insertions + 1):
        current_estimates = []

        # Insert element in all counters
        for counter in counters:
            counter.insert()
            current_estimates.append(counter.query())

        # Calculate estimates
        # Mean
        mean_est = sum(current_estimates) / num_counters

        # Median
        median_est = statistics.median(current_estimates)

        mean_estimations.append(mean_est)
        median_estimations.append(median_est)

    plt.figure(figsize=(12, 7))
    # Plot Mean, Median, and True Value
    plt.plot(range(1, n_insertions + 1), mean_estimations, label='Mean (Μέσος Όρος)', color='red', linewidth=1.5,
             alpha=0.8)
    plt.plot(range(1, n_insertions + 1), median_estimations, label='Median (Διάμεσος)', color='green', linewidth=1.5,
             alpha=0.9)
    plt.plot(range(1, n_insertions + 1), range(1, n_insertions + 1), label='True Value', color='blue', linewidth=2)

    plt.xlabel('n')
    plt.ylabel('Counter Value')
    plt.title('Morris Counter: Mean vs Median of 5 Counters (alpha=2)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def exercise_1d():
    n_insertions = 1000000
    c_limit = 255  # 2^8 - 1 bits

    alphas_test = [1.03, 1.045, 1.05, 1.08]

    # Keep the estimations in a dictionary
    all_estimations = {alpha: [] for alpha in alphas_test}

    for alpha in alphas_test:
        # Create the counter
        counter = MorrisCounter(alpha=alpha, c_max=c_limit)

        for _ in range(1, n_insertions + 1):
            counter.insert()
            all_estimations[alpha].append(counter.query())

    plt.figure(figsize=(12, 7))
    colors = ['red', 'purple', 'orange', 'green']

    for (alpha, estimations), color in zip(all_estimations.items(), colors):
        plt.plot(range(1, n_insertions + 1), estimations, label=f'alpha = {alpha}', color=color, linewidth=1.5)

    plt.plot(range(1, n_insertions + 1), range(1, n_insertions + 1), label='True Value', color='blue', linewidth=2)

    plt.xlabel('n (Insertions)')
    plt.ylabel('Counter Estimation')
    plt.title('Morris Counter with 8-bit limit (C max = 255)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def exercise_1e():
    n_insertions = 1000000
    mc_runs = 100

    target_min = 800000
    target_max = 1200000

    alg1_successes = 0
    alg2_successes = 0

    # Lists to store the success frequency
    alg1_freq_history = []
    alg2_freq_history = []

    alpha2 = 1.55

    for run in range(1, mc_runs + 1):

        # Algorithm 1: Single counter, alpha=2.0
        counter1 = MorrisCounter(alpha=2.0)
        for _ in range(n_insertions):
            counter1.insert()

        est1 = counter1.query()
        if target_min <= est1 <= target_max:
            alg1_successes += 1

        # Algorithm 2: Three counters, alpha=1.55, C max = 31
        c2_1 = MorrisCounter(alpha=alpha2, c_max=31)
        c2_2 = MorrisCounter(alpha=alpha2, c_max=31)
        c2_3 = MorrisCounter(alpha=alpha2, c_max=31)

        for _ in range(n_insertions):
            c2_1.insert()
            c2_2.insert()
            c2_3.insert()

        # Calculate the mean of the three counters
        est2 = (c2_1.query() + c2_2.query() + c2_3.query()) / 3.0

        if target_min <= est2 <= target_max:
            alg2_successes += 1

        # Calculate current frequency of success and append to history
        alg1_freq_history.append(alg1_successes / run)
        alg2_freq_history.append(alg2_successes / run)

    # Calculate final success probabilities
    prob1 = (alg1_successes / mc_runs) * 100
    prob2 = (alg2_successes / mc_runs) * 100

    print("MONTE CARLO RESULTS")
    print(f"Algorithm 1 (1 counter, a=2.0): Success = {prob1:.1f}%")
    print(f"Algorithm 2 (3 counters, a={alpha2}): Success = {prob2:.1f}%")

    plt.figure(figsize=(10, 6))
    # Plot Alg 1 (Red line, matching the professor's example)
    plt.plot(range(1, mc_runs + 1), alg1_freq_history, label='Alg 1: frequency of success', color='red', linewidth=1.5)

    # Plot Alg 2 (Blue line for comparison)
    plt.plot(range(1, mc_runs + 1), alg2_freq_history, label='Alg 2: frequency of success', color='blue', linewidth=1.5)

    plt.xlabel('number of experiments')
    plt.ylabel('frequency of success')
    plt.title('Frequency of Success over Number of Experiments')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def exercise_2a():
    decimal.getcontext().prec = 100

    n_insertions = 1000
    c_values = [2, 3, 4, 5]

    P = defaultdict(decimal.Decimal)
    P[0] = decimal.Decimal('1')

    # Dictionary to store the history of probabilities
    history = {c: [] for c in c_values}

    min_probs = {c: (decimal.Decimal('2'), -1) for c in c_values}

    for n in range(1, n_insertions + 1):
        # Dictionary to store probabilities for the next step
        new_P = defaultdict(decimal.Decimal)

        for C, prob in P.items():
            if prob == 0:
                continue

            p_up = decimal.Decimal('1') / (decimal.Decimal('2') ** C)
            p_stay = decimal.Decimal('1') - p_up

            # Counter stays at C
            new_P[C] += prob * p_stay
            # Counter goes up to C+1
            new_P[C + 1] += prob * p_up

        P = new_P

        # Check success probability for each target c
        for c in c_values:
            prob_success = decimal.Decimal('0')
            lower_bound = n / c
            upper_bound = c * n

            # Sum the probabilities
            for C, prob in P.items():
                estimation = (2 ** C) - 1
                if lower_bound <= estimation <= upper_bound:
                    prob_success += prob

            history[c].append(float(prob_success))

            # Track the minimum probability found so far
            if prob_success < min_probs[c][0]:
                min_probs[c] = (prob_success, n)

        if n % 250 == 0:
            print(f"Processed {n}/1000 insertions...")

    print("EXACT PROBABILITY RESULTS")

    for c in c_values:
        min_prob, min_n = min_probs[c]
        print(f"c={c}: Minimum Probability = {min_prob:.10f} at n = {min_n}")

    plt.figure(figsize=(12, 7))
    colors = {2: 'red', 3: 'purple', 4: 'orange', 5: 'green'}

    for c in c_values:
        plt.plot(range(1, n_insertions + 1), history[c], label=f'c = {c}', color=colors[c], linewidth=1.5)

    plt.xlabel('n (Insertions)')
    plt.ylabel('Exact Probability of Success')
    plt.title('Morris Counter (alpha=2): Exact Success Probability bounds [n/c, cn]')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def exercise_2b():
    decimal.getcontext().prec = 100

    n_insertions = 1000
    c_values = [2, 3, 4, 5]

    state_probs = {c: defaultdict(decimal.Decimal) for c in c_values}

    for c in c_values:
        state_probs[c][0] = decimal.Decimal('1')

    for n in range(1, n_insertions + 1):
        for c in c_values:
            new_P = defaultdict(decimal.Decimal)
            lower_bound = n / c
            upper_bound = c * n

            # Calculate transitions for surviving paths
            for C, prob in state_probs[c].items():
                if prob == 0:
                    continue

                p_up = decimal.Decimal('1') / (decimal.Decimal('2') ** C)
                p_stay = decimal.Decimal('1') - p_up

                new_P[C] += prob * p_stay
                new_P[C + 1] += prob * p_up

            # Kill paths that went out of bounds at this step
            pruned_P = defaultdict(decimal.Decimal)
            for C, prob in new_P.items():
                estimation = (2 ** C) - 1
                if lower_bound <= estimation <= upper_bound:
                    pruned_P[C] = prob

            # Update the state distribution for the next step
            state_probs[c] = pruned_P

        if n % 250 == 0:
            print(f"Processed {n}/1000 insertions...")

    print("EXACT PROBABILITY RESULTS (SURVIVED ALL 1000 STEPS) ")
    for c in c_values:
        # The total success probability is the sum of probabilities of all surviving paths
        total_prob = sum(state_probs[c].values())
        print(f"c={c}: Strict Success Probability = {total_prob:.10f}")
