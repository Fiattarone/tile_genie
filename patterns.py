import random
from PIL import ImageDraw

PATTERN_GENERATORS = {}

def register_pattern(name):
    """
    Decorator to register a pattern function under a certain name
    in the global PATTERN_GENERATORS dictionary.
    """
    def decorator(func):
        PATTERN_GENERATORS[name] = func
        return func
    return decorator


# -------------------------------------------------------------------------
# Existing Patterns (You already have these)
# -------------------------------------------------------------------------

@register_pattern("solid")
def pattern_solid(draw, palette):
    """
    Fill all pixels with random picks from the palette.
    """
    for x in range(16):
        for y in range(16):
            color_choice = random.choice(palette)
            draw.point((x, y), fill=color_choice)

@register_pattern("stripes_horizontal")
def pattern_stripes_horizontal(draw, palette):
    """
    Draw horizontal stripes in 2-pixel bands, using the palette in rotation.
    """
    stripe_height = 2
    color_index = 0
    for y in range(16):
        if y % stripe_height == 0:
            color_index = (color_index + 1) % len(palette)
        for x in range(16):
            draw.point((x, y), fill=palette[color_index])

@register_pattern("stripes_vertical")
def pattern_stripes_vertical(draw, palette):
    """
    Draw vertical stripes in 2-pixel bands, using the palette in rotation.
    """
    stripe_width = 2
    color_index = 0
    for x in range(16):
        if x % stripe_width == 0:
            color_index = (color_index + 1) % len(palette)
        for y in range(16):
            draw.point((x, y), fill=palette[color_index])

@register_pattern("checkerboard")
def pattern_checkerboard(draw, palette):
    """
    Classic checkerboard pattern: alternate colors in a 2×2 block.
    """
    colors = palette[:]
    random.shuffle(colors)
    for y in range(16):
        for x in range(16):
            index = ((x // 2) + (y // 2)) % len(colors)
            draw.point((x, y), fill=colors[index])

@register_pattern("dots")
def pattern_dots(draw, palette):
    """
    Place small "dot" clusters with random radius.
    """
    for _ in range(10):  # number of dots
        dot_x = random.randint(0, 15)
        dot_y = random.randint(0, 15)
        radius = random.randint(1, 3)
        color = random.choice(palette)
        for rx in range(-radius, radius+1):
            for ry in range(-radius, radius+1):
                if 0 <= dot_x + rx < 16 and 0 <= dot_y + ry < 16:
                    if rx*rx + ry*ry <= radius*radius:
                        draw.point((dot_x + rx, dot_y + ry), fill=color)

@register_pattern("diagonal_lines")
def pattern_diagonal_lines(draw, palette):
    """
    Repeated diagonal lines going from top-left to bottom-right.
    """
    color_idx = 0
    for d in range(-15, 16):
        color = palette[color_idx % len(palette)]
        color_idx += 1
        for x in range(16):
            y = x - d
            if 0 <= x < 16 and 0 <= y < 16:
                draw.point((x, y), fill=color)

@register_pattern("gradient")
def pattern_gradient(draw, palette):
    """
    Simple top-to-bottom gradient from the first color to the last color in the palette.
    """
    if len(palette) < 2:
        c1 = palette[0]
        c2 = palette[0]
    else:
        c1 = palette[0]
        c2 = palette[-1]

    for y in range(16):
        t = y / 15.0  # interpolation factor
        r = int(c1[0] + t*(c2[0] - c1[0]))
        g = int(c1[1] + t*(c2[1] - c1[1]))
        b = int(c1[2] + t*(c2[2] - c1[2]))
        for x in range(16):
            draw.point((x, y), fill=(r, g, b))

@register_pattern("random_blocks")
def pattern_random_blocks(draw, palette):
    """
    Create random NxN blocks with random color from the palette.
    """
    block_size = 4
    for by in range(0, 16, block_size):
        for bx in range(0, 16, block_size):
            color = random.choice(palette)
            for x in range(bx, bx+block_size):
                for y in range(by, by+block_size):
                    draw.point((x, y), fill=color)


# -------------------------------------------------------------------------
# 25 New Patterns
# -------------------------------------------------------------------------

@register_pattern("chessboard_small")
def pattern_chessboard_small(draw, palette):
    """
    A smaller checkerboard pattern that alternates every single pixel.
    Uses only the first 2 colors from the palette, if available.
    """
    c1 = palette[0]
    c2 = palette[min(1, len(palette)-1)]
    for y in range(16):
        for x in range(16):
            if (x + y) % 2 == 0:
                draw.point((x, y), fill=c1)
            else:
                draw.point((x, y), fill=c2)

@register_pattern("rings")
def pattern_rings(draw, palette):
    """
    Concentric rings centered in the tile.
    Each ring picks a color from the palette in sequence.
    """
    center = (8, 8)
    max_radius = 8
    color_index = 0
    for r in range(max_radius, 0, -1):
        color = palette[color_index % len(palette)]
        color_index += 1
        # Draw a circle of radius r
        for angle_deg in range(0, 360):
            import math
            angle = math.radians(angle_deg)
            x = int(center[0] + r * math.cos(angle))
            y = int(center[1] + r * math.sin(angle))
            if 0 <= x < 16 and 0 <= y < 16:
                draw.point((x, y), fill=color)

@register_pattern("squares")
def pattern_squares(draw, palette):
    """
    Concentric squares from outer edge to inner center.
    """
    color_index = 0
    for size in range(16, 0, -2):
        color = palette[color_index % len(palette)]
        color_index += 1
        offset = (16 - size) // 2
        for x in range(offset, offset+size):
            draw.point((x, offset), fill=color)
            draw.point((x, offset+size-1), fill=color)
        for y in range(offset, offset+size):
            draw.point((offset, y), fill=color)
            draw.point((offset+size-1, y), fill=color)

@register_pattern("triangles")
def pattern_triangles(draw, palette):
    """
    Simple triangular fill pattern: top-left to bottom-right diagonals.
    """
    for y in range(16):
        for x in range(16):
            # Decide a color by x+y
            index = ((x + y) // 2) % len(palette)
            draw.point((x, y), fill=palette[index])

@register_pattern("zigzag")
def pattern_zigzag(draw, palette):
    """
    Horizontal zigzag lines across the tile.
    """
    color_index = 0
    for y in range(16):
        color = palette[color_index % len(palette)]
        color_index += 1
        direction = 1 if (y // 2) % 2 == 0 else -1
        # shift the row's starting x to create a zigzag
        x_start = 0 if direction == 1 else 15
        for step in range(16):
            x = x_start + (step * direction)
            if 0 <= x < 16:
                draw.point((x, y), fill=color)

@register_pattern("random_specks")
def pattern_random_specks(draw, palette):
    """
    Scatter random single-pixel specks in random colors from the palette.
    """
    for _ in range(50):  # number of specks
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        color = random.choice(palette)
        draw.point((x, y), fill=color)

@register_pattern("random_lines")
def pattern_random_lines(draw, palette):
    """
    Draw random lines of random color from palette.
    """
    for _ in range(10):
        color = random.choice(palette)
        x1, y1 = random.randint(0, 15), random.randint(0, 15)
        x2, y2 = random.randint(0, 15), random.randint(0, 15)
        ImageDraw.Draw(draw.im).line((x1, y1, x2, y2), fill=color)

@register_pattern("maze")
def pattern_maze(draw, palette):
    """
    A very rough 'maze-like' pattern using random horizontal or vertical segments.
    """
    for y in range(16):
        for x in range(16):
            # 50% chance to connect horizontally, 50% vertically
            color = random.choice(palette)
            if random.random() < 0.5 and x < 15:
                draw.point((x, y), fill=color)
                draw.point((x+1, y), fill=color)
            else:
                if y < 15:
                    draw.point((x, y), fill=color)
                    draw.point((x, y+1), fill=color)

@register_pattern("sprinkle")
def pattern_sprinkle(draw, palette):
    """
    Like 'dots', but each dot is just a single pixel (sprinkle).
    """
    for _ in range(30):
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        draw.point((x, y), fill=random.choice(palette))

@register_pattern("grain")
def pattern_grain(draw, palette):
    """
    Vertical 'grain' lines, each column has a color that might slightly change randomly.
    """
    base_color = random.choice(palette)
    for x in range(16):
        # Slightly shift color from base
        col_color = random.choice(palette)
        for y in range(16):
            draw.point((x, y), fill=col_color)

@register_pattern("shaded_circle")
def pattern_shaded_circle(draw, palette):
    """
    A large circle in the center, shaded from one color to another radially.
    """
    if len(palette) < 2:
        c1 = palette[0]
        c2 = palette[0]
    else:
        c1 = palette[0]
        c2 = palette[-1]
    cx, cy = 8, 8
    max_r2 = 8 * 8  # radius^2
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy
            dist2 = dx*dx + dy*dy
            if dist2 <= max_r2:
                t = dist2 / float(max_r2)
                r = int(c1[0] + t*(c2[0] - c1[0]))
                g = int(c1[1] + t*(c2[1] - c1[1]))
                b = int(c1[2] + t*(c2[2] - c1[2]))
                draw.point((x, y), fill=(r, g, b))

@register_pattern("border")
def pattern_border(draw, palette):
    """
    A simple border around the tile with the first color in palette, fill center with another color.
    """
    c1 = palette[0]
    c2 = palette[min(1, len(palette)-1)]
    for y in range(16):
        for x in range(16):
            if x == 0 or x == 15 or y == 0 or y == 15:
                draw.point((x, y), fill=c1)
            else:
                draw.point((x, y), fill=c2)

@register_pattern("concentric_circles")
def pattern_concentric_circles(draw, palette):
    """
    Circles that increase in radius by 2, each ring a different color.
    """
    center = (8, 8)
    color_index = 0
    for radius in range(1, 9, 2):
        color = palette[color_index % len(palette)]
        color_index += 1
        for angle_deg in range(360):
            import math
            angle = math.radians(angle_deg)
            x = int(center[0] + radius * math.cos(angle))
            y = int(center[1] + radius * math.sin(angle))
            if 0 <= x < 16 and 0 <= y < 16:
                draw.point((x, y), fill=color)

@register_pattern("x_cross")
def pattern_x_cross(draw, palette):
    """
    Draws an 'X' across the tile in 2 random colors from the palette.
    """
    c1 = random.choice(palette)
    c2 = random.choice(palette)
    for i in range(16):
        draw.point((i, i), fill=c1)
        draw.point((15 - i, i), fill=c2)

@register_pattern("crosshatch")
def pattern_crosshatch(draw, palette):
    """
    Combine horizontal, vertical, and diagonal lines for a crosshatch effect.
    """
    c1 = random.choice(palette)
    c2 = random.choice(palette)
    c3 = random.choice(palette)
    # Horizontal lines
    for y in range(0, 16, 2):
        for x in range(16):
            draw.point((x, y), fill=c1)
    # Vertical lines
    for x in range(0, 16, 2):
        for y in range(16):
            draw.point((x, y), fill=c2)
    # Diagonal
    for i in range(16):
        draw.point((i, i), fill=c3)
        if 15 - i != i:
            draw.point((15 - i, i), fill=c3)

@register_pattern("stars")
def pattern_stars(draw, palette):
    """
    Random small 'star' shapes (a plus sign) in random colors.
    """
    for _ in range(10):
        x = random.randint(1, 14)
        y = random.randint(1, 14)
        c = random.choice(palette)
        draw.point((x, y), fill=c)
        draw.point((x-1, y), fill=c)
        draw.point((x+1, y), fill=c)
        draw.point((x, y-1), fill=c)
        draw.point((x, y+1), fill=c)

@register_pattern("barcode")
def pattern_barcode(draw, palette):
    """
    Vertical stripes of random width in random colors.
    """
    x = 0
    while x < 16:
        width = random.randint(1, 4)
        color = random.choice(palette)
        for cx in range(x, min(x+width, 16)):
            for y in range(16):
                draw.point((cx, y), fill=color)
        x += width

@register_pattern("plaid")
def pattern_plaid(draw, palette):
    """
    A rudimentary plaid: horizontal + vertical stripes in random palette colors.
    """
    # Fill everything with a base color
    base_color = palette[0]
    for y in range(16):
        for x in range(16):
            draw.point((x, y), fill=base_color)

    # Draw horizontal stripes
    for y in range(0, 16, 4):
        c = random.choice(palette)
        for x in range(16):
            draw.point((x, y), fill=c)
    # Draw vertical stripes
    for x in range(0, 16, 4):
        c = random.choice(palette)
        for y in range(16):
            draw.point((x, y), fill=c)

@register_pattern("circles_in_cells")
def pattern_circles_in_cells(draw, palette):
    """
    Divide the tile into 4x4 cells, draw small circles in each.
    """
    cidx = 0
    cell_size = 4
    for cy in range(4):
        for cx in range(4):
            color = palette[cidx % len(palette)]
            cidx += 1
            # center of cell
            center_x = cx*cell_size + cell_size//2
            center_y = cy*cell_size + cell_size//2
            radius = 1
            for angle_deg in range(360):
                import math
                angle = math.radians(angle_deg)
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                if 0 <= x < 16 and 0 <= y < 16:
                    draw.point((x, y), fill=color)

@register_pattern("diagonal_stripes_large")
def pattern_diagonal_stripes_large(draw, palette):
    """
    Wider diagonal stripes (4 px wide).
    """
    stripe_width = 4
    for x in range(16):
        for y in range(16):
            # Stripe index by integer division with stripe_width
            idx = ((x - y) // stripe_width) % len(palette)
            draw.point((x, y), fill=palette[idx])

@register_pattern("bricks")
def pattern_bricks(draw, palette):
    """
    Brick-like horizontal rows offset in a 'bricklaying' pattern.
    """
    brick_height = 4
    for y in range(0, 16, brick_height):
        offset = (y // brick_height) % 2
        for x in range(16):
            color = palette[((x // 4) + offset) % len(palette)]
            for row in range(brick_height):
                if y + row < 16:
                    draw.point((x, y + row), fill=color)

@register_pattern("stipple")
def pattern_stipple(draw, palette):
    """
    A stipple effect: each pixel is chosen by a threshold on random.
    """
    for y in range(16):
        for x in range(16):
            if random.random() < 0.5:
                draw.point((x, y), fill=random.choice(palette))

@register_pattern("honeycomb")
def pattern_honeycomb(draw, palette):
    """
    Simplified honeycomb pattern: hex-like rings.
    """
    cidx = 0
    for y in range(0, 16, 2):
        shift = (y // 2) % 2
        for x in range(0, 16, 3):
            color = palette[cidx % len(palette)]
            cidx += 1
            # center of hex cell
            cx = x + (1 if shift else 0)
            cy = y
            # draw a small hex ring
            coords = [
                (cx,   cy),
                (cx+1, cy+1),
                (cx+1, cy+2),
                (cx,   cy+3),
                (cx-1, cy+2),
                (cx-1, cy+1)
            ]
            for (px, py) in coords:
                if 0 <= px < 16 and 0 <= py < 16:
                    draw.point((px, py), fill=color)

@register_pattern("wave")
def pattern_wave(draw, palette):
    """
    Wave-like arcs across the tile.
    """
    for y in range(16):
        color = random.choice(palette)
        for x in range(16):
            import math
            # Use a sinusoidal wave
            wave_offset = int(2.0 * math.sin(x / 2.0))
            ty = (y + wave_offset) % 16
            draw.point((x, ty), fill=color)

@register_pattern("clouds_8bit")
def pattern_clouds_8bit(draw, palette):
    """
    Blocky 'clouds' effect. We'll fill random squares that drift horizontally.
    """
    for y_block in range(0, 16, 4):
        # random offset
        offset = random.randint(-2, 2)
        color = random.choice(palette)
        for x_block in range(0, 16, 4):
            for yy in range(y_block, y_block + 4):
                for xx in range(x_block, x_block + 4):
                    tx = (xx + offset) % 16
                    ty = yy % 16
                    draw.point((tx, ty), fill=color)


"""
Tessellations 
"""

@register_pattern("tessellated_mirror")
def pattern_tessellated_mirror(draw, palette):
    """
    Fill the top-left quadrant with random picks from the palette,
    then mirror it horizontally and vertically, ensuring the tile edges
    match seamlessly.
    
    This results in a 16x16 tile that "tessellates" or repeats seamlessly
    on both X and Y axes.
    """
    # Fill the top-left 8x8 region randomly
    quadrant = [[random.choice(palette) for _ in range(8)] for _ in range(8)]

    # Mirror horizontally for the top-right
    # Mirror vertically for the bottom row
    # Then place them all onto the tile
    for y in range(8):
        for x in range(8):
            # top-left
            draw.point((x, y), fill=quadrant[y][x])
            # top-right (mirror horizontally)
            draw.point((15 - x, y), fill=quadrant[y][x])
            # bottom-left (mirror vertically)
            draw.point((x, 15 - y), fill=quadrant[y][x])
            # bottom-right (mirror both)
            draw.point((15 - x, 15 - y), fill=quadrant[y][x])


@register_pattern("tileable_noise")
def pattern_tileable_noise(draw, palette):
    """
    A simple tileable noise approach:
      - We'll create random offsets in a 2D grid, but wrap at the edges
        to ensure the left and right edges match, top and bottom edges match.
      - Then we map the noise value to a color from the palette.
    
    This won't be "true Perlin" noise, but it's a quick demonstration of
    a tileable random pattern for seamless edges.
    """
    # We'll create a 16x16 array of random floats in [0,1) but ensure wrap.
    # Then we choose colors from palette based on that noise value.
    # For more advanced usage, you could implement or import real
    # "tileable Perlin or simplex noise."
    
    # 1) Generate a 17x17 "seed" so edges wrap (index 16 wraps to 0).
    #    We'll average corners to help continuity.
    noise_grid = [[random.random() for _ in range(17)] for _ in range(17)]

    # 2) Blend the final column/row with the start to ensure wrap
    for i in range(17):
        noise_grid[i][16] = noise_grid[i][0]   # wrap horizontally
        noise_grid[16][i] = noise_grid[0][i]   # wrap vertically
    # corner noise_grid[16][16] is same as noise_grid[0][0]

    # 3) Now fill each pixel by interpolating the noise.
    #    For simplicity, let's do no interpolation, just sample nearest:
    #    (x, y) in [0..15] => noise_grid[y][x].
    #    Then map that value to the palette.
    #    If you'd like smooth transitions, you could do bilinear interpolation,
    #    but let's keep it simple.
    # 4) Convert noise to color by dividing the noise range into len(palette) bands.
    palette_count = len(palette)
    step = 1.0 / float(palette_count)

    for y in range(16):
        for x in range(16):
            val = noise_grid[y][x]  # range [0,1)
            # figure out which color index
            idx = int(val / step)
            if idx >= palette_count:
                idx = palette_count - 1
            draw.point((x, y), fill=palette[idx])


@register_pattern("tessellated_stripes")
def pattern_tessellated_stripes(draw, palette):
    """
    Example of stripes that wrap seamlessly:
      - The top edge and bottom edge continue the stripes,
      - The left edge and right edge continue the stripes.
    """
    # Let's define a repeating stripe pattern that wraps both ways:
    stripe_width = 4  # each stripe is 4 px wide
    palette_count = len(palette)

    for y in range(16):
        for x in range(16):
            # We can define a "diagonal" approach that depends on (x + y).
            # Because we want wrap, let's do mod 16 on (x+y).
            idx = ((x + y) // stripe_width) % palette_count
            draw.point((x, y), fill=palette[idx])


@register_pattern("tileable_voronoi")
def pattern_tileable_voronoi(draw, palette):
    """
    A simple 'Voronoi-like' pattern that attempts to be tileable:
      - We place random points *in a 16x16 domain plus an overlapping margin*
        so that the domain wraps around.
      - For each pixel, we find the nearest random point, ignoring wrap or 
        considering wrap. We then color by the index of that nearest point mod palette length.
    
    This is computationally heavier (16x16 with nearest search),
    but can produce interesting 'cell-like' or 'patch-like' patterns that tile.
    """
    # Number of points
    num_points = 6
    # We'll store random points in an extended domain [-16..32, -16..32],
    # then map them "mod 16" so edges wrap. This is to approximate tileable Voronoi.
    points = []
    for _ in range(num_points):
        # place in [0..16) but let's also replicate them in margin
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        # We'll store them + extra offsets of 16 for wrap
        for dx in [0, 16, -16]:
            for dy in [0, 16, -16]:
                points.append((x + dx, y + dy))

    palette_count = len(palette)

    for y in range(16):
        for x in range(16):
            # Find nearest point
            nearest_dist2 = 999999
            nearest_index = 0
            for i, (px, py) in enumerate(points):
                dx = px - x
                dy = py - y
                dist2 = dx*dx + dy*dy
                if dist2 < nearest_dist2:
                    nearest_dist2 = dist2
                    nearest_index = i
            # The "original" random points were repeated 9 times (including offsets).
            # The real "index" is just nearest_index // 9 if we repeated 9 times each.
            # That ensures the color is consistent for the same point across margins.
            true_index = (nearest_index // 9) % palette_count
            draw.point((x, y), fill=palette[true_index])