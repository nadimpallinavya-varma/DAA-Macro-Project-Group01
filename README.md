# Project 7: Traveling Salesperson Problem using Dynamic Programming (Held-Karp)

**Unit III - Dynamic Programming**

## Description

This project solves the Traveling Salesperson Problem (TSP) for 4 cities using the Held-Karp dynamic programming algorithm and visualizes the DP table and the subset-to-subset state transitions through prompt engineering.

Instead of trying all `(n-1)!` tours, the DP stores the best cost for every pair *(subset of visited cities, last city)*, giving `O(n² · 2ⁿ)` time instead of `O(n!)`.

## Input

Distance matrix (cities 0 to 3, start and end at city 0):

|   | 0  | 1  | 2  | 3  |
|---|----|----|----|----|
| 0 | 0  | 10 | 15 | 20 |
| 1 | 10 | 0  | 35 | 25 |
| 2 | 15 | 35 | 0  | 30 |
| 3 | 20 | 25 | 30 | 0  |

## Algorithm

**State:** `dp[S][j]` = minimum cost of a path that starts at city 0, visits exactly the cities in `S` (`0 ∉ S`), and ends at city `j ∈ S`.

```
HeldKarp(dist, n):
    for each j in 1..n-1:
        dp[{j}][j] = dist[0][j]                    // base case

    for size = 2 to n-1:
        for each subset S of {1..n-1} with |S| = size:
            for each j in S:
                dp[S][j] = min over k in S\{j} of
                           ( dp[S\{j}][k] + dist[k][j] )
                parent[S][j] = argmin k

    full = {1..n-1}
    answer = min over j in full of ( dp[full][j] + dist[j][0] )
    reconstruct the tour by following parent[][] backwards from the best j
```

**Complexity:** Time `O(n² · 2ⁿ)`, space `O(n · 2ⁿ)`.

## Prompt Used

> "Visualize DP state transitions for TSP with 4 cities."

The refined prompt is in [`Prompt.txt`](Prompt.txt).

## Output

![TSP DP Visualization](Visualization.png)

### DP table (cost, predecessor)

| Subset S | end at j=1 | end at j=2 | end at j=3 |
|----------|-----------|-----------|-----------|
| {1}      | 10 (from 0) | -         | -         |
| {2}      | -         | 15 (from 0) | -         |
| {3}      | -         | -         | 20 (from 0) |
| {1,2}    | 50 (from 2) | 45 (from 1) | -       |
| {1,3}    | 45 (from 3) | -         | 35 (from 1) |
| {2,3}    | -         | 50 (from 3) | 45 (from 2) |
| {1,2,3}  | 70 (from 3) | 65 (from 3) | 75 (from 1) |

Closing the tour (add the edge back to city 0):

- end at 1: 70 + 10 = **80**
- end at 2: 65 + 15 = **80**
- end at 3: 75 + 20 = 95

**Optimal tour: 0 → 2 → 3 → 1 → 0, cost = 80.** The reverse tour 0 → 1 → 3 → 2 → 0 has the same cost because the distance matrix is symmetric. The script checks the DP answer against brute force.

## Explanation of the Visualization

- **Left, the DP table:** each row is a subset `S` of visited cities and each column is the ending city `j`. Each cell holds the minimum cost and the predecessor `k` that achieved it. Grey cells are impossible states (`j ∉ S`). Red cells are the states on the optimal tour.
- **Right, the transition graph:** nodes are DP states `(S, j)`, arranged in layers by subset size (1, 2, 3). An arrow from `(S\{j}, k)` to `(S, j)` means "extend the path from `k` to `j`". Each node picks the cheapest incoming arrow, which is the `min` in the recurrence. The red path shows the optimal tour being built from START to END.

## How to Run

```bash
pip install matplotlib
python Project7_TSP_DP.py
```

This prints the DP table, the optimal tour and cost, runs a brute-force check, and regenerates `Visualization.png`.

## Files

| File | Purpose |
|------|---------|
| `Project7_TSP_DP.py` | Held-Karp implementation and visualization code |
| `Prompt.txt` | Prompt used for the visualization |
| `Visualization.png` | Generated DP table and transition graph |
| `README.md` | This document |

## Learning Outcome

- Understood subset-based dynamic programming (bitmask / Held-Karp) and why it beats brute force for TSP.
- Learned to read DP state transitions as a layered graph.
- Learned prompt-based visualization.
- Practiced GitHub documentation.
