"""
Package Selection Strategy for Hackathon 2025 Delivery Challenge
Analyzes packages and selects the most profitable ones to deliver.
"""
from typing import Dict, List, Tuple, Optional
from graph import Graph
from utils import euclidean_distance
from config import MAX_PACKAGES_PER_TRIP, DISTANCE_WEIGHT, REWARD_WEIGHT


class Package:
    """Represents a delivery package."""
    
    def __init__(self, package_id: int, pickup_pos: Tuple[float, float], 
                 dropoff_pos: Optional[Tuple[float, float]] = None, reward: float = 1.0):
        """
        Initialize package.
        
        Args:
            package_id: Unique package identifier
            pickup_pos: Pickup location (x, y)
            dropoff_pos: Dropoff location (x, y), can be None initially
            reward: Monetary reward for delivery
        """
        self.id = package_id
        self.pickup_pos = pickup_pos
        self.dropoff_pos = dropoff_pos
        self.reward = reward
        self.delivered = False
    
    def __repr__(self):
        return f"Package({self.id}, pickup={self.pickup_pos}, reward={self.reward})"


class PackageSelector:
    """Selects optimal packages for delivery."""
    
    def __init__(self, graph: Graph):
        """
        Initialize package selector.
        
        Args:
            graph: Road network graph
        """
        self.graph = graph
        self.packages = {}
    
    def load_packages(self, packages_data: Dict):
        """
        Load packages from API response.
        
        Args:
            packages_data: Dict from /packages endpoint
        """
        self.packages = {}
        for pkg_id, pkg_info in packages_data.items():
            pkg_id_int = int(pkg_id)
            position = tuple(pkg_info['position'])
            
            # Check if dropoff location is provided
            dropoff_pos = None
            if 'dropoff' in pkg_info:
                dropoff_pos = tuple(pkg_info['dropoff'])
            
            # Get reward value (default to 100.0 if not provided)
            reward = pkg_info.get('reward', 100.0)
            
            pkg = Package(pkg_id_int, position, dropoff_pos, reward)
            self.packages[pkg_id_int] = pkg
            print(f"  📦 Package {pkg_id_int}: pickup={position}, dropoff={dropoff_pos}, reward={reward:.2f}")
        
        print(f"✓ Loaded {len(self.packages)} packages")
    
    def update_package_dropoff(self, package_id: int, dropoff_pos: Tuple[float, float]):
        """
        Update dropoff location for a package.
        
        Args:
            package_id: Package ID
            dropoff_pos: Dropoff location (x, y)
        """
        if package_id in self.packages:
            self.packages[package_id].dropoff_pos = dropoff_pos
    
    def calculate_package_profit(self, package: Package, current_pos: Tuple[float, float]) -> float:
        """
        Calculate profit score for a package.
        Profit = Reward - Distance_Cost
        
        Args:
            package: Package to evaluate
            current_pos: Current vehicle position
        
        Returns:
            Profit score (higher is better)
        """
        if package.delivered or package.dropoff_pos is None:
            return -float('inf')
        
        # Calculate distance: current -> pickup -> dropoff
        result1 = self.graph.find_path(current_pos, package.pickup_pos)
        result2 = self.graph.find_path(package.pickup_pos, package.dropoff_pos)
        
        if result1 is None or result2 is None:
            # Fallback to direct distance
            dist_to_pickup = euclidean_distance(current_pos, package.pickup_pos)
            dist_delivery = euclidean_distance(package.pickup_pos, package.dropoff_pos)
            total_distance = dist_to_pickup + dist_delivery
        else:
            _, dist_to_pickup = result1
            _, dist_delivery = result2
            total_distance = dist_to_pickup + dist_delivery
        
        # Calculate profit
        profit = (package.reward * REWARD_WEIGHT) - (total_distance * DISTANCE_WEIGHT)
        
        return profit
    
    def select_best_package(self, current_pos: Tuple[float, float]) -> Optional[Package]:
        """
        Select the single best package to deliver from current position.
        
        Args:
            current_pos: Current vehicle position
        
        Returns:
            Best package or None
        """
        best_package = None
        best_profit = -float('inf')
        
        for package in self.packages.values():
            if package.delivered or package.dropoff_pos is None:
                continue
            
            profit = self.calculate_package_profit(package, current_pos)
            
            if profit > best_profit:
                best_profit = profit
                best_package = package
        
        return best_package
    
    def select_packages_greedy(self, current_pos: Tuple[float, float], 
                               max_packages: int = MAX_PACKAGES_PER_TRIP) -> List[Package]:
        """
        Greedily select up to max_packages starting from current position.
        
        Args:
            current_pos: Current vehicle position
            max_packages: Maximum number of packages to select
        
        Returns:
            List of selected packages
        """
        selected = []
        temp_pos = current_pos
        
        # Debug: Print profit for all packages
        print(f"\n🔍 DEBUG: Evaluating {len(self.packages)} packages from position {current_pos}")
        for pkg in self.packages.values():
            if not pkg.delivered and pkg.dropoff_pos is not None:
                profit = self.calculate_package_profit(pkg, temp_pos)
                print(f"  Package {pkg.id}: pickup={pkg.pickup_pos}, dropoff={pkg.dropoff_pos}, reward={pkg.reward:.2f}, profit={profit:.2f}")
        
        for _ in range(max_packages):
            best_pkg = None
            best_profit = -float('inf')
            
            for package in self.packages.values():
                if package.delivered or package in selected or package.dropoff_pos is None:
                    continue
                
                profit = self.calculate_package_profit(package, temp_pos)
                
                if profit > best_profit and profit > 0:  # Only select if profitable
                    best_profit = profit
                    best_pkg = package
            
            if best_pkg is None:
                break
            
            selected.append(best_pkg)
            # Update position for next selection
            temp_pos = best_pkg.dropoff_pos
        
        return selected
    
    def select_packages_by_density(self, current_pos: Tuple[float, float],
                                   max_packages: int = MAX_PACKAGES_PER_TRIP) -> List[Package]:
        """
        Select packages that are close to each other (cluster-based).
        
        Args:
            current_pos: Current vehicle position
            max_packages: Maximum number of packages to select
        
        Returns:
            List of selected packages
        """
        available = [pkg for pkg in self.packages.values() 
                    if not pkg.delivered and pkg.dropoff_pos is not None]
        
        if not available:
            return []
        
        # Find nearest package to current position
        nearest = min(available, key=lambda p: euclidean_distance(current_pos, p.pickup_pos))
        selected = [nearest]
        
        # Find packages close to the first one
        for _ in range(max_packages - 1):
            if len(available) <= len(selected):
                break
            
            # Calculate average position of selected packages
            avg_x = sum(p.pickup_pos[0] for p in selected) / len(selected)
            avg_y = sum(p.pickup_pos[1] for p in selected) / len(selected)
            centroid = (avg_x, avg_y)
            
            # Find nearest unselected package to centroid
            best_pkg = None
            best_dist = float('inf')
            
            for pkg in available:
                if pkg not in selected:
                    dist = euclidean_distance(centroid, pkg.pickup_pos)
                    if dist < best_dist:
                        best_dist = dist
                        best_pkg = pkg
            
            if best_pkg is None:
                break
            
            selected.append(best_pkg)
        
        # Verify profitability
        total_profit = sum(self.calculate_package_profit(pkg, current_pos) for pkg in selected)
        
        if total_profit > 0:
            return selected
        else:
            # If not profitable as group, try single best
            return [self.select_best_package(current_pos)] if self.select_best_package(current_pos) else []
    
    def mark_delivered(self, package_id: int):
        """Mark a package as delivered."""
        if package_id in self.packages:
            self.packages[package_id].delivered = True
    
    def get_undelivered_count(self) -> int:
        """Get count of undelivered packages."""
        return sum(1 for pkg in self.packages.values() if not pkg.delivered)
    
    def get_total_reward_earned(self) -> float:
        """Get total reward from delivered packages."""
        return sum(pkg.reward for pkg in self.packages.values() if pkg.delivered)
