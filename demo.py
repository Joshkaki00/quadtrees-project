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