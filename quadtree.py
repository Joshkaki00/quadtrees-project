from dataclasses import dataclass
from typing import List, Optional
from typing import Tuple

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
        
    def subdivide(self):
        """Divide this node into four quadrants."""
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2
        
        # Create four child nodes
        ne = Rectangle(x + w, y - h, w, h)
        self.northeast = QuadTree(ne, self.capacity)
        
        nw = Rectangle(x - w, y - h, w, h)
        self.northwest = QuadTree(nw, self.capacity)
        
        se = Rectangle(x + w, y + h, w, h)
        self.southeast = QuadTree(se, self.capacity)
        
        sw = Rectangle(x - w, y + h, w, h)
        self.southwest = QuadTree(sw, self.capacity)
        
        self.divided = True
        
    def insert(self, point: Point) -> bool:
        """
        Insert a point into the quadtree.
        
        Args:
            point: The point to insert
            
        Returns:
            True if insertion was successful, False otherwise
        """
        # Ignore objects that don't belong in this quad tree
        if not self.boundary.contains(point):
            return False
        
        # If there's space and we haven't subdivided, add it here
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        
        # Otherwise, subdivide if needed and add to children
        if not self.divided:
            self.subdivide()
        
        # Try to insert into children
        if self.northeast.insert(point):
            return True
        if self.northwest.insert(point):
            return True
        if self.southeast.insert(point):
            return True
        if self.southwest.insert(point):
            return True
        
        # Should never reach here
        return False
    
    def query(self, range_rect: Rectangle, found: Optional[List[Point]] = None) -> List[Point]:
        """
        Find all points within a given range.
        
        Args:
            range_rect: The rectangular area to search
            found: List to accumulate found points (used in recursion)
            
        Returns:
            List of points within the range
        """
        if found is None:
            found = []
        
        # If range doesn't intersect this quad, return
        if not self.boundary.intersects(range_rect):
            return found
        
        # Check points at this level
        for point in self.points:
            if range_rect.contains(point):
                found.append(point)
        
        # If subdivided, check children
        if self.divided:
            self.northwest.query(range_rect, found)
            self.northeast.query(range_rect, found)
            self.southwest.query(range_rect, found)
            self.southeast.query(range_rect, found)
        
        return found
    
    def clear(self):
        """Clear all points from the quadtree."""
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def get_all_boundaries(self) -> List[Rectangle]:
        """
        Get all boundaries in the tree (for visualization).
        
        Returns:
            List of all rectangular boundaries in the tree
        """
        boundaries = [self.boundary]
        
        if self.divided:
            boundaries.extend(self.northeast.get_all_boundaries())
            boundaries.extend(self.northwest.get_all_boundaries())
            boundaries.extend(self.southeast.get_all_boundaries())
            boundaries.extend(self.southwest.get_all_boundaries())
        
        return boundaries
    
class CollisionDetector:
    """Handles collision detection using different methods."""
    
    @staticmethod
    def brute_force(particles: List[Particle]) -> List[Tuple[int, int]]:
        """
        Detect collisions using brute force O(n²) method.
        
        Args:
            particles: List of particles to check
            
        Returns:
            List of tuples containing indices of colliding particles
        """
        collisions = []
        n = len(particles)
        
        for i in range(n):
            for j in range(i + 1, n):
                if particles[i].collides_with(particles[j]):
                    collisions.append((i, j))
        
        return collisions