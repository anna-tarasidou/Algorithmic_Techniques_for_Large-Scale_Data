import random


def random_file():
    return str(''.join(random.choice('01') for _ in range(100)))


def create_hash(a, b, p, N):
    def h(X):
        blocks = [int(X[i:i+20], 2) for i in range(0, 100, 20)]
        c = 0
        for Bi in blocks:
            c = (a * (Bi + c) + b) % p
        return c % N
    return h


class BloomFilter:
    def __init__(self, N, k):
        self.N = N
        self.bits = [0] * N
        self.hashes = []
        p = 1048583

        for _ in range(k):
            a = random.randint(1, p - 1)
            b = random.randint(0, p - 1)
            self.hashes.append(create_hash(a, b, p, N))

    def add(self, item):
        for h in self.hashes:
            self.bits[h(item)] = 1

    def check(self, item):
        return all(self.bits[h(item)] for h in self.hashes)


def exercise_1a(k_hash=3, rounds=2, dynamic=False):
    # Create files
    common = {random_file() for _ in range(10)}

    A = set(common)
    B = set(common)

    while len(A) < 100000:
        A.add(random_file())

    while len(B) < 100000:
        B.add(random_file())

    current_A = A.copy()
    current_B = B.copy()

    N = 500000

    for r in range(rounds):
        # A -> B
        bf_A = BloomFilter(N, k_hash)
        for x in current_A:
            bf_A.add(x)

        passed_B = {x for x in current_B if bf_A.check(x)}

        if r == rounds - 1:
            count = len(passed_B)
            correct = common.issubset(passed_B)

            print("count:", count)
            print("contains all common:", correct)
            return count, correct

        # B -> A
        if dynamic:
            N = max(1, 5 * len(passed_B))

        bf_B = BloomFilter(N, k_hash)
        for x in passed_B:
            bf_B.add(x)

        passed_A = {x for x in current_A if bf_B.check(x)}

        if dynamic:
            N = max(1, 5 * len(passed_A))

        current_A = passed_A
        current_B = passed_B
