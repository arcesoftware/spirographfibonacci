import turtle
import math
from time import sleep

# --- Constants ---
# The Golden Ratio (Phi or Tau)
PHI = (1.0 + math.sqrt(5.0)) / 2.0
# The reciprocal of the Golden Ratio
PHI_INV = 1.0 / PHI

# --- Tiling Setup ---

# The tiles are defined by their vertices and orientation.
# Each tile is a dictionary:
# {'type': 'KITE'/'DART', 'vertices': [v1, v2, v3, v4]}

# The core of the Penrose Tiling is the substitution (or deflation) rule.
# This rule replaces a large tile with a set of smaller tiles that are correctly
# positioned and oriented.

# --- Drawing Configuration ---
TILE_SCALE = 150  # Initial size of the tiles
ITERATIONS = 3    # Number of substitution steps (3 is a good balance of detail/speed)
DRAW_SPEED = 0    # 0 = fastest drawing speed

# --- Tiling Logic ---

def polar_to_cartesian(r, theta_deg, origin=(0, 0)):
    """Converts polar coordinates (r, theta in degrees) to cartesian (x, y)."""
    theta_rad = math.radians(theta_deg)
    x = origin[0] + r * math.cos(theta_rad)
    y = origin[1] + r * math.sin(theta_rad)
    return (x, y)

def create_initial_kite(center=(0, 0), size=TILE_SCALE):
    """Creates a central 'sun' pattern of 10 kites around a point."""
    tiles = []
    # Each kite has side length 'size'
    # The inner angle of the kite tip is 36 degrees (360/10)
    for i in range(10):
        # A kite's vertices are A, B, C, D (where A is the top tip)
        # Side length is 1 (scaled by size)
        
        # Calculate angle of the vertices relative to the center
        # Start angle for the loop (36 degrees apart)
        start_angle = 36 * i
        
        # Vertex A (Tip, 36 degrees angle)
        A = center
        
        # Calculate B and D (the 108 degree vertices)
        # B and D are PHI_INV * size distance from C.
        # However, for drawing, it's easier to define C and then B, D relative to C.
        
        # The 10 Kites form a central 'sun' pattern.
        # Vertices of the large Kite structure:
        
        # V0 (Center point)
        V0 = center
        
        # V1 and V2 are the ends of the short diagonal of the kite
        V1_angle = start_angle + 18
        V2_angle = start_angle - 18
        
        # Length of the short diagonal (2 * sin(18) * size)
        # Easier: C is at distance 'size' from A along the angle i*36.
        C_angle = start_angle + 18
        C_dist = size * PHI_INV
        
        # Let's use the standard Kite coordinates based on the origin:
        # A (Tip), C (Tail), B (Left), D (Right)
        
        # A is the center (0,0) for the initial kite structure
        A = center
        
        # C is the tail point, distance PHI from A
        C = polar_to_cartesian(size, start_angle + 18, A)
        
        # B and D are the side vertices
        B = polar_to_cartesian(size * PHI_INV, start_angle + 36, A)
        D = polar_to_cartesian(size * PHI_INV, start_angle, A)
        
        tiles.append({'type': 'KITE', 'vertices': [A, B, C, D], 'rotation': start_angle})
        
    return tiles

def substitute_tiles(tiles):
    """Applies the Penrose substitution rule (deflation) to the list of tiles."""
    new_tiles = []
    
    for tile in tiles:
        A, B, C, D = tile['vertices']
        
        if tile['type'] == 'KITE':
            # KITE Substitution: replaced by a smaller KITE and a DART.
            # Side length is reduced by PHI (multiplied by PHI_INV)
            
            # Find new vertex E on the side AB, which divides it in PHI_INV : PHI_INV^2 ratio
            # Use vector addition: E = A + (B - A) * PHI_INV
            
            # Vector A to B
            AB = (B[0] - A[0], B[1] - A[1])
            AD = (D[0] - A[0], D[1] - A[1])
            
            # E divides AB, F divides AD. Since the sides are equal in length, 
            # E and F are found by moving PHI_INV * length along the side.
            
            # E is on AB, F is on AD
            E = (A[0] + AB[0] * PHI_INV, A[1] + AB[1] * PHI_INV)
            F = (A[0] + AD[0] * PHI_INV, A[1] + AD[1] * PHI_INV)
            
            # G is the new inner vertex (on the line AC)
            # G is distance PHI_INV from C
            AC = (C[0] - A[0], C[1] - A[1])
            CG = (A[0] - C[0], A[1] - C[1])
            
            # G is located at the intersection of DF and BE, or (it's simpler) 
            # it is the point dividing the central diagonal in PHI_INV ratio from C.
            G = (C[0] + CG[0] * PHI_INV, C[1] + CG[1] * PHI_INV)
            
            # 1. New KITE (Small)
            # Vertices: A, E, G, F
            new_tiles.append({'type': 'KITE', 'vertices': [A, E, G, F]})
            
            # 2. New DART (Small)
            # Vertices: E, B, C, G
            new_tiles.append({'type': 'DART', 'vertices': [E, B, C, G]})
            
            # 3. New DART (Small, symmetric)
            # Vertices: F, G, C, D
            new_tiles.append({'type': 'DART', 'vertices': [F, G, C, D]})
            
        elif tile['type'] == 'DART':
            # DART Substitution: replaced by a smaller KITE and a DART.
            
            # Find new vertex E on side BA (B is the concave vertex)
            BA = (A[0] - B[0], A[1] - B[1])
            BC = (C[0] - B[0], C[1] - B[1])
            
            # E is on BA, F is on BC. E and F divide the side PHI_INV : PHI_INV^2 from B.
            E = (B[0] + BA[0] * PHI_INV, B[1] + BA[1] * PHI_INV)
            F = (B[0] + BC[0] * PHI_INV, B[1] + BC[1] * PHI_INV)
            
            # G is the new inner vertex (on the line BD)
            BD = (D[0] - B[0], D[1] - B[1])
            # G divides the diagonal BD in PHI_INV : PHI_INV^2 from B
            G = (B[0] + BD[0] * PHI_INV, B[1] + BD[1] * PHI_INV)
            
            # H is the new inner vertex (on AD/CD)
            AD = (D[0] - A[0], D[1] - A[1])
            CD = (D[0] - C[0], D[1] - C[1])
            
            # H is on the line segment joining the two 108 deg vertices (A and C)
            # H is distance PHI_INV from D
            DA = (A[0] - D[0], A[1] - D[1])
            DC = (C[0] - D[0], C[1] - D[1])
            H = (D[0] + DA[0] * PHI_INV, D[1] + DA[1] * PHI_INV)
            
            # 1. New KITE (Small)
            # Vertices: B, E, G, F
            new_tiles.append({'type': 'KITE', 'vertices': [B, E, G, F]})
            
            # 2. New DART (Small)
            # Vertices: D, H, C, F
            new_tiles.append({'type': 'DART', 'vertices': [D, H, C, F]})

            # 3. New DART (Small, symmetric)
            # Vertices: D, H, A, E
            new_tiles.append({'type': 'DART', 'vertices': [D, H, A, E]})
            
    return new_tiles

def draw_tiling(tiles, drawer):
    """Draws all tiles in the list using the Turtle."""
    kite_color = "#336699"  # Blue
    dart_color = "#E08F32"  # Orange
    
    for tile in tiles:
        drawer.up()
        drawer.goto(tile['vertices'][0])
        drawer.down()
        drawer.begin_fill()
        
        if tile['type'] == 'KITE':
            drawer.fillcolor(kite_color)
            drawer.pencolor(kite_color)
        else:
            drawer.fillcolor(dart_color)
            drawer.pencolor(dart_color)
        
        # Draw the polygon defined by the vertices
        for vertex in tile['vertices']:
            drawer.goto(vertex)
        
        drawer.goto(tile['vertices'][0]) # Close the shape
        drawer.end_fill()

# --- Main Execution ---

def main():
    # Setup the screen and turtle
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.title("Penrose Kite and Dart Tiling (Deflation Method)")
    screen.colormode(255) # Use RGB colors
    screen.bgcolor(20, 20, 20) # Dark background
    
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.speed(DRAW_SPEED) # Set to maximum speed for drawing

    # 1. Initialize the tiling with the initial 'sun' pattern
    current_tiles = create_initial_kite()

    # 2. Perform substitutions (deflation)
    for i in range(ITERATIONS):
        screen.tracer(0, 0) # Turn off screen updates for speed
        current_tiles = substitute_tiles(current_tiles)
        print(f"Iteration {i+1}: {len(current_tiles)} tiles generated.")
        screen.tracer(1, 10) # Turn on updates briefly to show progress
        
    # 3. Draw the final set of tiles
    screen.tracer(0, 0) # Turn off screen updates for final drawing
    draw_tiling(current_tiles, drawer)
    screen.tracer(1, 10) # Turn on updates
    
    drawer.up()
    drawer.goto(0, 0)
    drawer.pencolor("white")
    drawer.write(f"Penrose Tiling (Kites & Darts)\nIterations: {ITERATIONS} | Tiles: {len(current_tiles)}", 
                 align="center", font=("Inter", 16, "bold"))
    
    screen.exitonclick()

if __name__ == '__main__':
    main()
