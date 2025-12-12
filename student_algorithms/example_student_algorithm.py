"""
Example Student Algorithm - Template

STUDENTS: Copy this template and implement your own algorithm!

Your function must:
1. Take two parameters: items (list) and capacity (int)
2. Return a list of bins (each bin is a list of items)

That's it! The system handles the rest.
"""

def MyCustomAlgorithm(items, capacity):
    """
    Your algorithm description here.

    Args:
        items: List of item sizes [4, 5, 6, ...]
        capacity: Maximum bin capacity (e.g., 10)

    Returns:
        List of bins, where each bin is a list of items
        Example: [[4, 5], [6, 3], [7]]
    """

    # Example: Simple Next Fit implementation
    bins = [[]]  # Start with one empty bin

    for item in items:
        # Try to fit in current bin (last bin)
        if sum(bins[-1]) + item <= capacity:
            bins[-1].append(item)
        else:
            # Create new bin
            bins.append([item])

    return bins


# Optional: Add a description for the web interface
ALGORITHM_NAME = "My Custom Algorithm"
ALGORITHM_DESCRIPTION = "Brief description of what your algorithm does"
COMPLEXITY = "O(N)"  # Your time complexity
