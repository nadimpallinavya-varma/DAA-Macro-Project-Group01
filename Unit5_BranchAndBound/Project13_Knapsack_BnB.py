"""
Project 13: 0/1 Knapsack using Branch and Bound (best-first search)
Unit V - Branch and Bound

Bound at a node: ub = v + (W - w) * (v[next] / w[next])
Items must be sorted by value/weight ratio (descending).
Left child = take the item, right child = skip the item.
"""
import heapq

def bound(level, w, v, items, W):
    """Optimistic upper bound: fill leftover capacity at the best remaining ratio."""
    n = len(items)
    if level == n:
        return v
    wt, val = items[level]
    return v + (W - w) * (val / wt)

def knapsack_bb(items, W):
    items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    n = len(items)
    best, best_set = 0, []
    node_id = 0
    # heap entries: (-ub, id, level, w, v, chosen)
    root_ub = bound(0, 0, 0, items, W)
    heap = [(-root_ub, 0, 0, 0, 0, ())]
    print(f"Node 0 (root): w=0, v=0, ub={root_ub:g}")

    while heap:
        neg_ub, nid, level, w, v, chosen = heapq.heappop(heap)
        ub = -neg_ub
        if ub <= best:
            print(f"Node {nid}: ub={ub:g} <= best={best} -> PRUNED")
            continue
        if level == n:
            continue

        wt, val = items[level]

        # Left child: take item
        node_id += 1
        lw, lv = w + wt, v + val
        if lw > W:
            print(f"Node {node_id}: take item {level+1}, w={lw} > {W} -> INFEASIBLE")
        else:
            lub = bound(level + 1, lw, lv, items, W)
            lchosen = chosen + (level + 1,)
            print(f"Node {node_id}: take item {level+1}, w={lw}, v={lv}, ub={lub:g}")
            if lv > best:
                best, best_set = lv, list(lchosen)
                print(f"           new best = {best} with items {best_set}")
            if lub > best:
                heapq.heappush(heap, (-lub, node_id, level + 1, lw, lv, lchosen))
            else:
                print(f"           ub={lub:g} <= best={best} -> PRUNED")

        # Right child: skip item
        node_id += 1
        rub = bound(level + 1, w, v, items, W)
        print(f"Node {node_id}: skip item {level+1}, w={w}, v={v}, ub={rub:g}")
        if level + 1 == n:
            print(f"           leaf reached, solution value = {v} (best = {best})")
        elif rub > best:
            heapq.heappush(heap, (-rub, node_id, level + 1, w, v, chosen))
        else:
            print(f"           ub={rub:g} <= best={best} -> PRUNED")

    return best, best_set

if __name__ == "__main__":
    # (weight, value) pairs
    items = [(4, 40), (7, 42), (5, 25), (3, 12)]
    W = 10
    best, chosen = knapsack_bb(items, W)
    print(f"\nMaximum value = {best}, items chosen (sorted order) = {chosen}")
