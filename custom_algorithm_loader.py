"""
Custom Algorithm Loader - Makes student algorithms compatible with the system

This module provides utilities to load simple student functions and wrap them
into the framework's StepResult format for visualization.
"""

from typing import List, Callable, Optional, Dict
from dataclasses import dataclass
import importlib.util
import sys
from pathlib import Path

from algorithms import StepResult


@dataclass
class CustomAlgorithmInfo:
    """Information about a loaded custom algorithm."""
    name: str
    description: str
    complexity: str
    function: Callable


class StudentAlgorithmWrapper:
    """
    Wraps a simple student function into our framework format.

    Converts from:
        def my_algo(items, capacity) -> bins

    To:
        Compatible with step-by-step visualization
    """

    def __init__(self, function: Callable, capacity: int, items: List[int],
                 name: str = "Custom", description: str = "", complexity: str = ""):
        self.function = function
        self.capacity = capacity
        # Keep the original items order for visualization; student code may mutate/sort the input list
        self.original_items = list(items)
        # This will later reflect the order the student's algorithm actually processed
        self.processed_items = list(items)
        self.name = name
        self.description = description
        self.complexity = complexity

        # Execute algorithm once to get all bins
        self.bins_sequence: List[StepResult] = []
        self.current_step = -1
        self._execute_algorithm()

    def _execute_algorithm(self):
        """Execute the student's algorithm and capture the bin sequence."""
        try:
            # Work on a copy so we can detect if the student reorders items
            items_for_algorithm = list(self.original_items)

            # Run student's function
            final_bins = self.function(items_for_algorithm, self.capacity)

            # Validate output
            if not isinstance(final_bins, list):
                raise ValueError("Algorithm must return a list of bins")
            if not all(isinstance(b, list) for b in final_bins):
                raise ValueError("Each bin must be a list of items")

            # If the student mutated the input order, keep that for visualization
            if items_for_algorithm != self.original_items:
                self.processed_items = list(items_for_algorithm)

            # Convert to our format and track steps
            # Since we can't step through their code, we simulate steps
            # by showing items being placed in order
            item_to_bin = {}  # Map item index to bin index

            # Figure out where each item ended up
            for bin_idx, bin_items in enumerate(final_bins):
                for item in bin_items:
                    # Find first unassigned occurrence of this item value
                    for item_idx, original_item in enumerate(self.processed_items):
                        if original_item == item and item_idx not in item_to_bin:
                            item_to_bin[item_idx] = bin_idx
                            break

            # Make sure every item found a bin
            missing_items = [i for i in range(len(self.processed_items)) if i not in item_to_bin]
            if missing_items:
                raise ValueError(f"Algorithm did not place items at indexes: {missing_items}")

            # Create step sequence
            current_bins = [[] for _ in range(len(final_bins))]
            highest_bin_created = -1

            for item_idx in range(len(self.processed_items)):
                bin_idx = item_to_bin.get(item_idx, 0)
                target_bin = current_bins[bin_idx]
                is_new_bin = len(target_bin) == 0
                target_bin.append(self.processed_items[item_idx])
                highest_bin_created = max(highest_bin_created, bin_idx)

                # Snapshot of bins created so far
                bins_state = [bin_items.copy() for bin_items in current_bins[:highest_bin_created + 1]]

                self.bins_sequence.append(StepResult(
                    item=self.processed_items[item_idx],
                    item_index=item_idx,
                    bin_index=bin_idx,
                    bins_state=bins_state,
                    explanation=f"Item {self.processed_items[item_idx]} placed in Bin #{bin_idx + 1} (Student Algorithm)",
                    bins_checked=[],  # We cannot introspect student bin checks
                    is_new_bin=is_new_bin
                ))

        except Exception as e:
            raise ValueError(f"Error executing algorithm: {str(e)}")

    def step(self) -> Optional[StepResult]:
        """Execute one step of the algorithm."""
        if self.current_step + 1 >= len(self.bins_sequence):
            return None

        self.current_step += 1

        return self.bins_sequence[self.current_step]

    def get_state(self) -> Dict:
        """Get current state."""
        if self.current_step < 0:
            bins: List[List[int]] = []
        else:
            bins = self.bins_sequence[self.current_step].bins_state

        bins_with_capacity = [
            {
                'items': bin_items,
                'current_capacity': sum(bin_items)
            }
            for bin_items in bins
        ]

        return {
            'bins': bins_with_capacity,
            'current_index': self.current_step,
            'statistics': self.get_statistics(),
            'items_order': self.processed_items
        }

    def get_statistics(self) -> Dict:
        """Calculate statistics."""
        if self.current_step < 0:
            return {
                'items_processed': 0,
                'total_items': len(self.processed_items),
                'bins_used': 0,
                'efficiency': 0,
                'bin_details': []
            }

        step_index = min(self.current_step, len(self.bins_sequence) - 1)
        bins = self.bins_sequence[step_index].bins_state
        bins = [b for b in bins if b]  # Filter empty bins

        total_items_size = sum(self.processed_items[:step_index + 1])
        total_capacity = len(bins) * self.capacity
        efficiency = (total_items_size / total_capacity * 100) if total_capacity > 0 else 0

        bin_stats = []
        for i, bin_items in enumerate(bins):
            if bin_items:
                capacity = sum(bin_items)
                utilization = (capacity / self.capacity * 100)
                bin_stats.append({
                    'bin_number': i + 1,
                    'items': bin_items,
                    'capacity': capacity,
                    'utilization': round(utilization, 1)
                })

        return {
            'items_processed': step_index + 1,
            'total_items': len(self.processed_items),
            'bins_used': len(bins),
            'efficiency': round(efficiency, 1),
            'bin_details': bin_stats
        }

    def reset(self):
        """Reset to beginning."""
        self.current_step = -1


def load_algorithm_from_file(file_path: str) -> CustomAlgorithmInfo:
    """
    Load a student algorithm from a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        CustomAlgorithmInfo with the loaded algorithm

    Raises:
        ValueError: If file is invalid or algorithm not found
    """
    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"File not found: {file_path}")

    if not path.suffix == '.py':
        raise ValueError("File must be a .py file")

    # Load the module
    spec = importlib.util.spec_from_file_location("student_module", path)
    if spec is None or spec.loader is None:
        raise ValueError("Could not load module")

    module = importlib.util.module_from_spec(spec)
    sys.modules["student_module"] = module
    spec.loader.exec_module(module)

    # Find the algorithm function
    # Look for a function that takes 2 parameters
    algorithm_func = None
    func_name = None

    for name in dir(module):
        if name.startswith('_'):
            continue

        obj = getattr(module, name)
        if callable(obj) and obj.__module__ == "student_module":
            # Check if it takes 2 parameters
            try:
                import inspect
                sig = inspect.signature(obj)
                if len(sig.parameters) == 2:
                    algorithm_func = obj
                    func_name = name
                    break
            except:
                continue

    if algorithm_func is None:
        raise ValueError(
            "No valid algorithm function found. "
            "Function must take exactly 2 parameters: (items, capacity)"
        )

    # Get metadata if available
    name = getattr(module, 'ALGORITHM_NAME', func_name)
    description = getattr(module, 'ALGORITHM_DESCRIPTION', 'Custom student algorithm')
    complexity = getattr(module, 'COMPLEXITY', 'Unknown')

    return CustomAlgorithmInfo(
        name=name,
        description=description,
        complexity=complexity,
        function=algorithm_func
    )


def load_algorithm_from_code(code: str, function_name: str = None) -> CustomAlgorithmInfo:
    """
    Load algorithm directly from code string.

    Args:
        code: Python code as string
        function_name: Name of the function (if None, auto-detect)

    Returns:
        CustomAlgorithmInfo with the loaded algorithm
    """
    # Create a temporary module
    namespace = {}

    try:
        exec(code, namespace)
    except Exception as e:
        raise ValueError(f"Error executing code: {str(e)}")

    # Find the algorithm function
    if function_name:
        if function_name not in namespace:
            raise ValueError(f"Function '{function_name}' not found in code")
        algorithm_func = namespace[function_name]
    else:
        # Auto-detect function
        algorithm_func = None
        func_name = None

        for name, obj in namespace.items():
            if name.startswith('_'):
                continue
            if callable(obj):
                import inspect
                try:
                    sig = inspect.signature(obj)
                    if len(sig.parameters) == 2:
                        algorithm_func = obj
                        func_name = name
                        break
                except:
                    continue

        if algorithm_func is None:
            raise ValueError("No valid function found. Must take 2 parameters: (items, capacity)")

    # Get metadata
    name = namespace.get('ALGORITHM_NAME', func_name or 'Custom')
    description = namespace.get('ALGORITHM_DESCRIPTION', 'Custom algorithm')
    complexity = namespace.get('COMPLEXITY', 'Unknown')

    return CustomAlgorithmInfo(
        name=name,
        description=description,
        complexity=complexity,
        function=algorithm_func
    )


def validate_algorithm(function: Callable, test_items: List[int] = None,
                      test_capacity: int = 10) -> Dict:
    """
    Validate that an algorithm function works correctly.

    Args:
        function: The algorithm function to test
        test_items: Items to test with (default: [4, 5, 6])
        test_capacity: Capacity to test with

    Returns:
        Dict with validation results
    """
    if test_items is None:
        test_items = [4, 5, 6, 3]

    try:
        original_items = list(test_items)
        working_items = list(test_items)

        # Run the algorithm
        result = function(working_items, test_capacity)

        # Validate structure
        if not isinstance(result, list):
            return {
                'valid': False,
                'error': 'Result must be a list of bins'
            }

        # Check all items are placed
        all_items = []
        for bin_items in result:
            if not isinstance(bin_items, list):
                return {
                    'valid': False,
                    'error': 'Each bin must be a list'
                }
            all_items.extend(bin_items)

        all_items_sorted = sorted(all_items)
        test_items_sorted = sorted(original_items)

        if all_items_sorted != test_items_sorted:
            return {
                'valid': False,
                'error': 'Not all items were placed correctly'
            }

        # Check capacity constraints
        for i, bin_items in enumerate(result):
            if sum(bin_items) > test_capacity:
                return {
                    'valid': False,
                    'error': f'Bin #{i+1} exceeds capacity: {sum(bin_items)} > {test_capacity}'
                }

        return {
            'valid': True,
            'bins_used': len([b for b in result if b]),
            'items_placed': len(all_items),
            'message': 'Algorithm validated successfully!'
        }

    except Exception as e:
        return {
            'valid': False,
            'error': f'Execution error: {str(e)}'
        }
