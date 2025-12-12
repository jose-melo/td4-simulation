# Custom Input Feature - User Guide

## Overview

The Bin Packing Visualizer now supports **custom user input**, allowing you to test your own bin capacities and item sets in addition to the pre-loaded lecture demo data.

## How to Use Custom Input

### Step 1: Access the Web App

```bash
./run.sh
# or
python app.py
```

Then open: http://localhost:5001

### Step 2: Select Configuration Mode

At the top of the page, you'll see two options:

- **Use Demo Data (Lecture)** - Default lecture slides data
- **Custom Input** - Your own data

Click on **"Custom Input"** to enable custom data entry.

### Step 3: Enter Your Data

#### Bin Capacity
- Enter a number between 1 and 100
- Example: `10`, `15`, `20`

#### Items
Enter your items separated by spaces or commas:
- **Space-separated**: `4 5 6 7 8 3`
- **Comma-separated**: `4, 5, 6, 7, 8, 3`
- **Mixed**: `4, 5 6 7, 8 3`

**Requirements**:
- All items must be positive integers
- All items must be ≤ bin capacity
- At least one item required

### Step 4: Validate Input

Click the **"Validate Input"** button (or press Enter).

#### Success
You'll see a green message:
```
✓ Valid input: 6 items, capacity 10, total size 33
```

#### Error
You'll see a red message explaining the issue:
```
✗ Some items are larger than bin capacity (10)
```

### Step 5: Run Simulation

Once validated:
1. Select algorithm (First Fit or Best Fit)
2. Click **"Start"**
3. Use **"Next Step"** or **"Auto Play"**

## Examples

### Example 1: Perfect Fit
```
Capacity: 10
Items: 4 6 3 7

Result: 2 bins (100% efficiency)
- Bin #1: [4, 6] = 10/10
- Bin #2: [3, 7] = 10/10
```

### Example 2: Challenging Case
```
Capacity: 15
Items: 5 5 10 7 8 3

First Fit: 3 bins (84.4% efficiency)
Best Fit:  3 bins (84.4% efficiency)
```

### Example 3: Worst Case for First Fit
```
Capacity: 10
Items: 6 6 6 6 6 4 4 4 4 4

First Fit: More bins than optimal
Best Fit:  Better packing
```

### Example 4: Large Items
```
Capacity: 20
Items: 10 11 12 8 9 7

Theoretical minimum: ⌈57/20⌉ = 3 bins
```

## Validation Rules

### Capacity Validation
- ✅ Must be an integer
- ✅ Must be between 1 and 100
- ❌ Cannot be empty
- ❌ Cannot be negative

### Items Validation
- ✅ Positive integers only
- ✅ Separated by spaces or commas
- ✅ At least one item required
- ❌ No item can exceed capacity
- ❌ No negative numbers
- ❌ No decimals

## Error Messages Guide

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "Capacity must be between 1 and 100" | Invalid capacity | Enter a number 1-100 |
| "Please enter items" | Empty items field | Add at least one item |
| "All items must be positive integers" | Invalid item format | Use only positive integers |
| "Some items are larger than bin capacity (X)" | Item > capacity | Reduce item sizes or increase capacity |
| "Please validate your custom input first" | Tried to start without validating | Click "Validate Input" first |

## Switching Between Demo and Custom

### To Demo Data
1. Click **"Use Demo Data (Lecture)"** radio button
2. Demo data loads automatically
3. Previous custom input is preserved if you switch back

### To Custom Data
1. Click **"Custom Input"** radio button
2. Enter your data
3. Click **"Validate Input"**
4. Start simulation

## Tips for Testing

### Test Edge Cases
```
# Single item
Capacity: 10, Items: 5

# All items same size
Capacity: 10, Items: 5 5 5 5 5 5

# Items that don't fit well
Capacity: 10, Items: 7 7 7 7

# Perfect fit
Capacity: 10, Items: 2 2 2 2 2 3 3 3 3 3
```

### Compare Algorithms
1. Enter custom data
2. Validate
3. Run First Fit (note bins used)
4. Reset
5. Run Best Fit (compare results)

### Find Worst Cases
Try to find inputs where:
- First Fit uses many more bins than Best Fit
- Both algorithms are far from optimal
- One algorithm is exactly optimal

## Keyboard Shortcuts

- **Enter** in Items field → Validates input automatically
- **Tab** → Move between fields
- **Space/Comma** → Separate items

## API Usage (For Developers)

You can also use custom input via the API:

```python
import requests

response = requests.post('http://localhost:5001/api/start', json={
    'algorithm': 'ff',
    'capacity': 15,
    'items': [5, 5, 10, 7, 8, 3]
})
```

See `test_custom_input.py` for more examples.

## Educational Use Cases

### For Students

1. **Understanding Algorithms**
   - Test simple cases first: `[4, 6]` with capacity 10
   - See how each algorithm makes decisions

2. **Finding Edge Cases**
   - Try: `[7, 7, 7]` with capacity 10
   - Observe when algorithms differ

3. **Worst Case Analysis**
   - Find inputs where greedy fails badly
   - Compare to theoretical minimum

### For Instructors

1. **Live Demos**
   - Start with simple examples
   - Build complexity gradually
   - Show algorithm differences in real-time

2. **Homework Assignments**
   ```
   "Find an input where First Fit uses at least
   2 more bins than the theoretical minimum"
   ```

3. **Quiz Questions**
   ```
   "For capacity=10 and items=[6,4,8,2,3,7]:
   - How many bins does FF use?
   - How many bins does BF use?
   - What is the theoretical minimum?"
   ```

## Troubleshooting

### Input Not Accepting
- Check that you clicked **"Custom Input"** radio button
- Input fields should be enabled (not grayed out)

### Validation Fails
- Read error message carefully
- Check for typos or invalid characters
- Ensure all items ≤ capacity

### Can't Start Simulation
- Make sure you clicked **"Validate Input"** first
- Check for green success message
- If using demo mode, validation not needed

### Unexpected Results
- Remember: greedy algorithms are not optimal
- Theoretical minimum is ⌈total_size / capacity⌉
- Algorithms may use more bins than minimum

## Examples Gallery

### Optimal Packing
```
Capacity: 10
Items: 1 2 3 4 5 5 4 3 2 1
Both algorithms: 3 bins (100% efficiency)
```

### FF vs BF Difference
```
Capacity: 10
Items: 7 5 5 5 4 4 4
First Fit: 4 bins
Best Fit:  3 bins
```

### Large Dataset
```
Capacity: 100
Items: 45 45 30 30 25 25 20 20 15 15 10 10 5 5
Test scalability and efficiency
```

## Next Steps

After testing custom inputs:
1. Try the CLI tool for batch testing: `python bin_packing_simulator.py`
2. Read the algorithm source: `algorithms.py`
3. Implement your own algorithm variant
4. Explore the API: `FLASK_SETUP.md`

## Need Help?

- **Documentation**: See `README.md`, `FLASK_SETUP.md`, `ARCHITECTURE.md`
- **Examples**: Check `test_custom_input.py`
- **Issues**: Test in browser console (F12) for errors

---

Happy packing! 📦
