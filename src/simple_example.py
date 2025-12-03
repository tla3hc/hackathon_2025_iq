"""
Simple example demonstrating basic usage of the delivery system.
This is a simplified version for learning and testing.
"""
from api_client import APIClient
from graph import Graph
from package_selector import PackageSelector
from route_optimizer import RouteOptimizer
from config import SERVER_URL, PASSWORD


def simple_example():
    """Simple example of using the system."""
    
    print("=" * 60)
    print("SIMPLE EXAMPLE - Hackathon 2025 Delivery System")
    print("=" * 60)
    
    # Step 1: Connect to server
    print("\n[Step 1] Connecting to server...")
    api = APIClient(SERVER_URL, PASSWORD)
    
    if not api.login():
        print("Failed to login!")
        return
    
    print("✓ Connected and authenticated")
    
    # Step 2: Load road network
    print("\n[Step 2] Loading road network...")
    road_data = api.get_road_information()
    
    if not road_data:
        print("Failed to get road data!")
        return
    
    graph = Graph()
    graph.build_from_road_data(road_data)
    print(f"✓ Loaded {len(graph.nodes)} road nodes")
    
    # Step 3: Load packages
    print("\n[Step 3] Loading packages...")
    packages_data = api.get_packages()
    
    if not packages_data:
        print("Failed to get packages!")
        return
    
    selector = PackageSelector(graph)
    selector.load_packages(packages_data)
    print(f"✓ Loaded {len(selector.packages)} packages")
    
    # Step 4: Get current car position
    print("\n[Step 4] Getting car position...")
    car_state = api.get_car_state()
    
    if not car_state:
        print("Failed to get car state!")
        return
    
    current_pos = tuple(car_state['position'])
    print(f"✓ Car at position: ({current_pos[0]:.2f}, {current_pos[1]:.2f})")
    print(f"  Car state: {car_state['state']}")
    
    # Step 5: Select packages to deliver
    print("\n[Step 5] Selecting packages...")
    # Note: In real competition, dropoff locations come from tokens
    # For this example, we'll just show which packages are available
    
    print(f"Available packages:")
    for pkg_id, pkg in list(selector.packages.items())[:5]:  # Show first 5
        print(f"  - Package {pkg_id}: at ({pkg.pickup_pos[0]:.1f}, {pkg.pickup_pos[1]:.1f})")
    
    # Step 6: Get tokens (if car is stopped)
    if car_state['state'] == 'STOP':
        print("\n[Step 6] Getting route tokens...")
        token_response = api.get_tokens()
        
        if token_response and "tokens" in token_response:
            tokens = token_response["tokens"]
            print(f"✓ Received {len(tokens)} tokens")
            
            # Decode first token to see coordinates
            if tokens:
                token_data = api.decode_token(tokens[0])
                if token_data and 'frame' in token_data:
                    coords = token_data['frame'].get('coordinates')
                    mac = token_data['frame'].get('MAC')
                    print(f"  Token coordinates: {coords}")
                    print(f"  Token MAC: {mac}")
        else:
            print("No tokens available (car may already be moving)")
    
    # Step 7: Demonstrate pathfinding
    print("\n[Step 7] Demonstrating pathfinding...")
    if len(selector.packages) > 0:
        first_package = list(selector.packages.values())[0]
        
        result = graph.find_path(current_pos, first_package.pickup_pos)
        if result:
            path, distance = result
            print(f"✓ Path to first package:")
            print(f"  - Distance: {distance:.2f} units")
            print(f"  - Waypoints: {len(path)} nodes")
        else:
            print("Could not find path to package")
    
    print("\n" + "=" * 60)
    print("Example complete! Check main.py for full implementation.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        simple_example()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
