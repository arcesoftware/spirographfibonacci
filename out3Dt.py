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
points_per_frame = 5    # Growth speed
turns_theta = 4
turns_phi = 6.85
z_growth_per_point = 0.3

# Camera settings
CAMERA_DISTANCE = -400.0  # Base distance behind the tip
CAMERA_LERP = 0.05        # Smoothing factor for camera following

# Generate rainbow colors
colors = [colorsys.hsv_to_rgb(h/360, 1, 1) for h in range(0, 360, 2)]

# =======================
# Spiral Data
# =======================
spiral1 = []
spiral2 = []
current_step = 0
camera_z = 0  # current camera Z position

# =======================
# Functions
# =======================
def add_new_points():
    global current_step
    for _ in range(points_per_frame):
        step = current_step / 100.0

        theta = 2 * math.pi * turns_theta * step
        phi = 2 * math.pi * turns_phi * step

        # Spiral 1
        x1 = (R + r * math.cos(phi)) * math.cos(theta)
        y1 = (R + r * math.cos(phi)) * math.sin(theta)
        z1 = r * math.sin(phi) + z_growth_per_point * current_step
        spiral1.append((x1, y1, z1))

        # Spiral 2 (offset pi)
        phi2 = phi + math.pi
        x2 = (R + r * math.cos(phi2)) * math.cos(theta)
        y2 = (R + r * math.cos(phi2)) * math.sin(theta)
        z2 = r * math.sin(phi2) + z_growth_per_point * current_step
        spiral2.append((x2, y2, z2))

        current_step += 1

def draw_spiral(points):
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
    global camera_z
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Torus Spiral with Camera Following Z")

    # 3D perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (WIDTH/HEIGHT), 0.1, 5000.0)
    glEnable(GL_DEPTH_TEST)
    glLineWidth(3)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Add new points
        add_new_points()

        # 2. Smooth camera tracking of the tip along Z
        target_camera_z = z_growth_per_point * current_step + CAMERA_DISTANCE
        camera_z += (target_camera_z - camera_z) * CAMERA_LERP

        # 3. Reset modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 4. Apply camera translation (only follow Z)
        glTranslatef(0.0, 0.0, -camera_z)

        # 5. Clear screen and draw spirals
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_spiral(spiral1)
        draw_spiral(spiral2)

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()
