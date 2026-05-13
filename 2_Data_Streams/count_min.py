import random
import math


class CountMinStructure:

    def __init__(self, epsilon, delta):
        # Calculate the grid dimensions based on mathematical bounds
        # w (width/columns) - error limit
        # d (depth/rows) - probability of success
        self.w = math.ceil(math.e / epsilon)
        self.d = math.ceil(math.log(1 / delta))

        # Create the actual grid (a 2D list of zeros)
        self.table = [[0] * self.w for _ in range(self.d)]

        # Prime number p = 1048583 - the smallest prime larger than 2^20
        self.p = 1048583

        # Vector size = 5 (2^20)^5 = 2^100
        self.t = 5

        # Create hash functions for each row
        self.alpha_vectors = []
        for _ in range(self.d):
            alphas = [random.randint(0, self.p - 1) for _ in range(self.t)]
            self.alpha_vectors.append(alphas)

    def _get_base_p_vector(self, s):
        # Convert the binary string into a normal integer
        num = int(s, 2)
        z_vector = []

        # Divide by p to find the base-p digits
        while num > 0:
            z_vector.append(num % self.p)
            num = num // self.p

        # If the number didn't fill 5 chunks, add zeros at the end
        while len(z_vector) < self.t:
            z_vector.append(0)

        return z_vector

    def _hash(self, z_vector, row):
        # Get the unique random multipliers (alphas) for this row
        alphas = self.alpha_vectors[row]

        # Multiply each chunk by its corresponding alpha, and sum them
        dot_product = sum(a * z for a, z in zip(alphas, z_vector))

        # Apply Vec_p rule
        return (dot_product % self.p) % self.w

    def update(self, s, c):
        # Slice the stream into 5 chunks
        z_vector = self._get_base_p_vector(s)

        for i in range(self.d):
            col = self._hash(z_vector, i)
            self.table[i][col] += c

    def estimate(self, s):
        # Slice the string into 5 chunks
        z_vector = self._get_base_p_vector(s)

        min_est = float('inf')
        for i in range(self.d):
            col = self._hash(z_vector, i)
            # Keep the smallest value
            min_est = min(min_est, self.table[i][col])

        return min_est
