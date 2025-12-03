"""
Route Optimizer for Hackathon 2025 Delivery Challenge
Optimizes delivery sequences and routes for selected packages.
"""
from typing import List, Tuple, Optional
import itertools
from graph import Graph
from package_selector import Package
from utils import euclidean_distance


class RouteOptimizer:
    """Optimizes delivery routes for packages."""
    
    def __init__(self, graph: Graph):
        """
        Initialize route optimizer.
        
        Args:
            graph: Road network graph
        """
        self.graph = graph
    
    def optimize_delivery_order(self, packages: List[Package], 
                                start_pos: Tuple[float, float]) -> List[Package]:
        """
        Find optimal order to deliver packages using nearest neighbor heuristic.
        
        Args:
            packages: List of packages to deliver
            start_pos: Starting position
        
        Returns:
            Optimized list of packages
        """
        if not packages:
            return []
        
        if len(packages) == 1:
            return packages
        
        # Use nearest neighbor approach
        unvisited = packages.copy()
        optimized = []
        current_pos = start_pos
        
        while unvisited:
            # Find nearest package pickup
            nearest = min(unvisited, key=lambda p: self._distance(current_pos, p.pickup_pos))
            optimized.append(nearest)
            unvisited.remove(nearest)
            # Update position to dropoff location
            current_pos = nearest.dropoff_pos
        
        return optimized
    
    def optimize_delivery_order_bruteforce(self, packages: List[Package],
                                           start_pos: Tuple[float, float]) -> List[Package]:
        """
        Find optimal order by trying all permutations (only practical for small package counts).
        
        Args:
            packages: List of packages to deliver
            start_pos: Starting position
        
        Returns:
            Optimized list of packages
        """
        if not packages:
            return []
        
        if len(packages) == 1:
            return packages
        
        # Only use brute force for small sets (max 3 packages as per rules)
        if len(packages) > 6:
            return self.optimize_delivery_order(packages, start_pos)
        
        best_order = packages
        best_distance = float('inf')
        
        # Try all permutations
        for perm in itertools.permutations(packages):
            distance = self._calculate_route_distance(list(perm), start_pos)
            if distance < best_distance:
                best_distance = distance
                best_order = list(perm)
        
        return best_order
    
    def _distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate distance between two positions using graph path or euclidean."""
        result = self.graph.find_path(pos1, pos2)
        if result:
            _, distance = result
            return distance
        else:
            return euclidean_distance(pos1, pos2)
    
    def _calculate_route_distance(self, packages: List[Package], 
                                  start_pos: Tuple[float, float]) -> float:
        """
        Calculate total distance for a delivery route.
        
        Args:
            packages: List of packages in delivery order
            start_pos: Starting position
        
        Returns:
            Total distance
        """
        if not packages:
            return 0.0
        
        total_distance = 0.0
        current_pos = start_pos
        
        for package in packages:
            # Distance to pickup
            total_distance += self._distance(current_pos, package.pickup_pos)
            # Distance from pickup to dropoff
            total_distance += self._distance(package.pickup_pos, package.dropoff_pos)
            # Update current position
            current_pos = package.dropoff_pos
        
        return total_distance
    
    def generate_waypoints(self, packages: List[Package], 
                          start_pos: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Generate waypoint list for a delivery route.
        
        Args:
            packages: List of packages in delivery order
            start_pos: Starting position
        
        Returns:
            List of waypoints (x, y) to visit
        """
        waypoints = [start_pos]
        
        for package in packages:
            waypoints.append(package.pickup_pos)
            waypoints.append(package.dropoff_pos)
        
        return waypoints
    
    def build_full_path(self, packages: List[Package],
                       start_pos: Tuple[float, float]) -> Tuple[List[Tuple[float, float]], float]:
        """
        Build complete path with all intermediate points.
        
        Args:
            packages: List of packages in delivery order
            start_pos: Starting position
        
        Returns:
            Tuple of (complete path, total distance)
        """
        full_path = []
        total_distance = 0.0
        current_pos = start_pos
        
        for package in packages:
            # Path to pickup
            result = self.graph.find_path(current_pos, package.pickup_pos)
            if result:
                path, distance = result
                full_path.extend(path[:-1] if full_path else path)  # Avoid duplicates
                total_distance += distance
            else:
                full_path.append(package.pickup_pos)
                total_distance += euclidean_distance(current_pos, package.pickup_pos)
            
            # Path from pickup to dropoff
            result = self.graph.find_path(package.pickup_pos, package.dropoff_pos)
            if result:
                path, distance = result
                full_path.extend(path[1:])  # Avoid duplicate pickup point
                total_distance += distance
            else:
                full_path.append(package.dropoff_pos)
                total_distance += euclidean_distance(package.pickup_pos, package.dropoff_pos)
            
            current_pos = package.dropoff_pos
        
        return (full_path, total_distance)
    
    def estimate_total_cost(self, packages: List[Package],
                           start_pos: Tuple[float, float]) -> Tuple[float, float, float]:
        """
        Estimate total profit for delivering packages.
        
        Args:
            packages: List of packages
            start_pos: Starting position
        
        Returns:
            Tuple of (total_reward, total_distance, net_profit)
        """
        total_reward = sum(pkg.reward for pkg in packages)
        total_distance = self._calculate_route_distance(packages, start_pos)
        net_profit = total_reward - total_distance
        
        return (total_reward, total_distance, net_profit)
    
    def optimize_and_evaluate(self, packages: List[Package],
                             start_pos: Tuple[float, float]) -> dict:
        """
        Optimize route and return comprehensive evaluation.
        
        Args:
            packages: List of packages to deliver
            start_pos: Starting position
        
        Returns:
            Dict with optimization results
        """
        if not packages:
            return {
                'optimized_packages': [],
                'waypoints': [start_pos],
                'total_reward': 0.0,
                'total_distance': 0.0,
                'net_profit': 0.0,
                'package_count': 0
            }
        
        # Optimize order (use brute force for small sets, heuristic for larger)
        if len(packages) <= 3:
            optimized = self.optimize_delivery_order_bruteforce(packages, start_pos)
        else:
            optimized = self.optimize_delivery_order(packages, start_pos)
        
        # Calculate metrics
        total_reward, total_distance, net_profit = self.estimate_total_cost(optimized, start_pos)
        waypoints = self.generate_waypoints(optimized, start_pos)
        
        return {
            'optimized_packages': optimized,
            'waypoints': waypoints,
            'total_reward': total_reward,
            'total_distance': total_distance,
            'net_profit': net_profit,
            'package_count': len(optimized)
        }
