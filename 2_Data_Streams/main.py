from count_min import *


def main():
    # Total sum of 10,090
    # Error less than 90, epsilon = 0.008
    # 99% guarantee of success, delta = 0.01.
    epsilon = 0.008
    delta = 0.01

    # Create the CountMin grid
    cms = CountMinStructure(epsilon, delta)
    print(f"CountMin initialized with Depth (rows) = {cms.d} and Width (cols) = {cms.w}")
    print(f"Total cells used: {cms.d * cms.w}")

    # Variables to track the Heavy Hitter
    max_string = None
    max_estimate = -1

    ''' 
    strings = [format(random.getrandbits(100), '0100b') for _ in range(1000)]

    # First 999 strings - each gets a count of 10
    for i in range(999):
        s = strings[i]
        cms.update(s, 10)

        # Check estimated count - remember if it's the highest
        est = cms.estimate(s)
        if est > max_estimate:
            max_estimate = est
            max_string = s

    # Final string - count of 100
    target_heavy_hitter = strings[999]
    cms.update(target_heavy_hitter, 100)

    # Check if 100-count string beats previous highest record
    est = cms.estimate(target_heavy_hitter)
    if est > max_estimate:
        max_estimate = est
        max_string = target_heavy_hitter
    '''

    target_heavy_hitter = format(random.getrandbits(100), '0100b')

    for i in range(1000):
        if i < 999:
            # Generate random 100-bit string
            s = format(random.getrandbits(100), '0100b')
            count = 10
        else:
            # Inject the special heavy hitter at the end
            s = target_heavy_hitter
            count = 100

        cms.update(s, count)
        est = cms.estimate(s)

        if est > max_estimate:
            max_estimate = est
            max_string = s

    print(f"Target Heavy Hitter (Real): {target_heavy_hitter}")
    print(f"Algorithm Reported Hitter : {max_string}")

    if target_heavy_hitter == max_string:
        print("\nSuccess! The CountMinStructure found the heavy hitter.")
        print(f"Estimated count: {max_estimate} (Real was 100)")
    else:
        print("\nFailed!")


main()
