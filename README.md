# Quadtree Collision Detection

**Author:** Joshkaki00  
**Course:** ACS 3310 - Advanced Trees & Sorting Algorithms  
**Date:** March 2026

## 🎯 Project Overview

This project implements a **Quadtree** data structure for efficient 2D collision detection in games. The quadtree reduces collision checking from O(n²) brute force to approximately O(n log n) by spatially partitioning objects.

## 🌲 What is a Quadtree?

A quadtree is a tree data structure where each node has exactly four children. It recursively divides 2D space into quadrants, allowing efficient spatial queries like:
- Finding all objects in a region
- Detecting nearby objects for collision
- Culling objects outside the camera view

### How It Works

1. **Start with entire space** as one node
2. **When capacity exceeded** (e.g., 4 objects), split into 4 quadrants:
   - Northeast (top-right)
   - Northwest (top-left)
   - Southeast (bottom-right)
   - Southwest (bottom-left)
3. **Recursively subdivide** each quadrant as needed
4. **Query efficiently** by only checking relevant quadrants

## 📊 Performance Comparison

| Method       | Time Complexity | 100 Particles | 500 Particles |
|--------------|----------------|---------------|---------------|
| Brute Force  | O(n²)          | 4,950 checks  | 124,750 checks|
| Quadtree     | O(n log n)     | ~400 checks   | ~2,500 checks |

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone [your-repo-url]
cd quadtree-collision

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Running the Demo

### Interactive Pygame Demo

```bash
python demo.py
```

**Controls:**
- `SPACE` - Toggle between Brute Force and Quadtree
- `UP/DOWN` - Increase/decrease particle count
- `R` - Reset particles with random positions
- `T` - Toggle quadtree visualization
- `Q` - Quit

### Run Tests

```bash
# Install pytest if needed
pip install pytest

# Run all tests
pytest test_quadtree.py -v

# Run with coverage
pytest test_quadtree.py --cov=quadtree --cov-report=html
```

## 📁 Project Structure

```
quadtree-collision/
├── quadtree.py          # Main quadtree implementation
├── test_quadtree.py     # Unit tests (pytest)
├── demo.py              # Pygame visualization demo
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── docs/
    └── article.md      # Technical article (for Medium)
```

## 🔧 Core Components

### `quadtree.py`

**Classes:**
- `Point` - Represents a 2D point
- `Rectangle` - Represents a rectangular boundary
- `Particle` - Moving object with velocity and radius
- `QuadTree` - Main quadtree data structure
- `CollisionDetector` - Collision detection methods

**Key Methods:**
- `insert(point)` - Add point to tree, subdividing if needed
- `query(range)` - Find all points in a rectangular range
- `subdivide()` - Split node into four quadrants
- `clear()` - Reset tree to empty state

### `test_quadtree.py`

Comprehensive test suite covering:
- Rectangle containment and intersection
- Quadtree insertion and subdivision
- Range queries
- Collision detection accuracy
- Edge cases

### `demo.py`

Interactive visualization showing:
- Real-time particle movement
- Collision highlighting (red = colliding)
- Quadtree subdivision boundaries
- Performance metrics (FPS, check time, comparisons)
- Side-by-side method comparison

## 📈 Usage Examples

### Basic Quadtree Usage

```python
from quadtree import QuadTree, Point, Rectangle

# Create a quadtree for 800x600 space
boundary = Rectangle(400, 300, 400, 300)
qt = QuadTree(boundary, capacity=4)

# Insert points
qt.insert(Point(100, 100))
qt.insert(Point(200, 150))
qt.insert(Point(350, 400))

# Query a region
search_area = Rectangle(150, 150, 100, 100)
found_points = qt.query(search_area)
print(f"Found {len(found_points)} points in search area")
```

### Collision Detection

```python
from quadtree import Particle, CollisionDetector, Rectangle

# Create particles
particles = [
    Particle(100, 100, vx=2, vy=1, radius=10),
    Particle(150, 150, vx=-1, vy=2, radius=10),
    Particle(200, 200, vx=1, vy=-1, radius=10),
]

# Detect collisions with brute force
collisions_bf = CollisionDetector.brute_force(particles)

# Detect collisions with quadtree
boundary = Rectangle(400, 300, 400, 300)
collisions_qt = CollisionDetector.quadtree_method(particles, boundary)

print(f"Brute force found: {len(collisions_bf)} collisions")
print(f"Quadtree found: {len(collisions_qt)} collisions")
```

## 🎓 Educational Value

This project demonstrates:

1. **Space Partitioning** - Dividing space for efficient queries
2. **Recursive Data Structures** - Trees with recursive subdivision
3. **Algorithm Analysis** - Comparing O(n²) vs O(n log n)
4. **Real-world Application** - Used in game engines, physics simulations
5. **Testing** - Comprehensive unit test coverage

## 🔬 Algorithm Analysis

### Insertion
- **Average Case:** O(log n)
- **Worst Case:** O(n) if all points in same quadrant
- Subdivides when node capacity exceeded

### Query (Range Search)
- **Average Case:** O(log n + k) where k = points found
- **Worst Case:** O(n) if query covers entire space
- Prunes entire subtrees when ranges don't intersect

### Collision Detection
- **Brute Force:** O(n²) - check every pair
- **Quadtree:** O(n log n) - only check nearby objects
- **Speedup:** Significant for n > 50 particles

## 🎯 Real-world Applications

Quadtrees are used in:

1. **Game Development**
   - Collision detection in 2D games
   - Spatial audio systems
   - Particle systems optimization

2. **Computer Graphics**
   - View frustum culling
   - Level of detail (LOD) selection
   - Ray tracing acceleration

3. **Geographic Information Systems (GIS)**
   - Map rendering
   - Location-based queries
   - Spatial indexing

4. **Image Processing**
   - Image compression
   - Region detection
   - Adaptive mesh refinement

## 📚 Resources

- [Wikipedia: Quadtree](https://en.wikipedia.org/wiki/Quadtree)
- [Coding Challenge: Quadtree](https://www.youtube.com/watch?v=OJxEcs0w_kE) (The Coding Train)
- [Game Programming Patterns: Spatial Partition](https://gameprogrammingpatterns.com/spatial-partition.html)

## 🤝 Contributing

Not accepting contributions.

## 📄 License

MIT License - See LICENSE file for details

## ✨ Future Improvements

- [ ] Add octree for 3D collision detection
- [ ] Implement point removal from quadtree
- [ ] Add Barnes-Hut algorithm for N-body simulation
- [ ] Optimize with spatial hashing hybrid approach
- [ ] Add benchmark suite for performance testing