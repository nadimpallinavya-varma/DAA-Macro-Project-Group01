# Project Title
0/1 Knapsack Problem using Branch and Bound

## Description
This project solves the 0/1 Knapsack problem using best-first Branch and Bound and visualizes the bounding and pruning in the state space tree through prompt engineering.

Instance used: capacity W = 10, items (weight, value) = (4,40), (7,42), (5,25), (3,12), already sorted by value/weight ratio (10, 6, 5, 4).

## Algorithm
Upper bound at a node: `ub = v + (W - w) * (v_next / w_next)`

```
KnapsackBB(items, W):          // items sorted by v/w, descending
    best <- 0
    root <- (level=0, w=0, v=0); root.ub <- Bound(root)
    PQ <- max-priority-queue ordered by ub; insert root

    while PQ not empty:
        node <- PQ.extractMax()
        if node.ub <= best: continue            // PRUNE by bound
        i <- node.level + 1
        if i > n: continue

        L <- (i, node.w + w[i], node.v + v[i])  // take item i
        if L.w <= W:
            best <- max(best, L.v)
            L.ub <- Bound(L)
            if L.ub > best: PQ.insert(L)
        // else: infeasible, discard

        R <- (i, node.w, node.v)                // skip item i
        R.ub <- Bound(R)
        if R.ub > best: PQ.insert(R)            // otherwise PRUNE

    return best

Bound(node):
    if node.level = n: return node.v
    return node.v + (W - node.w) * (v[node.level+1] / w[node.level+1])
```

Code: [Project13_Knapsack_BnB.py](Project13_Knapsack_BnB.py)

## Prompt Used
"Illustrate bounding and pruning in 0/1 Knapsack using node values. Use items (w,v) = (4,40), (7,42), (5,25), (3,12) with capacity W=10. Draw the state-space tree with weight, value and upper bound at each node. Left child = take item, right child = skip item. Mark pruned nodes in red, infeasible nodes (w > W) in gray dashed, and the best solution in green."

## Output
![Knapsack Branch and Bound Tree](Visualization.png)

Explanation of the visualization:
- Each node shows weight (w), value (v) and upper bound (ub). Left child = take item, right child = skip item.
- Root has ub = 100. Node 1 (take item 1, ub = 76) is expanded first because it has the highest bound.
- Nodes 3 and 7 are infeasible (w = 11 and w = 12 exceed W = 10) and are discarded.
- Node 5 (take item 3) gives w = 9, v = 65, so the best value becomes 65.
- Node 6 (ub = 64) and Node 2 (ub = 60) have ub <= 65, so they are pruned and never expanded.
- Result: maximum value = 65 with items 1 and 3 (weight 9). Only 9 of the 31 possible nodes were generated.

Time complexity: O(2^n) in the worst case, but pruning reduces the nodes explored in practice.

## Learning Outcome
- Understood bounding and pruning in Branch and Bound.
- Learned how an optimistic upper bound lets us discard branches early.
- Learned prompt-based visualization.
- Practiced GitHub documentation.
