from graph_algorithms import *

TOTAL_COMMANDS = 500000


def run_stream():
    # Initialization
    adj = {i: [] for i in range(1, N_NODES + 1)}
    samplers = {i: defaultdict(int) for i in range(1, N_NODES + 1)}

    for step in range(1, TOTAL_COMMANDS + 1):
        # 75% Probability: Delete edge
        if random.random() < 0.75:
            v = random.randint(1, N_NODES)
            if len(adj[v]) > 0:
                # Delete a random incident edge
                u = random.choice(adj[v])
                adj[v].remove(u)
                adj[u].remove(v)

                # Update Samplers (Incidence Vectors)
                min_node, max_node = min(u, v), max(u, v)
                samplers[min_node][(min_node, max_node)] -= 1
                samplers[max_node][(min_node, max_node)] += 1
            else:
                # Add an edge instead if no edges exist
                u = random.randint(1, N_NODES)
                while u == v:
                    u = random.randint(1, N_NODES)
                adj[v].append(u)
                adj[u].append(v)

                min_node, max_node = min(u, v), max(u, v)
                samplers[min_node][(min_node, max_node)] += 1
                samplers[max_node][(min_node, max_node)] -= 1

        # 25% Probability: Add edge
        else:
            v = random.randint(1, N_NODES)
            u = random.randint(1, N_NODES)
            while u == v:
                u = random.randint(1, N_NODES)
            adj[v].append(u)
            adj[u].append(v)

            min_node, max_node = min(u, v), max(u, v)
            samplers[min_node][(min_node, max_node)] += 1
            samplers[max_node][(min_node, max_node)] -= 1

        # Every 1000 steps, evaluate and print
        if step % 1000 == 0:
            gt_cc_count, gt_max_size = get_ground_truth_ccs(adj)
            boruvka_cc_count, boruvka_max_size = run_boruvka_stream(samplers)

            if (gt_cc_count != boruvka_cc_count) or (gt_max_size != boruvka_max_size):
                print("error")
            else:
                print(f"{step} {gt_cc_count} {gt_max_size}")


if __name__ == '__main__':
    run_stream()
