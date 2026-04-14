import random
import statistics

import matplotlib.pyplot as plt


class MorrisCounter:
    def __init__(self, alpha=2.0):
        # Initialize variable C to 0
        self.c = 0
        self.alpha = alpha

    def insert(self):
        # Calculate probability of incrementing C: 1 / ( alpha^C )
        probability = 1.0 / (self.alpha ** self.c)

        # Generate a random float number in [0.0, 0.1)
        if random.random() < probability:
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
    plt.plot(range(1, n_insertions + 1), mean_estimations, label='Mean (Μέσος Όρος)', color='red',
             linewidth=1.5, alpha=0.8)
    plt.plot(range(1, n_insertions + 1), median_estimations, label='Median (Διάμεσος)', color='green',
             linewidth=1.5, alpha=0.9)
    plt.plot(range(1, n_insertions + 1), range(1, n_insertions + 1), label='True Value', color='blue', linewidth=2)

    plt.xlabel('n')
    plt.ylabel('Counter Value')
    plt.title('Morris Counter: Mean vs Median of 5 Counters (alpha=2)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
