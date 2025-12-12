# Bin Packing Visualizer - Architecture Documentation

## Overview

This is a professional Flask web application with clean separation of concerns, following MVC (Model-View-Controller) architecture and modern web development best practices.

## Project Structure

```
td4-simulation/
│
├── Backend (Python)
│   ├── app.py                      # Flask server & RESTful API endpoints
│   ├── algorithms.py               # Pure algorithm logic (Business Layer)
│   └── requirements.txt            # Python dependencies
│
├── Frontend (JavaScript Modules)
│   ├── static/
│   │   ├── js/
│   │   │   ├── api.js             # API communication layer
│   │   │   ├── visualizer.js      # UI rendering & animations
│   │   │   └── main.js            # Application controller
│   │   └── css/
│   │       └── style.css          # Separated stylesheets
│   └── templates/
│       └── index.html             # HTML template
│
├── Testing & Utilities
│   ├── test_algorithms.py         # Unit tests for algorithms
│   ├── test_api.py                # Integration tests for API
│   ├── run.sh                     # Startup script
│   └── quick_demo.py              # CLI quick demo
│
└── Documentation
    ├── README.md                  # Main documentation
    ├── ARCHITECTURE.md            # This file
    ├── FLASK_SETUP.md             # Setup & deployment guide
    ├── WEB_APP_GUIDE.md           # User guide
    └── COMPARISON.md              # Web vs CLI comparison
```

## Architecture Layers

### 1. Data/Model Layer (`algorithms.py`)

**Purpose**: Pure business logic with no dependencies on UI or framework

**Components**:
- `BinState` - Represents a single bin
- `StepResult` - Result of one algorithm step
- `BinPackingAlgorithm` - Base class
- `FirstFit` - First Fit implementation
- `BestFit` - Best Fit implementation
- `create_algorithm()` - Factory function

**Benefits**:
- ✅ Testable independently
- ✅ Reusable in other projects
- ✅ No UI coupling
- ✅ Type hints and dataclasses for clarity

**Example**:
```python
# Pure logic - no Flask, no UI
algo = create_algorithm('ff', capacity=10, items=[4, 5, 6])
result = algo.step()
print(result.explanation)  # "Item 4 doesn't fit..."
```

### 2. Controller Layer (`app.py`)

**Purpose**: HTTP request handling and routing

**Responsibilities**:
- Route definitions (`@app.route`)
- Request validation
- Session management
- Response formatting (JSON)
- Error handling

**API Endpoints**:
```
GET  /                  → Serve main page
GET  /api/config        → Get demo data
POST /api/start         → Initialize simulation
POST /api/step          → Execute one step
GET  /api/state         → Get current state
GET  /api/statistics    → Get statistics
POST /api/reset         → Reset simulation
GET  /api/health        → Health check
```

**Benefits**:
- ✅ RESTful design
- ✅ Stateless (session-based)
- ✅ JSON API for flexibility
- ✅ Can be consumed by any client (web, mobile, etc.)

### 3. Service Layer (`static/js/api.js`)

**Purpose**: Client-side API communication

**Responsibilities**:
- HTTP requests to backend
- Error handling
- Response parsing
- Abstraction layer for network calls

**Example**:
```javascript
const api = new BinPackingAPI();
const config = await api.getConfig();
await api.startSimulation('ff');
const result = await api.executeStep();
```

**Benefits**:
- ✅ Decoupled from UI logic
- ✅ Easy to mock for testing
- ✅ Single source of truth for API calls
- ✅ Can switch backends easily

### 4. Presentation Layer (`static/js/visualizer.js`)

**Purpose**: DOM manipulation and visualization

**Responsibilities**:
- Rendering bins
- Animating transitions
- Updating statistics
- Managing visual state

**Example**:
```javascript
const viz = new BinPackingVisualizer(capacity);
viz.renderBins(bins);
await viz.highlightBin(0, 'selected');
viz.updateStatistics(stats);
```

**Benefits**:
- ✅ Separated from business logic
- ✅ Reusable UI components
- ✅ Easy to test visuals
- ✅ Can change styling without touching logic

### 5. Application Layer (`static/js/main.js`)

**Purpose**: Coordinate between layers

**Responsibilities**:
- Initialize application
- Handle user interactions
- Coordinate API calls and visualization
- Manage application state

**Flow**:
```
User Click → main.js → api.js → Flask Backend
                                      ↓
                                  algorithms.py
                                      ↓
                                  JSON Response
                                      ↓
User sees → visualizer.js ← main.js ←
```

**Benefits**:
- ✅ Clear separation of concerns
- ✅ Easy to follow data flow
- ✅ Testable integration
- ✅ Single entry point

### 6. View Layer (`templates/index.html`)

**Purpose**: Semantic HTML structure

**Characteristics**:
- Clean semantic HTML
- No business logic
- Uses Jinja2 templating
- Loads modular JavaScript

**Benefits**:
- ✅ SEO friendly
- ✅ Accessible
- ✅ Easy to modify
- ✅ Framework-agnostic

## Data Flow

### Starting a Simulation

```
┌─────────────┐
│   User      │ Clicks "Start"
└──────┬──────┘
       ↓
┌──────────────────┐
│   main.js        │ Calls api.startSimulation('ff')
└──────┬───────────┘
       ↓
┌──────────────────┐
│   api.js         │ POST /api/start
└──────┬───────────┘
       ↓
┌──────────────────┐
│   app.py         │ Creates algorithm instance
└──────┬───────────┘
       ↓
┌──────────────────┐
│   algorithms.py  │ FirstFit(capacity, items)
└──────┬───────────┘
       ↓
┌──────────────────┐
│   Response       │ { session_id, state }
└──────┬───────────┘
       ↓
┌──────────────────┐
│   main.js        │ Updates UI state
└──────┬───────────┘
       ↓
┌──────────────────┐
│   visualizer.js  │ Renders initial state
└──────────────────┘
```

### Executing a Step

```
User clicks "Next Step"
       ↓
main.js.step()
       ↓
api.executeStep() → POST /api/step
       ↓
app.py retrieves algorithm from session
       ↓
algorithm.step() returns StepResult
       ↓
Response: { step_result, state, is_complete }
       ↓
main.js receives result
       ↓
visualizer.animateBinChecking(bins_checked)
       ↓
visualizer.renderBins(bins_state)
       ↓
User sees animation
```

## Design Patterns Used

### 1. Factory Pattern
```python
# In algorithms.py
def create_algorithm(algorithm_type, capacity, items):
    algorithms = {'ff': FirstFit, 'bf': BestFit}
    return algorithms[algorithm_type](capacity, items)
```

### 2. Strategy Pattern
```python
# Different algorithms with same interface
class FirstFit(BinPackingAlgorithm):
    def _place_item(self, item, item_index):
        # First fit strategy

class BestFit(BinPackingAlgorithm):
    def _place_item(self, item, item_index):
        # Best fit strategy
```

### 3. MVC Pattern
- **Model**: `algorithms.py` (business logic)
- **View**: `templates/index.html` + `static/css/style.css`
- **Controller**: `app.py` (routes) + `static/js/main.js` (coordination)

### 4. Module Pattern
```javascript
// api.js, visualizer.js, main.js are separate modules
export default class BinPackingAPI { }
```

### 5. Observer Pattern
```javascript
// Event listeners in main.js
document.getElementById('startBtn').addEventListener('click', () => this.start());
```

## Communication Protocols

### REST API

All backend communication uses REST principles:
- **GET** - Retrieve data (idempotent)
- **POST** - Create/modify data (non-idempotent)
- **JSON** - Data format
- **HTTP status codes** - 200 (success), 400 (client error), 500 (server error)

### Session Management

- Flask sessions (cookie-based)
- Algorithm instances stored in memory by session ID
- Frontend uses `requests.Session()` to maintain cookies

## State Management

### Backend State
```python
# In-memory store (per session)
algorithms_store: Dict[str, BinPackingAlgorithm] = {}

# Accessed by session ID
session_id = get_session_id()
algorithm = algorithms_store[session_id]
```

### Frontend State
```javascript
// In main.js
this.isRunning = false;
this.autoPlay = false;
this.speed = 1000;
this.currentAlgorithm = 'ff';
```

## Security Considerations

### Current Implementation (Development)
- `debug=True` - Should be `False` in production
- `host='0.0.0.0'` - Accepts all connections
- In-memory session storage - Not scalable

### Production Recommendations
1. **Use environment variables**:
   ```python
   app.secret_key = os.environ.get('SECRET_KEY')
   ```

2. **Use Redis for sessions**:
   ```python
   from flask_session import Session
   app.config['SESSION_TYPE'] = 'redis'
   ```

3. **Add rate limiting**:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app)
   ```

4. **Use HTTPS** in production

5. **Add CSRF protection**:
   ```python
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   ```

## Performance Considerations

### Current Performance
- **Algorithm**: O(N²) where N = number of items
- **API**: Synchronous (blocking)
- **Session storage**: In-memory (not distributed)

### Optimization Opportunities

1. **Caching**:
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def calculate_statistics(bins_tuple):
       # Cache expensive calculations
   ```

2. **Async processing**:
   ```python
   from flask import Flask
   from flask_executor import Executor

   executor = Executor(app)

   @executor.job
   def run_full_simulation(algorithm):
       # Run in background
   ```

3. **Database for persistence**:
   ```python
   from flask_sqlalchemy import SQLAlchemy

   # Store simulation history
   ```

## Testing Strategy

### Unit Tests (`test_algorithms.py`)
- Test pure algorithm logic
- No Flask dependencies
- Fast execution

### Integration Tests (`test_api.py`)
- Test API endpoints
- Use requests library
- Test full request/response cycle

### Frontend Tests (Not implemented yet)
```javascript
// Using Jest or similar
describe('BinPackingAPI', () => {
    it('should fetch config', async () => {
        const api = new BinPackingAPI();
        const config = await api.getConfig();
        expect(config.capacity).toBe(10);
    });
});
```

## Extending the Application

### Adding a New Algorithm

1. **Create class in `algorithms.py`**:
```python
class WorstFit(BinPackingAlgorithm):
    def _place_item(self, item, item_index):
        # Find bin with MOST remaining space
        pass
```

2. **Register in factory**:
```python
def create_algorithm(algorithm_type, capacity, items):
    algorithms = {
        'ff': FirstFit,
        'bf': BestFit,
        'wf': WorstFit  # Add here
    }
```

3. **Update frontend**:
```html
<select id="algorithmSelect">
    <option value="wf">Worst Fit (WF)</option>
</select>
```

### Adding Real-time Updates

Use WebSockets for live updates:
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('execute_step')
def handle_step():
    result = algorithm.step()
    emit('step_result', result.to_dict())
```

```javascript
const socket = io();
socket.on('step_result', (data) => {
    visualizer.renderBins(data.bins_state);
});
```

## Deployment Options

### Option 1: Heroku
```bash
# Procfile
web: gunicorn app:app

# Deploy
git push heroku main
```

### Option 2: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### Option 3: AWS Lambda (Serverless)
```python
# Use Zappa
zappa init
zappa deploy production
```

## Conclusion

This architecture provides:
- ✅ **Separation of Concerns** - Each layer has single responsibility
- ✅ **Testability** - Each component can be tested independently
- ✅ **Scalability** - Can add features without breaking existing code
- ✅ **Maintainability** - Easy to find and fix bugs
- ✅ **Reusability** - Components can be reused in other projects
- ✅ **Professional Quality** - Follows industry best practices

Perfect for educational purposes and production use!
