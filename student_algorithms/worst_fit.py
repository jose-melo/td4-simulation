"""
Example: Worst Fit Algorithm
Student Example - Shows advanced technique
"""

def WorstFit(items, capacity):
    """
    Worst Fit: Place each item in the bin with the MOST remaining space.

    Strategy:
    - For each item, check all existing bins
    - Choose the bin that has the most empty space
    - If no bin fits, create a new one

    Time Complexity: O(N²) - checks all bins for each item
    """

    bins = []

    for item in items:
        # Find the bin with maximum remaining space that can fit this item
        best_bin_idx = -1
        max_remaining_space = -1

        for i in range(len(bins)):
            current_capacity = sum(bins[i])

            # Can this item fit?
            if current_capacity + item <= capacity:
                remaining_space = capacity - (current_capacity + item)

                # Is this bin better than previous best?
                if remaining_space > max_remaining_space:
                    max_remaining_space = remaining_space
                    best_bin_idx = i

        # Place item in best bin or create new bin
        if best_bin_idx != -1:
            bins[best_bin_idx].append(item)
        else:
            bins.append([item])

    return bins


# Metadata
ALGORITHM_NAME = "Worst Fit"
ALGORITHM_DESCRIPTION = "Places items in bin with most remaining space"
COMPLEXITY = "O(N²)"
