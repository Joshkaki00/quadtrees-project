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
            
    def draw_particles(self):
        """Draw all particles."""
        colliding_particles = set()
        for i, j in self.collisions:
            colliding_particles.add(i)
            colliding_particles.add(j)
        
        for i, particle in enumerate(self.particles):
            color = RED if i in colliding_particles else GREEN
            pygame.draw.circle(self.screen, color, 
                            (int(particle.x), int(particle.y)), 
                            int(particle.radius))
            
    def draw_ui(self):
        """Draw user interface and stats."""
        y_offset = 10
        
        # Title
        method = "QUADTREE" if self.use_quadtree else "BRUTE FORCE"
        title = self.large_font.render(method, True, YELLOW)
        self.screen.blit(title, (10, y_offset))
        y_offset += 40
        
        # Stats
        stats = [
            f"Particles: {len(self.particles)}",
            f"Collisions: {len(self.collisions)}",
            f"Comparisons: ~{self.comparison_count}",
            f"Check Time: {self.collision_check_time:.2f}ms",
            f"FPS: {int(self.clock.get_fps())}",
        ]
        
        for stat in stats:
            text = self.font.render(stat, True, WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
        # Controls
        y_offset = HEIGHT - 120
        controls = [
            "SPACE - Toggle Method",
            "R - Reset Particles",
            "UP/DOWN - Change Count",
            "T - Toggle Tree View",
            "Q - Quit"
        ]
        
        for control in controls:
            text = self.font.render(control, True, WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 20
        
        # Performance comparison
        if not self.use_quadtree:
            n = len(self.particles)
            theoretical = n * (n - 1) // 2
            warn = self.font.render(
                f"O(n²) = {theoretical} comparisons!", 
                True, RED
            )
            self.screen.blit(warn, (WIDTH - 300, 10))
            
    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                
                elif event.key == pygame.K_SPACE:
                    self.use_quadtree = not self.use_quadtree
                    print(f"Switched to {'Quadtree' if self.use_quadtree else 'Brute Force'}")
                
                elif event.key == pygame.K_r:
                    self.reset_particles()
                    print("Particles reset")
                
                elif event.key == pygame.K_t:
                    self.show_tree = not self.show_tree
                
                elif event.key == pygame.K_UP:
                    self.num_particles = min(500, self.num_particles + 10)
                    self.reset_particles()
                    print(f"Particle count: {self.num_particles}")
                
                elif event.key == pygame.K_DOWN:
                    self.num_particles = max(10, self.num_particles - 10)
                    self.reset_particles()
                    print(f"Particle count: {self.num_particles}")
                    
    def run(self):
        """Main game loop."""
        print("=== Quadtree Collision Detection Demo ===")
        print("Press SPACE to toggle between methods")
        print("Press UP/DOWN to change particle count")
        print("Press T to toggle tree visualization")
        print("Press R to reset particles")
        print("Press Q to quit")
        print()
        
        while self.running:
            self.handle_events()
            
            # Update
            self.update_particles()
            self.detect_collisions()
            
            # Draw
            self.screen.fill(BLACK)
            self.draw_quadtree()
            self.draw_particles()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        print("Demo closed")