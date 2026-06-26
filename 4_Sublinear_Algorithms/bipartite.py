import random
from collections import deque


def is_bipartite(graph, nodes):
    # Dictionary to store the color of each node (0 or 1)
    color = {}

    # Check all components of the subgraph
    for node in nodes:
        if node not in color:
            # Start BFS for unvisited component
            color[node] = 0
            queue = deque([node])

            while queue:
                current = queue.popleft()

                # Check neighbors of the current node
                for neighbor in graph.get(current, []):
                    if neighbor not in color:
                        # Color with opposite color and add to queue
                        color[neighbor] = 1 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        # Odd-length cycle found, not bipartite
                        return False
    return True


def simulate_bipartite_tests():
    n_total = 1000
    trials = 100

    # K values from 0 to 13 inclusive
    for k in range(14):
        p = 1 / (2 ** k)
        bipartite_count = 0
        total_n_used = 0

        for _ in range(trials):
            known_edges = {}
            # Adjacency list representation for the subgraph
            induced_graph = {}

            # The sequence of sample sizes N
            n_sequence = [3, 9, 27, 81, 243, 729, n_total]

            final_n = n_total
            is_graph_bipartite = True

            for N in n_sequence:
                # Add nodes to the induced graph representation if not already present
                for i in range(N):
                    if i not in induced_graph:
                        induced_graph[i] = []

                # Check all possible pairs in the current sample size N
                for i in range(N):
                    for j in range(i + 1, N):
                        edge_pair = (i, j)

                        if edge_pair not in known_edges:
                            edge_exists = random.random() < p
                            known_edges[edge_pair] = edge_exists

                            # If edge exists, add to our adjacency list
                            if edge_exists:
                                induced_graph[i].append(j)
                                induced_graph[j].append(i)

                # Test bipartiteness of the current subgraph
                if not is_bipartite(induced_graph, range(N)):
                    is_graph_bipartite = False
                    final_n = N
                    break  # Found non-bipartite, exit the N loop

                # If we reached the end of the sequence and it's still bipartite
                if N == n_total:
                    final_n = N

            if is_graph_bipartite:
                bipartite_count += 1

            total_n_used += final_n

        # Calculate statistics for the current p
        prob_bipartite = bipartite_count / trials
        avg_n = total_n_used / trials

        print(f"k = {k:2d} | p = {p:.5f} | B(1000, p) estimate = {prob_bipartite:.2f} | Average N = {avg_n:.2f}")


simulate_bipartite_tests()
