import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import colorsys

# =======================
# CONFIG
# =======================
WIDTH, HEIGHT = 1200, 800
R = 150         # Major radius (torus)
r = 50          # Minor radius (tube)
points_per_frame = 5   # How many new points are added per frame
turns_theta = 4
turns_phi = 6.85
z_growth_per_point = 0.3  # Vertical growth per point

# Maximum points to keep in memory (prevents overflow)
max_points = 1000

# Generate rainbow colors
colors = [colorsys.hsv_to_rgb(h/360, 1, 1) for h in range(0, 360, 2)]

# =======================
# Spiral Data
# =======================
spiral1 = []
spiral2 = []
current_step = 0  # Keeps track of total steps for parametric angles

# =======================
# Functions
# =======================
def add_new_points():
    """Add new points to the spiral for continuous growth."""
    global current_step
    for _ in range(points_per_frame):
        step = current_step / 100.0  # scaling factor for speed

        theta = 2 * math.pi * turns_theta * step
        phi = 2 * math.pi * turns_phi * step

        # Spiral 1
        x1 = (R + r * math.cos(phi)) * math.cos(theta)
        y1 = (R + r * math.cos(phi)) * math.sin(theta)
        z1 = r * math.sin(phi) + z_growth_per_point * current_step
        spiral1.append((x1, y1, z1))

        # Spiral 2 offset by pi
        phi2 = phi + math.pi
        x2 = (R + r * math.cos(phi2)) * math.cos(theta)
        y2 = (R + r * math.cos(phi2)) * math.sin(theta)
        z2 = r * math.sin(phi2) + z_growth_per_point * current_step
        spiral2.append((x2, y2, z2))

        # Keep spirals within max_points
        if len(spiral1) > max_points:
            spiral1.pop(0)
            spiral2.pop(0)

        current_step += 1

def draw_spiral(points):
    """Draw the spiral with rainbow colors."""
    glBegin(GL_LINE_STRIP)
    for idx, (x, y, z) in enumerate(points):
        c = colors[idx % len(colors)]
        glColor3f(*c)
        glVertex3f(x, y, z)
    glEnd()

# =======================
# MAIN LOOP
# =======================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Continuously Growing Double Spiral")

    gluPerspective(45, (WIDTH/HEIGHT), 0.1, 3000.0)
    glTranslatef(0.0, 0.0, -800)
    glEnable(GL_DEPTH_TEST)
    glLineWidth(3)

    clock = pygame.time.Clock()
    angle = 0

    running = True
    while running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Add new points each frame
        add_new_points()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(angle, 0,1,0)
        draw_spiral(spiral1)
        draw_spiral(spiral2)
        glPopMatrix()

        angle += 20*dt  # rotation speed

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()
