# Bin Packing Problem Simulator

An interactive educational tool for visualizing and understanding First Fit (FF) and Best Fit (BF) greedy algorithms for the Bin Packing Problem.

## 🎯 Available Versions

### 1. **Flask Web App** (Recommended) ⭐
Professional full-stack application with REST API and modular architecture.
- **Start**: `./run.sh` or `python app.py`
- **Access**: http://localhost:5001
- **Best for**: Production, teaching, demonstrations, API integration

### 2. **Standalone Web App**
Single-file HTML application (no backend required).
- **Start**: Open `index.html` in browser
- **Best for**: Quick demos, no Python needed

### 3. **CLI Tool**
Terminal-based interactive simulator with ASCII visualization.
- **Start**: `python bin_packing_simulator.py`
- **Best for**: Research, custom data, scripting

## Features

### Web App (Recommended for Teaching)
- **Beautiful Visual Interface**: Modern, colorful bin visualization
- **Step-by-Step Animation**: Watch the algorithm think and make decisions
- **Interactive Controls**: Play, pause, step forward, adjust speed
- **Live Algorithm Explanation**: See the reasoning behind each placement
- **Real-time Statistics**: Track efficiency and bin usage
- **Highlight Effects**: See which bins are being considered
- **Auto-play Mode**: Automated demonstrations

### CLI Tool
- **Two Greedy Algorithms**: First Fit and Best Fit implementations
- **ASCII Visualization**: Vertical bin representation showing items stacking in real-time
- **Step-by-Step Mode**: Pause after each item placement to trace algorithm decisions
- **Demo Mode**: Pre-loaded with lecture slide data
- **Custom Mode**: Test with your own capacity and items
- **Algorithm Comparison**: Run both algorithms and compare results
- **Detailed Statistics**: Bin utilization, efficiency metrics, and more

## Demo Data (from Lecture Slides)

- **Capacity (B)**: 10
- **Items (O)**: [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]

## 🚀 Quick Start (Flask App)

```bash
# 1. Clone or navigate to the project directory
cd td4-simulation

# 2. Run the startup script
./run.sh

# 3. Open in browser
# http://localhost:5001
```

That's it! The script will:
- Create virtual environment
- Install dependencies
- Start Flask server

## Usage

### Flask Web App (Recommended)

```bash
# Option 1: Use the startup script
./run.sh

# Option 2: Manual start
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5001 in your browser.

**Features**:
- RESTful API backend
- Modular JavaScript frontend
- Professional architecture
- See `FLASK_SETUP.md` for details

### Standalone Web App (No Python)

Simply open `index.html` in any modern web browser:

```bash
open index.html
# or double-click the file in your file explorer
```

Then:
1. Select algorithm (First Fit or Best Fit)
2. Click "Start"
3. Click "Next Step" to see each placement decision
4. Or click "Auto Play" for continuous animation
5. Adjust speed with the slider

### CLI Tool

Run the program:

```bash
python bin_packing_simulator.py
```

Or make it executable:

```bash
chmod +x bin_packing_simulator.py
./bin_packing_simulator.py
```

## Algorithm Complexity

Both algorithms have **O(N²)** time complexity in the worst case:
- N items to pack
- Each item may require checking up to N bins
- Total: O(N × N) = O(N²)

## Example Output

```
  Bin #1        Bin #2
  ┌────────┐    ┌────────┐
  │        │    │        │
  │        │    │        │
  │████████│    │████████│
  │████████│    │████████│
  │████████│    │████████│
  │████████│    │████████│
  │████████│    │████████│
  └────────┘    └────────┘
  5/10          5/10
```

## Web App Features Explained

### Visual Feedback
- **Yellow Border + Glow**: Bin currently being checked
- **Green Border + Glow**: Selected bin for placement
- **Red Border**: Rejected bin (item doesn't fit)
- **Pulsing Red Box**: Current item being placed

### Controls
- **Next Step**: Manually advance through each decision
- **Auto Play**: Continuous animation (adjustable speed)
- **Speed Slider**: Control animation speed (0.2s to 2.0s)
- **Reset**: Start over with same or different algorithm

### Real-Time Information
- Items processed count
- Number of bins used
- Overall packing efficiency
- Detailed explanation of each decision
- Visual item list showing what's been packed

## Learning Objectives

1. **Understand greedy algorithm design patterns**: See how each algorithm makes locally optimal choices
2. **Compare different heuristic strategies**: First Fit vs Best Fit side-by-side
3. **Visualize data structure operations**: Watch bins (lists) being created and filled
4. **Analyze algorithm efficiency**: Track utilization and wasted space
5. **See real-time decision-making process**: Step through the algorithm's "thinking"
6. **Observe O(N²) complexity**: Count how many bins are checked for each item

## Educational Notes

### First Fit Algorithm
- **Strategy**: Use the first bin that has enough space
- **Pros**: Fast - stops searching as soon as a fit is found
- **Cons**: May waste space at the beginning of the bin list
- **Behavior**: Early bins get filled first, later ones may be underutilized

### Best Fit Algorithm
- **Strategy**: Use the bin that leaves the least empty space
- **Pros**: Tries to minimize wasted space in each bin
- **Cons**: Must check ALL bins before deciding (slower)
- **Behavior**: Better space utilization but not always fewer bins

### Important Insights
- Neither algorithm guarantees the optimal (minimum) number of bins
- Both are approximation algorithms for an NP-hard problem
- In some cases, First Fit can actually perform better than Best Fit!
- The theoretical minimum bins needed: ⌈total_size / capacity⌉ = ⌈110 / 10⌉ = 11 bins
