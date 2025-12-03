"""
Utility functions for Hackathon 2025 Delivery Challenge
"""
import math
from typing import List, Tuple

def euclidean_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: (x, y) coordinates
        point2: (x, y) coordinates
    
    Returns:
        Distance as float
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def manhattan_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Manhattan distance between two points.
    
    Args:
        point1: (x, y) coordinates
        point2: (x, y) coordinates
    
    Returns:
        Distance as float
    """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def angle_between_points(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate angle between two points in radians.
    
    Args:
        point1: Starting point (x, y)
        point2: Ending point (x, y)
    
    Returns:
        Angle in radians
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.atan2(dy, dx)


def normalize_angle(angle: float) -> float:
    """
    Normalize angle to [-pi, pi] range.
    
    Args:
        angle: Angle in radians
    
    Returns:
        Normalized angle
    """
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def closest_point(point: Tuple[float, float], points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Find the closest point from a list of points.
    
    Args:
        point: Reference point
        points: List of candidate points
    
    Returns:
        Closest point from the list
    """
    if not points:
        return None
    
    min_dist = float('inf')
    closest = points[0]
    
    for p in points:
        dist = euclidean_distance(point, p)
        if dist < min_dist:
            min_dist = dist
            closest = p
    
    return closest


def path_length(path: List[Tuple[float, float]]) -> float:
    """
    Calculate total length of a path.
    
    Args:
        path: List of (x, y) coordinates
    
    Returns:
        Total path length
    """
    if len(path) < 2:
        return 0.0
    
    total = 0.0
    for i in range(len(path) - 1):
        total += euclidean_distance(path[i], path[i + 1])
    
    return total


def format_position(position: List[float]) -> str:
    """Format position for logging."""
    return f"({position[0]:.2f}, {position[1]:.2f})"


def format_distance(distance: float) -> str:
    """Format distance for logging."""
    return f"{distance:.2f}"
