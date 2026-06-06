import random


class NonZeroSampler:
    def __init__(self, N, L=14, T=80, P=1048583):
        self.L = L  # Levels
        self.T = T  # Repetitions per level for 99% overall certainty
        self.P = P  # Prime number > N

        # Hash function parameters for each Level (l) and Repetition (t)
        # h(x) = ((a*x + b) % P) % n_l
        self.a = [[random.randint(1, P - 1) for _ in range(T)] for _ in range(L)]
        self.b = [[random.randint(0, P - 1) for _ in range(T)] for _ in range(L)]
        self.target = [[random.randint(1, 2 ** (l + 2)) for _ in range(T)] for l in range(L)]

        # 1-Sparse Recovery parameters (alpha, beta, gamma)
        self.alpha = [[0] * T for _ in range(L)]
        self.beta = [[0] * T for _ in range(L)]
        self.gamma = [[0] * T for _ in range(L)]

    def update(self, index, value):
        for l in range(self.L):
            n_l = 2 ** (l + 2)
            for t in range(self.T):
                # Calculate hash for this specific bucket
                h_val = ((self.a[l][t] * index + self.b[l][t]) % self.P) % n_l + 1

                # If the item falls into the target bucket, update the 3 counters
                if h_val == self.target[l][t]:
                    self.alpha[l][t] += value
                    self.beta[l][t] += index * value
                    self.gamma[l][t] += (index ** 2) * value

    def query(self):
        # Returns a valid non-zero index, or -1 if it fails to find any isolated element.

        for l in range(self.L):
            for t in range(self.T):
                al = self.alpha[l][t]
                be = self.beta[l][t]
                ga = self.gamma[l][t]

                # Check deterministic 1-sparse conditions for non-negative values
                if al > 0 and be % al == 0:
                    if be ** 2 == al * ga:
                        return be // al  # Found exactly one! Return its index.

        return -1  # Error: Failed to isolate any element
