# fib_helical_spiro.py
# Fibonacci Helical Spirals adapted into the OpenGL evolving-loop engine
# Requires: pygame, numpy, PyOpenGL
# Author: adapted for Juan Arce — November 2025

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import colorsys
import numpy as np

# =======================
# CONFIG / TUNABLES
# =======================
WIDTH, HEIGHT = 1200, 800
POINTS_PER_FRAME = 4        # growth per loop per frame
LOOP_GROWTH_Z = 2.2        # Z increment per completed cycle (stacking height)
CYCLE_LENGTH = 360         # steps per logical helix cycle
MAX_LOOPS = 80             # safety cap
MERGE_DISTANCE = 10.0      # tip-merging threshold
BASE_SPLIT_PROB = 0.0008   # base chance of random split (small)
CURV_SPLIT_THRESHOLD = 0.35  # curvature threshold to force split
SPLIT_COOLDOWN_FRAMES = 140  # frames to wait before same loop can split again
CURV_TWIST_SCALE = 20.0    # how strongly curvature affects twist amplitude

# Fibonacci helical controls
FIB_COUNT = 30            # number of Fibonacci numbers we precompute
FIB_RADIUS_SCALE = 0.75   # how much fib value increases radius
FIB_PITCH_SCALE = 0.035   # how much fib value increases pitch (z per step)
FIB_ANG_FREQ_BASE = 1.0   # base angular frequency multiplier
FIB_ANG_FREQ_SCALE = 0.006  # how fib value affects angular frequency
HELIX_NOISE_AMP = 6.0     # jitter orthogonal to helix for visual richness

# Camera
camera_distance = 900.0
camera_lerp = 0.06
zoom_speed = 30.0

# Interaction state
last_mouse_pos = None
rotation_x, rotation_y = 0.0, 0.0
pan_x, pan_y = 0.0, 0.0
camera_z = 0.0

# =======================
# Helpers
# =======================
def hsv_to_rgb(h, s, v):
    return colorsys.hsv_to_rgb(h % 1.0, s, v)

def compute_fibonacci_list(n):
    fib = [1, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib[:n]

FIB_LIST = compute_fibonacci_list(FIB_COUNT)
FIB_MAX = float(FIB_LIST[-1])

# =======================
# LOOP CLASS
# =======================
class Loop:
    def __init__(self, phase=0.0, fib_index=0):
        self.points = []            # list of (x,y,z) tuples
        self.phase = phase          # starting angular offset
        self.step = 0               # parametric step counter
        self.cycle = 0              # completed cycles
        self.active = True
        self.last_split_frame = -SPLIT_COOLDOWN_FRAMES
        self.id = random.randint(0, 2**31-1)
        # Fibonacci-related
        self.fib_index = int(fib_index) % len(FIB_LIST)
        self.fib_value = float(FIB_LIST[self.fib_index])
        # tuning per-loop multipliers (small random variance)
        self.radius_offset = random.uniform(-8.0, 8.0)
        self.pitch_offset = random.uniform(-0.6, 0.6)

    def append_point(self, p):
        self.points.append(p)

    def tip(self):
        return self.points[-1] if self.points else None

# =======================
# GLOBAL MANIFOLD STATE
# =======================
loops = [Loop(phase=0.0, fib_index=3)]
frame_count = 0

# =======================
# MATH HELPERS
# =======================
def discrete_curvature(p_prev, p_curr, p_next):
    """Discrete curvature vector magnitude (approx second derivative)."""
    if p_prev is None or p_next is None:
        return 0.0
    prev = np.array(p_prev, dtype=float)
    curr = np.array(p_curr, dtype=float)
    nxt  = np.array(p_next, dtype=float)
    second = nxt - 2.0*curr + prev
    step_len = (np.linalg.norm(curr - prev) + np.linalg.norm(nxt - curr)) * 0.5 + 1e-6
    kappa = np.linalg.norm(second) / (step_len**2 + 1e-12)
    return kappa

def fib_helical_point(t, cycle, loop: Loop):
    """
    Generate a 3D helix point parameterized by step t.
    Helix parameters are modulated by a Fibonacci number attached to the loop.
    """
    # fibonacci factor normalized
    fib_val = loop.fib_value
    fib_norm = fib_val / (FIB_MAX + 1e-9)

    # angular parameter (radians)
    ang = t * (2.0 * math.pi /  (CYCLE_LENGTH/ (FIB_ANG_FREQ_BASE + fib_val * FIB_ANG_FREQ_SCALE))) + loop.phase

    # radius grows with fibonacci number (with base radius)
    base_radius = 60.0 + FIB_RADIUS_SCALE * fib_val + loop.radius_offset
    radius = base_radius * (1.0 + 0.06 * math.sin(t * 0.12 + loop.id % 17))

    # vertical pitch per step influenced by fib
    pitch = (1.0 + fib_norm * FIB_PITCH_SCALE * fib_val) + loop.pitch_offset
    z = cycle * LOOP_GROWTH_Z + t * pitch + 6.0 * math.sin(2.0 * ang + fib_norm * 3.14)

    # helix coordinates
    x = radius * math.cos(ang)
    y = radius * math.sin(ang)

    # add a small orthogonal noise/jitter for richness
    jitter_dir = np.array([math.cos(ang + 0.5), math.sin(ang + 0.5), 0.0])
    jitter = (math.sin(t * 0.23 + loop.id % 31) * HELIX_NOISE_AMP * (0.2 + 0.8*fib_norm))
    x += jitter_dir[0] * jitter
    y += jitter_dir[1] * jitter

    return np.array([x, y, z], dtype=float)

# =======================
# EVOLUTION FUNCTIONS
# =======================
def add_new_points_and_evolve():
    global loops, frame_count

    new_loops = []
    for loop in list(loops):
        if not loop.active:
            continue

        for _ in range(POINTS_PER_FRAME):
            t = loop.step
            base = fib_helical_point(t, loop.cycle, loop)

            # compute curvature-influenced twist using last couple points
            prev = loop.points[-2] if len(loop.points) >= 2 else None
            curr = loop.points[-1] if len(loop.points) >= 1 else None
            kappa = discrete_curvature(prev, curr, base) if curr is not None else 0.0

            # curvature-scaled twist (stronger twist in high curvature areas)
            twist_amp = 1.0 + CURV_TWIST_SCALE * min(kappa, 1.0)
            seed = (loop.id ^ loop.step) & 0xffffffff
            rnd = (random.Random(seed).random() - 0.5)

            # apply twist roughly perpendicular to local tangent
            if curr is not None:
                tangent = base - curr
                if np.linalg.norm(tangent) < 1e-6:
                    tangent = np.array([1.0,0.0,0.0])
                tangent = tangent / (np.linalg.norm(tangent) + 1e-9)
                perp = np.cross(tangent, np.array([0.0,0.0,1.0]))
                if np.linalg.norm(perp) < 1e-6:
                    perp = np.cross(tangent, np.array([0.0,1.0,0.0]))
                perp = perp / (np.linalg.norm(perp)+1e-9)
                twist_vec = perp * (rnd * twist_amp * (0.6 + 0.4*math.sin(loop.step*0.03)))
                base = base + twist_vec
            else:
                base = base + np.array([rnd*0.8, (random.Random(seed+1).random()-0.5)*0.8, 0.0])

            loop.append_point(tuple(base.tolist()))
            loop.step += 1

            # when completing a cycle, increase cycle and occasionally advance Fibonacci index
            if loop.step >= CYCLE_LENGTH:
                loop.step = 0
                loop.cycle += 1
                # small chance to advance to next fib (produces larger shells)
                if random.random() < 0.25:
                    loop.fib_index = (loop.fib_index + 1) % len(FIB_LIST)
                    loop.fib_value = float(FIB_LIST[loop.fib_index])
                # small random phase tweak for variety
                loop.phase += random.uniform(-0.15, 0.15)

        # splitting logic based on curvature
        if len(loop.points) >= 4:
            i = len(loop.points)-2
            p_prev = loop.points[i-1]
            p_curr = loop.points[i]
            p_next = loop.points[i+1]
            kappa = discrete_curvature(p_prev, p_curr, p_next)

            if kappa > CURV_SPLIT_THRESHOLD and (frame_count - loop.last_split_frame) > SPLIT_COOLDOWN_FRAMES:
                if len(loops) + len(new_loops) < MAX_LOOPS:
                    split_pt = np.array(p_curr)
                    tangent1 = np.array(p_curr) - np.array(p_prev)
                    tangent2 = np.array(p_next) - np.array(p_curr)
                    normal = np.cross(tangent1, tangent2)
                    if np.linalg.norm(normal) < 1e-6:
                        normal = np.array([random.uniform(-1,1), random.uniform(-1,1), 0.0])
                    normal = normal / (np.linalg.norm(normal)+1e-9)
                    offset = normal * (4.0 + 3.0 * random.random())
                    new_phase = loop.phase + random.uniform(-0.6, 0.6)

                    # choose new fib index biased to be nearby but sometimes jump
                    if random.random() < 0.7:
                        new_fib_idx = (loop.fib_index + 1) % len(FIB_LIST)
                    else:
                        new_fib_idx = random.randint(0, len(FIB_LIST)-1)

                    new_loop = Loop(phase=new_phase, fib_index=new_fib_idx)
                    for s in range(3):
                        jitter = normal * s * 0.6
                        new_loop.points.append(tuple((split_pt + jitter).tolist()))
                    new_loop.step = loop.step
                    new_loop.cycle = loop.cycle
                    new_loop.last_split_frame = frame_count
                    loop.last_split_frame = frame_count
                    new_loops.append(new_loop)

        # spontaneous split with small prob
        if random.random() < BASE_SPLIT_PROB and len(loops) + len(new_loops) < MAX_LOOPS:
            # spawn new loop near tip with fib index shifted
            nl_idx = (loop.fib_index + random.choice([0,1,2])) % len(FIB_LIST)
            nl = Loop(phase=loop.phase + random.uniform(-0.6, 0.6), fib_index=nl_idx)
            tip = loop.tip()
            if tip is not None:
                for s in range(2):
                    nl.points.append(tuple((np.array(tip) + np.random.randn(3)*2.0).tolist()))
            new_loops.append(nl)

    if new_loops:
        loops.extend(new_loops)

    # MERGING
    tips = [(i, loop.tip()) for i, loop in enumerate(loops) if loop.points and loop.active]
    for a in range(len(tips)):
        idx_i, tip_i = tips[a]
        if tip_i is None:
            continue
        for b in range(a+1, len(tips)):
            idx_j, tip_j = tips[b]
            if tip_j is None or idx_i==idx_j:
                continue
            dist = np.linalg.norm(np.array(tip_i) - np.array(tip_j))
            if dist < MERGE_DISTANCE:
                midpoint = 0.5*(np.array(tip_i) + np.array(tip_j))
                loops[idx_i].points[-1] = tuple(midpoint.tolist())
                loops[idx_j].points[-1] = tuple(midpoint.tolist())
                loops[idx_j].active = False

# =======================
# RENDERING
# =======================
def curvature_color_for_point(loop, idx):
    pts = loop.points
    if idx <= 0 or idx >= len(pts)-1:
        return (0.18, 0.18, 0.5)
    k = discrete_curvature(pts[idx-1], pts[idx], pts[idx+1])
    k_norm = min(k / 0.6, 1.0)
    # base hue from fibonacci index (wrap around)
    hue = (loop.fib_index / float(len(FIB_LIST))) % 1.0
    # shift hue slightly depending on local curvature
    hue = (hue + 0.12 * k_norm) % 1.0
    # s and v modulated by curvature for contrast
    s = 0.6 + 0.4 * (1.0 - k_norm)
    v = 0.6 + 0.4 * k_norm
    r, g, b = hsv_to_rgb(hue, s, v)
    return (r, g, b)

def draw_loops():
    glLineWidth(2.0)
    for loop in loops:
        if not loop.points:
            continue
        glBegin(GL_LINE_STRIP)
        for idx, (x,y,z) in enumerate(loop.points):
            c = curvature_color_for_point(loop, idx)
            glColor3f(*c)
            glVertex3f(x, y, z)
        glEnd()

# =======================
# MAIN
# =======================
def main():
    global last_mouse_pos, rotation_x, rotation_y, pan_x, pan_y, camera_distance, camera_z, frame_count

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Fibonacci Helical Spirals — Curvature Branching")

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, (WIDTH/HEIGHT), 0.1, 8000.0)
    glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        frame_count += 1

        # --- events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                camera_distance += -event.y * zoom_speed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                last_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION and last_mouse_pos:
                mx, my = event.pos
                dx = mx - last_mouse_pos[0]
                dy = my - last_mouse_pos[1]
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    rotation_y += dx * 0.28
                    rotation_x += dy * 0.28
                if buttons[1]:
                    pan_x += dx * 0.6
                    pan_y -= dy * 0.6
                last_mouse_pos = (mx, my)

        # --- evolution
        add_new_points_and_evolve()

        # --- camera follow highest tip
        active_tips = [loop.tip()[2] for loop in loops if loop.points and loop.active]
        tip_z = max(active_tips) if active_tips else 0.0
        target_camera_z = tip_z + camera_distance
        camera_z += (target_camera_z - camera_z) * camera_lerp

        # --- render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-pan_x, -pan_y, -camera_z)
        glRotatef(rotation_x, 1.0, 0.0, 0.0)
        glRotatef(rotation_y, 0.0, 1.0, 0.0)

        draw_loops()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
