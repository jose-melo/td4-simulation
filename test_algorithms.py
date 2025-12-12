"""
Quick test script for algorithms module
"""

from algorithms import create_algorithm

# Test data
CAPACITY = 10
ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

print("=" * 60)
print("Testing Bin Packing Algorithms")
print("=" * 60)

# Test First Fit
print("\n1. Testing First Fit Algorithm")
print("-" * 60)
ff_algo = create_algorithm('ff', CAPACITY, ITEMS)

step_count = 0
while True:
    result = ff_algo.step()
    if result is None:
        break
    step_count += 1
    print(f"Step {step_count}: Item {result.item} -> Bin #{result.bin_index + 1}")

stats_ff = ff_algo.get_statistics()
print(f"\nFirst Fit Results:")
print(f"  Bins used: {stats_ff['bins_used']}")
print(f"  Efficiency: {stats_ff['efficiency']}%")

# Test Best Fit
print("\n2. Testing Best Fit Algorithm")
print("-" * 60)
bf_algo = create_algorithm('bf', CAPACITY, ITEMS)

step_count = 0
while True:
    result = bf_algo.step()
    if result is None:
        break
    step_count += 1
    print(f"Step {step_count}: Item {result.item} -> Bin #{result.bin_index + 1}")

stats_bf = bf_algo.get_statistics()
print(f"\nBest Fit Results:")
print(f"  Bins used: {stats_bf['bins_used']}")
print(f"  Efficiency: {stats_bf['efficiency']}%")

# Compare
print("\n" + "=" * 60)
print("Comparison")
print("=" * 60)
print(f"First Fit: {stats_ff['bins_used']} bins ({stats_ff['efficiency']}% efficient)")
print(f"Best Fit:  {stats_bf['bins_used']} bins ({stats_bf['efficiency']}% efficient)")

if stats_ff['bins_used'] < stats_bf['bins_used']:
    print("\nFirst Fit performed better!")
elif stats_bf['bins_used'] < stats_ff['bins_used']:
    print("\nBest Fit performed better!")
else:
    print("\nBoth algorithms performed equally!")

print("=" * 60)
print("Algorithm tests completed successfully!")
print("=" * 60)
