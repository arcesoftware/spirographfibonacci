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
R = 150          # Major radius (torus)
r = 50           # Minor radius (tube)
points_per_spiral = 200
turns = 4        # number of full torus rotations
z_growth = 0.0   # can add vertical growth if desired

# Generate rainbow colors
colors = [colorsys.hsv_to_rgb(h/360, 1, 1) for h in range(0, 360, 2)]

# =======================
# Torus spiral generation
# =======================
def generate_double_spiral():
    spiral1 = []
    spiral2 = []
    for i in range(points_per_spiral):
        theta = (2 * math.pi * turns * i / points_per_spiral)  # around torus
        phi = theta  # along tube

        # Spiral 1
        x1 = (R + r * math.cos(phi)) * math.cos(theta)
        y1 = (R + r * math.cos(phi)) * math.sin(theta)
        z1 = r * math.sin(phi) + z_growth * i / points_per_spiral
        spiral1.append((x1, y1, z1))

        # Spiral 2, offset by pi
        phi2 = phi + math.pi
        x2 = (R + r * math.cos(phi2)) * math.cos(theta)
        y2 = (R + r * math.cos(phi2)) * math.sin(theta)
        z2 = r * math.sin(phi2) + z_growth * i / points_per_spiral
        spiral2.append((x2, y2, z2))

    return spiral1, spiral2

# =======================
# DRAWING
# =======================
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("3D Double Spiral Torus")

    gluPerspective(45, (WIDTH/HEIGHT), 0.1, 2000.0)
    glTranslatef(0.0, 0.0, -600)
    glEnable(GL_DEPTH_TEST)
    glLineWidth(3)

    spiral1, spiral2 = generate_double_spiral()

    clock = pygame.time.Clock()
    angle = 0

    running = True
    while running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(angle, 0,1,0)
        draw_spiral(spiral1)
        draw_spiral(spiral2)
        glPopMatrix()

        angle += 30*dt  # rotate 30 degrees/sec

        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    main()
