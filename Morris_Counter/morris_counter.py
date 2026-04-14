import random
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
