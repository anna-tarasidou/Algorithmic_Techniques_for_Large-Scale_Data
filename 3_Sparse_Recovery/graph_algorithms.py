import random
from collections import defaultdict

# Core Constants
N_NODES = 10000
# Delta calculation: 500 checks * 14 phases * 10000 max queries = 70,000,000 queries.
# To have overall success >= 0.99, (1 - delta)^70000000 >= 0.99 => delta = 1e-10
DELTA = 1e-10


def get_ground_truth_ccs(adj):
    # Calculates Connected Components and Max Component Size using standard BFS on adjacency list.
    visited = set()
    cc_count = 0
    max_cc_size = 0

    for i in range(1, N_NODES + 1):
        if i not in visited:
            cc_count += 1
            size = 0
            # Standard BFS
            queue = [i]
            visited.add(i)

            while queue:
                curr = queue.pop(0)
                size += 1
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            if size > max_cc_size:
                max_cc_size = size

    return cc_count, max_cc_size


def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]


def union(parent, rank, i, j):
    root_i = find(parent, i)
    root_j = find(parent, j)
    if root_i != root_j:
        if rank[root_i] > rank[root_j]:
            parent[root_j] = root_i
        elif rank[root_i] < rank[root_j]:
            parent[root_i] = root_j
        else:
            parent[root_j] = root_i
            rank[root_i] += 1


def run_boruvka_stream(samplers):
    # Simulates Boruvka's algorithm using dummy non-zero samplers (incidence vectors).

    parent = {i: i for i in range(1, N_NODES + 1)}
    rank = {i: 0 for i in range(1, N_NODES + 1)}

    # Maximum log2(V) phases needed for Boruvka
    for phase in range(15):
        # Merge dictionaries for each component to simulate querying the summed sampler
        component_samplers = defaultdict(lambda: defaultdict(int))

        for u in range(1, N_NODES + 1):
            root_u = find(parent, u)
            for edge, value in samplers[u].items():
                if value != 0:
                    component_samplers[root_u][edge] += value

        edges_to_add = []

        # Query the summed sampler for each active component
        for comp, edge_dict in component_samplers.items():
            # Keep only edges that haven't cancelled out to 0
            valid_edges = [e for e, val in edge_dict.items() if val != 0]

            if valid_edges:
                # Dummy sampler failure condition
                if random.random() < DELTA:
                    continue  # Sampler pretends it found nothing

                # Return a uniform random outgoing edge
                chosen_edge = random.choice(valid_edges)
                edges_to_add.append(chosen_edge)

        if not edges_to_add:
            break  # No more merges possible, algorithm finishes

        merged_in_phase = False
        for u, v in edges_to_add:
            root_u = find(parent, u)
            root_v = find(parent, v)
            if root_u != root_v:
                union(parent, rank, root_u, root_v)
                merged_in_phase = True

        if not merged_in_phase:
            break

    # Calculate Boruvka results
    final_components = set(find(parent, i) for i in range(1, N_NODES + 1))
    cc_count = len(final_components)

    sizes = defaultdict(int)
    for i in range(1, N_NODES + 1):
        sizes[find(parent, i)] += 1
    max_cc_size = max(sizes.values()) if sizes else 0

    return cc_count, max_cc_size
