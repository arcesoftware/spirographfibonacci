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
points_per_frame = 5    # How many new points are added per frame (growth speed)
turns_theta = 4 # Rotations around the torus
turns_phi = 6.85 # Rotations along the tube (non-integer for complexity)
z_growth_per_point = 0.3 # Vertical growth per step

# Define camera parameters for tracking
CAMERA_DISTANCE = -800.0 # Initial distance back from the object
VIEWING_OFFSET_Z = -200.0 # How far below the tip the camera looks

# Generate rainbow colors (360 colors for a full HSV cycle)
colors = [colorsys.hsv_to_rgb(h/360, 1, 1) for h in range(0, 360, 2)]

# =======================
# Spiral Data and State
# =======================
spiral1 = []
spiral2 = []
current_step = 0    # Keeps track of total steps for parametric angles
angle = 0           # For continuous rotation of the view

# =======================
# Functions
# =======================
def add_new_points():
    """Adds new points to the spiral for continuous, infinite growth."""
    global current_step
    global spiral1
    global spiral2
    
    for _ in range(points_per_frame):
        # We use current_step for calculation, but scale it down for speed control
        step = current_step / 100.0

        # Calculate angles: Theta (around torus), Phi (along tube)
        theta = 2 * math.pi * turns_theta * step
        phi = 2 * math.pi * turns_phi * step

        # --- Spiral 1 ---
        x1 = (R + r * math.cos(phi)) * math.cos(theta)
        y1 = (R + r * math.cos(phi)) * math.sin(theta)
        # Z component: Base height + continuous vertical growth
        z1 = r * math.sin(phi) + z_growth_per_point * current_step
        spiral1.append((x1, y1, z1))

        # --- Spiral 2 offset by pi ---
        phi2 = phi + math.pi
        x2 = (R + r * math.cos(phi2)) * math.cos(theta)
        y2 = (R + r * math.cos(phi2)) * math.sin(theta)
        z2 = r * math.sin(phi2) + z_growth_per_point * current_step
        spiral2.append((x2, y2, z2))

        # IMPORTANT: The code for limiting point size has been removed.
        # The spiral will grow indefinitely in memory.

        current_step += 1

def draw_spiral(points):
    """Draw the spiral with rainbow colors."""
    glBegin(GL_LINE_STRIP)
    for idx, (x, y, z) in enumerate(points):
        # Cycle through colors based on the point index
        c = colors[idx % len(colors)]
        glColor3f(*c)
        glVertex3f(x, y, z)
    glEnd()

# =======================
# MAIN LOOP
# =======================
def main():
    global angle
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Continuously Growing Torus Spiral (Infinite Growth)")

    # Setup 3D projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (WIDTH/HEIGHT), 0.1, 3000.0)
    
    glEnable(GL_DEPTH_TEST) # Enable depth testing for 3D perspective
    glLineWidth(3)

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Add new points each frame
        add_new_points()

        # 2. Camera Tracking Logic
        tip_z = z_growth_per_point * current_step
        
        # Reset the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Apply View Transform:
        
        # A. Zoom out (fixed distance back)
        glTranslatef(0.0, 0.0, CAMERA_DISTANCE)
        
        # B. Tracking Translation: Move the camera *down* the negative Z axis 
        # to follow the upward (positive Z) growth of the tip.
        # tip_z is the current height. -tip_z translates the world back down.
        # VIEWING_OFFSET_Z ensures the camera looks slightly below the tip.
        glTranslatef(0.0, 0.0, -tip_z + VIEWING_OFFSET_Z) 

        # C. Aesthetic Rotation: Slowly rotate the view around the Y-axis
        angle += 15 * dt
        glRotatef(angle, 0, 1, 0)
        
        # 3. Drawing
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        draw_spiral(spiral1)
        draw_spiral(spiral2)

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()
