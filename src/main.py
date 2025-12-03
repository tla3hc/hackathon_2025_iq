"""
Main Controller for Hackathon 2025 Delivery Challenge
Orchestrates the entire delivery process.
"""
import time
import sys
from typing import Optional

from api_client import APIClient
from graph import Graph
from package_selector import PackageSelector, Package
from route_optimizer import RouteOptimizer
from config import (
    SERVER_URL, PASSWORD, MAX_PACKAGES_PER_TRIP, 
    USE_ASTAR, POLL_INTERVAL, DEBUG, DISTANCE_WEIGHT, REWARD_WEIGHT
)
from utils import format_position, format_distance


class DeliveryController:
    """Main controller for the delivery challenge."""
    
    def __init__(self, server_url: str = SERVER_URL, password: str = PASSWORD):
        """
        Initialize delivery controller.
        
        Args:
            server_url: Competition server URL
            password: Authentication password
        """
        self.api = APIClient(server_url, password)
        self.graph = Graph()
        self.selector = None
        self.optimizer = None
        self.initialized = False
        
        self.total_packages_delivered = 0
        self.total_distance_traveled = 0.0
        self.total_reward_earned = 0.0
    
    def initialize(self) -> bool:
        """
        Initialize the system: login, get road data, get packages.
        
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("HACKATHON 2025 - DELIVERY OPTIMIZATION SYSTEM")
        print("=" * 60)
        
        # Check server health
        print("\n[1/4] Checking server health...")
        health = self.api.check_health()
        if health:
            print(f"✓ Server healthy: {health.get('status')}")
        else:
            print("✗ Server health check failed")
            return False
        
        # Login
        print("\n[2/4] Authenticating...")
        if not self.api.login():
            print("✗ Authentication failed")
            return False
        
        # Get road information
        print("\n[3/4] Loading road network...")
        road_data = self.api.get_road_information()
        if not road_data:
            print("✗ Failed to get road information")
            return False
        
        self.graph.build_from_road_data(road_data)
        
        # Get packages
        print("\n[4/4] Loading packages...")
        packages_data = self.api.get_packages()
        if not packages_data:
            print("✗ Failed to get packages")
            return False
        
        self.selector = PackageSelector(self.graph)
        self.selector.load_packages(packages_data)
        self.optimizer = RouteOptimizer(self.graph)
        
        self.initialized = True
        print("\n✓ Initialization complete!")
        print("=" * 60)
        
        return True
    
    def get_current_position(self) -> Optional[tuple]:
        """Get current car position."""
        car_state = self.api.get_car_state()
        if car_state:
            return tuple(car_state['position'])
        return None
    
    def wait_for_stop(self) -> bool:
        """Wait for car to stop."""
        print("⏳ Waiting for car to stop...")
        return self.api.wait_for_car_stop(poll_interval=POLL_INTERVAL)
    
    def execute_delivery_cycle(self) -> bool:
        """
        Execute one delivery cycle:
        1. Get current position
        2. Select best packages
        3. Optimize route
        4. Submit route
        5. Wait for completion
        
        Returns:
            True if successful, False otherwise
        """
        # Get current position
        current_pos = self.get_current_position()
        if not current_pos:
            print("✗ Failed to get current position")
            return False
        
        print(f"\n📍 Current position: {format_position(list(current_pos))}")
        
        # Check for remaining packages
        undelivered = self.selector.get_undelivered_count()
        print(f"📦 Undelivered packages: {undelivered}")
        
        if undelivered == 0:
            print("✓ All packages delivered!")
            return False
        
        # Get tokens and decode to find waypoint information
        print("\n🔑 Getting route tokens...")
        token_response = self.api.get_tokens()
        
        if not token_response:
            print("✗ Failed to get tokens")
            return False
        
        if "tokens" not in token_response:
            print(f"ℹ️  {token_response.get('message', 'No tokens available')}")
            return False
        
        tokens = token_response["tokens"]
        print(f"✓ Received {len(tokens)} tokens")
        
        # Decode first token to get coordinates (for verification)
        if tokens:
            token_payload = self.api.decode_token(tokens[0])
            if token_payload and 'frame' in token_payload:
                frame = token_payload['frame']
                coordinates = frame.get('coordinates')
                mac = frame.get('MAC')
                if DEBUG:
                    print(f"  Token coordinates: {coordinates}")
                    print(f"  Token MAC: {mac}")
        
        # Select packages for this trip
        print(f"\n🎯 Selecting up to {MAX_PACKAGES_PER_TRIP} packages...")
        selected_packages = self.selector.select_packages_greedy(
            current_pos, 
            max_packages=MAX_PACKAGES_PER_TRIP
        )
        
        if not selected_packages:
            print("✗ No profitable packages found")
            return False
        
        print(f"✓ Selected {len(selected_packages)} packages:")
        for pkg in selected_packages:
            print(f"  - Package {pkg.id}: {format_position(list(pkg.pickup_pos))}")
        
        # Optimize route
        print("\n🚀 Optimizing delivery route...")
        optimization = self.optimizer.optimize_and_evaluate(selected_packages, current_pos)
        
        print(f"✓ Route optimized:")
        print(f"  - Packages: {optimization['package_count']}")
        print(f"  - Distance: {format_distance(optimization['total_distance'])}")
        print(f"  - Reward: ${optimization['total_reward']:.2f}")
        print(f"  - Net Profit: ${optimization['net_profit']:.2f}")
        
        # For now, we submit index 0 as the example does
        # In a real implementation, you would need to understand the token system better
        # and determine the correct index based on the route planning
        route_index = 0
        
        print(f"\n📤 Submitting route (index: {route_index})...")
        if not self.api.set_route_index(route_index):
            print("✗ Failed to submit route")
            return False
        
        # Wait for car to complete the route
        if not self.wait_for_stop():
            print("✗ Car did not complete route in time")
            return False
        
        # Mark packages as delivered
        for pkg in selected_packages:
            self.selector.mark_delivered(pkg.id)
        
        # Update statistics
        self.total_packages_delivered += len(selected_packages)
        self.total_distance_traveled += optimization['total_distance']
        self.total_reward_earned += optimization['total_reward']
        
        print(f"✓ Delivery cycle complete!")
        print(f"  - Delivered: {len(selected_packages)} packages")
        
        return True
    
    def run(self):
        """Main execution loop."""
        if not self.initialized:
            print("✗ System not initialized. Call initialize() first.")
            return
        
        print("\n" + "=" * 60)
        print("STARTING DELIVERY OPERATIONS")
        print("=" * 60)
        
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                print(f"\n{'=' * 60}")
                print(f"DELIVERY CYCLE #{cycle_count}")
                print(f"{'=' * 60}")
                
                if not self.execute_delivery_cycle():
                    break
                
                time.sleep(1)  # Brief pause between cycles
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        except Exception as e:
            print(f"\n\n✗ Error: {e}")
            if DEBUG:
                import traceback
                traceback.print_exc()
        finally:
            self.print_summary()
    
    def print_summary(self):
        """Print final summary statistics."""
        distance_cost = self.total_distance_traveled * DISTANCE_WEIGHT
        net_profit = (self.total_reward_earned * REWARD_WEIGHT) - distance_cost
        
        print("\n" + "=" * 60)
        print("DELIVERY SUMMARY")
        print("=" * 60)
        print(f"Total Packages Delivered: {self.total_packages_delivered}")
        print(f"Total Distance Traveled: {format_distance(self.total_distance_traveled)}")
        print(f"Total Reward Earned: ${self.total_reward_earned:.2f}")
        print(f"Distance Cost: ${distance_cost:.2f}")
        print(f"Net Profit: ${net_profit:.2f}")
        print("=" * 60)


def main():
    """Main entry point."""
    controller = DeliveryController()
    
    if not controller.initialize():
        print("\n✗ Failed to initialize system")
        sys.exit(1)
    
    controller.run()


if __name__ == "__main__":
    main()
