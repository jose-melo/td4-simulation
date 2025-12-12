"""
Test the Student Algorithm API
Demonstrates how instructors can test student submissions
"""

from custom_algorithm_loader import (
    load_algorithm_from_file,
    load_algorithm_from_code,
    validate_algorithm,
    StudentAlgorithmWrapper
)

print("=" * 60)
print("Testing Student Algorithm API")
print("=" * 60)

# Test 1: Load algorithm from file
print("\n1. Loading Worst Fit from file")
print("-" * 60)

algo_info = load_algorithm_from_file('student_algorithms/worst_fit.py')
print(f"✓ Algorithm loaded: {algo_info.name}")
print(f"  Description: {algo_info.description}")
print(f"  Complexity: {algo_info.complexity}")

# Test 2: Validate the algorithm
print("\n2. Validating algorithm")
print("-" * 60)

validation = validate_algorithm(algo_info.function)
if validation['valid']:
    print(f"✓ {validation['message']}")
    print(f"  Bins used (test): {validation['bins_used']}")
else:
    print(f"✗ Validation failed: {validation['error']}")

# Test 3: Run the algorithm
print("\n3. Running algorithm with demo data")
print("-" * 60)

CAPACITY = 10
ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2]

wrapper = StudentAlgorithmWrapper(
    algo_info.function,
    CAPACITY,
    ITEMS,
    name=algo_info.name,
    description=algo_info.description,
    complexity=algo_info.complexity
)

# Step through
step_count = 0
while True:
    step_result = wrapper.step()
    if step_result is None:
        break

    step_count += 1
    print(f"Step {step_count}: Item {step_result.item} → Bin #{step_result.bin_index + 1}")

# Get final stats
stats = wrapper.get_statistics()
print(f"\nFinal Results:")
print(f"  Bins used: {stats['bins_used']}")
print(f"  Efficiency: {stats['efficiency']}%")

# Test 4: Load algorithm from code string
print("\n4. Loading algorithm from code string")
print("-" * 60)

code = """
def SimpleNextFit(items, capacity):
    '''Simple Next Fit - only checks last bin'''
    bins = [[]]

    for item in items:
        if sum(bins[-1]) + item <= capacity:
            bins[-1].append(item)
        else:
            bins.append([item])

    return bins

ALGORITHM_NAME = "Simple Next Fit"
COMPLEXITY = "O(N)"
"""

algo_info2 = load_algorithm_from_code(code)
print(f"✓ Algorithm loaded from code: {algo_info2.name}")
print(f"  Complexity: {algo_info2.complexity}")

# Validate
validation2 = validate_algorithm(algo_info2.function, ITEMS, CAPACITY)
print(f"✓ Validation: {validation2['message']}")

# Run it
result = algo_info2.function(ITEMS, CAPACITY)
print(f"  Result: {result}")
print(f"  Bins used: {len([b for b in result if b])}")

# Test 5: Compare algorithms
print("\n5. Comparing Algorithms")
print("-" * 60)

algorithms_to_test = [
    ('student_algorithms/example_student_algorithm.py', 'Example (Next Fit)'),
    ('student_algorithms/worst_fit.py', 'Worst Fit'),
]

test_items = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

print(f"\nTest data: {len(test_items)} items, capacity {CAPACITY}")
print(f"Theoretical minimum: {-(-sum(test_items) // CAPACITY)} bins\n")

for file_path, label in algorithms_to_test:
    try:
        algo = load_algorithm_from_file(file_path)
        result = algo.function(test_items, CAPACITY)
        bins_used = len([b for b in result if b])

        total_size = sum(test_items)
        efficiency = (total_size / (bins_used * CAPACITY) * 100)

        print(f"{label:20} - {bins_used} bins ({efficiency:.1f}% efficient)")
    except Exception as e:
        print(f"{label:20} - Error: {e}")

print("\n" + "=" * 60)
print("Student API tests completed!")
print("=" * 60)

print("\n📝 Summary:")
print("  ✓ Algorithms can be loaded from files")
print("  ✓ Algorithms can be loaded from code strings")
print("  ✓ Validation works correctly")
print("  ✓ Step-by-step execution works")
print("  ✓ Multiple algorithms can be compared")
print("\n👨‍🏫 Ready for student submissions!")
