"""
Project 1: Sorting Complexity Visualizer
Unit 1 - Algorithm Analysis

Compares Merge Sort and Quick Sort for n = 10, 100, 1000 by counting
comparisons and measuring running time, then plots growth rates.
"""
import math
import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIZES = [10, 100, 1000]


# ---------------- Merge Sort ----------------
def merge_sort(arr, counter):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], counter)
    right = merge_sort(arr[mid:], counter)
    return merge(left, right, counter)


def merge(left, right, counter):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------- Quick Sort ----------------
def quick_sort(arr, counter):
    if len(arr) <= 1:
        return arr
    pivot = arr[random.randrange(len(arr))]  # random pivot
    less, equal, greater = [], [], []
    for x in arr:
        counter[0] += 1
        if x < pivot:
            less.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            greater.append(x)
    return quick_sort(less, counter) + equal + quick_sort(greater, counter)


# ---------------- Experiment ----------------
def run(sort_fn, n, trials=20):
    comps, times = [], []
    for _ in range(trials):
        data = random.sample(range(n * 10), n)
        counter = [0]
        start = time.perf_counter()
        out = sort_fn(data, counter)
        times.append(time.perf_counter() - start)
        assert out == sorted(data)
        comps.append(counter[0])
    return sum(comps) / trials, sum(times) / trials


def main():
    random.seed(42)
    merge_c, quick_c, merge_t, quick_t = [], [], [], []
    for n in SIZES:
        c, t = run(merge_sort, n); merge_c.append(c); merge_t.append(t)
        c, t = run(quick_sort, n); quick_c.append(c); quick_t.append(t)

    nlogn = [n * math.log2(n) for n in SIZES]
    worst = [n * (n - 1) / 2 for n in SIZES]  # Quick Sort worst case O(n^2)

    print(f"{'n':>6} {'Merge cmp':>10} {'Quick cmp':>10} {'n log n':>9} {'Merge ms':>9} {'Quick ms':>9}")
    for i, n in enumerate(SIZES):
        print(f"{n:>6} {merge_c[i]:>10.0f} {quick_c[i]:>10.0f} {nlogn[i]:>9.0f} "
              f"{merge_t[i]*1000:>9.3f} {quick_t[i]*1000:>9.3f}")

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(SIZES, merge_c, "o-", color="#1f77b4", lw=2, label="Merge Sort (measured comparisons)")
    ax.plot(SIZES, quick_c, "s-", color="#2ca02c", lw=2, label="Quick Sort - average (measured comparisons)")
    ax.plot(SIZES, nlogn, "--", color="gray", lw=1.5, label="Theoretical n log₂ n")
    ax.plot(SIZES, worst, "^:", color="#d62728", lw=1.5, label="Quick Sort worst case O(n²)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks(SIZES); ax.set_xticklabels([str(n) for n in SIZES])
    ax.set_xlabel("Input size (n)")
    ax.set_ylabel("Number of comparisons (log scale)")
    ax.set_title("Time Complexity Growth: Merge Sort vs Quick Sort")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("Visualization.png", dpi=150)
    print("Saved Visualization.png")


if __name__ == "__main__":
    main()
