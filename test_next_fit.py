"""
Test Next Fit Algorithm - O(N) complexity
"""

from algorithms import create_algorithm

# Test data
CAPACITY = 10
ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

print("=" * 60)
print("Testing Next Fit Algorithm - O(N)")
print("=" * 60)

# Test Next Fit
print("\n1. Testing Next Fit (NF)")
print("-" * 60)
nf_algo = create_algorithm('nf', CAPACITY, ITEMS)

step_count = 0
while True:
    result = nf_algo.step()
    if result is None:
        break
    step_count += 1
    print(f"Step {step_count}: Item {result.item} -> Bin #{result.bin_index + 1} " +
          f"{'(NEW)' if result.is_new_bin else '(current)'}")

stats_nf = nf_algo.get_statistics()
print(f"\nNext Fit Results:")
print(f"  Bins used: {stats_nf['bins_used']}")
print(f"  Efficiency: {stats_nf['efficiency']}%")
print(f"  Bin details:")
for bin_detail in stats_nf['bin_details']:
    print(f"    Bin #{bin_detail['bin_number']}: {bin_detail['items']} = " +
          f"{bin_detail['capacity']}/{CAPACITY}")

# Compare with FF and BF
print("\n" + "=" * 60)
print("Comparison: Next Fit vs First Fit vs Best Fit")
print("=" * 60)

ff_algo = create_algorithm('ff', CAPACITY, ITEMS)
while ff_algo.step() is not None:
    pass
stats_ff = ff_algo.get_statistics()

bf_algo = create_algorithm('bf', CAPACITY, ITEMS)
while bf_algo.step() is not None:
    pass
stats_bf = bf_algo.get_statistics()

print(f"Next Fit:  {stats_nf['bins_used']} bins ({stats_nf['efficiency']}% efficient) - O(N)")
print(f"First Fit: {stats_ff['bins_used']} bins ({stats_ff['efficiency']}% efficient) - O(N²)")
print(f"Best Fit:  {stats_bf['bins_used']} bins ({stats_bf['efficiency']}% efficient) - O(N²)")

print("\nAnalysis:")
theoretical_min = -(-sum(ITEMS) // CAPACITY)  # Ceiling division
print(f"  Theoretical minimum: {theoretical_min} bins")
print(f"  Next Fit overhead: +{stats_nf['bins_used'] - theoretical_min} bins")
print(f"  First Fit overhead: +{stats_ff['bins_used'] - theoretical_min} bins")
print(f"  Best Fit overhead: +{stats_bf['bins_used'] - theoretical_min} bins")

# Test with simple example
print("\n" + "=" * 60)
print("Simple Example: [4, 6, 3, 7] with capacity 10")
print("=" * 60)

simple_items = [4, 6, 3, 7]

nf_simple = create_algorithm('nf', 10, simple_items)
ff_simple = create_algorithm('ff', 10, simple_items)
bf_simple = create_algorithm('bf', 10, simple_items)

while nf_simple.step() is not None:
    pass
while ff_simple.step() is not None:
    pass
while bf_simple.step() is not None:
    pass

print(f"Next Fit:  {len(nf_simple.bins)} bins - {nf_simple.bins}")
print(f"First Fit: {len(ff_simple.bins)} bins - {ff_simple.bins}")
print(f"Best Fit:  {len(bf_simple.bins)} bins - {bf_simple.bins}")

# Test worst case for Next Fit
print("\n" + "=" * 60)
print("Worst Case for Next Fit: [6, 4, 6, 4, 6, 4]")
print("=" * 60)

worst_case = [6, 4, 6, 4, 6, 4]

nf_worst = create_algorithm('nf', 10, worst_case)
ff_worst = create_algorithm('ff', 10, worst_case)
bf_worst = create_algorithm('bf', 10, worst_case)

print("\nNext Fit execution:")
step = 0
while True:
    result = nf_worst.step()
    if result is None:
        break
    step += 1
    print(f"  Step {step}: Item {result.item} -> Bin #{result.bin_index + 1} " +
          f"{'(NEW - can\'t go back!)' if result.is_new_bin else '(fits in current)'}")

while ff_worst.step() is not None:
    pass
while bf_worst.step() is not None:
    pass

print(f"\nNext Fit:  {len(nf_worst.bins)} bins - {[bin.items for bin in nf_worst.bins]}")
print(f"First Fit: {len(ff_worst.bins)} bins - {[bin.items for bin in ff_worst.bins]}")
print(f"Best Fit:  {len(bf_worst.bins)} bins - {[bin.items for bin in bf_worst.bins]}")
print("\nNote: Next Fit can't go back to previous bins!")

print("\n" + "=" * 60)
print("Next Fit algorithm tests completed!")
print("=" * 60)
