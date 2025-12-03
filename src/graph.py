"""
Graph and Pathfinding module for Hackathon 2025 Delivery Challenge
Implements A* and Dijkstra algorithms for route planning.
"""
import heapq
import math
from typing import Dict, List, Tuple, Optional, Set
from utils import euclidean_distance


class Graph:
    """Graph representation of the road network."""
    
    def __init__(self):
        """Initialize empty graph."""
        self.nodes = {}  # node_id -> (x, y)
        self.edges = {}  # node_id -> [(neighbor_id, distance), ...]
        self.points = []  # List of all points
        self.streets = []  # List of all streets
    
    def build_from_road_data(self, road_data: Dict):
        """
        Build graph from road information API response.
        
        Args:
            road_data: Dict with 'points' and 'streets' keys
        """
        self.points = road_data.get('points', [])
        self.streets = road_data.get('streets', [])
        
        # Create nodes from points
        for i, point in enumerate(self.points):
            self.nodes[i] = tuple(point)
            self.edges[i] = []
        
        # Create edges from streets
        for street in self.streets:
            start = tuple(street['start'])
            end = tuple(street['end'])
            
            # Find node IDs for start and end points
            start_id = self._find_or_add_node(start)
            end_id = self._find_or_add_node(end)
            
            if start_id is not None and end_id is not None:
                distance = euclidean_distance(start, end)
                # Add bidirectional edges
                self.edges[start_id].append((end_id, distance))
                self.edges[end_id].append((start_id, distance))
        
        print(f"✓ Graph built: {len(self.nodes)} nodes, {sum(len(e) for e in self.edges.values())} edges")
    
    def _find_or_add_node(self, point: Tuple[float, float]) -> Optional[int]:
        """Find existing node or add new one."""
        # Check if point already exists
        for node_id, node_pos in self.nodes.items():
            if abs(node_pos[0] - point[0]) < 0.1 and abs(node_pos[1] - point[1]) < 0.1:
                return node_id
        
        # Add new node
        new_id = len(self.nodes)
        self.nodes[new_id] = point
        self.edges[new_id] = []
        return new_id
    
    def find_nearest_node(self, point: Tuple[float, float]) -> Optional[int]:
        """
        Find the nearest node to a given point.
        
        Args:
            point: (x, y) coordinates
        
        Returns:
            Node ID of nearest node
        """
        if not self.nodes:
            return None
        
        min_dist = float('inf')
        nearest_id = None
        
        for node_id, node_pos in self.nodes.items():
            dist = euclidean_distance(point, node_pos)
            if dist < min_dist:
                min_dist = dist
                nearest_id = node_id
        
        return nearest_id
    
    def astar(self, start_id: int, goal_id: int) -> Optional[Tuple[List[int], float]]:
        """
        A* pathfinding algorithm.
        
        Args:
            start_id: Starting node ID
            goal_id: Goal node ID
        
        Returns:
            Tuple of (path as list of node IDs, total distance) or None
        """
        if start_id not in self.nodes or goal_id not in self.nodes:
            return None
        
        if start_id == goal_id:
            return ([start_id], 0.0)
        
        goal_pos = self.nodes[goal_id]
        
        # Priority queue: (f_score, node_id)
        open_set = [(0, start_id)]
        came_from = {}
        
        g_score = {start_id: 0}
        f_score = {start_id: euclidean_distance(self.nodes[start_id], goal_pos)}
        
        closed_set = set()
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
            
            if current == goal_id:
                # Reconstruct path
                path = []
                node = goal_id
                while node in came_from:
                    path.append(node)
                    node = came_from[node]
                path.append(start_id)
                path.reverse()
                return (path, g_score[goal_id])
            
            closed_set.add(current)
            
            for neighbor, edge_dist in self.edges.get(current, []):
                if neighbor in closed_set:
                    continue
                
                tentative_g = g_score[current] + edge_dist
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    h = euclidean_distance(self.nodes[neighbor], goal_pos)
                    f_score[neighbor] = tentative_g + h
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None  # No path found
    
    def dijkstra(self, start_id: int, goal_id: int) -> Optional[Tuple[List[int], float]]:
        """
        Dijkstra's shortest path algorithm.
        
        Args:
            start_id: Starting node ID
            goal_id: Goal node ID
        
        Returns:
            Tuple of (path as list of node IDs, total distance) or None
        """
        if start_id not in self.nodes or goal_id not in self.nodes:
            return None
        
        if start_id == goal_id:
            return ([start_id], 0.0)
        
        # Priority queue: (distance, node_id)
        pq = [(0, start_id)]
        distances = {start_id: 0}
        came_from = {}
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            if current == goal_id:
                # Reconstruct path
                path = []
                node = goal_id
                while node in came_from:
                    path.append(node)
                    node = came_from[node]
                path.append(start_id)
                path.reverse()
                return (path, distances[goal_id])
            
            visited.add(current)
            
            for neighbor, edge_dist in self.edges.get(current, []):
                if neighbor in visited:
                    continue
                
                new_dist = distances[current] + edge_dist
                
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    came_from[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return None  # No path found
    
    def find_path(self, start_pos: Tuple[float, float], goal_pos: Tuple[float, float], 
                  use_astar: bool = True) -> Optional[Tuple[List[Tuple[float, float]], float]]:
        """
        Find path between two positions.
        
        Args:
            start_pos: Starting (x, y) position
            goal_pos: Goal (x, y) position
            use_astar: If True use A*, else use Dijkstra
        
        Returns:
            Tuple of (path as list of (x,y) coordinates, total distance) or None
        """
        start_id = self.find_nearest_node(start_pos)
        goal_id = self.find_nearest_node(goal_pos)
        
        if start_id is None or goal_id is None:
            return None
        
        # Find path between nodes
        if use_astar:
            result = self.astar(start_id, goal_id)
        else:
            result = self.dijkstra(start_id, goal_id)
        
        if result is None:
            return None
        
        path_ids, distance = result
        
        # Convert node IDs to coordinates
        path_coords = [self.nodes[node_id] for node_id in path_ids]
        
        # Add actual start and goal positions if they differ from nearest nodes
        if euclidean_distance(start_pos, path_coords[0]) > 0.1:
            path_coords.insert(0, start_pos)
            distance += euclidean_distance(start_pos, path_coords[1])
        
        if euclidean_distance(goal_pos, path_coords[-1]) > 0.1:
            distance += euclidean_distance(path_coords[-1], goal_pos)
            path_coords.append(goal_pos)
        
        return (path_coords, distance)
    
    def calculate_route_distance(self, waypoints: List[Tuple[float, float]], 
                                 use_astar: bool = True) -> float:
        """
        Calculate total distance for a route through multiple waypoints.
        
        Args:
            waypoints: List of (x, y) positions to visit in order
            use_astar: If True use A*, else use Dijkstra
        
        Returns:
            Total distance
        """
        if len(waypoints) < 2:
            return 0.0
        
        total_distance = 0.0
        
        for i in range(len(waypoints) - 1):
            result = self.find_path(waypoints[i], waypoints[i + 1], use_astar)
            if result:
                _, distance = result
                total_distance += distance
            else:
                # If no path found, use direct distance as fallback
                total_distance += euclidean_distance(waypoints[i], waypoints[i + 1])
        
        return total_distance
