# Quick Start Guide

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure the system:**
Edit `config.py` to set your server URL and password:
```python
SERVER_URL = "http://127.0.0.1:5000"
PASSWORD = "your_password_here"
```

## Running the System

### Option 1: Run the complete system
```bash
python main.py
```

This will:
- Login to the server
- Load road network and packages
- Continuously select and deliver packages
- Optimize routes for maximum profit
- Display progress and statistics

### Option 2: Run the simple example
```bash
python simple_example.py
```

This demonstrates basic functionality without running the full delivery loop.

### Option 3: Test components individually
```bash
python test_components.py
```

This runs unit tests on all components.

## Understanding the Output

```
====================================================
HACKATHON 2025 - DELIVERY OPTIMIZATION SYSTEM
====================================================

[1/4] Checking server health...
✓ Server healthy: healthy

[2/4] Authenticating...
✓ Login successful

[3/4] Loading road network...
✓ Graph built: 28 nodes, 86 edges

[4/4] Loading packages...
✓ Loaded 10 packages

✓ Initialization complete!
====================================================

====================================================
DELIVERY CYCLE #1
====================================================

📍 Current position: (178.25, 190.00)
📦 Undelivered packages: 10

🔑 Getting route tokens...
✓ Received 10 tokens

🎯 Selecting up to 3 packages...
✓ Selected 3 packages:
  - Package 1: (1524.00, 2389.00)
  - Package 2: (1127.00, 1350.00)
  - Package 3: (833.00, 2488.00)

🚀 Optimizing delivery route...
✓ Route optimized:
  - Packages: 3
  - Distance: 4521.34
  - Reward: $3.00
  - Net Profit: $-4518.34

📤 Submitting route (index: 0)...
✓ Route index 0 submitted successfully

⏳ Waiting for car to stop...
✓ Delivery cycle complete!
  - Delivered: 3 packages
```

## Configuration Options

### Algorithm Selection
```python
USE_ASTAR = True  # Use A* (faster) vs Dijkstra (more accurate)
```

### Profit Calculation
```python
DISTANCE_WEIGHT = 1.0  # Cost per unit distance
REWARD_WEIGHT = 1.0    # Value multiplier for rewards
```

Adjust these to change how profit is calculated:
- Higher `DISTANCE_WEIGHT` → Prefer shorter routes
- Higher `REWARD_WEIGHT` → Prefer high-value packages

### Package Selection
```python
MAX_PACKAGES_PER_TRIP = 3  # Maximum packages per delivery
```

## Strategy Tips

1. **For Maximum Packages Delivered:**
   - Use greedy selection strategy
   - Minimize distance between pickups
   - Cluster nearby packages

2. **For Shortest Distance (Tiebreaker):**
   - Use A* pathfinding
   - Optimize delivery order with brute force (for small sets)
   - Avoid backtracking

3. **For Maximum Profit:**
   - Select high-value packages first
   - Consider distance vs reward ratio
   - Use profit density metric

## Troubleshooting

**Problem:** "Login failed"
- Check `PASSWORD` in config.py
- Verify server is running at `SERVER_URL`

**Problem:** "No path found"
- Road network may be disconnected
- Try different start/end positions
- Check graph building output

**Problem:** "No profitable packages"
- Adjust `DISTANCE_WEIGHT` and `REWARD_WEIGHT`
- Check if packages have dropoff locations set
- Verify packages aren't all delivered

**Problem:** "Car not stopping"
- Increase timeout in `wait_for_car_stop()`
- Check car state with `api.get_car_state()`
- Verify route submission was successful

## Advanced Usage

### Using Advanced Strategies
```python
from advanced_strategies import AdvancedPackageSelector, AdaptiveStrategy

# Use profit density selection
advanced = AdvancedPackageSelector(graph)
advanced.load_packages(packages_data)
selected = advanced.select_packages_by_profit_density(current_pos)

# Use adaptive strategy
adaptive = AdaptiveStrategy(selector)
selected = adaptive.select_packages_adaptive(current_pos, remaining_time=120)
```

### Custom Package Selection
```python
# Select single best package
best = selector.select_best_package(current_pos)

# Greedy selection
selected = selector.select_packages_greedy(current_pos, max_packages=3)

# Clustering-based selection
selected = selector.select_packages_by_density(current_pos, max_packages=3)
```

### Route Optimization
```python
from route_optimizer import RouteOptimizer

optimizer = RouteOptimizer(graph)

# Optimize order (nearest neighbor)
optimized = optimizer.optimize_delivery_order(packages, start_pos)

# Optimize order (brute force for small sets)
optimized = optimizer.optimize_delivery_order_bruteforce(packages, start_pos)

# Get full evaluation
result = optimizer.optimize_and_evaluate(packages, start_pos)
print(f"Net profit: ${result['net_profit']:.2f}")
```

## Competition Checklist

Before the competition:
- [ ] Test connection to competition server
- [ ] Verify login credentials work
- [ ] Run `test_components.py` successfully
- [ ] Test a complete delivery cycle
- [ ] Check profit calculations are reasonable
- [ ] Ensure code handles edge cases (no packages, no path, etc.)

During the competition:
- [ ] Monitor console output for errors
- [ ] Track packages delivered vs remaining
- [ ] Watch profit/distance metrics
- [ ] Be ready to adjust weights if needed

## Files Reference

- `main.py` - Main entry point, full delivery system
- `api_client.py` - Server communication
- `graph.py` - Pathfinding algorithms
- `package_selector.py` - Package selection strategies
- `route_optimizer.py` - Route optimization
- `config.py` - Configuration parameters
- `utils.py` - Utility functions
- `simple_example.py` - Basic usage example
- `test_components.py` - Component tests
- `advanced_strategies.py` - Advanced algorithms

Good luck! 🚚📦
