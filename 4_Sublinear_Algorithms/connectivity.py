import math
import random
import time
import matplotlib.pyplot as plt
from collections import deque

# Constants as defined in the exercise
N = 100000
DELTA = 10
STEPS = 250000


def add_edge(graph, u, v):
    graph[u].add(v)
    graph[v].add(u)


def remove_edge(graph, u, v):
    graph[u].remove(v)
    graph[v].remove(u)


def simple_sublinear_connectivity_test(graph, epsilon):
    # Number of samples N = ceil(16 / (epsilon * Delta))
    s_samples = math.ceil(16.0 / (epsilon * DELTA))

    # Budget B = ceil(8 / (epsilon * Delta))
    B = math.ceil(8.0 / (epsilon * DELTA))

    for _ in range(s_samples):
        start_node = random.randint(0, N - 1)

        # Standard BFS
        visited = {start_node}
        queue = deque([start_node])

        while queue and len(visited) <= B:
            curr = queue.popleft()
            for neighbor in graph[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

                    # Stop early
                    if len(visited) > B:
                        break
            if len(visited) > B:
                break

        # If queue is empty and we explored <= B nodes, we found a small, isolated component
        if len(visited) <= B:
            return False  # Disconnected

    # If all sampled components are larger than B, we assume it's connected
    return True


def refined_sublinear_connectivity_test(graph, epsilon):
    # L = ceil(log2( 8 / (epsilon * Delta) + 1 ))
    val = 8.0 / (epsilon * DELTA) + 1
    L = math.ceil(math.log2(val))
    if L <= 0:
        L = 1

    # For each level t from 1 to L
    for t in range(1, L + 1):
        # Budget B_t = 2^t - 1
        B_t = (2 ** t) - 1
        if B_t <= 0:
            B_t = 1

        # Sample size N_t = ceil( 32*L / (2^t * epsilon * Delta) )
        N_t = math.ceil((32.0 * L) / ((2 ** t) * epsilon * DELTA))

        # Sample N_t nodes
        for _ in range(N_t):
            start_node = random.randint(0, N - 1)

            # Local BFS to find at least B_t + 1 nodes
            visited = {start_node}
            queue = deque([start_node])

            while queue and len(visited) <= B_t:
                curr = queue.popleft()
                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

                        # If we found B_t + 1 nodes, stop early
                        if len(visited) > B_t:
                            break
                if len(visited) > B_t:
                    break

            if len(visited) <= B_t:
                return False  # Non-connectivity
    # If all levels pass without returning False, we assume it is connected
    return True


def run_simulation():
    graph = [set() for _ in range(N)]

    steps_list = []
    simple_calls_list = []
    refined_calls_list = []

    start_time_total = time.time()

    # Track accumulated time for comparison
    total_time_simple = 0
    total_time_refined = 0

    for step in range(1, STEPS + 1):
        # --- 1. Graph Modification Phase ---
        if random.random() < 0.10:
            v = random.randint(0, N - 1)
            if len(graph[v]) > 0:
                u = random.choice(tuple(graph[v]))
                remove_edge(graph, u, v)
            else:
                while True:
                    u = random.randint(0, N - 1)
                    if u != v and len(graph[u]) < DELTA and u not in graph[v]:
                        break
                add_edge(graph, u, v)
        else:
            while True:
                v = random.randint(0, N - 1)
                if len(graph[v]) < DELTA:
                    break
            while True:
                u = random.randint(0, N - 1)
                if u != v and len(graph[u]) < DELTA and u not in graph[v]:
                    break
            add_edge(graph, u, v)

        # --- 2a. Simple Algorithm ---
        t_start_simp = time.time()
        epsilon_s = 1.0 / DELTA
        calls_s = 0
        while True:
            calls_s += 1
            if int(2 / (epsilon_s * DELTA)) >= N:
                break
            if not simple_sublinear_connectivity_test(graph, epsilon_s):
                break
            epsilon_s /= 2.0
        total_time_simple += (time.time() - t_start_simp)

        # --- 2b. Refined Algorithm ---
        t_start_ref = time.time()
        epsilon_r = 1.0 / DELTA
        calls_r = 0
        while True:
            calls_r += 1
            if int(2 / (epsilon_r * DELTA)) >= N:
                break
            if not refined_sublinear_connectivity_test(graph, epsilon_r):
                break
            epsilon_r /= 2.0
        total_time_refined += (time.time() - t_start_ref)

        # Record the data
        if step % 100 == 0 or step == 1:
            steps_list.append(step)
            simple_calls_list.append(calls_s)
            refined_calls_list.append(calls_r)

        # Print progress
        if step % 25000 == 0:
            elapsed = time.time() - start_time_total
            print(
                f"Step {step}/{STEPS} | Simple Calls: {calls_s} | Refined Calls: {calls_r} | Total elapsed: {elapsed:.2f}s")

    print("\n--- PERFORMANCE RESULTS ---")
    print(f"Time spent in SIMPLE algorithm:  {total_time_simple:.2f} seconds")
    print(f"Time spent in REFINED algorithm: {total_time_refined:.2f} seconds")

    # --- 3. Plotting the Results (Two Subplots) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    # Plot Simple Algorithm
    ax1.scatter(steps_list, simple_calls_list, color='blue', s=15)
    ax1.set_xlabel('steps')
    ax1.set_ylabel('# of calls')
    ax1.set_title('Simple Sublinear Algorithm Calls')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Plot Refined Algorithm
    ax2.scatter(steps_list, refined_calls_list, color='red', s=15)
    ax2.set_xlabel('steps')
    ax2.set_title('Refined Sublinear Algorithm Calls')
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()


run_simulation()
