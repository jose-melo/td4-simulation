#!/usr/bin/env python3
"""
Quick demo of the Bin Packing Simulator without interactive prompts.
Useful for testing or demonstrations.
"""

from bin_packing_simulator import BinPackingSimulator

# Demo data from lecture slides
CAPACITY = 10
ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

print("=" * 80)
print("QUICK DEMO: Comparing First Fit vs Best Fit")
print("=" * 80)
print(f"\nBin Capacity: {CAPACITY}")
print(f"Items: {ITEMS}")
print(f"Number of items: {len(ITEMS)}")
print(f"Total size: {sum(ITEMS)}")
print(f"Theoretical minimum bins: {sum(ITEMS) / CAPACITY:.1f}")

# Test First Fit
print("\n\n" + "=" * 80)
print("RUNNING FIRST FIT ALGORITHM (non-interactive)")
print("=" * 80)
simulator_ff = BinPackingSimulator(CAPACITY, ITEMS)
simulator_ff.run_simulation('ff', step_by_step=False)

input("\n\nPress Enter to run Best Fit...")

# Test Best Fit
print("\n\n" + "=" * 80)
print("RUNNING BEST FIT ALGORITHM (non-interactive)")
print("=" * 80)
simulator_bf = BinPackingSimulator(CAPACITY, ITEMS)
simulator_bf.run_simulation('bf', step_by_step=False)

# Comparison
print("\n\n" + "=" * 80)
print("COMPARISON")
print("=" * 80)
print(f"First Fit: {len(simulator_ff.bins)} bins")
print(f"Best Fit:  {len(simulator_bf.bins)} bins")

if len(simulator_ff.bins) < len(simulator_bf.bins):
    print(f"\nFirst Fit is better by {len(simulator_bf.bins) - len(simulator_ff.bins)} bin(s)!")
elif len(simulator_bf.bins) < len(simulator_ff.bins):
    print(f"\nBest Fit is better by {len(simulator_ff.bins) - len(simulator_bf.bins)} bin(s)!")
else:
    print("\nBoth algorithms achieved the same result!")

print("\n" + "=" * 80)
