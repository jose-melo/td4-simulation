# Next Fit Algorithm - Complete Guide

## Overview

**Next Fit (NF)** is the fastest bin packing algorithm with **O(N)** time complexity. Unlike First Fit and Best Fit which check multiple bins, Next Fit only considers the most recently opened bin.

## Algorithm Description

### Strategy
```
For each item:
    If item fits in CURRENT bin:
        Place it there
    Else:
        Create NEW bin
        Make it the current bin
        Place item there
        NEVER go back to previous bins!
```

### Key Characteristic
🔑 **Only checks ONE bin per item** - the most recent one!

## Time Complexity

### Next Fit: O(N)
```python
for item in items:              # N iterations
    check_current_bin()         # O(1) - only one bin!
    possibly_create_new_bin()   # O(1)

Total: O(N)
```

### Compare to Others
- **First Fit**: O(N²) - checks up to N bins for each item
- **Best Fit**: O(N²) - checks ALL bins for each item
- **Next Fit**: O(N) - checks only 1 bin for each item ⚡

## Performance Characteristics

### Advantages ✅
1. **Fastest algorithm** - O(N) linear time
2. **Simplest logic** - easy to understand and implement
3. **Low memory overhead** - only tracks current bin
4. **Cache-friendly** - always working with recent data
5. **Online algorithm** - doesn't need to know future items

### Disadvantages ❌
1. **Uses more bins** - typically the worst packing
2. **Can't backtrack** - once you move to a new bin, can't go back
3. **Wastes space** - may create new bins when old ones have room
4. **No global optimization** - makes purely local decisions

## Example Walkthrough

### Example 1: Simple Case
```
Capacity: 10
Items: [4, 6, 3, 7]

Step 1: Item 4
  - No bins exist → Create Bin #1
  - Bin #1: [4] (4/10) ← CURRENT

Step 2: Item 6
  - Current bin: 4 + 6 = 10 ≤ 10 ✓
  - Bin #1: [4, 6] (10/10) ← CURRENT

Step 3: Item 3
  - Current bin: 10 + 3 = 13 > 10 ✗
  - Create Bin #2
  - Bin #1: [4, 6] (FULL, can't use anymore!)
  - Bin #2: [3] (3/10) ← CURRENT

Step 4: Item 7
  - Current bin: 3 + 7 = 10 ≤ 10 ✓
  - Bin #2: [3, 7] (10/10) ← CURRENT

Result: 2 bins (100% efficiency)
```

### Example 2: Worst Case
```
Capacity: 10
Items: [6, 4, 6, 4, 6, 4]

Step 1-2: Items 6, 4
  - Bin #1: [6, 4] (10/10) ← CURRENT

Step 3: Item 6
  - Current: 10 + 6 > 10 ✗
  - Create Bin #2
  - Bin #1: [6, 4] ← CAN'T GO BACK!
  - Bin #2: [6] (6/10) ← CURRENT

Step 4: Item 4
  - Current: 6 + 4 = 10 ✓
  - Bin #2: [6, 4] (10/10) ← CURRENT

Step 5-6: Items 6, 4
  - Same pattern...
  - Bin #3: [6, 4] (10/10)

Result: 3 bins
Note: First Fit and Best Fit also use 3 bins here!
```

### Example 3: Next Fit Weakness
```
Capacity: 10
Items: [5, 5, 5, 3, 3, 3]

Next Fit:
  Bin #1: [5, 5] (10/10)
  Bin #2: [5, 3, 3] ← Could fit in Bin #1 but can't go back!
  Bin #3: [3] (3/10)
  Total: 3 bins (73% efficiency)

First Fit or Best Fit:
  Bin #1: [5, 5] (10/10)
  Bin #2: [5, 3] (8/10)
  Bin #3: [3, 3] (6/10)
  Total: 3 bins (same bins but different packing)

Optimal:
  Bin #1: [5, 5] (10/10)
  Bin #2: [5, 3, 3, 3] (would need capacity 14)
  Actually optimal is also 3 bins for capacity 10
```

## Comparison with Other Algorithms

### Demo Data Results
```
Capacity: 10
Items: [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

┌────────────┬──────┬────────────┬─────────────┐
│ Algorithm  │ Bins │ Efficiency │ Complexity  │
├────────────┼──────┼────────────┼─────────────┤
│ Next Fit   │  14  │   78.6%    │   O(N)  ⚡  │
│ First Fit  │  13  │   84.6%    │   O(N²)     │
│ Best Fit   │  12  │   91.7%    │   O(N²)     │
│ Optimal    │  11  │   100%     │   O(2^N)    │
└────────────┴──────┴────────────┴─────────────┘

Analysis:
- Next Fit: +3 bins over optimal (27% overhead)
- First Fit: +2 bins over optimal (18% overhead)
- Best Fit: +1 bin over optimal (9% overhead)
```

### Trade-off Summary
```
Speed vs Quality:

Next Fit:  ████████████████████ Fast (O(N))
           ████████░░░░░░░░░░░░ Quality (78.6%)

First Fit: ██████████░░░░░░░░░░ Fast (O(N²))
           ████████████░░░░░░░░ Quality (84.6%)

Best Fit:  █████░░░░░░░░░░░░░░░ Fast (O(N²))
           ████████████████░░░░ Quality (91.7%)
```

## When to Use Next Fit

### ✅ Good For:
- **Real-time systems** - need constant-time guarantees
- **Streaming data** - items arrive one at a time
- **Very large datasets** - billions of items
- **Resource-constrained** - limited CPU/memory
- **First approximation** - quick initial solution
- **Time-critical** - speed is more important than quality

### ❌ Not Good For:
- **Optimal packing needed** - use exact algorithms
- **Small datasets** - overhead of O(N²) is acceptable
- **Offline packing** - all items known in advance
- **High utilization required** - need better efficiency
- **Cost of bins is high** - each extra bin is expensive

## Visual Example in Web App

When you select Next Fit in the web app, you'll see:

1. **Yellow glow on ONLY the last bin** (current bin)
   - Never glows on earlier bins!

2. **Red border when item doesn't fit**
   - New bin created immediately

3. **Explanation shows**: "Only checking current Bin #X"

4. **Notice**: Earlier bins may have space, but are ignored!

## Code Implementation

### Python (from your code)
```python
def NextFit(O, B):
    Aff = [[]]  # Start with one empty bin

    for o in O:
        if sum(Aff[-1]) + o > B:  # Check ONLY last bin
            Aff.append([o])        # Create new bin
        else:
            Aff[-1].append(o)      # Add to current bin

    return Aff
```

### Our Implementation (OOP)
```python
class NextFit(BinPackingAlgorithm):
    def _place_item(self, item, item_index):
        # Only check the LAST bin (current bin)
        current_bin_idx = len(self.bins) - 1
        current_bin = self.bins[current_bin_idx]

        if current_bin.can_fit(item, self.capacity):
            current_bin.items.append(item)  # Fits!
        else:
            new_bin = BinState(items=[item])  # New bin
            self.bins.append(new_bin)
```

## Performance Guarantees

### Approximation Ratio
Next Fit has a **2-approximation** guarantee:
```
NF(I) ≤ 2 × OPT(I)

Where:
- NF(I) = bins used by Next Fit
- OPT(I) = optimal number of bins

Example:
- If optimal uses 10 bins
- Next Fit uses at most 20 bins
```

### Proof Sketch
1. Every pair of consecutive bins is more than half full
2. If we use N bins, sum of items > (N/2) × capacity
3. Therefore N ≤ 2 × (sum of items / capacity)
4. OPT ≥ (sum of items / capacity)
5. So N ≤ 2 × OPT

## Educational Value

### For Students

**Learning Objectives:**
1. Understand time complexity trade-offs
2. See greedy algorithms in action
3. Learn about online vs offline algorithms
4. Observe local vs global optimization

**Exercises:**
1. Find input where NF uses 2× optimal bins
2. Compare NF vs FF on same input
3. Measure actual runtime difference
4. Identify when NF = FF = BF

### For Instructors

**Teaching Points:**
1. **Complexity Analysis**: Show O(N) vs O(N²) practically
2. **Trade-offs**: Speed vs quality discussion
3. **Real-world**: When is "fast enough" good enough?
4. **Streaming**: Introduce online algorithm concepts

## Testing

### Run Tests
```bash
# Algorithm test
python test_next_fit.py

# API test
python test_next_fit_api.py

# Web app test
# Select "Next Fit (NF) - O(N) ⚡" in browser
```

### Expected Results
```
Demo data (24 items):
- 14 bins
- 78.6% efficiency
- Completes in O(N) time
```

## Frequently Asked Questions

**Q: Why can't Next Fit go back to previous bins?**
A: That's the algorithm's defining characteristic! It only maintains a pointer to the "current" bin, making it O(1) per item instead of O(N).

**Q: Is Next Fit always worse than First Fit?**
A: Usually, but not always! Sometimes they use the same number of bins (see test examples).

**Q: When would I actually use Next Fit?**
A: In real-time systems where you need guaranteed O(N) time, or when dealing with billions of items where O(N²) is too slow.

**Q: Can Next Fit ever be optimal?**
A: Yes! If the input is carefully ordered, NF can achieve optimal packing. Example: [5,5,4,4,3,3,2,2] with capacity 10.

**Q: What's the worst-case for Next Fit?**
A: Alternating large and small items, like [7,3,7,3,7,3] with capacity 10. Each pair fills a bin, but NF can't optimize.

## Summary

Next Fit is the **fastest but least efficient** bin packing algorithm:

**Pros:**
- ⚡ O(N) linear time
- 💡 Simple to understand
- 📊 2-approximation guarantee
- 🎯 Good for streaming data

**Cons:**
- 📦 Uses more bins than FF or BF
- ⬅️ Can't backtrack to previous bins
- 💸 Lower space efficiency
- 🎲 No global optimization

**Perfect for learning about algorithm trade-offs!**

---

Try it in the web app: http://localhost:5001
Select "Next Fit (NF) - O(N) ⚡" and watch how it only checks the current bin!
