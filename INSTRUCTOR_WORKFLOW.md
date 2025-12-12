# Instructor Workflow - Testing Student Algorithms

## Quick Workflow (Copy-Paste-Test)

### Step 1: Receive Student Code

Student submits their code (e.g., via email, LMS, or file):

```python
def StudentAlgorithm(items, capacity):
    bins = []
    # Student's implementation...
    return bins
```

### Step 2: Save the File

Save as `student_algorithms/student_name.py`

### Step 3: Test It

```bash
python -c "
from custom_algorithm_loader import load_algorithm_from_file, validate_algorithm

# Load
algo = load_algorithm_from_file('student_algorithms/student_name.py')

# Validate
result = validate_algorithm(algo.function)
print(f'Valid: {result[\"valid\"]}')
if result['valid']:
    print(f'Bins: {result[\"bins_used\"]}')
else:
    print(f'Error: {result[\"error\"]}')
"
```

Done! You now know if it works and how many bins it uses.

## Detailed Testing Workflow

### Option 1: Quick Validation Only

```python
from custom_algorithm_loader import load_algorithm_from_file, validate_algorithm

# Load student's file
algo_info = load_algorithm_from_file('student_algorithms/student_name.py')

# Quick validation
validation = validate_algorithm(algo_info.function)

if validation['valid']:
    print(f"✓ Code works! Uses {validation['bins_used']} bins")
else:
    print(f"✗ Error: {validation['error']}")
```

### Option 2: Full Testing with Demo Data

```python
from custom_algorithm_loader import load_algorithm_from_file

# Load
algo_info = load_algorithm_from_file('student_algorithms/student_name.py')

# Run with demo data
CAPACITY = 10
ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

result = algo_info.function(ITEMS, CAPACITY)

bins_used = len([b for b in result if b])
efficiency = (sum(ITEMS) / (bins_used * CAPACITY) * 100)

print(f"Algorithm: {algo_info.name}")
print(f"Bins used: {bins_used}")
print(f"Efficiency: {efficiency:.1f}%")
print(f"Result: {result}")
```

### Option 3: Compare with Reference Algorithms

```python
from custom_algorithm_loader import load_algorithm_from_file
from algorithms import create_algorithm

CAPACITY = 10
ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

# Student's algorithm
student = load_algorithm_from_file('student_algorithms/student_name.py')
student_bins = student.function(ITEMS, CAPACITY)

# Reference algorithms
ff = create_algorithm('ff', CAPACITY, ITEMS)
bf = create_algorithm('bf', CAPACITY, ITEMS)
nf = create_algorithm('nf', CAPACITY, ITEMS)

while ff.step(): pass
while bf.step(): pass
while nf.step(): pass

print(f"Student ({student.name}): {len(student_bins)} bins")
print(f"First Fit:  {len(ff.bins)} bins")
print(f"Best Fit:   {len(bf.bins)} bins")
print(f"Next Fit:   {len(nf.bins)} bins")
print(f"Optimal:    {-(-sum(ITEMS) // CAPACITY)} bins (theoretical)")
```

### Option 4: Visualize in Web App

```python
import requests

# Read student's file
with open('student_algorithms/student_name.py') as f:
    code = f.read()

# Load into web app
response = requests.post('http://localhost:5001/api/custom/run', json={
    'code': code
})

if response.status_code == 200:
    print(f"✓ Loaded into web app!")
    print(f"  Session ID: {response.json()['session_id']}")
    print(f"  Open: http://localhost:5001")
    print(f"  Now step through in the browser!")
else:
    print(f"✗ Error: {response.json()['error']}")
```

## Batch Testing Multiple Students

```python
from pathlib import Path
from custom_algorithm_loader import load_algorithm_from_file, validate_algorithm

students_dir = Path('student_algorithms')
results = []

for file in students_dir.glob('*.py'):
    if file.name in ['README.md', '__init__.py', 'example_student_algorithm.py']:
        continue

    try:
        # Load and validate
        algo = load_algorithm_from_file(str(file))
        validation = validate_algorithm(algo.function)

        if validation['valid']:
            # Run with demo data
            ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3]
            result = algo.function(ITEMS, 10)
            bins_used = len([b for b in result if b])

            results.append({
                'file': file.name,
                'name': algo.name,
                'bins': bins_used,
                'valid': True
            })
        else:
            results.append({
                'file': file.name,
                'error': validation['error'],
                'valid': False
            })

    except Exception as e:
        results.append({
            'file': file.name,
            'error': str(e),
            'valid': False
        })

# Print results
print("\nStudent Results:")
print("=" * 60)
for r in sorted(results, key=lambda x: x.get('bins', 999)):
    if r['valid']:
        print(f"{r['file']:30} → {r['bins']} bins")
    else:
        print(f"{r['file']:30} → Error: {r['error']}")
```

## Grading Rubric Example

```python
def grade_algorithm(student_file):
    """
    Grade student algorithm:
    - 40 points: Code works
    - 30 points: Bins used (fewer is better)
    - 20 points: Code quality
    - 10 points: Documentation
    """

    from custom_algorithm_loader import load_algorithm_from_file, validate_algorithm

    try:
        algo = load_algorithm_from_file(student_file)
        validation = validate_algorithm(algo.function)

        if not validation['valid']:
            return {'grade': 0, 'feedback': f"Code doesn't work: {validation['error']}"}

        # 40 points for working code
        grade = 40

        # 30 points based on bins used
        ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]
        result = algo.function(ITEMS, 10)
        bins_used = len([b for b in result if b])

        # Optimal is 11, acceptable is ≤ 14
        if bins_used <= 11:
            grade += 30  # Optimal
        elif bins_used <= 12:
            grade += 25  # Excellent
        elif bins_used <= 13:
            grade += 20  # Good
        elif bins_used <= 14:
            grade += 15  # Acceptable
        else:
            grade += 5   # Needs improvement

        # 20 points for code quality (manual review)
        # 10 points for documentation (manual review)

        return {
            'grade': grade,
            'bins_used': bins_used,
            'algorithm': algo.name,
            'feedback': f"Good! Used {bins_used} bins (optimal is 11)"
        }

    except Exception as e:
        return {'grade': 0, 'feedback': f"Error: {str(e)}"}


# Use it:
result = grade_algorithm('student_algorithms/student_name.py')
print(f"Grade: {result['grade']}/100")
print(f"Feedback: {result['feedback']}")
```

## Common Student Errors

### Error 1: Wrong Return Type
```python
# Student writes:
return {'bins': [[4, 5]]}  # ✗ Dictionary

# Should be:
return [[4, 5]]  # ✓ List of lists
```

**Auto-feedback:**
```python
if not isinstance(result, list):
    print("Error: Must return a list, not", type(result))
```

### Error 2: Exceeding Capacity
```python
# Student doesn't check capacity
bins.append(items)  # ✗ All items in one bin!
```

**Auto-feedback:**
```python
for i, bin_items in enumerate(result):
    if sum(bin_items) > capacity:
        print(f"Error: Bin #{i+1} exceeds capacity: {sum(bin_items)} > {capacity}")
```

### Error 3: Missing Items
```python
# Student skips some items
if item < 5:  # ✗ Only packs small items
    bins[-1].append(item)
```

**Auto-feedback:**
```python
items_placed = sum(len(b) for b in result)
if items_placed != len(items):
    print(f"Error: Placed {items_placed} items but have {len(items)}")
```

## Integration with LMS

### Automated Submission Handler

```python
def handle_submission(student_id, code_string):
    """
    Process student submission automatically.
    Can be integrated with Canvas, Moodle, etc.
    """

    from custom_algorithm_loader import load_algorithm_from_code, validate_algorithm

    try:
        # Load from code string
        algo = load_algorithm_from_code(code_string)

        # Validate
        validation = validate_algorithm(algo.function)

        if not validation['valid']:
            return {
                'student_id': student_id,
                'status': 'failed',
                'error': validation['error'],
                'grade': 0
            }

        # Run tests
        test_cases = [
            ([4, 6, 3, 7], 10, 2),  # (items, capacity, expected_bins)
            ([5, 5, 5, 5], 10, 2),
            ([4, 4, 5, 5, 5, 4], 10, 3)
        ]

        all_passed = True
        for items, capacity, expected in test_cases:
            result = algo.function(items, capacity)
            bins_used = len([b for b in result if b])
            if bins_used > expected + 1:  # Allow 1 extra bin
                all_passed = False

        return {
            'student_id': student_id,
            'status': 'passed' if all_passed else 'needs_improvement',
            'algorithm_name': algo.name,
            'bins_demo': validation['bins_used'],
            'grade': 100 if all_passed else 70
        }

    except Exception as e:
        return {
            'student_id': student_id,
            'status': 'error',
            'error': str(e),
            'grade': 0
        }
```

## Summary

**For instructors, the workflow is:**

1. **Receive student code** (file or string)
2. **Copy to `student_algorithms/`** directory
3. **Run validation**: `python test_student_api.py`
4. **View in browser**: Load in web app and step through
5. **Grade**: Compare with reference algorithms

**No framework knowledge needed from students!**
**Just pure Python functions.**

---

See `STUDENT_API_GUIDE.md` for student-facing documentation.
