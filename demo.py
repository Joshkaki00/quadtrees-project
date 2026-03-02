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