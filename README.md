# Sorting Complexity Visualizer (Merge Sort vs Quick Sort)

## Description
This project implements **Merge Sort** and **Quick Sort** in Python and compares their time complexity for input sizes **n = 10, 100, 1000**. It counts the comparisons each algorithm performs on random data and visualizes the growth rates as a line chart through prompt engineering.

## Algorithm

**Merge Sort** (Divide and Conquer, O(n log n) in all cases)
```
MERGE-SORT(A):
    if length(A) <= 1: return A
    mid = length(A) / 2
    L = MERGE-SORT(A[0..mid])
    R = MERGE-SORT(A[mid..end])
    return MERGE(L, R)

MERGE(L, R):
    result = []
    while L and R are not empty:
        append the smaller front element of L or R to result
    append remaining elements of L or R
    return result
```

**Quick Sort** (Divide and Conquer, O(n log n) average, O(n²) worst case)
```
QUICK-SORT(A):
    if length(A) <= 1: return A
    pivot = random element of A
    less    = elements < pivot
    equal   = elements == pivot
    greater = elements > pivot
    return QUICK-SORT(less) + equal + QUICK-SORT(greater)
```

**Visualization logic:** For each n, both algorithms sort 20 random arrays and the average number of comparisons is recorded. These are plotted against the theoretical n log₂ n curve and the Quick Sort worst case n(n-1)/2, on log-log axes.

## Prompt Used
“Generate a graph comparing time complexity of Merge, and Quick Sort for n = 10, 100, 1000.”

## Output
![Sorting Complexity Visualization](Visualization.png)

| n    | Merge Sort comparisons | Quick Sort comparisons | n log₂ n |
|------|-----------------------:|-----------------------:|---------:|
| 10   | 23                     | 30                     | 33       |
| 100  | 541                    | 719                    | 664      |
| 1000 | 8711                   | 11570                  | 9966     |

Both algorithms track the n log n curve closely, while the Quick Sort worst case (O(n²)) grows far faster.

## How to Run
```bash
pip install matplotlib
python Project1_SortingComplexity.py
```

## Learning Outcome
- Understood divide-and-conquer sorting and its time complexity.
- Compared average-case and worst-case behavior of Merge Sort and Quick Sort.
- Learned prompt-based visualization of algorithm growth rates.
- Practiced GitHub documentation.
