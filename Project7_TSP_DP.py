"""
Project 7 - Traveling Salesperson Problem using Dynamic Programming (Held-Karp)
Unit III - Dynamic Programming

State:       dp[S][j] = minimum cost of a path that starts at city 0, visits
             exactly the cities in subset S (S does not contain 0), and ends at j (j in S).
Transition:  dp[S][j] = min over k in S\\{j} of ( dp[S\\{j}][k] + dist[k][j] )
Base case:   dp[{j}][j] = dist[0][j]
Answer:      min over j of ( dp[all][j] + dist[j][0] )

Running this file prints the DP table and saves Visualization.png
(DP table + subset-transition graph) next to the script.
"""

import itertools
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Input: 4 cities (0, 1, 2, 3). Symmetric distance matrix.
# ----------------------------------------------------------------------------
DIST = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0],
]


def label(S):
    """Pretty-print a subset, e.g. frozenset({1, 2}) -> '{1,2}'."""
    return "{" + ",".join(str(x) for x in sorted(S)) + "}"


def held_karp(dist):
    """Return (dp, parent, optimal_cost, tour, optimal_states)."""
    n = len(dist)
    others = list(range(1, n))
    dp, parent = {}, {}

    # Base case: subsets of size 1
    for j in others:
        S = frozenset([j])
        dp[(S, j)] = dist[0][j]
        parent[(S, j)] = 0

    # Fill subsets in increasing size
    for size in range(2, n):
        for S in map(frozenset, itertools.combinations(others, size)):
            for j in S:
                prev = S - {j}
                best, arg = min((dp[(prev, k)] + dist[k][j], k) for k in prev)
                dp[(S, j)] = best
                parent[(S, j)] = arg

    # Close the tour by returning to city 0
    full = frozenset(others)
    cost, last = min((dp[(full, j)] + dist[j][0], j) for j in full)

    # Reconstruct the optimal tour from the parent pointers
    states, seq = [], []
    S, j = full, last
    while S:
        states.append((S, j))
        seq.append(j)
        k = parent[(S, j)]
        S, j = S - {j}, k
    tour = [0] + seq[::-1] + [0]
    return dp, parent, cost, tour, set(states)


def brute_force(dist):
    """Check the DP answer by trying every permutation."""
    n = len(dist)
    best = min(
        sum(dist[a][b] for a, b in zip((0,) + p, p + (0,)))
        for p in itertools.permutations(range(1, n))
    )
    return best


def print_table(dp, parent, n):
    others = list(range(1, n))
    print("\nDP table: dp[S][j] = min cost, starting at 0, visiting S, ending at j")
    print("-" * 56)
    header = f"{'Subset S':<12}" + "".join(f"{'j=' + str(j):<14}" for j in others)
    print(header)
    print("-" * 56)
    for size in range(1, n):
        for S in map(frozenset, itertools.combinations(others, size)):
            row = f"{label(S):<12}"
            for j in others:
                if j in S:
                    row += f"{str(dp[(S, j)]) + ' (via ' + str(parent[(S, j)]) + ')':<14}"
                else:
                    row += f"{'-':<14}"
            print(row)
    print("-" * 56)


def draw(dp, parent, cost, tour, opt_states, dist, out_path):
    n = len(dist)
    others = list(range(1, n))
    subsets = [
        frozenset(c)
        for size in range(1, n)
        for c in itertools.combinations(others, size)
    ]
    full = frozenset(others)

    fig, (axT, axG) = plt.subplots(
        1, 2, figsize=(22, 9), gridspec_kw={"width_ratios": [1, 1.7]}
    )

    # ---------------- Left: DP table ----------------
    axT.axis("off")
    axT.set_title("DP Table  dp[S][j]  (cost, predecessor)", fontsize=15, pad=14)
    cell_text, colors = [], []
    for S in subsets:
        row, crow = [label(S)], ["#e8eef7"]
        for j in others:
            if j in S:
                src = parent[(S, j)]
                row.append(f"{dp[(S, j)]}\n(from {src})")
                crow.append("#ffd6d6" if (S, j) in opt_states else "#ffffff")
            else:
                row.append("-")
                crow.append("#f2f2f2")
        cell_text.append(row)
        colors.append(crow)
    tbl = axT.table(
        cellText=cell_text,
        cellColours=colors,
        colLabels=["Subset S"] + [f"end at j={j}" for j in others],
        colColours=["#c9d6ea"] * (n),
        loc="upper center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 3.1)

    dist_txt = "Distance matrix (rows/cols = city 0..3)\n" + "\n".join(
        "   ".join(f"{v:>2}" for v in row) for row in dist
    )
    axT.text(0.5, 0.17, dist_txt, ha="center", va="center", fontsize=12,
             family="monospace", transform=axT.transAxes,
             bbox=dict(boxstyle="round", fc="#fafafa", ec="#999999"))
    axT.text(0.5, 0.01, "Red cells = states on the optimal tour",
             ha="center", fontsize=11, color="#b00020", transform=axT.transAxes)

    # ---------------- Right: subset transition graph ----------------
    axG.axis("off")
    axG.set_title("Subset transitions  (S\\{j}, k)  →  (S, j)", fontsize=15, pad=14)

    pos = {}
    pos["start"] = (0, 0)
    layers = {1: [], 2: [], 3: []}
    for S in subsets:
        for j in sorted(S):
            layers[len(S)].append((S, j))
    for size, nodes in layers.items():
        m = len(nodes)
        for i, node in enumerate(nodes):
            pos[node] = (size, (m - 1) / 2 - i)
    pos["end"] = (n, 0)

    def node_text(node):
        if node == "start":
            return "START\ncity 0"
        if node == "end":
            return f"END\nback to 0\ncost {cost}"
        S, j = node
        return f"S={label(S)}, j={j}\ncost {dp[(S, j)]}"

    # edges: (src, dst, weight)
    edges = []
    for j in others:
        edges.append(("start", (frozenset([j]), j), dist[0][j]))
    for size in range(2, n):
        for (S, j) in layers[size]:
            for k in S - {j}:
                edges.append(((S - {j}, k), (S, j), dist[k][j]))
    for j in others:
        edges.append(((full, j), "end", dist[j][0]))

    # optimal path as list of nodes
    opt_nodes = ["start"] + [
        (frozenset(tour[1 : i + 1]), tour[i]) for i in range(1, n)
    ] + ["end"]
    opt_edges = set(zip(opt_nodes[:-1], opt_nodes[1:]))

    for src, dst, w in edges:
        is_opt = (src, dst) in opt_edges
        axG.annotate(
            "", xy=pos[dst], xytext=pos[src],
            arrowprops=dict(
                arrowstyle="-|>", color="#d62728" if is_opt else "#9aa0a6",
                lw=3.2 if is_opt else 1.0, alpha=1.0 if is_opt else 0.6,
                shrinkA=34, shrinkB=34,
            ),
            zorder=3 if is_opt else 1,
        )

    for node, (x, y) in pos.items():
        if node == "start" or node == "end":
            fc = "#d4edda"
        elif node in opt_states:
            fc = "#ffd6d6"
        else:
            fc = "#e8eef7"
        axG.text(x, y, node_text(node), ha="center", va="center", fontsize=9.5,
                 zorder=5,
                 bbox=dict(boxstyle="round,pad=0.4", fc=fc,
                           ec="#d62728" if node in opt_states else "#555555", lw=1.4))

    titles = ["", "|S| = 1\n(base case)", "|S| = 2", "|S| = 3\n(all cities)", ""]
    for x, t in enumerate(titles):
        if t:
            axG.text(x, 3.1, t, ha="center", va="bottom", fontsize=12, fontweight="bold")
    axG.set_xlim(-0.6, n + 0.6)
    axG.set_ylim(-3.4, 4.0)

    tour_txt = " → ".join(map(str, tour))
    fig.suptitle(
        f"TSP with 4 cities - Held-Karp DP     Optimal tour: {tour_txt}     Cost = {cost}",
        fontsize=18, fontweight="bold", y=0.98,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main():
    dp, parent, cost, tour, opt_states = held_karp(DIST)
    print_table(dp, parent, len(DIST))
    print(f"\nOptimal tour : {' -> '.join(map(str, tour))}")
    print(f"Optimal cost : {cost}")

    expected = brute_force(DIST)
    assert cost == expected, f"DP gave {cost}, brute force gave {expected}"
    print(f"Brute-force check passed (cost {expected}).")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Visualization.png")
    draw(dp, parent, cost, tour, opt_states, DIST, out)
    print(f"Saved visualization to {out}")


if __name__ == "__main__":
    main()
