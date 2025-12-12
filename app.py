"""
Flask Backend for Bin Packing Visualizer
RESTful API for algorithm execution and state management
"""

from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
from algorithms import create_algorithm, BinPackingAlgorithm
from custom_algorithm_loader import (
    load_algorithm_from_code,
    load_algorithm_from_file,
    StudentAlgorithmWrapper,
    validate_algorithm
)
from typing import Dict, Optional, Union
import secrets
from pathlib import Path

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Demo data from lecture slides
DEMO_CAPACITY = 10
DEMO_ITEMS = [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

# In-memory storage for algorithm instances (session-based)
# In production, use Redis or database
algorithms_store: Dict[str, Union[BinPackingAlgorithm, StudentAlgorithmWrapper]] = {}


def get_session_id() -> str:
    """Get or create session ID."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    return session['session_id']


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get demo configuration data."""
    return jsonify({
        'capacity': DEMO_CAPACITY,
        'items': DEMO_ITEMS,
        'total_items': len(DEMO_ITEMS),
        'total_size': sum(DEMO_ITEMS),
        'theoretical_minimum': -(-sum(DEMO_ITEMS) // DEMO_CAPACITY)  # Ceiling division
    })


@app.route('/api/start', methods=['POST'])
def start_simulation():
    """
    Initialize a new simulation.

    Expected JSON body:
    {
        "algorithm": "ff" | "bf",
        "capacity": int (optional, defaults to DEMO_CAPACITY),
        "items": list[int] (optional, defaults to DEMO_ITEMS)
    }

    Returns:
    {
        "session_id": str,
        "algorithm": str,
        "state": {...}
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        algorithm_type = data.get('algorithm', 'ff')
        capacity = data.get('capacity', DEMO_CAPACITY)
        items = data.get('items', DEMO_ITEMS)

        # Validate inputs
        if algorithm_type not in ['ff', 'bf', 'nf']:
            return jsonify({'error': 'Invalid algorithm. Must be "ff", "bf", or "nf"'}), 400

        if capacity <= 0:
            return jsonify({'error': 'Capacity must be positive'}), 400

        if not items or not all(isinstance(x, int) and x > 0 for x in items):
            return jsonify({'error': 'Items must be a non-empty list of positive integers'}), 400

        if any(item > capacity for item in items):
            return jsonify({'error': 'Some items are larger than bin capacity'}), 400

        # Create algorithm instance
        session_id = get_session_id()
        algorithm = create_algorithm(algorithm_type, capacity, items)
        algorithms_store[session_id] = algorithm

        return jsonify({
            'session_id': session_id,
            'algorithm': algorithm_type,
            'state': algorithm.get_state()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/step', methods=['POST'])
def execute_step():
    """
    Execute one step of the algorithm.

    Returns:
    {
        "step_result": {...},
        "state": {...},
        "is_complete": bool
    }
    """
    try:
        session_id = get_session_id()

        if session_id not in algorithms_store:
            return jsonify({'error': 'No active simulation. Please start first.'}), 400

        algorithm = algorithms_store[session_id]
        step_result = algorithm.step()

        if step_result is None:
            return jsonify({
                'step_result': None,
                'state': algorithm.get_state(),
                'is_complete': True
            }), 200

        return jsonify({
            'step_result': step_result.to_dict(),
            'state': algorithm.get_state(),
            'is_complete': False
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current state of the algorithm."""
    try:
        session_id = get_session_id()

        if session_id not in algorithms_store:
            return jsonify({'error': 'No active simulation'}), 400

        algorithm = algorithms_store[session_id]
        return jsonify(algorithm.get_state()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get detailed statistics about the current packing."""
    try:
        session_id = get_session_id()

        if session_id not in algorithms_store:
            return jsonify({'error': 'No active simulation'}), 400

        algorithm = algorithms_store[session_id]
        return jsonify(algorithm.get_statistics()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    """Reset the current simulation."""
    try:
        session_id = get_session_id()

        if session_id in algorithms_store:
            del algorithms_store[session_id]

        return jsonify({'message': 'Simulation reset successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/custom/validate', methods=['POST'])
def validate_custom_algorithm():
    """
    Validate a custom student algorithm.

    Expected JSON:
    {
        "code": "def MyAlgo(items, capacity): ..."
    }

    Returns:
    {
        "valid": bool,
        "message": str,
        "bins_used": int (if valid)
    }
    """
    try:
        data = request.get_json()

        if not data or 'code' not in data:
            return jsonify({'error': 'No code provided'}), 400

        code = data['code']

        # Load and validate the algorithm
        algo_info = load_algorithm_from_code(code)
        validation = validate_algorithm(algo_info.function)

        if validation['valid']:
            return jsonify({
                'valid': True,
                'message': validation['message'],
                'bins_used': validation['bins_used'],
                'algorithm_name': algo_info.name,
                'complexity': algo_info.complexity
            }), 200
        else:
            return jsonify({
                'valid': False,
                'error': validation['error']
            }), 400

    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 400


@app.route('/api/custom/run', methods=['POST'])
def run_custom_algorithm():
    """
    Run a custom algorithm with specific data.

    Expected JSON:
    {
        "code": "def MyAlgo(items, capacity): ...",
        "capacity": int (optional),
        "items": list[int] (optional)
    }

    Returns:
    {
        "session_id": str,
        "algorithm_name": str,
        "state": {...}
    }
    """
    try:
        data = request.get_json()

        if not data or 'code' not in data:
            return jsonify({'error': 'No code provided'}), 400

        code = data['code']
        capacity = data.get('capacity', DEMO_CAPACITY)
        items = data.get('items', DEMO_ITEMS)

        # Validate inputs
        if capacity <= 0:
            return jsonify({'error': 'Capacity must be positive'}), 400

        if not items or any(item > capacity for item in items):
            return jsonify({'error': 'Invalid items'}), 400

        # Load the algorithm
        algo_info = load_algorithm_from_code(code)

        # Validate it works
        validation = validate_algorithm(algo_info.function, items, capacity)
        if not validation['valid']:
            return jsonify({'error': f'Algorithm validation failed: {validation["error"]}'}), 400

        # Create wrapper
        session_id = get_session_id()
        wrapper = StudentAlgorithmWrapper(
            algo_info.function,
            capacity,
            items,
            name=algo_info.name,
            description=algo_info.description,
            complexity=algo_info.complexity
        )

        algorithms_store[session_id] = wrapper

        return jsonify({
            'session_id': session_id,
            'algorithm_name': algo_info.name,
            'algorithm_type': 'custom',
            'complexity': algo_info.complexity,
            'state': wrapper.get_state()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/custom/load-file', methods=['POST'])
def load_custom_file():
    """
    Load algorithm from a file in student_algorithms/ directory.

    Expected JSON:
    {
        "filename": "my_algorithm.py",
        "capacity": int (optional),
        "items": list[int] (optional)
    }
    """
    try:
        data = request.get_json()

        if not data or 'filename' not in data:
            return jsonify({'error': 'No filename provided'}), 400

        filename = data['filename']
        capacity = data.get('capacity', DEMO_CAPACITY)
        items = data.get('items', DEMO_ITEMS)

        # Security: Only allow files from student_algorithms directory
        base_path = Path('student_algorithms')
        file_path = base_path / filename

        if not file_path.exists() or not str(file_path).startswith(str(base_path)):
            return jsonify({'error': 'File not found or invalid path'}), 404

        # Load the algorithm
        algo_info = load_algorithm_from_file(str(file_path))

        # Validate it
        validation = validate_algorithm(algo_info.function, items, capacity)
        if not validation['valid']:
            return jsonify({'error': f'Algorithm validation failed: {validation["error"]}'}), 400

        # Create wrapper
        session_id = get_session_id()
        wrapper = StudentAlgorithmWrapper(
            algo_info.function,
            capacity,
            items,
            name=algo_info.name,
            description=algo_info.description,
            complexity=algo_info.complexity
        )

        algorithms_store[session_id] = wrapper

        return jsonify({
            'session_id': session_id,
            'algorithm_name': algo_info.name,
            'algorithm_type': 'custom',
            'complexity': algo_info.complexity,
            'state': wrapper.get_state()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'active_simulations': len(algorithms_store)
    }), 200


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))

    print("=" * 60)
    print("Bin Packing Visualizer - Flask Backend")
    print("=" * 60)
    print(f"\nServer starting at: http://localhost:{port}")
    print("\nAPI Endpoints:")
    print("  GET  /                  - Main application")
    print("  GET  /api/config        - Get demo configuration")
    print("  POST /api/start         - Start simulation")
    print("  POST /api/step          - Execute one step")
    print("  GET  /api/state         - Get current state")
    print("  GET  /api/statistics    - Get statistics")
    print("  POST /api/reset         - Reset simulation")
    print("  GET  /api/health        - Health check")
    print("\n" + "=" * 60)

    app.run(debug=True, host='0.0.0.0', port=port)
