"""
Test script for Hackathon 2025 Delivery Challenge
Run this to test individual components.
"""
from api_client import APIClient
from graph import Graph
from package_selector import PackageSelector
from route_optimizer import RouteOptimizer
from config import SERVER_URL, PASSWORD


def test_api_connection():
    """Test API connection and authentication."""
    print("=" * 60)
    print("TEST 1: API Connection")
    print("=" * 60)
    
    api = APIClient(SERVER_URL, PASSWORD)
    
    # Test health check
    print("\n[1] Testing health check...")
    health = api.check_health()
    if health:
        print(f"✓ Health check passed: {health}")
    else:
        print("✗ Health check failed")
        return False
    
    # Test login
    print("\n[2] Testing login...")
    if api.login():
        print("✓ Login successful")
    else:
        print("✗ Login failed")
        return False
    
    return True


def test_road_network(api):
    """Test road network loading."""
    print("\n" + "=" * 60)
    print("TEST 2: Road Network")
    print("=" * 60)
    
    print("\n[1] Getting road information...")
    road_data = api.get_road_information()
    if not road_data:
        print("✗ Failed to get road data")
        return False
    
    print(f"✓ Road data received:")
    print(f"  - Points: {len(road_data.get('points', []))}")
    print(f"  - Streets: {len(road_data.get('streets', []))}")
    
    print("\n[2] Building graph...")
    graph = Graph()
    graph.build_from_road_data(road_data)
    
    print("\n[3] Testing pathfinding...")
    if len(graph.nodes) >= 2:
        start_id = 0
        goal_id = min(5, len(graph.nodes) - 1)
        
        # Test A*
        result_astar = graph.astar(start_id, goal_id)
        if result_astar:
            path, distance = result_astar
            print(f"✓ A* path found: {len(path)} nodes, distance: {distance:.2f}")
        else:
            print("✗ A* failed")
        
        # Test Dijkstra
        result_dijkstra = graph.dijkstra(start_id, goal_id)
        if result_dijkstra:
            path, distance = result_dijkstra
            print(f"✓ Dijkstra path found: {len(path)} nodes, distance: {distance:.2f}")
        else:
            print("✗ Dijkstra failed")
    
    return graph


def test_packages(api, graph):
    """Test package loading and selection."""
    print("\n" + "=" * 60)
    print("TEST 3: Package Management")
    print("=" * 60)
    
    print("\n[1] Getting packages...")
    packages_data = api.get_packages()
    if not packages_data:
        print("✗ Failed to get packages")
        return False
    
    print(f"✓ Packages received: {len(packages_data)}")
    
    print("\n[2] Loading packages...")
    selector = PackageSelector(graph)
    selector.load_packages(packages_data)
    
    print("\n[3] Testing package selection...")
    # Use a sample position
    current_pos = (200.0, 187.0)
    
    # Test single best package
    best = selector.select_best_package(current_pos)
    if best:
        print(f"✓ Best package: {best.id}")
    else:
        print("⚠️  No best package found (may need dropoff locations)")
    
    # Test greedy selection
    selected = selector.select_packages_greedy(current_pos, max_packages=3)
    print(f"✓ Greedy selection: {len(selected)} packages")
    
    return selector


def test_route_optimization(graph, selector):
    """Test route optimization."""
    print("\n" + "=" * 60)
    print("TEST 4: Route Optimization")
    print("=" * 60)
    
    optimizer = RouteOptimizer(graph)
    
    # Create some test packages with dummy dropoff locations
    test_packages = []
    for pkg_id, pkg in list(selector.packages.items())[:3]:
        # Set dummy dropoff (in real competition, these come from server)
        pkg.dropoff_pos = (pkg.pickup_pos[0] + 100, pkg.pickup_pos[1] + 100)
        test_packages.append(pkg)
    
    if not test_packages:
        print("⚠️  No packages available for optimization test")
        return
    
    print(f"\n[1] Testing with {len(test_packages)} packages...")
    current_pos = (200.0, 187.0)
    
    # Test optimization
    result = optimizer.optimize_and_evaluate(test_packages, current_pos)
    
    print(f"✓ Optimization complete:")
    print(f"  - Packages: {result['package_count']}")
    print(f"  - Distance: {result['total_distance']:.2f}")
    print(f"  - Reward: ${result['total_reward']:.2f}")
    print(f"  - Net Profit: ${result['net_profit']:.2f}")
    print(f"  - Waypoints: {len(result['waypoints'])}")


def test_car_state(api):
    """Test car state retrieval."""
    print("\n" + "=" * 60)
    print("TEST 5: Car State")
    print("=" * 60)
    
    print("\n[1] Getting car state...")
    car_state = api.get_car_state()
    
    if car_state:
        print(f"✓ Car state received:")
        print(f"  - State: {car_state.get('state')}")
        print(f"  - Position: {car_state.get('position')}")
        print(f"  - Orientation: {car_state.get('orientation')}")
        print(f"  - Obstacles: {len(car_state.get('obstacles', []))} points")
    else:
        print("✗ Failed to get car state")


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("*" * 60)
    print("HACKATHON 2025 - COMPONENT TEST SUITE")
    print("*" * 60)
    
    # Test 1: API
    if not test_api_connection():
        print("\n✗ API tests failed, cannot continue")
        return
    
    api = APIClient(SERVER_URL, PASSWORD)
    api.login()
    
    # Test 2: Road Network
    graph = test_road_network(api)
    if not graph:
        print("\n✗ Road network tests failed, cannot continue")
        return
    
    # Test 3: Packages
    selector = test_packages(api, graph)
    if not selector:
        print("\n✗ Package tests failed")
    
    # Test 4: Route Optimization
    if selector:
        test_route_optimization(graph, selector)
    
    # Test 5: Car State
    test_car_state(api)
    
    print("\n" + "*" * 60)
    print("ALL TESTS COMPLETE")
    print("*" * 60)


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Test error: {e}")
        import traceback
        traceback.print_exc()
