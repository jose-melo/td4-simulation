#!/usr/bin/env python3
"""
Bin Packing Problem Simulator - Educational Tool
Implements First Fit and Best Fit greedy algorithms with visual ASCII representation.
"""

from typing import List, Tuple
import os
import time


class BinPackingSimulator:
    """
    Interactive simulator for the Bin Packing Problem.

    Time Complexity: O(N * M) where N is the number of items and M is the number of bins.
    In worst case, M can be N, making it O(N^2).
    """

    def __init__(self, capacity: int, items: List[int]):
        """
        Initialize the simulator with bin capacity and items to pack.

        Args:
            capacity: Maximum capacity of each bin
            items: List of item sizes to pack
        """
        self.capacity = capacity
        self.items = items
        self.bins: List[List[int]] = []
        self.algorithm_name = ""

    def clear_screen(self) -> None:
        """Clear the terminal screen for better visualization."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def draw_bin(self, bin_items: List[int], bin_number: int) -> str:
        """
        Draw a single bin as ASCII art with vertical visualization.

        Args:
            bin_items: List of items in this bin
            bin_number: The bin number (1-indexed for display)

        Returns:
            String representation of the bin
        """
        current_capacity = sum(bin_items)
        remaining = self.capacity - current_capacity

        # Create visual representation
        lines = []
        lines.append(f"  Bin #{bin_number}")
        lines.append("  ┌────────┐")

        # Draw empty space at top
        if remaining > 0:
            for _ in range(remaining):
                lines.append("  │        │")

        # Draw items from top to bottom (stack)
        for item in bin_items:
            for _ in range(item):
                lines.append("  │████████│")

        lines.append("  └────────┘")
        lines.append(f"  {current_capacity}/{self.capacity}")

        return "\n".join(lines)

    def visualize_bins(self, current_item: int = None, item_index: int = None) -> None:
        """
        Display all bins side by side with current state.

        Args:
            current_item: The item currently being placed (if any)
            item_index: Index of current item in the list
        """
        self.clear_screen()

        print("=" * 80)
        print(f"BIN PACKING SIMULATOR - {self.algorithm_name}")
        print("=" * 80)

        if current_item is not None and item_index is not None:
            print(f"\nPlacing item #{item_index + 1}: Size = {current_item}")
            print(f"Items remaining: {len(self.items) - item_index - 1}")

        print(f"\nTotal bins used: {len(self.bins)}")
        print()

        if not self.bins:
            print("  No bins created yet.")
            return

        # Create visual representation of all bins
        bin_visuals = []
        for i, bin_items in enumerate(self.bins):
            bin_visuals.append(self.draw_bin(bin_items, i + 1).split('\n'))

        # Print bins side by side
        max_height = max(len(visual) for visual in bin_visuals)

        for row_idx in range(max_height):
            row_parts = []
            for bin_visual in bin_visuals:
                if row_idx < len(bin_visual):
                    row_parts.append(bin_visual[row_idx])
                else:
                    row_parts.append(" " * 12)  # Empty space for shorter bins
            print("  ".join(row_parts))

        print("\n" + "=" * 80)

    def first_fit(self, item: int) -> int:
        """
        First Fit Algorithm: Place item in the first bin where it fits.

        Time Complexity: O(M) where M is the number of bins (worst case O(N)).

        Args:
            item: Size of the item to place

        Returns:
            Index of the bin where item was placed
        """
        # Try to fit in existing bins
        for i, bin_items in enumerate(self.bins):
            if sum(bin_items) + item <= self.capacity:
                self.bins[i].append(item)
                return i

        # If no bin found, create a new one
        self.bins.append([item])
        return len(self.bins) - 1

    def best_fit(self, item: int) -> int:
        """
        Best Fit Algorithm: Place item in the bin with least remaining space after placement.

        Time Complexity: O(M) where M is the number of bins (worst case O(N)).

        Args:
            item: Size of the item to place

        Returns:
            Index of the bin where item was placed
        """
        best_bin_idx = -1
        min_remaining_space = self.capacity + 1

        # Find the bin with minimum remaining space after placing the item
        for i, bin_items in enumerate(self.bins):
            current_capacity = sum(bin_items)
            if current_capacity + item <= self.capacity:
                remaining_space = self.capacity - (current_capacity + item)
                if remaining_space < min_remaining_space:
                    min_remaining_space = remaining_space
                    best_bin_idx = i

        # If found a suitable bin, place the item
        if best_bin_idx != -1:
            self.bins[best_bin_idx].append(item)
            return best_bin_idx

        # Otherwise, create a new bin
        self.bins.append([item])
        return len(self.bins) - 1

    def run_simulation(self, algorithm: str, step_by_step: bool = True) -> None:
        """
        Run the bin packing simulation with the chosen algorithm.

        Overall Time Complexity: O(N^2) where N is the number of items.
        Each of the N items requires checking up to N bins in worst case.

        Args:
            algorithm: Either 'ff' for First Fit or 'bf' for Best Fit
            step_by_step: If True, pause after each item placement
        """
        self.bins = []
        self.algorithm_name = "FIRST FIT" if algorithm == 'ff' else "BEST FIT"

        for idx, item in enumerate(self.items):
            # Place the item using the chosen algorithm
            if algorithm == 'ff':
                bin_idx = self.first_fit(item)
            else:  # bf
                bin_idx = self.best_fit(item)

            # Visualize the current state
            self.visualize_bins(item, idx)

            print(f"Item {item} placed in Bin #{bin_idx + 1}")

            if step_by_step and idx < len(self.items) - 1:
                input("\nPress Enter to place next item...")

        # Final summary
        print("\n" + "=" * 80)
        print("SIMULATION COMPLETE!")
        print("=" * 80)
        print(f"Algorithm: {self.algorithm_name}")
        print(f"Total items packed: {len(self.items)}")
        print(f"Total bins used: {len(self.bins)}")
        print(f"Bin capacity: {self.capacity}")

        # Show bin utilization
        print("\nBin Utilization:")
        for i, bin_items in enumerate(self.bins):
            utilization = (sum(bin_items) / self.capacity) * 100
            print(f"  Bin #{i + 1}: {sum(bin_items)}/{self.capacity} ({utilization:.1f}%) - Items: {bin_items}")

        total_items_size = sum(self.items)
        total_capacity_used = len(self.bins) * self.capacity
        overall_efficiency = (total_items_size / total_capacity_used) * 100
        print(f"\nOverall Efficiency: {overall_efficiency:.1f}%")
        print("=" * 80)


def demo_mode() -> None:
    """
    Run the demo mode with the specific instance from the lecture slides.

    Demo Data:
        Capacity (B): 10
        Items (O): [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]
    """
    CAPACITY = 10
    ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

    print("\n" + "=" * 80)
    print("BIN PACKING PROBLEM - DEMO MODE")
    print("=" * 80)
    print(f"\nBin Capacity: {CAPACITY}")
    print(f"Items to pack: {ITEMS}")
    print(f"Number of items: {len(ITEMS)}")
    print(f"Total size: {sum(ITEMS)}")
    print(f"Minimum bins needed (theoretical): {sum(ITEMS) / CAPACITY:.1f}")
    print("\n" + "=" * 80)

    print("\nSelect Algorithm:")
    print("  1. First Fit (FF)")
    print("  2. Best Fit (BF)")
    print("  3. Run both and compare")

    choice = input("\nEnter your choice (1/2/3): ").strip()

    step_by_step = input("\nStep-by-step mode? (y/n): ").strip().lower() == 'y'

    if choice == '1':
        simulator = BinPackingSimulator(CAPACITY, ITEMS)
        simulator.run_simulation('ff', step_by_step)
    elif choice == '2':
        simulator = BinPackingSimulator(CAPACITY, ITEMS)
        simulator.run_simulation('bf', step_by_step)
    elif choice == '3':
        # Run First Fit
        print("\n\nRunning FIRST FIT algorithm...")
        time.sleep(1)
        simulator_ff = BinPackingSimulator(CAPACITY, ITEMS)
        simulator_ff.run_simulation('ff', step_by_step)
        ff_bins = len(simulator_ff.bins)

        input("\nPress Enter to run Best Fit...")

        # Run Best Fit
        print("\n\nRunning BEST FIT algorithm...")
        time.sleep(1)
        simulator_bf = BinPackingSimulator(CAPACITY, ITEMS)
        simulator_bf.run_simulation('bf', step_by_step)
        bf_bins = len(simulator_bf.bins)

        # Comparison
        print("\n" + "=" * 80)
        print("ALGORITHM COMPARISON")
        print("=" * 80)
        print(f"First Fit: {ff_bins} bins")
        print(f"Best Fit:  {bf_bins} bins")

        if ff_bins < bf_bins:
            print(f"\nFirst Fit performed better by {bf_bins - ff_bins} bin(s)!")
        elif bf_bins < ff_bins:
            print(f"\nBest Fit performed better by {ff_bins - bf_bins} bin(s)!")
        else:
            print("\nBoth algorithms used the same number of bins!")
        print("=" * 80)
    else:
        print("Invalid choice!")


def custom_mode() -> None:
    """Allow users to input their own bin capacity and items."""
    print("\n" + "=" * 80)
    print("BIN PACKING PROBLEM - CUSTOM MODE")
    print("=" * 80)

    try:
        capacity = int(input("\nEnter bin capacity: "))
        items_input = input("Enter items (space-separated, e.g., '4 5 6 2 3'): ")
        items = [int(x) for x in items_input.split()]

        if any(item > capacity for item in items):
            print("\nError: Some items are larger than bin capacity!")
            return

        print("\nSelect Algorithm:")
        print("  1. First Fit (FF)")
        print("  2. Best Fit (BF)")

        choice = input("\nEnter your choice (1/2): ").strip()
        step_by_step = input("Step-by-step mode? (y/n): ").strip().lower() == 'y'

        algorithm = 'ff' if choice == '1' else 'bf'
        simulator = BinPackingSimulator(capacity, items)
        simulator.run_simulation(algorithm, step_by_step)

    except ValueError:
        print("\nError: Invalid input format!")


def main() -> None:
    """Main entry point for the Bin Packing Simulator."""
    while True:
        print("\n" + "=" * 80)
        print("BIN PACKING PROBLEM - INTERACTIVE SIMULATOR")
        print("Educational Tool for Learning Greedy Algorithms")
        print("=" * 80)
        print("\nModes:")
        print("  1. Demo Mode (Lecture Slide Instance)")
        print("  2. Custom Mode (Your Own Data)")
        print("  3. Exit")

        choice = input("\nSelect mode (1/2/3): ").strip()

        if choice == '1':
            demo_mode()
        elif choice == '2':
            custom_mode()
        elif choice == '3':
            print("\nThank you for using the Bin Packing Simulator!")
            break
        else:
            print("\nInvalid choice! Please try again.")

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    main()
