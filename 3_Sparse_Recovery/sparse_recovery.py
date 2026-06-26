import random


class OneSparseRecovery:
    def __init__(self, n, p, t):
        # Initialize vector size, prime number, and iterations
        self.n = n
        self.p = p
        self.t = t
        self.a = 0
        self.b = 0

        # Randomly select T bases (r) from 1 to p-1
        self.r = [random.randint(1, self.p - 1) for _ in range(self.t)]
        self.R = [0] * self.t

    def update(self, index, value):
        # Update sum (a) and weighted sum (b)
        self.a += value
        self.b += index * value

        # Fast modular exponentiation using built-in pow() for T fingerprints
        for k in range(self.t):
            term = (value * pow(self.r[k], index, self.p)) % self.p
            self.R[k] = (self.R[k] + term) % self.p

    def query(self):
        # Returns: (is_1_sparse, candidate_index, rejected_by_ab_only)

        # Quick rejection using purely a and b
        if self.a == 0:
            return False, -1, True

        if self.b % self.a != 0:
            return False, -1, True

        candidate_index = self.b // self.a
        if candidate_index < 1 or candidate_index > self.n:
            return False, -1, True

        # Probabilistic verification using T fingerprints
        for k in range(self.t):
            expected_R = (self.a * pow(self.r[k], candidate_index, self.p)) % self.p
            if self.R[k] != expected_R:
                return False, -1, False  # Rejected by R verification, not a/b

        return True, candidate_index, False
