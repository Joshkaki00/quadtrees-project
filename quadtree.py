from dataclasses import dataclass

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