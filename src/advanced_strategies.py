"""
Advanced Strategies for Hackathon 2025 Delivery Challenge
Alternative algorithms and approaches for optimization.
"""
from typing import List, Tuple, Dict
from package_selector import Package, PackageSelector
from graph import Graph
from utils import euclidean_distance
import math


class AdvancedPackageSelector(PackageSelector):
    """Extended package selector with advanced strategies."""
    
    def select_packages_by_profit_density(self, current_pos: Tuple[float, float],
                                          max_packages: int = 3) -> List[Package]:
        """
        Select packages based on profit per unit distance (profit density).
        
        Args:
            current_pos: Current vehicle position
            max_packages: Maximum packages to select
        
        Returns:
            List of selected packages
        """
        available = [pkg for pkg in self.packages.values() 
                    if not pkg.delivered and pkg.dropoff_pos is not None]
        
        if not available:
            return []
        
        # Calculate profit density for each package
        package_scores = []
        for pkg in available:
            profit = self.calculate_package_profit(pkg, current_pos)
            
            # Calculate total distance
            dist_to_pickup = self._get_distance(current_pos, pkg.pickup_pos)
            dist_delivery = self._get_distance(pkg.pickup_pos, pkg.dropoff_pos)
            total_distance = dist_to_pickup + dist_delivery
            
            if total_distance > 0:
                density = profit / total_distance
            else:
                density = profit
            
            package_scores.append((pkg, profit, density))
        
        # Sort by profit density (descending)
        package_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Select top packages
        selected = [item[0] for item in package_scores[:max_packages] if item[1] > 0]
        
        return selected
    
    def select_packages_two_phase(self, current_pos: Tuple[float, float],
                                  max_packages: int = 3) -> List[Package]:
        """
        Two-phase selection: first by clustering, then by profit within cluster.
        
        Args:
            current_pos: Current vehicle position
            max_packages: Maximum packages to select
        
        Returns:
            List of selected packages
        """
        available = [pkg for pkg in self.packages.values() 
                    if not pkg.delivered and pkg.dropoff_pos is not None]
        
        if not available:
            return []
        
        if len(available) <= max_packages:
            return available
        
        # Phase 1: Find clusters using simple k-means-like approach
        clusters = self._cluster_packages(available, num_clusters=3)
        
        # Phase 2: Select best cluster based on total profit
        best_cluster = None
        best_total_profit = -float('inf')
        
        for cluster in clusters:
            total_profit = sum(self.calculate_package_profit(pkg, current_pos) 
                             for pkg in cluster)
            if total_profit > best_total_profit:
                best_total_profit = total_profit
                best_cluster = cluster
        
        # Return top packages from best cluster
        if best_cluster:
            scored = [(pkg, self.calculate_package_profit(pkg, current_pos)) 
                     for pkg in best_cluster]
            scored.sort(key=lambda x: x[1], reverse=True)
            return [pkg for pkg, score in scored[:max_packages] if score > 0]
        
        return []
    
    def _cluster_packages(self, packages: List[Package], 
                         num_clusters: int = 3) -> List[List[Package]]:
        """Simple clustering of packages by location."""
        if len(packages) <= num_clusters:
            return [[pkg] for pkg in packages]
        
        # Initialize centroids randomly
        import random
        centroids = random.sample([pkg.pickup_pos for pkg in packages], 
                                min(num_clusters, len(packages)))
        
        # Assign packages to nearest centroid
        for _ in range(5):  # Max iterations
            clusters = [[] for _ in range(len(centroids))]
            
            for pkg in packages:
                nearest_idx = 0
                nearest_dist = float('inf')
                
                for i, centroid in enumerate(centroids):
                    dist = euclidean_distance(pkg.pickup_pos, centroid)
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest_idx = i
                
                clusters[nearest_idx].append(pkg)
            
            # Update centroids
            new_centroids = []
            for cluster in clusters:
                if cluster:
                    avg_x = sum(pkg.pickup_pos[0] for pkg in cluster) / len(cluster)
                    avg_y = sum(pkg.pickup_pos[1] for pkg in cluster) / len(cluster)
                    new_centroids.append((avg_x, avg_y))
                else:
                    new_centroids.append(centroids[len(new_centroids)])
            
            centroids = new_centroids
        
        return [c for c in clusters if c]
    
    def _get_distance(self, pos1: Tuple[float, float], 
                     pos2: Tuple[float, float]) -> float:
        """Get distance using graph or euclidean."""
        result = self.graph.find_path(pos1, pos2)
        if result:
            _, distance = result
            return distance
        return euclidean_distance(pos1, pos2)


class AdaptiveStrategy:
    """Adaptive strategy that switches between approaches based on conditions."""
    
    def __init__(self, selector: PackageSelector):
        """Initialize adaptive strategy."""
        self.selector = selector
        self.advanced_selector = AdvancedPackageSelector(selector.graph)
        self.advanced_selector.packages = selector.packages
    
    def select_packages_adaptive(self, current_pos: Tuple[float, float],
                                max_packages: int = 3,
                                remaining_time: float = float('inf')) -> List[Package]:
        """
        Adaptively select packages based on current conditions.
        
        Args:
            current_pos: Current position
            max_packages: Maximum packages
            remaining_time: Remaining time in competition
        
        Returns:
            List of selected packages
        """
        undelivered = self.selector.get_undelivered_count()
        
        # If few packages left, use brute force
        if undelivered <= 5:
            return self.selector.select_packages_greedy(current_pos, max_packages)
        
        # If lots of time, use clustering for better long-term strategy
        if remaining_time > 60:
            return self.advanced_selector.select_packages_two_phase(
                current_pos, max_packages
            )
        
        # If time is limited, use profit density for quick wins
        return self.advanced_selector.select_packages_by_profit_density(
            current_pos, max_packages
        )


def calculate_expected_value(packages: List[Package], graph: Graph,
                            current_pos: Tuple[float, float]) -> Dict:
    """
    Calculate expected value metrics for a package selection.
    
    Args:
        packages: List of packages
        graph: Road network graph
        current_pos: Starting position
    
    Returns:
        Dict with metrics
    """
    if not packages:
        return {
            'total_reward': 0,
            'total_distance': 0,
            'avg_profit_per_package': 0,
            'profit_density': 0
        }
    
    total_reward = sum(pkg.reward for pkg in packages)
    
    # Calculate total distance
    total_distance = 0
    pos = current_pos
    for pkg in packages:
        result = graph.find_path(pos, pkg.pickup_pos)
        if result:
            _, dist = result
            total_distance += dist
        else:
            total_distance += euclidean_distance(pos, pkg.pickup_pos)
        
        result = graph.find_path(pkg.pickup_pos, pkg.dropoff_pos)
        if result:
            _, dist = result
            total_distance += dist
        else:
            total_distance += euclidean_distance(pkg.pickup_pos, pkg.dropoff_pos)
        
        pos = pkg.dropoff_pos
    
    profit = total_reward - total_distance
    avg_profit = profit / len(packages) if packages else 0
    density = profit / total_distance if total_distance > 0 else 0
    
    return {
        'total_reward': total_reward,
        'total_distance': total_distance,
        'net_profit': profit,
        'avg_profit_per_package': avg_profit,
        'profit_density': density,
        'package_count': len(packages)
    }
