# Flask Application Setup Guide

## Project Structure

```
td4-simulation/
├── app.py                          # Flask backend (main server)
├── algorithms.py                   # Pure algorithm logic (no UI)
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Clean HTML template
└── static/
    ├── css/
    │   └── style.css              # Separated CSS styles
    └── js/
        ├── api.js                 # API communication layer
        ├── visualizer.js          # UI rendering logic
        └── main.js                # Application controller
```

## Architecture Overview

### Separation of Concerns

**Backend (Python):**
- `algorithms.py` - Pure algorithm logic (First Fit, Best Fit)
- `app.py` - Flask server with RESTful API endpoints

**Frontend (JavaScript):**
- `api.js` - Handles all HTTP communication with backend
- `visualizer.js` - Manages DOM manipulation and animations
- `main.js` - Coordinates between API and Visualizer

**Presentation:**
- `style.css` - All styling separated from logic
- `index.html` - Clean semantic HTML template

### Benefits of This Architecture

1. **Testability**: Each module can be tested independently
2. **Maintainability**: Easy to find and modify specific functionality
3. **Scalability**: Can add new algorithms or UI features easily
4. **Reusability**: Algorithm logic can be used in other projects
5. **Professional**: Follows industry best practices (MVC pattern)

## Installation

### 1. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

## Running the Application

### Start the Flask Server

```bash
python app.py
```

You should see:
```
============================================================
Bin Packing Visualizer - Flask Backend
============================================================

Server starting at: http://localhost:5000

API Endpoints:
  GET  /                  - Main application
  GET  /api/config        - Get demo configuration
  POST /api/start         - Start simulation
  POST /api/step          - Execute one step
  GET  /api/state         - Get current state
  GET  /api/statistics    - Get statistics
  POST /api/reset         - Reset simulation
  GET  /api/health        - Health check

============================================================
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## API Documentation

### GET /api/config
Get demo configuration data.

**Response:**
```json
{
  "capacity": 10,
  "items": [4, 4, 5, 5, ...],
  "total_items": 24,
  "total_size": 110,
  "theoretical_minimum": 11
}
```

### POST /api/start
Start a new simulation.

**Request Body:**
```json
{
  "algorithm": "ff",  // or "bf"
  "capacity": 10,     // optional
  "items": [4, 4, 5]  // optional
}
```

**Response:**
```json
{
  "session_id": "abc123...",
  "algorithm": "ff",
  "state": {
    "bins": [],
    "current_index": -1,
    "statistics": {...}
  }
}
```

### POST /api/step
Execute one step of the algorithm.

**Response:**
```json
{
  "step_result": {
    "item": 4,
    "item_index": 0,
    "bin_index": 0,
    "bins_state": [[4]],
    "explanation": "Item 4 placed in Bin #1",
    "bins_checked": [...],
    "is_new_bin": true
  },
  "state": {...},
  "is_complete": false
}
```

### GET /api/state
Get current algorithm state.

### GET /api/statistics
Get detailed packing statistics.

**Response:**
```json
{
  "items_processed": 12,
  "total_items": 24,
  "bins_used": 5,
  "efficiency": 88.5,
  "bin_details": [
    {
      "bin_number": 1,
      "items": [4, 4, 2],
      "capacity": 10,
      "utilization": 100.0
    }
  ]
}
```

### POST /api/reset
Reset the current simulation.

### GET /api/health
Health check endpoint.

## Development

### Run in Debug Mode

The app is already configured with `debug=True`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

This enables:
- Auto-reload on code changes
- Better error messages
- Debug console

### Testing the API

Using curl:
```bash
# Health check
curl http://localhost:5000/api/health

# Get config
curl http://localhost:5000/api/config

# Start simulation
curl -X POST http://localhost:5000/api/start \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "ff"}'

# Execute step
curl -X POST http://localhost:5000/api/step
```

Using Python:
```python
import requests

# Get config
response = requests.get('http://localhost:5000/api/config')
print(response.json())

# Start simulation
response = requests.post('http://localhost:5000/api/start',
    json={'algorithm': 'ff'})
print(response.json())
```

### Adding New Algorithms

1. Create new class in `algorithms.py`:
```python
class MyNewAlgorithm(BinPackingAlgorithm):
    def _place_item(self, item, item_index):
        # Your implementation
        pass
```

2. Register in factory:
```python
def create_algorithm(algorithm_type, capacity, items):
    algorithms = {
        'ff': FirstFit,
        'bf': BestFit,
        'my': MyNewAlgorithm  # Add here
    }
    # ...
```

3. Update frontend:
```html
<select id="algorithmSelect">
    <option value="ff">First Fit</option>
    <option value="bf">Best Fit</option>
    <option value="my">My Algorithm</option>
</select>
```

## Deployment

### Production Considerations

For production deployment, consider:

1. **Use a production WSGI server** (not Flask's dev server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Add environment variables**:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')
```

3. **Use Redis for session storage**:
```python
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'
```

4. **Add logging**:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Run:
```bash
docker build -t bin-packing .
docker run -p 5000:5000 bin-packing
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or use different port
python app.py  # Edit port in app.py
```

### Module Import Errors
```bash
# Make sure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Issues
Already handled with `flask-cors`. If issues persist:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Session Issues
Clear browser cookies or use incognito mode.

## Code Quality

### Run Tests (if you add them)
```bash
pytest tests/
```

### Code Formatting
```bash
pip install black
black *.py
```

### Type Checking
```bash
pip install mypy
mypy algorithms.py
```

## Performance

### Current Implementation
- In-memory session storage (suitable for demos)
- Single-threaded Flask dev server

### For Production
- Use Redis for session storage
- Use Gunicorn with multiple workers
- Add caching for static assets
- Consider WebSocket for real-time updates

## Educational Use

### For Students
1. Study `algorithms.py` to understand the logic
2. Try modifying the algorithms
3. Add new algorithms
4. Experiment with different data

### For Instructors
1. Use the API to create automated tests
2. Build custom frontends
3. Create homework assignments
4. Integrate with learning management systems

## License & Credits

Created as an educational tool for teaching greedy algorithms and the Bin Packing Problem.

Feel free to modify and extend for your needs!
