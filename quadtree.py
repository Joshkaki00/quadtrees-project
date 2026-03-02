from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Point:
    """Represents a 2D point with x, y coordinates."""
    x: float
    y: float
    
@dataclass
class Rectangle:
    """Represents a rectangular boundary."""
    x: float  # Center x
    y: float  # Center y
    width: float
    height: float
    
    def contains(self, point: Point) -> bool:
        """Check if a point is within this rectangle."""
        return (self.x - self.width <= point.x <= self.x + self.width and
                self.y - self.height <= point.y <= self.y + self.height)
    
    def intersects(self, other: 'Rectangle') -> bool:
        """Check if this rectangle intersects with another rectangle."""
        return not (self.x + self.width < other.x - other.width or
                    self.x - self.width > other.x + other.width or
                    self.y + self.height < other.y - other.height or
                    self.y - self.height > other.y + other.height)
        
@dataclass
class Particle:
    """Represents a moving particle/object in 2D space."""
    x: float
    y: float
    vx: float = 0.0  # Velocity x
    vy: float = 0.0  # Velocity y
    radius: float = 5.0
    
    def update(self, dt: float = 1.0):
        """Update particle position based on velocity."""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def collides_with(self, other: 'Particle') -> bool:
        """Check if this particle collides with another particle."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < (self.radius + other.radius)
    


class QuadTree:
    """
    A quadtree data structure for efficient spatial queries.
    
    The quadtree recursively subdivides 2D space into four quadrants when
    the number of objects exceeds a threshold (capacity).
    """
    
    def __init__(self, boundary: Rectangle, capacity: int = 4):
        """
        Initialize a quadtree node.
        
        Args:
            boundary: The rectangular boundary this node covers
            capacity: Maximum number of points before subdivision
        """
        self.boundary = boundary
        self.capacity = capacity
        self.points: List[Point] = []
        self.divided = False
        
        # Child nodes (will be created when subdividing)
        self.northeast: Optional[QuadTree] = None
        self.northwest: Optional[QuadTree] = None
        self.southeast: Optional[QuadTree] = None
        self.southwest: Optional[QuadTree] = None