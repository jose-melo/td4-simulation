"""
Sorted Best Fit Algorithm

Variation of Best Fit that first sorts items in descending order
before applying the best-fit placement. Often yields better packing
than processing items in their original order.
"""


def SortedBestFit(items, capacity: int):
    """
    Best Fit after sorting items descending.

    Strategy:
    1) Sort items largest-to-smallest.
    2) For each item, place it in the bin that leaves the least remaining space.
       If no existing bin fits, open a new bin.
    """
    # Sort in place so the simulator can reflect the same order
    items.sort(reverse=True)
    sorted_items = items
    bins = []

    for item in sorted_items:
        best_bin_index = -1
        min_remaining = capacity + 1

        for i, bin_items in enumerate(bins):
            current_capacity = sum(bin_items)
            if current_capacity + item <= capacity:
                remaining = capacity - (current_capacity + item)
                if remaining < min_remaining:
                    min_remaining = remaining
                    best_bin_index = i

        if best_bin_index == -1:
            bins.append([item])
        else:
            bins[best_bin_index].append(item)

    return bins


# Metadata for the simulator UI
ALGORITHM_NAME = "Sorted Best Fit"
ALGORITHM_DESCRIPTION = "Sorts items descending, then applies Best Fit"
COMPLEXITY = "O(N²)"
