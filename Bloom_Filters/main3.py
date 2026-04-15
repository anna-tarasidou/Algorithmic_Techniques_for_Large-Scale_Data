from Bloom_Filters.bloom_filters import *


def main():
    for k in [1, 2, 3, 5, 10]:
        for r in [1, 2, 3, 4, 5]:
            count, _ = exercise_1a(k_hash=k, rounds=r)
            print(k, r, count)


main()
