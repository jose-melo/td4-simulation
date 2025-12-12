# Web App Quick Start Guide

## How to Run

**Option 1: Double-click**
- Simply double-click `index.html` in your file explorer

**Option 2: Command line**
```bash
open index.html
# or on Linux: xdg-open index.html
# or on Windows: start index.html
```

**Option 3: Python web server** (if double-click doesn't work)
```bash
python -m http.server 8000
# Then open: http://localhost:8000/index.html
```

## Using the Visualizer

### Step-by-Step Mode (Recommended for Learning)

1. **Select Algorithm**: Choose "First Fit" or "Best Fit" from dropdown
2. **Click "Start"**: Initializes the simulation
3. **Click "Next Step"**: Advances one item placement at a time
4. **Watch the Animation**:
   - Yellow glow = bin being checked
   - Green glow = bin selected for item
   - Red border = bin rejected (item too big)
5. **Read the Explanation**: Text below controls explains each decision
6. **Repeat Step 3**: Until all items are packed

### Auto-Play Mode (Demonstrations)

1. **Select Algorithm**
2. **Click "Start"**
3. **Click "Auto Play"**: Runs continuously
4. **Adjust Speed**: Use the slider (0.2s to 2.0s per step)
5. **Click "Pause"**: Stop auto-play anytime
6. **Continue manually**: Use "Next Step" after pausing

## What to Observe

### First Fit Algorithm
- Watch how it checks bins from left to right
- Stops at the FIRST bin that fits
- Notice how early bins fill up quickly
- Some later bins might be underutilized

**Example Decision:**
```
Item 4 → Check Bin #1 (6/10) → Fits! (6+4=10) → Place it!
(Stops checking - doesn't look at other bins)
```

### Best Fit Algorithm
- Watch how it checks ALL bins before deciding
- Yellow glow moves across all bins
- Chooses the bin with LEAST remaining space
- Better space utilization per bin

**Example Decision:**
```
Item 4 → Check Bin #1 (6/10, would leave 0)
       → Check Bin #2 (5/10, would leave 1)
       → Check Bin #3 (4/10, would leave 2)
       → Best is Bin #1 (leaves 0 space) → Place it!
```

## Understanding the Statistics

### Items Processed
- Shows progress: "12 / 24"
- Total of 24 items from lecture slides

### Bins Used
- How many bins have been created
- Goal: Minimize this number!

### Efficiency
- Percentage of space actually used
- Formula: `(total_items_size / total_bin_capacity) × 100`
- Higher is better!
- 100% would mean no wasted space

## Visual Guide

### Bin Colors
- **Gray background**: Normal bin
- **Yellow background + glow**: Currently checking this bin
- **Green background + glow**: Selected - item will go here!
- **Red background**: Rejected - item doesn't fit

### Item Display
- **Gray chips**: Not yet processed
- **Green chips**: Already packed
- **Red pulsing chip**: Currently being placed

### Bin Capacity Display
- **Green text**: Bin is 100% full
- **Yellow text**: Bin is 80-99% full
- **Gray text**: Bin is under 80%

## Classroom Tips

### For Instructors

1. **First Demo - First Fit**
   - Run in step-by-step mode
   - Pause after each item
   - Ask: "Where will this item go?"
   - Click "Next Step" to reveal

2. **Second Demo - Best Fit**
   - Run same data with Best Fit
   - Compare final bin counts
   - Discuss: "Which is better? Why?"

3. **Speed Comparison**
   - First Fit: Checks fewer bins (faster)
   - Best Fit: Checks all bins (slower but more thorough)

4. **Edge Cases to Highlight**
   - Item 8: Creates new bin in both algorithms
   - Small items (2, 3): Fill gaps in Best Fit
   - Large items (7, 8): Often need new bins

### Discussion Questions

1. "Why doesn't Best Fit always use fewer bins than First Fit?"
2. "What's the theoretical minimum bins needed? (Answer: 11)"
3. "Can you think of an item order that would be optimal?"
4. "What if we sorted items first? (Hint: First Fit Decreasing!)"

## Troubleshooting

### Web App Won't Load
- Make sure you're using a modern browser (Chrome, Firefox, Safari, Edge)
- Try the Python web server method (see "How to Run" above)

### Animations Too Fast/Slow
- Use the speed slider
- Range: 0.2s (fast) to 2.0s (slow) per step

### Want to Try Again
- Click "Reset" button
- Switch algorithms
- Click "Start" to begin fresh

## Technical Details

- **No installation required**: Pure HTML/CSS/JavaScript
- **Works offline**: No internet connection needed
- **No data collection**: Everything runs in your browser
- **Browser requirements**: Any modern browser from last 5 years

## Lecture Data

Pre-loaded with your specific instance:
- **Bin Capacity**: 10
- **Items**: [4, 4, 5, 5, 5, 4, 4, 6, 6, 2, 2, 3, 3, 7, 7, 2, 2, 5, 5, 8, 8, 4, 4, 5]
- **Total Items**: 24
- **Total Size**: 110
- **Theoretical Minimum**: ⌈110/10⌉ = 11 bins

---

**Pro Tip**: Open this guide in one window and the web app in another window side-by-side!
