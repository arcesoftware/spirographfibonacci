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
points_per_spiral = 500 # Increased point density for smoother look
turns_theta = 4 # Number of rotations around the Torus (Theta angle)
turns_phi = 6.85 # Number of rotations along the Tube (Phi angle) - Non-integer for a more complex spiral
z_growth = 150.0 # **New:** Vertical growth after each turn

# Generate rainbow colors
colors = [colorsys.hsv_to_rgb(h/360, 1, 1) for h in range(0, 360, 2)]

# =======================
# Torus spiral generation
# =======================
def generate_double_spiral():
    """Generates a double spiral wrapped around a growing torus."""
    spiral1 = []
    spiral2 = []
    
    # Pre-calculate the total angular travel for turns_theta and turns_phi
    total_theta = 2 * math.pi * turns_theta
    total_phi = 2 * math.pi * turns_phi
    
    for i in range(points_per_spiral):
        # Normalized step (0 to 1)
        step = i / points_per_spiral

        # Calculate angles: Theta is around the torus, Phi is along the tube
        theta = total_theta * step
        phi = total_phi * step

        # --- Spiral 1 ---
        # Parametric equations for a torus knot
        x1 = (R + r * math.cos(phi)) * math.cos(theta)
        y1 = (R + r * math.cos(phi)) * math.sin(theta)
        
        # Z component: Base height + vertical growth based on the step
        z1 = r * math.sin(phi) + z_growth * step
        spiral1.append((x1, y1, z1))

        # --- Spiral 2, offset by pi ---
        # Creates the double helix effect
        phi2 = phi + math.pi
        x2 = (R + r * math.cos(phi2)) * math.cos(theta)
        y2 = (R + r * math.cos(phi2)) * math.sin(theta)
        z2 = r * math.sin(phi2) + z_growth * step
        spiral2.append((x2, y2, z2))

    return spiral1, spiral2

# =======================
# DRAWING
# =======================
def draw_spiral(points):
    """Draws the 3D line strip with rainbow colors."""
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("3D Growing Double Spiral")

    # Setup 3D projection
    gluPerspective(45, (WIDTH/HEIGHT), 0.1, 2000.0)
    
    # Translate the camera back. Adjusted the distance slightly for the taller object.
    glTranslatef(0.0, 0.0, -800) 
    glEnable(GL_DEPTH_TEST) # Ensure correct drawing order
    glLineWidth(3)

    spiral1, spiral2 = generate_double_spiral()

    clock = pygame.time.Clock()
    angle = 0

    running = True
    while running:
        dt = clock.tick(60)/1000.0 # Time elapsed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Allow camera movement via arrow keys (optional, but helpful)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glRotatef(5, 1, 0, 0) # Rotate X
                if event.key == pygame.K_DOWN:
                    glRotatef(-5, 1, 0, 0)
                if event.key == pygame.K_LEFT:
                    glRotatef(5, 0, 1, 0) # Rotate Y
                if event.key == pygame.K_RIGHT:
                    glRotatef(-5, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Draw the model
        glPushMatrix()
        
        # Automatic Y-axis rotation for animation
        glRotatef(angle, 0,1,0) 
        
        draw_spiral(spiral1)
        draw_spiral(spiral2)
        glPopMatrix()

        angle += 30*dt  # rotate 30 degrees/sec

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()
