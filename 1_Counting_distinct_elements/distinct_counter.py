import random


class BinaryTrie:
    def __init__(self, max_bits):
        self.root = {}
        self.distinct_count = 0
        self.max_bits = max_bits

    def insert(self, num):
        node = self.root
        is_new = False

        # Traverse the bits from most significant to the least significant
        for i in range(self.max_bits - 1, -1, -1):
            # Extract the i-th bit (0 or 1)
            bit = (num >> i) & 1

            # If the bit path doesn't exist, create it
            if bit not in node:
                node[bit] = {}
                is_new = True  # We created at least one new branch, so it's a new element

            # Move to the child node
            node = node[bit]

        # If it's a new distinct element, increment our exact counter
        if is_new:
            self.distinct_count += 1

        return is_new


def count_trailing_zeroes(n, max_bits):
    # Edge case: If n is 0, in a d-bit system, it has d trailing zeroes.
    if n == 0:
        return max_bits

    count = 0
    # Check if the least significant bit is 0
    while (n & 1) == 0:
        count += 1
        n >>= 1  # Shift right by 1 bit

    return count


def exercise_1a():
    d = 20
    max_value = (1 << d) - 1  # 2^20 - 1
    total_elements = 1000000

    R = 0
    trie = BinaryTrie(max_bits=d)

    print("[Elements Produced] | [True Distinct] | [Estimated Distinct]")

    for i in range(1, total_elements + 1):
        x = random.randint(0, max_value)

        # Insert to get the true distinct count
        trie.insert(x)

        # The hash function is h(x) = x for part (a)
        h_x = x

        # Find trailing zeroes and update R
        r = count_trailing_zeroes(h_x, d)
        if r >= R:
            R = r

        if i % 100000 == 0 or i == 1:
            estimated_distinct = 1 << R
            print(f"{i:7d} | {trie.distinct_count:7d} | {estimated_distinct:7d}")


def generate_x():
    num = 0

    # Bits 1 to 5: 1 with probability 1/2
    for _ in range(5):
        num = (num << 1) | (1 if random.random() < 1 / 2 else 0)

    # Bits 6 to 10: 1 with probability 1/4
    for _ in range(5):
        num = (num << 1) | (1 if random.random() < 1 / 4 else 0)

    # Bits 11 to 15: 1 with probability 1/8
    for _ in range(5):
        num = (num << 1) | (1 if random.random() < 1 / 8 else 0)

    # Bits 16 to 20: 1 with probability 1/16
    for _ in range(5):
        num = (num << 1) | (1 if random.random() < 1 / 16 else 0)

    return num


def exercise_1b():
    d = 20
    total_elements = 1000000
    p = 1048583  # Smallest prime > 2^20

    # Randomly select alpha in [1, p-1] and beta in [0, p-1]
    alpha = random.randint(1, p - 1)
    beta = random.randint(0, p - 1)

    # Initialize estimators
    R_no_hash = 0
    R_with_hash = 0

    trie = BinaryTrie(max_bits=d)

    print(f"Hash parameters: p={p}, alpha={alpha}, beta={beta}")
    print("Format: [Elements] | [True Distinct] | [Est. no Hash] | [Est. with Hash]")

    for i in range(1, total_elements + 1):
        # Generate χ number
        x = generate_x()

        # Insert to Trie
        trie.insert(x)

        # No Hash (h(x) = x)
        r_no_hash = count_trailing_zeroes(x, d)
        if r_no_hash >= R_no_hash:
            R_no_hash = r_no_hash

        # With Hash
        h_x = ((alpha * x + beta) % p) % (1 << d)

        r_with_hash = count_trailing_zeroes(h_x, d)
        if r_with_hash >= R_with_hash:
            R_with_hash = r_with_hash

        if i % 100000 == 0 or i == 1:
            est_no_hash = 1 << R_no_hash
            est_with_hash = 1 << R_with_hash
            print(f"{i:10d} | {trie.distinct_count:15d} | {est_no_hash:14d} | {est_with_hash:16d}")
