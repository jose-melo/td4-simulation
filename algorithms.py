"""
Bin Packing Algorithms - Pure Logic Layer
Separated from UI and framework code for better testability and reusability.
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class BinState:
    """Represents the state of a single bin."""
    items: List[int] = field(default_factory=list)

    @property
    def current_capacity(self) -> int:
        """Calculate current capacity used in this bin."""
        return sum(self.items)

    def can_fit(self, item: int, capacity: int) -> bool:
        """Check if an item can fit in this bin."""
        return self.current_capacity + item <= capacity

    def remaining_space(self, item: int, capacity: int) -> int:
        """Calculate remaining space after adding an item."""
        return capacity - (self.current_capacity + item)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'items': self.items,
            'current_capacity': self.current_capacity
        }


@dataclass
class StepResult:
    """Result of a single algorithm step."""
    item: int
    item_index: int
    bin_index: int
    bins_state: List[List[int]]
    explanation: str
    bins_checked: List[Dict]  # List of bins checked with their states
    is_new_bin: bool

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'item': self.item,
            'item_index': self.item_index,
            'bin_index': self.bin_index,
            'bins_state': self.bins_state,
            'explanation': self.explanation,
            'bins_checked': self.bins_checked,
            'is_new_bin': self.is_new_bin
        }


class BinPackingAlgorithm:
    """
    Base class for bin packing algorithms.

    Time Complexity: O(N * M) where N = items, M = bins
    Worst case: O(N²) when M approaches N
    """

    def __init__(self, capacity: int, items: List[int]):
        """
        Initialize the algorithm.

        Args:
            capacity: Maximum capacity of each bin
            items: List of items to pack
        """
        self.capacity = capacity
        self.items = items
        self.bins: List[BinState] = []
        self.current_index = -1

    def reset(self) -> None:
        """Reset the algorithm state."""
        self.bins = []
        self.current_index = -1

    def step(self) -> Optional[StepResult]:
        """
        Execute one step of the algorithm.

        Returns:
            StepResult if there are items remaining, None if complete
        """
        if self.current_index >= len(self.items) - 1:
            return None

        self.current_index += 1
        item = self.items[self.current_index]

        return self._place_item(item, self.current_index)

    def _place_item(self, item: int, item_index: int) -> StepResult:
        """
        Place an item using the specific algorithm.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get_statistics(self) -> Dict:
        """Calculate statistics about the current packing."""
        total_items_size = sum(self.items[:self.current_index + 1])
        total_capacity = len(self.bins) * self.capacity
        efficiency = (total_items_size / total_capacity * 100) if total_capacity > 0 else 0

        bin_stats = []
        for i, bin_state in enumerate(self.bins):
            utilization = (bin_state.current_capacity / self.capacity * 100)
            bin_stats.append({
                'bin_number': i + 1,
                'items': bin_state.items,
                'capacity': bin_state.current_capacity,
                'utilization': round(utilization, 1)
            })

        return {
            'items_processed': self.current_index + 1,
            'total_items': len(self.items),
            'bins_used': len(self.bins),
            'efficiency': round(efficiency, 1),
            'bin_details': bin_stats
        }

    def get_state(self) -> Dict:
        """Get current state of the algorithm."""
        return {
            'bins': [bin_state.to_dict() for bin_state in self.bins],
            'current_index': self.current_index,
            'statistics': self.get_statistics()
        }


class FirstFit(BinPackingAlgorithm):
    """
    First Fit Algorithm: Place item in the first bin where it fits.

    Strategy: Iterate through bins sequentially, place in first available.
    Time Complexity: O(N * M) = O(N²) worst case
    """

    def _place_item(self, item: int, item_index: int) -> StepResult:
        """
        Place item using First Fit strategy.

        Args:
            item: Size of item to place
            item_index: Index of item in original list

        Returns:
            StepResult with placement details
        """
        bins_checked = []

        # Try existing bins
        for i, bin_state in enumerate(self.bins):
            bins_checked.append({
                'bin_index': i,
                'current_capacity': bin_state.current_capacity,
                'can_fit': bin_state.can_fit(item, self.capacity),
                'status': 'checking'
            })

            if bin_state.can_fit(item, self.capacity):
                # Found a fit!
                bin_state.items.append(item)
                bins_checked[-1]['status'] = 'selected'

                explanation = (
                    f"Item {item} fits in Bin #{i + 1}! "
                    f"({bin_state.current_capacity - item} + {item} = "
                    f"{bin_state.current_capacity} ≤ {self.capacity})"
                )

                return StepResult(
                    item=item,
                    item_index=item_index,
                    bin_index=i,
                    bins_state=[b.items.copy() for b in self.bins],
                    explanation=explanation,
                    bins_checked=bins_checked,
                    is_new_bin=False
                )
            else:
                bins_checked[-1]['status'] = 'rejected'

        # Create new bin
        new_bin = BinState(items=[item])
        self.bins.append(new_bin)

        explanation = (
            f"Item {item} doesn't fit in any existing bin. "
            f"Creating new Bin #{len(self.bins)}!"
        )

        return StepResult(
            item=item,
            item_index=item_index,
            bin_index=len(self.bins) - 1,
            bins_state=[b.items.copy() for b in self.bins],
            explanation=explanation,
            bins_checked=bins_checked,
            is_new_bin=True
        )


class NextFit(BinPackingAlgorithm):
    """
    Next Fit Algorithm: Only consider the most recent bin.

    Strategy: Try to place item in the current (last) bin only.
    If it doesn't fit, create a new bin and make it current.

    Time Complexity: O(N) - Only checks one bin per item!
    Space Complexity: O(1) - Only tracks current bin

    Performance: Fastest but typically uses most bins
    """

    def _place_item(self, item: int, item_index: int) -> StepResult:
        """
        Place item using Next Fit strategy.

        Args:
            item: Size of item to place
            item_index: Index of item in original list

        Returns:
            StepResult with placement details
        """
        bins_checked = []

        # If no bins exist, create the first one
        if not self.bins:
            new_bin = BinState(items=[item])
            self.bins.append(new_bin)

            explanation = (
                f"No bins exist. Creating first Bin #1 with item {item}."
            )

            return StepResult(
                item=item,
                item_index=item_index,
                bin_index=0,
                bins_state=[b.items.copy() for b in self.bins],
                explanation=explanation,
                bins_checked=[],
                is_new_bin=True
            )

        # Only check the LAST bin (current bin)
        current_bin_idx = len(self.bins) - 1
        current_bin = self.bins[current_bin_idx]

        bins_checked.append({
            'bin_index': current_bin_idx,
            'current_capacity': current_bin.current_capacity,
            'can_fit': current_bin.can_fit(item, self.capacity),
            'status': 'checking'
        })

        if current_bin.can_fit(item, self.capacity):
            # Fits in current bin
            current_bin.items.append(item)
            bins_checked[-1]['status'] = 'selected'

            explanation = (
                f"Item {item} fits in current Bin #{current_bin_idx + 1}! "
                f"({current_bin.current_capacity - item} + {item} = "
                f"{current_bin.current_capacity} ≤ {self.capacity})"
            )

            return StepResult(
                item=item,
                item_index=item_index,
                bin_index=current_bin_idx,
                bins_state=[b.items.copy() for b in self.bins],
                explanation=explanation,
                bins_checked=bins_checked,
                is_new_bin=False
            )
        else:
            # Doesn't fit - create new bin and make it current
            bins_checked[-1]['status'] = 'rejected'
            new_bin = BinState(items=[item])
            self.bins.append(new_bin)

            explanation = (
                f"Item {item} doesn't fit in current Bin #{current_bin_idx + 1} "
                f"({current_bin.current_capacity} + {item} > {self.capacity}). "
                f"Creating new Bin #{len(self.bins)} and moving on!"
            )

            return StepResult(
                item=item,
                item_index=item_index,
                bin_index=len(self.bins) - 1,
                bins_state=[b.items.copy() for b in self.bins],
                explanation=explanation,
                bins_checked=bins_checked,
                is_new_bin=True
            )


class BestFit(BinPackingAlgorithm):
    """
    Best Fit Algorithm: Place item in bin with least remaining space.

    Strategy: Check all bins, choose one with minimum remaining space.
    Time Complexity: O(N * M) = O(N²) worst case
    """

    def _place_item(self, item: int, item_index: int) -> StepResult:
        """
        Place item using Best Fit strategy.

        Args:
            item: Size of item to place
            item_index: Index of item in original list

        Returns:
            StepResult with placement details
        """
        bins_checked = []
        best_bin_idx = -1
        min_remaining_space = self.capacity + 1

        # Check all bins
        for i, bin_state in enumerate(self.bins):
            can_fit = bin_state.can_fit(item, self.capacity)

            check_info = {
                'bin_index': i,
                'current_capacity': bin_state.current_capacity,
                'can_fit': can_fit,
                'status': 'checking'
            }

            if can_fit:
                remaining = bin_state.remaining_space(item, self.capacity)
                check_info['remaining_space'] = remaining

                if remaining < min_remaining_space:
                    min_remaining_space = remaining
                    best_bin_idx = i
                    check_info['status'] = 'best_so_far'
                else:
                    check_info['status'] = 'not_best'
            else:
                check_info['status'] = 'rejected'

            bins_checked.append(check_info)

        # Place in best bin or create new
        if best_bin_idx != -1:
            self.bins[best_bin_idx].items.append(item)

            # Update the selected bin status
            for check in bins_checked:
                if check['bin_index'] == best_bin_idx:
                    check['status'] = 'selected'

            explanation = (
                f"Placing item {item} in Bin #{best_bin_idx + 1} "
                f"(leaves {min_remaining_space} space - the best fit!)"
            )

            return StepResult(
                item=item,
                item_index=item_index,
                bin_index=best_bin_idx,
                bins_state=[b.items.copy() for b in self.bins],
                explanation=explanation,
                bins_checked=bins_checked,
                is_new_bin=False
            )
        else:
            # Create new bin
            new_bin = BinState(items=[item])
            self.bins.append(new_bin)

            explanation = (
                f"Item {item} doesn't fit in any existing bin. "
                f"Creating new Bin #{len(self.bins)}!"
            )

            return StepResult(
                item=item,
                item_index=item_index,
                bin_index=len(self.bins) - 1,
                bins_state=[b.items.copy() for b in self.bins],
                explanation=explanation,
                bins_checked=bins_checked,
                is_new_bin=True
            )


def create_algorithm(algorithm_type: str, capacity: int, items: List[int]) -> BinPackingAlgorithm:
    """
    Factory function to create algorithm instances.

    Args:
        algorithm_type: 'ff' for First Fit, 'bf' for Best Fit, 'nf' for Next Fit
        capacity: Bin capacity
        items: Items to pack

    Returns:
        Instance of the appropriate algorithm

    Raises:
        ValueError: If algorithm_type is invalid
    """
    algorithms = {
        'ff': FirstFit,
        'bf': BestFit,
        'nf': NextFit
    }

    if algorithm_type not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm_type}. Must be 'ff', 'bf', or 'nf'")

    return algorithms[algorithm_type](capacity, items)
