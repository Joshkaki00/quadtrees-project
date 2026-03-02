"""
Pygame Visualization Demo for Quadtree Collision Detection
Shows real-time comparison between brute force and quadtree methods

Controls:
- SPACE: Toggle between Brute Force and Quadtree mode
- R: Reset particles
- UP/DOWN: Increase/decrease particle count
- Q: Quit
"""

import pygame
import random
import time
from quadtree import QuadTree, Point, Rectangle, Particle, CollisionDetector

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Screen settings
WIDTH = 800
HEIGHT = 600
FPS = 60

class Demo:
    """Main demo application."""
    
    def __init__(self):
        """Initialize the demo."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quadtree Collision Detection Demo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        
        self.running = True
        self.use_quadtree = True
        self.show_tree = True
        
        self.num_particles = 100
        self.particles = []
        self.collisions = []
        
        self.boundary = Rectangle(WIDTH / 2, HEIGHT / 2, WIDTH / 2, HEIGHT / 2)
        
        # Performance tracking
        self.fps_history = []
        self.collision_check_time = 0
        self.comparison_count = 0
        
        self.reset_particles()
        
    def reset_particles(self):
        """Create new random particles."""
        self.particles = []
        for _ in range(self.num_particles):
            x = random.uniform(50, WIDTH - 50)
            y = random.uniform(50, HEIGHT - 50)
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            radius = random.uniform(5, 10)
            self.particles.append(Particle(x, y, vx, vy, radius))
            
    def update_particles(self):
        """Update particle positions and handle boundary collisions."""
        for particle in self.particles:
            particle.update()
            
            # Bounce off walls
            if particle.x - particle.radius < 0 or particle.x + particle.radius > WIDTH:
                particle.vx *= -1
                particle.x = max(particle.radius, min(WIDTH - particle.radius, particle.x))
            
            if particle.y - particle.radius < 0 or particle.y + particle.radius > HEIGHT:
                particle.vy *= -1
                particle.y = max(particle.radius, min(HEIGHT - particle.radius, particle.y))
                
    def detect_collisions(self):
        """Detect collisions using selected method."""
        start_time = time.time()
        
        if self.use_quadtree:
            self.collisions = CollisionDetector.quadtree_method(
                self.particles, self.boundary
            )
            # Estimate comparisons saved
            self.comparison_count = len(self.particles) * 4  # Rough estimate
        else:
            self.collisions = CollisionDetector.brute_force(self.particles)
            self.comparison_count = (len(self.particles) * (len(self.particles) - 1)) // 2
        
        self.collision_check_time = (time.time() - start_time) * 1000  # Convert to ms
        
    def draw_quadtree(self):
        """Draw quadtree boundaries."""
        if not self.show_tree or not self.use_quadtree:
            return
        
        # Build quadtree
        qt = QuadTree(self.boundary, capacity=4)
        for particle in self.particles:
            qt.insert(Point(particle.x, particle.y))
        
        # Draw all boundaries
        boundaries = qt.get_all_boundaries()
        for boundary in boundaries:
            left = boundary.x - boundary.width
            top = boundary.y - boundary.height
            width = boundary.width * 2
            height = boundary.height * 2
            
            pygame.draw.rect(self.screen, GRAY, 
                        (left, top, width, height), 1)