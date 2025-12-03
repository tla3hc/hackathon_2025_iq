# Hackathon 2025 - Delivery Optimization System

## Overview
This is a Python-based delivery optimization system for the Hackathon 2025 competition. The system uses advanced algorithms (A*, Dijkstra) to plan optimal delivery routes and maximize profit.

## Project Structure
```
src/
├── main.py              # Main controller and entry point
├── api_client.py        # API communication with competition server
├── graph.py             # Graph representation and pathfinding (A*, Dijkstra)
├── package_selector.py  # Package selection strategies
├── route_optimizer.py   # Route optimization algorithms
├── config.py            # Configuration parameters
└── utils.py             # Utility functions
```

## Requirements
```bash
pip install requests pyjwt
```

## Configuration
Edit `config.py` to adjust:
- `SERVER_URL`: Competition server URL (default: http://127.0.0.1:5000)
- `PASSWORD`: Authentication password
- `MAX_PACKAGES_PER_TRIP`: Maximum packages per delivery (default: 3)
- `USE_ASTAR`: Use A* (True) or Dijkstra (False)
- `DISTANCE_WEIGHT`: Weight for distance cost
- `REWARD_WEIGHT`: Weight for delivery reward

## Usage

### Basic Usage
```bash
python src/main.py
```

### Advanced Usage
You can also import and use individual components:

```python
from api_client import APIClient
from graph import Graph
from package_selector import PackageSelector
from route_optimizer import RouteOptimizer

# Initialize components
api = APIClient()
api.login()

# Get road data and build graph
road_data = api.get_road_information()
graph = Graph()
graph.build_from_road_data(road_data)

# Load and select packages
packages_data = api.get_packages()
selector = PackageSelector(graph)
selector.load_packages(packages_data)

current_pos = (200.0, 187.0)
selected = selector.select_packages_greedy(current_pos, max_packages=3)

# Optimize route
optimizer = RouteOptimizer(graph)
result = optimizer.optimize_and_evaluate(selected, current_pos)
print(f"Net profit: ${result['net_profit']:.2f}")
```

## Algorithm Features

### 1. Pathfinding (graph.py)
- **A* Algorithm**: Efficient pathfinding with heuristic
- **Dijkstra Algorithm**: Guaranteed shortest path
- Automatically builds graph from road network
- Finds nearest road nodes to arbitrary positions

### 2. Package Selection (package_selector.py)
- **Greedy Selection**: Iteratively selects most profitable packages
- **Density-based Selection**: Groups nearby packages for efficient delivery
- **Profit Calculation**: Considers reward vs distance cost
- Supports dynamic dropoff locations

### 3. Route Optimization (route_optimizer.py)
- **Nearest Neighbor Heuristic**: Fast route ordering
- **Brute Force Optimization**: Exhaustive search for small package sets
- **Full Path Generation**: Complete waypoint sequences
- **Cost Estimation**: Calculates total distance and profit

## Competition Strategy

### Winning Approach
1. **Package Selection**: Choose packages with highest profit (reward - distance)
2. **Route Optimization**: Minimize total travel distance
3. **Capacity Management**: Deliver up to 3 packages per trip efficiently
4. **Greedy Strategy**: Continuously deliver most profitable remaining packages

### Profit Formula
```
Profit = Total_Reward - (Total_Distance × Distance_Weight)
```

### Scoring
- **Primary**: Number of packages delivered
- **Tiebreaker**: Shortest total distance traveled

## API Endpoints Used
- `POST /login`: Authenticate with server
- `GET /health`: Check server status
- `GET /road_information`: Get road network map
- `GET /packages`: Get available packages
- `GET /car`: Get current car state
- `GET /get_tokens`: Get route verification tokens
- `POST /set_index`: Submit route index

## Troubleshooting

### Login Failed
- Verify `PASSWORD` in config.py matches server password
- Check server is running at `SERVER_URL`

### No Path Found
- Ensure road network data is loaded correctly
- Check if start/end positions are reachable
- Try increasing distance tolerance in graph building

### No Profitable Packages
- Adjust `DISTANCE_WEIGHT` and `REWARD_WEIGHT` in config.py
- Check package dropoff locations are set
- Verify packages haven't all been delivered

## Development Tips

### Testing Locally
1. Start the localization server (provided by organizers)
2. Update `SERVER_URL` in config.py if needed
3. Run: `python src/main.py`

### Debugging
Enable debug mode in config.py:
```python
DEBUG = True
```

### Customization
- Modify selection strategy in `package_selector.py`
- Adjust optimization algorithm in `route_optimizer.py`
- Tune weights and parameters in `config.py`

## Performance Optimization

### For Speed
- Use A* instead of Dijkstra (faster with similar accuracy)
- Use greedy selection instead of brute force
- Reduce `POLL_INTERVAL` for faster status checks

### For Accuracy
- Use brute force optimization for small package sets
- Increase graph resolution
- Use Dijkstra for guaranteed shortest paths

## Competition Day Checklist
- [ ] Verify server connection
- [ ] Test login credentials
- [ ] Confirm package data format
- [ ] Validate route submission
- [ ] Check timing constraints
- [ ] Monitor profit calculations
- [ ] Backup configuration

## License
Competition entry for Hackathon 2025

## Authors
Your Team Name Here

---
**Good luck and deliver smart, not fast!** 🚚📦
