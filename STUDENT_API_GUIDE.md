# Student Algorithm API - Integration Guide

## Overview

This guide shows students how to write their own bin packing algorithms and test them in the web visualizer **without modifying any framework code**.

## Quick Start (3 Steps)

### Step 1: Write Your Algorithm

Create a Python file with a single function:

```python
def MyAlgorithm(items, capacity):
    """
    Your bin packing algorithm.

    Args:
        items: List of item sizes, e.g., [4, 5, 6, 3, 7]
        capacity: Maximum bin capacity, e.g., 10

    Returns:
        List of bins (each bin is a list of items)
        Example: [[4, 6], [5, 3], [7]]
    """

    bins = [[]]  # Start with one empty bin

    for item in items:
        # Your logic here
        if sum(bins[-1]) + item <= capacity:
            bins[-1].append(item)
        else:
            bins.append([item])

    return bins
```

**That's it!** No classes, no inheritance, no framework knowledge needed.

### Step 2: Save the File

Save as `student_algorithms/my_algorithm.py`

### Step 3: Test in Web App

Option A - Copy/paste your code into the web interface (coming soon)
Option B - Use the test script (see below)

## Complete Template

```python
"""
Student: [Your Name]
Algorithm: [Brief Description]
"""

def MyBinPackingAlgorithm(items, capacity):
    """
    Describe your algorithm strategy here.

    Example: "This algorithm always tries to pack items
    in decreasing order of size."

    Args:
        items: List[int] - Item sizes to pack
        capacity: int - Maximum bin capacity

    Returns:
        List[List[int]] - List of bins, each containing items
    """

    # Initialize bins
    bins = []

    # Your algorithm logic here
    # ...

    return bins


# Optional: Metadata for the web interface
ALGORITHM_NAME = "My Awesome Algorithm"
ALGORITHM_DESCRIPTION = "Packs items using [your strategy]"
COMPLEXITY = "O(N log N)"  # Your time complexity
```

## Rules & Requirements

### What Your Function MUST Do:

1. ✅ Take exactly 2 parameters: `items` and `capacity`
2. ✅ Return a list of bins (list of lists)
3. ✅ Place ALL items exactly once
4. ✅ Respect capacity constraints (no bin over capacity)

### What Your Function CAN'T Do:

1. ❌ Modify the input `items` list (make a copy if needed)
2. ❌ Return bins that exceed capacity
3. ❌ Skip any items
4. ❌ Place items multiple times

### What's Allowed:

- ✅ Import standard Python libraries (`math`, `random`, etc.)
- ✅ Sort items (on a copy!)
- ✅ Use any data structures
- ✅ Multiple helper functions
- ✅ Comments and documentation

## Testing Your Algorithm

### Method 1: Quick Test Script

Create `test_my_algorithm.py`:

```python
from custom_algorithm_loader import load_algorithm_from_file, validate_algorithm

# Load your algorithm
algo_info = load_algorithm_from_file('student_algorithms/my_algorithm.py')

# Test it
test_items = [4, 5, 6, 3, 7, 8, 2]
test_capacity = 10

validation = validate_algorithm(algo_info.function, test_items, test_capacity)

if validation['valid']:
    print(f"✓ Algorithm works!")
    print(f"  Bins used: {validation['bins_used']}")

    # Run it
    result = algo_info.function(test_items, test_capacity)
    print(f"  Result: {result}")
else:
    print(f"✗ Error: {validation['error']}")
```

Run: `python test_my_algorithm.py`

### Method 2: Using the API

```python
import requests

# Read your code
with open('student_algorithms/my_algorithm.py') as f:
    code = f.read()

# Validate
response = requests.post('http://localhost:5001/api/custom/validate', json={
    'code': code
})

print(response.json())

# If valid, run simulation
if response.json()['valid']:
    response = requests.post('http://localhost:5001/api/custom/run', json={
        'code': code,
        'capacity': 10,
        'items': [4, 5, 6, 3, 7, 8, 2]
    })

    # Now step through in the web app!
    session_id = response.json()['session_id']
```

### Method 3: Load from File (Instructor/Easy Method)

Place file in `student_algorithms/` directory, then:

```python
import requests

response = requests.post('http://localhost:5001/api/custom/load-file', json={
    'filename': 'my_algorithm.py'
})

print(response.json())
```

## Example Algorithms

### Example 1: Next Fit (Simple)

```python
def NextFit(items, capacity):
    """Only check the last bin - O(N) complexity."""
    bins = [[]]

    for item in items:
        if sum(bins[-1]) + item <= capacity:
            bins[-1].append(item)
        else:
            bins.append([item])

    return bins

ALGORITHM_NAME = "Next Fit"
COMPLEXITY = "O(N)"
```

### Example 2: First Fit (Medium)

```python
def FirstFit(items, capacity):
    """Check bins from first to last - O(N²) complexity."""
    bins = []

    for item in items:
        # Try existing bins
        placed = False
        for bin_items in bins:
            if sum(bin_items) + item <= capacity:
                bin_items.append(item)
                placed = True
                break

        # Create new bin if needed
        if not placed:
            bins.append([item])

    return bins

ALGORITHM_NAME = "First Fit"
COMPLEXITY = "O(N²)"
```

### Example 3: First Fit Decreasing (Advanced)

```python
def FirstFitDecreasing(items, capacity):
    """Sort items first, then use First Fit - O(N log N)."""

    # Sort items in decreasing order
    sorted_items = sorted(items, reverse=True)

    bins = []

    for item in sorted_items:
        placed = False
        for bin_items in bins:
            if sum(bin_items) + item <= capacity:
                bin_items.append(item)
                placed = True
                break

        if not placed:
            bins.append([item])

    return bins

ALGORITHM_NAME = "First Fit Decreasing"
COMPLEXITY = "O(N log N)"
```

### Example 4: Worst Fit (Creative)

```python
def WorstFit(items, capacity):
    """Place items in bin with MOST remaining space."""
    bins = []

    for item in items:
        # Find bin with most space
        best_bin_idx = -1
        max_remaining = -1

        for i, bin_items in enumerate(bins):
            current = sum(bin_items)
            if current + item <= capacity:
                remaining = capacity - (current + item)
                if remaining > max_remaining:
                    max_remaining = remaining
                    best_bin_idx = i

        if best_bin_idx >= 0:
            bins[best_bin_idx].append(item)
        else:
            bins.append([item])

    return bins

ALGORITHM_NAME = "Worst Fit"
ALGORITHM_DESCRIPTION = "Place in bin with most remaining space"
COMPLEXITY = "O(N²)"
```

## Common Mistakes & Fixes

### Mistake 1: Modifying Input
```python
# ❌ Wrong - modifies original list
def BadAlgorithm(items, capacity):
    items.sort()  # MODIFIES INPUT!
    # ...

# ✓ Correct - work on copy
def GoodAlgorithm(items, capacity):
    sorted_items = sorted(items)  # Creates copy
    # ...
```

### Mistake 2: Returning Wrong Format
```python
# ❌ Wrong - returns dictionary
def BadAlgorithm(items, capacity):
    return {'bins': [[4, 5], [6]]}

# ✓ Correct - returns list of lists
def GoodAlgorithm(items, capacity):
    return [[4, 5], [6]]
```

### Mistake 3: Exceeding Capacity
```python
# ❌ Wrong - no capacity check
def BadAlgorithm(items, capacity):
    return [items]  # All items in one bin!

# ✓ Correct - check capacity
def GoodAlgorithm(items, capacity):
    bins = [[]]
    for item in items:
        if sum(bins[-1]) + item <= capacity:
            bins[-1].append(item)
        else:
            bins.append([item])
    return bins
```

### Mistake 4: Missing Items
```python
# ❌ Wrong - skips items
def BadAlgorithm(items, capacity):
    bins = []
    for item in items:
        if item < 5:  # Only packs small items!
            # ...
    return bins

# ✓ Correct - pack all items
def GoodAlgorithm(items, capacity):
    bins = []
    for item in items:  # ALL items
        # ...
    return bins
```

## Validation Checklist

Before submitting, check:

- [ ] Function takes exactly 2 parameters
- [ ] Returns list of lists
- [ ] All items are placed
- [ ] No bin exceeds capacity
- [ ] No items are duplicated
- [ ] No items are skipped
- [ ] Code runs without errors

## Testing Checklist

Test your algorithm with:

- [ ] Simple case: `[4, 6]` capacity `10` → Should use 1 bin
- [ ] Doesn't fit: `[6, 7]` capacity `10` → Should use 2 bins
- [ ] Many items: `[4]*20` capacity `10` → Should use 8 bins
- [ ] Single item: `[5]` capacity `10` → Should use 1 bin
- [ ] All same size: `[5, 5, 5, 5]` capacity `10` → Should use 2 bins
- [ ] Lecture data: 24 items, capacity 10 → How many bins?

## Debugging Tips

### Print Intermediate Results
```python
def MyAlgorithm(items, capacity):
    bins = [[]]

    for i, item in enumerate(items):
        # Debug print
        print(f"Step {i+1}: Placing item {item}")

        if sum(bins[-1]) + item <= capacity:
            bins[-1].append(item)
            print(f"  → Added to bin {len(bins)}")
        else:
            bins.append([item])
            print(f"  → Created new bin {len(bins)}")

    return bins
```

### Validate Intermediate State
```python
def MyAlgorithm(items, capacity):
    bins = []

    for item in items:
        # Your logic...

        # Validate after each item
        for bin_items in bins:
            assert sum(bin_items) <= capacity, "Bin exceeds capacity!"

    return bins
```

## Homework Assignment Template

For instructors - give students this template:

```python
"""
Homework: Bin Packing Algorithm
Student: [Your Name]
Date: [Date]
"""

def MyBinPackingAlgorithm(items, capacity):
    """
    TODO: Describe your algorithm here

    Strategy:
    - [Explain how your algorithm decides which bin to use]
    - [Explain when it creates a new bin]
    - [Explain any optimizations or special cases]

    Time Complexity: TODO - analyze your algorithm
    Space Complexity: TODO - analyze memory usage
    """

    # TODO: Implement your algorithm here
    bins = []

    return bins


# Metadata
ALGORITHM_NAME = "TODO: Give your algorithm a name"
ALGORITHM_DESCRIPTION = "TODO: Brief description"
COMPLEXITY = "TODO: O(?)"


# Test cases (for your own testing)
if __name__ == "__main__":
    test_cases = [
        ([4, 6, 3, 7], 10),
        ([5, 5, 5, 5], 10),
        ([4, 4, 5, 5, 5, 4, 4, 6], 10)
    ]

    for items, capacity in test_cases:
        result = MyBinPackingAlgorithm(items, capacity)
        print(f"Items: {items}, Capacity: {capacity}")
        print(f"Result: {result}")
        print(f"Bins used: {len([b for b in result if b])}")
        print()
```

## API Endpoints for Custom Algorithms

### Validate Algorithm
```http
POST /api/custom/validate
Content-Type: application/json

{
  "code": "def MyAlgo(items, capacity): ..."
}

Response:
{
  "valid": true,
  "message": "Algorithm validated successfully!",
  "bins_used": 3,
  "algorithm_name": "MyAlgo"
}
```

### Run Algorithm
```http
POST /api/custom/run
Content-Type: application/json

{
  "code": "def MyAlgo(items, capacity): ...",
  "capacity": 10,
  "items": [4, 5, 6, 3, 7]
}

Response:
{
  "session_id": "abc123...",
  "algorithm_name": "MyAlgo",
  "state": {...}
}
```

### Load from File
```http
POST /api/custom/load-file
Content-Type: application/json

{
  "filename": "my_algorithm.py"
}

Response:
{
  "session_id": "abc123...",
  "algorithm_name": "My Algorithm"
}
```

## Summary

**For Students:**
1. Write a simple function: `def MyAlgo(items, capacity): ...`
2. Return list of bins: `[[4, 5], [6, 3]]`
3. Test it: `python test_my_algorithm.py`
4. Submit to instructor or run in web app!

**No framework knowledge required! Just pure Python logic.**

---

Questions? Check `example_student_algorithm.py` for a working example!
