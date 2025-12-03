"""
Mock Server for Hackathon 2025 Delivery Challenge
Simulates the competition server for testing purposes.
"""
from flask import Flask, request, jsonify, session, make_response, render_template
import json
import time
import random
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'hackathon2025_mock_secret_key'

# Load example payloads
EXAMPLE_DIR = Path(__file__).parent.parent / 'example_and_api' / 'example_payload'

with open(EXAMPLE_DIR / 'response_health.json', 'r') as f:
    HEALTH_RESPONSE = json.load(f)

with open(EXAMPLE_DIR / 'response_road_information.json', 'r') as f:
    ROAD_INFO = json.load(f)

with open(EXAMPLE_DIR / 'response_packages.json', 'r') as f:
    PACKAGES = json.load(f)

# Add random dropoff locations for packages (simulating competition behavior)
with open(EXAMPLE_DIR / 'response_road_information.json', 'r') as f:
    road_data = json.load(f)
    available_points = road_data.get('points', [])

# Assign random dropoff locations and rewards to each package
print(f"\n📦 Adding dropoffs and rewards to {len(PACKAGES)} packages...")
for pkg_id, pkg_data in PACKAGES.items():
    if 'dropoff' not in pkg_data and available_points:
        # Pick a random point from the road network as dropoff
        dropoff = random.choice(available_points)
        pkg_data['dropoff'] = dropoff
        print(f"  Package {pkg_id}: Added dropoff={dropoff}")
    
    # Add reward if not present (simulating point values)
    if 'reward' not in pkg_data:
        # Assign random reward between 500-1500 points (adjusted for large map scale)
        pkg_data['reward'] = random.uniform(500.0, 1500.0)
        print(f"  Package {pkg_id}: Added reward={pkg_data['reward']:.2f}")

with open(EXAMPLE_DIR / 'response_car.json', 'r') as f:
    CAR_STATE = json.load(f)

# Note: response_get_tokens.json has comments, so we define tokens directly
TOKENS_RESPONSE = {
    "tokens": [
        "eyJhbGciOiJFUzI1NiIsIm1hY0FsZyI6IkNNQUNfQUVTXzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmFtZSI6eyJjb29yZGluYXRlcyI6WzIwMC4wLDE4Ny4wXSwiTUFDIjoiMTVGMURGQ0I1RUIyOUEwOEZFRENFMDRBRUEyNkVEQzgifSwiaWF0IjoxNzY0NzI2MzI4LCJleHAiOjE3NjQ3MjgxMjh9.Wpo1JPmXWAkeHGcsRbUZYsqTvEYT-XhmDEnBvXZIH0fFtPhK9e6GYSkobVsZXn6UEdgn1BkFksZvR6a-RfTdXg",
        "eyJhbGciOiJFUzI1NiIsIm1hY0FsZyI6IkNNQUNfQUVTXzEyOCIsInR5cCI6IkpXVCJ9.eyJmcmFtZSI6eyJjb29yZGluYXRlcyI6WzIwMC4wLDE4Ny4wXSwiTUFDIjoiMjEzMGY5M2M0NDlhZDcwOWMwMWMxNDkxZmNkODczYzgifSwiaWF0IjoxNzY0NzI2MzI4LCJleHAiOjE3NjQ3MjgxMjh9.nMeoY49Ewx4jM7-A3cbLIPcsmVKq3CHDKpW-Rzk2dF0v2sGIftNzBPbNuJqReElwK17pmJRXw1RTmEMiIMBK1Q",
        "eyJhbGciOiJFUzI1NiIsIm1hY0FsZyI6IkhNQUNfU0hBXzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmFtZSI6eyJjb29yZGluYXRlcyI6WzIwMC4wLDE4Ny4wXSwiTUFDIjoiODAyQzRFREMyRkJBMzExQjdCODkzOTZCMUMyRTIwNkE4N0EwMkRDNTZDOEQ3QkE1OTcyMkU3MTc4Qzk2NkIwMSJ9LCJpYXQiOjE3NjQ3MjYzMjgsImV4cCI6MTc2NDcyODEyOH0.OTceefHip_-5dn-LA3NcCLTkV3Lgx8kOacHTc3rZtNyYkOcOg7Kgcz5xtf9NoRJTzm7x7zq88sMK1hvF8lGsig",
    ]
}

# Server state
PASSWORD = "dummy_password"

# Per-session state: key is session_id, value is dict with car_running, route_index, delivered_packages
session_states = {}

# Global delivered packages (for competitive mode - shared across all players)
globally_delivered_packages = set()

# Competition mode flag
COMPETITIVE_MODE = True  # Set to False for isolated testing

# Build adjacency graph for road-following waypoints
def build_road_graph():
    """Build adjacency list from streets for waypoint generation."""
    graph = {}
    for street in ROAD_INFO.get('streets', []):
        start = tuple(street['start'])
        end = tuple(street['end'])
        
        if start not in graph:
            graph[start] = []
        if end not in graph:
            graph[end] = []
        
        # Bidirectional roads
        if end not in graph[start]:
            graph[start].append(end)
        if start not in graph[end]:
            graph[end].append(start)
    
    return graph

ROAD_GRAPH = build_road_graph()

def generate_road_following_waypoints(start_point, num_waypoints=5):
    """Generate waypoints that follow actual roads."""
    if not ROAD_GRAPH:
        return [start_point]
    
    # Convert to tuple
    start = tuple(start_point)
    
    # If start not in graph, find nearest point
    if start not in ROAD_GRAPH:
        min_dist = float('inf')
        for point in ROAD_GRAPH.keys():
            dist = ((point[0] - start[0])**2 + (point[1] - start[1])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                start = point
    
    waypoints = [start]
    current = start
    visited = {start}
    
    # Generate path by following connected roads
    for _ in range(num_waypoints):
        neighbors = ROAD_GRAPH.get(current, [])
        if not neighbors:
            break
        
        # Prefer unvisited neighbors
        unvisited = [n for n in neighbors if n not in visited]
        if unvisited:
            next_point = random.choice(unvisited)
        else:
            # If all visited, pick any neighbor
            next_point = random.choice(neighbors)
        
        waypoints.append(next_point)
        visited.add(next_point)
        current = next_point
    
    return waypoints


@app.route('/')
def index():
    """Homepage with API listing."""
    num_sessions = len(session_states)
    mode = "🏆 COMPETITIVE" if COMPETITIVE_MODE else "🔒 ISOLATED"
    return f"""
    <html>
    <head><title>Mock Hackathon 2025 Server</title></head>
    <body>
        <h1>Mock Hackathon 2025 Delivery Challenge Server</h1>
        <h2>Available Endpoints:</h2>
        <ul>
            <li>GET /health - Health check</li>
            <li>POST /login - Login (password: dummy_password)</li>
            <li>GET /logout - Logout</li>
            <li>GET /road_information - Get road network</li>
            <li>GET /packages - Get available packages</li>
            <li>GET /car - Get car state</li>
            <li>GET /get_tokens - Get route tokens</li>
            <li>POST /set_index - Submit route index</li>
        </ul>
        <h2>Admin Endpoints:</h2>
        <ul>
            <li>GET /sessions - View all active sessions</li>
            <li>GET /leaderboard - Competition leaderboard</li>
            <li>GET /reset - Reset current session</li>
            <li>GET /reset_all - Reset all sessions and packages</li>
        </ul>
        <p><strong>Mode:</strong> {mode}</p>
        <p><strong>Active Sessions:</strong> {num_sessions}</p>
        <p><strong>Total Packages:</strong> {len(PACKAGES)}</p>
        <p><strong>Delivered:</strong> {len(globally_delivered_packages)}</p>
        <p><strong>Remaining:</strong> {len(PACKAGES) - len(globally_delivered_packages)}</p>
        <h2>🎮 Dashboard:</h2>
        <p><a href="/dashboard" style="font-size: 18px; color: blue;">📊 Open Live Dashboard</a></p>
    </body>
    </html>
    """


@app.route('/dashboard')
def dashboard():
    """Serve the live dashboard."""
    return render_template('dashboard.html')


@app.route('/api/road_information', methods=['GET'])
def api_road_information():
    """Get road information without authentication (for dashboard)."""
    return jsonify(ROAD_INFO)


@app.route('/api/packages_all', methods=['GET'])
def api_packages_all():
    """Get all packages with their status for dashboard."""
    packages_list = []
    for pkg_id, pkg_data in PACKAGES.items():
        packages_list.append({
            'id': pkg_id,
            'position': pkg_data.get('position', [0, 0]),
            'dropoff': pkg_data.get('dropoff', [0, 0]),
            'reward': pkg_data.get('reward', 0)
        })
    return jsonify(packages_list)


@app.route('/health')
def health():
    """Health check endpoint."""
    response = HEALTH_RESPONSE.copy()
    response['timestamp'] = time.time()
    return jsonify(response)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint."""
    if request.method == 'GET':
        return """
        <html>
        <body>
            <h2>Login</h2>
            <form method="POST">
                <label>Password: <input type="password" name="password"></label>
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
        """
    
    # POST request
    password = None
    if request.is_json:
        password = request.json.get('password')
    else:
        password = request.form.get('password')
    
    if password == PASSWORD:
        session['authenticated'] = True
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid password"}), 401


@app.route('/logout')
def logout():
    """Logout endpoint."""
    session.clear()
    return jsonify({"message": "Logged out successfully"})


def get_session_state():
    """Get or create session-specific state."""
    session_id = session.get('session_id')
    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    
    if session_id not in session_states:
        # Initialize car at depot (bottom-left corner of grid)
        session_states[session_id] = {
            'car_running': False,
            'current_route_index': 0,
            'delivered_packages': set(),
            'car_position': [300, 300],  # Start at depot
            'car_index': 0,
            'route_waypoints': [],  # Waypoints for current route
            'waypoint_index': 0  # Current waypoint progress
        }
    
    return session_states[session_id]


def require_auth(f):
    """Decorator to require authentication."""
    def wrapper(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/road_information')
@require_auth
def road_information():
    """Get road network information."""
    return jsonify(ROAD_INFO)


@app.route('/packages')
@require_auth
def packages():
    """Get available packages."""
    state = get_session_state()
    session_id = session.get('session_id')
    
    if COMPETITIVE_MODE:
        # In competitive mode, filter out packages delivered by ANY player
        available = {k: v for k, v in PACKAGES.items() if int(k) not in globally_delivered_packages}
    else:
        # In isolated mode, filter out only this session's delivered packages
        available = {k: v for k, v in PACKAGES.items() if int(k) not in state['delivered_packages']}
    
    # Ensure all packages have dropoff and reward (in case module-level code didn't run)
    available_points = ROAD_INFO.get('points', [])
    for pkg_id, pkg_data in available.items():
        if 'dropoff' not in pkg_data and available_points:
            pkg_data['dropoff'] = random.choice(available_points)
        if 'reward' not in pkg_data:
            pkg_data['reward'] = random.uniform(500.0, 1500.0)
    
    print(f"\n📤 [Session {session_id[:8]}] /packages: {len(available)} available ({len(globally_delivered_packages)} globally delivered)")
    return jsonify(available)


@app.route('/car')
@require_auth
def car():
    """Get car state."""
    session_state = get_session_state()
    
    state = CAR_STATE.copy()
    
    # Simulate car movement
    if session_state['car_running']:
        # Simulate gradual movement along waypoints
        waypoints = session_state.get('route_waypoints', [])
        waypoint_idx = session_state.get('waypoint_index', 0)
        
        if waypoints and waypoint_idx < len(waypoints):
            # Update position to next waypoint every 8 polls (slower movement)
            route_index = session_state['current_route_index']
            if route_index % 8 == 0 and waypoint_idx < len(waypoints) - 1:
                waypoint_idx += 1
                session_state['waypoint_index'] = waypoint_idx
                session_state['car_position'] = waypoints[waypoint_idx].copy()
        
        state['position'] = session_state['car_position'].copy()
        
        # Randomly choose a state
        states = ['MOVE_FORWARD', 'TURN', 'BLOCKED']
        state['state'] = random.choice(states)
        
        session_state['current_route_index'] += 1
    else:
        state['state'] = 'STOP'
        state['position'] = session_state['car_position'].copy()
    
    return jsonify(state)


@app.route('/get_tokens')
@require_auth
def get_tokens():
    """Get route tokens."""
    session_state = get_session_state()
    
    if session_state['car_running']:
        return jsonify({"message": "Car is running, cannot get tokens"})
    
    # Return tokens from example
    return jsonify(TOKENS_RESPONSE)


@app.route('/set_index', methods=['POST'])
@require_auth
def set_index():
    """Submit route index."""
    global globally_delivered_packages
    session_state = get_session_state()
    session_id = session.get('session_id')
    
    data = request.get_json()
    index = data.get('index')
    
    if index is None:
        return jsonify({"message": "Index required"}), 400
    
    session_state['current_route_index'] = index
    session_state['car_running'] = True
    
    # Generate waypoints that follow actual roads
    current_pos = session_state['car_position']
    num_waypoints = random.randint(4, 7)  # 4-7 stops
    waypoints = generate_road_following_waypoints(current_pos, num_waypoints)
    
    # Convert tuples back to lists for JSON serialization
    waypoints = [list(wp) for wp in waypoints]
    
    session_state['route_waypoints'] = waypoints
    session_state['waypoint_index'] = 0
    
    # Simulate car starting to move
    print(f"\n🚗 [Session {session_id[:8]}] Car starting route with index: {index}")
    
    # Simulate some packages being delivered
    # In a real scenario, this would depend on the route
    if COMPETITIVE_MODE:
        # In competitive mode, check globally available packages
        available = [k for k in PACKAGES.keys() if int(k) not in globally_delivered_packages]
    else:
        # In isolated mode, check only session's packages
        available = [k for k in PACKAGES.keys() if int(k) not in session_state['delivered_packages']]
    
    if available:
        num_to_deliver = min(3, len(available))
        to_deliver = random.sample(available, num_to_deliver)
        
        for pkg_id in to_deliver:
            pkg_id_int = int(pkg_id)
            session_state['delivered_packages'].add(pkg_id_int)
            if COMPETITIVE_MODE:
                globally_delivered_packages.add(pkg_id_int)
        
        print(f"   [Session {session_id[:8]}] Delivered packages: {to_deliver}")
        if COMPETITIVE_MODE:
            print(f"   🏆 Total delivered globally: {len(globally_delivered_packages)}/{len(PACKAGES)}")
    
    # Simulate car stopping after completing route
    import threading
    def stop_car(sid):
        # Calculate time based on number of waypoints (more time for longer routes)
        num_waypoints = len(session_states[sid].get('route_waypoints', []))
        # Give enough time for car to traverse all waypoints (8 polls per waypoint * 0.2s per poll)
        travel_time = max(5, num_waypoints * 1.8)  # At least 5 seconds, or 1.8s per waypoint
        time.sleep(travel_time)
        if sid in session_states:
            session_states[sid]['car_running'] = False
            print(f"   [Session {sid[:8]}] Car stopped")
    
    threading.Thread(target=stop_car, args=(session_id,), daemon=True).start()
    
    return jsonify({"message": f"Route index {index} submitted successfully"})


@app.route('/reset')
def reset():
    """Reset server state (for testing)."""
    session_id = session.get('session_id')
    if session_id and session_id in session_states:
        # Reset only this session's state
        session_states[session_id] = {
            'car_running': False,
            'current_route_index': 0,
            'delivered_packages': set()
        }
        message = f"Session {session_id[:8]} state reset (competitive packages NOT reset)"
    else:
        message = "No active session to reset"
    
    return jsonify({"message": message})


@app.route('/reset_all')
def reset_all():
    """Reset all session states (admin endpoint)."""
    global session_states, globally_delivered_packages
    num_sessions = len(session_states)
    num_global_pkgs = len(globally_delivered_packages)
    session_states.clear()
    globally_delivered_packages.clear()
    return jsonify({
        "message": f"All {num_sessions} session(s) reset, {num_global_pkgs} packages back in pool",
        "sessions_cleared": num_sessions,
        "packages_reset": num_global_pkgs
    })


@app.route('/sessions')
def sessions():
    """View all active sessions (admin endpoint)."""
    sessions_info = {}
    for sid, state in session_states.items():
        car_position = state.get('car_position', [0, 0])
        car_index = state.get('car_index', 0)
        route_waypoints = state.get('route_waypoints', [])
        waypoint_index = state.get('waypoint_index', 0)
        
        sessions_info[sid[:8]] = {
            'session_id': sid[:8],
            'car_running': state['car_running'],
            'delivered_count': len(state['delivered_packages']),
            'delivered_packages': list(state['delivered_packages']),
            'remaining_packages': len(PACKAGES) - len(state['delivered_packages']) if not COMPETITIVE_MODE else len(PACKAGES) - len(globally_delivered_packages),
            'car': {
                'status': 'running' if state['car_running'] else 'idle',
                'position': car_position,
                'index': car_index,
                'route_waypoints': route_waypoints,  # Planned path
                'waypoint_index': waypoint_index,     # Current progress
                'route_progress': f"{waypoint_index}/{len(route_waypoints)}" if route_waypoints else "0/0"
            } if state['car_running'] or car_position != [0, 0] else None
        }
    
    # Sort by delivered count (leaderboard)
    leaderboard = sorted(
        [(sid[:8], len(state['delivered_packages'])) for sid, state in session_states.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    return jsonify({
        "competitive_mode": COMPETITIVE_MODE,
        "total_sessions": len(session_states),
        "globally_delivered": list(globally_delivered_packages) if COMPETITIVE_MODE else [],
        "remaining_packages": len(PACKAGES) - len(globally_delivered_packages) if COMPETITIVE_MODE else None,
        "leaderboard": leaderboard[:10],  # Top 10
        "sessions": sessions_info
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Mock Hackathon 2025 Server Starting...")
    print("=" * 60)
    print(f"Server URL: http://127.0.0.1:5000")
    print(f"Password: {PASSWORD}")
    print(f"Total Packages: {len(PACKAGES)}")
    print(f"Mode: {'🏆 COMPETITIVE' if COMPETITIVE_MODE else '🔒 ISOLATED'}")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  GET  /health")
    print("  POST /login")
    print("  GET  /logout")
    print("  GET  /road_information")
    print("  GET  /packages")
    print("  GET  /car")
    print("  GET  /get_tokens")
    print("  POST /set_index")
    print("\nAdmin endpoints:")
    print("  GET  /sessions - View all active sessions")
    print("  GET  /leaderboard - Competition rankings")
    print("  GET  /reset - Reset current session")
    print("  GET  /reset_all - Reset all sessions and packages")
    print("=" * 60)
    if COMPETITIVE_MODE:
        print("\n🏆 COMPETITIVE MODE ENABLED!")
        print("   - Packages are shared across all players")
        print("   - First to deliver wins the package")
        print("   - Real-time leaderboard tracking")
    else:
        print("\n🔒 ISOLATED MODE")
        print("   - Each client has independent packages")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
