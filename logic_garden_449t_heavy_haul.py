"""
PROJECT: Logic Garden 449t (Exact Physical Construct // Heavy Haul Assembly - HOTFIX)
FORMAT: YouTube Shorts (1080x1920)
METADATA: HEAVY HAUL, PETERBILT, LOWBOY, BULLDOZER, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute mechanical integration: Vehicles precisely tethered at 5th Wheel without intersection overlaps.
- Forward Alignment: Rig operates flawlessly travelling into +X. Wheels rotate forward.
- Hotfix: Resolved positional argument omission in dynamic wheel generator.
- Explicit Payload Masking: Dozer tracks authentically overhang the trailer drop bed.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, synchronisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_449t_heavy_haul"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)
C_WHEEL     = '#111115'          # Indestructible Black (Tyre Treads)

C_PETE_CAB  = '#005599'          # Deep Marine (Tractor Body)
C_CHROME    = '#94A3B8'          # Machined Steel (Grille, Stacks, Rims)
C_PETE_CHAS = '#1E293B'          # Carbon Slate (Tractor Rails)
C_LIGHTS    = '#E11D48'          # Kinematic Red (Tail Lights)
C_LABEL     = '#FFB300'          # Dense Amber (Typography)

C_TRL_BODY  = '#1E293B'          # Carbon Slate (Trailer Main Beams)
C_TRL_BED   = '#475569'          # Slate Grey (Drop Deck Crosshatch)

C_DOZ_BODY  = '#FFB300'          # Dense Amber (Dozer Hull)
C_DOZ_BLADE = '#1E293B'          # Carbon Slate (Root Rake)
C_DOZ_ROPS  = '#475569'          # Slate Grey (Protection Structure)
C_DOZ_TRACK = '#111115'          # Indestructible Black (Grouser Tracks)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs, off=(0,0,0), scale_x=1.0):
    dx, dy, dz = off
    for i in range(len(xs) - 1):
        x1 = xs[i] * scale_x + dx
        x2 = xs[i+1] * scale_x + dx
        lines_dict[key].append(([x1, x2], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

def rotate_y_pitch(x, y, z, cx, cz, pitch_deg):
    p = np.radians(pitch_deg)
    x0, z0 = x - cx, z - cz
    x1 = x0 * np.cos(p) - z0 * np.sin(p)
    z1 = x0 * np.sin(p) + z0 * np.cos(p)
    return x1 + cx, y, z1 + cz

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES WITH OFFSET/MIRROR PIPELINING
# ------------------------------------------------------------------
def extrude_profile(lines_dict, col, xz_points, y_min, y_max, off=(0,0,0), scale_x=1.0):
    xs = [p[0] for p in xz_points]; zs = [p[1] for p in xz_points]
    xs.append(xs[0]); zs.append(zs[0])
    append_segmented(lines_dict, col, xs, [y_min]*len(xs), zs, off, scale_x)
    append_segmented(lines_dict, col, xs, [y_max]*len(xs), zs, off, scale_x)
    for x, z in xz_points:
        append_segmented(lines_dict, col, [x, x], [y_min, y_max], [z, z], off, scale_x)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='y', rings=6, t_count=16, off=(0,0,0), scale_x=1.0):
    t = np.linspace(0, 2*np.pi, t_count)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off, scale_x)
    for a in t[::(t_count//8)]:
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off, scale_x)

def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz, off=(0,0,0), scale_x=1.0):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]; ys1 = [cy-hy]*2 + [cy+hy]*2 + [cy-hy]; ys2 = ys1[:]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5, off, scale_x)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5, off, scale_x)
    for i in range(4): append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz], off, scale_x)

def draw_vector_text(lines_dict, text, start_x, y_plane, start_z, height, w_char, spacing, col, flip, off=(0,0,0)):
    font = {
        'S': [[(1,1),(0,1),(0,0.5),(1,0.5),(1,0),(0,0)]], 'I': [[(0.5,1),(0.5,0)], [(0,1),(1,1)], [(0,0),(1,0)]],
        'M': [[(0,0),(0,1),(0.5,0.5),(1,1),(1,0)]], 'G': [[(1,1),(0,1),(0,0),(1,0),(1,0.5),(0.5,0.5)]],
        'A': [[(0,0),(0.5,1),(1,0)], [(0.25,0.5),(0.75,0.5)]], 'R': [[(0,0),(0,1),(1,1),(1,0.5),(0,0.5)], [(0,0.5),(1,0)]],
        'D': [[(0,0),(0,1),(0.7,1),(1,0.7),(1,0.3),(0.7,0),(0,0)]], 'E': [[(1,1),(0,1),(0,0),(1,0)], [(0,0.5),(0.8,0.5)]],
        'N': [[(0,0),(0,1),(1,0),(1,1)]], ' ': []
    }
    cur_x = start_x
    for c_char in text:
        for stroke in font.get(c_char, []):
            sx, sy, sz = [], [], []
            for px, pz in stroke:
                act_x = cur_x + ((1.0 - px) if flip else px) * w_char
                sx.append(act_x); sy.append(y_plane); sz.append(start_z + pz * height)
            # Text is parsed linearly into world-space independently to prevent mirror corruption
            append_segmented(lines_dict, col, sx, sy, sz, off, scale_x=1.0) 
        cur_x += (w_char + spacing) if not flip else -(w_char + spacing)

# ------------------------------------------------------------------
# KINEMATIC DYNAMIC WHEELS
# ------------------------------------------------------------------
def add_rotating_wheel(lines_dict, cx, cy, cz, radius, width, rot_angle, rim_rad=0.5, off=(0,0,0), scale_x=1.0):
    # If the vehicle faces +X (flipped negative), we subtract rot_angle so elements move toward +X
    t = np.linspace(0, 2*np.pi, 20) - rot_angle
    for y_off in [-width/2, width/2]:
        ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + y_off), cz + radius*np.sin(t)
        append_segmented(lines_dict, 'C_WHEEL', list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off, scale_x)
        ix_rim, iy_rim, iz_rim = cx + (radius*rim_rad)*np.cos(t), np.full_like(t, cy + y_off*1.05), cz + (radius*rim_rad)*np.sin(t)
        append_segmented(lines_dict, 'C_CHROME', list(ix_rim)+[ix_rim[0]], list(iy_rim)+[iy_rim[0]], list(iz_rim)+[iz_rim[0]], off, scale_x)
    for a in t[::2]:
        append_segmented(lines_dict, 'C_WHEEL', [cx+radius*np.cos(a)]*2, [cy-width/2, cy+width/2], [cz+radius*np.sin(a)]*2, off, scale_x)

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS
# ------------------------------------------------------------------
def generate_peterbilt_static(lines, off=(0,0,0)):
    # Flips Pete onto +X axis globally to merge naturally
    SX = -1.0 
    cw = 0.45; c_zt = 0.9; c_zb = 0.5; ch_xf = -8.0; ch_xr = 5.0
    for sign in [-1, 1]:
        append_segmented(lines, 'C_PETE_CHAS', [ch_xf, ch_xr], [cw*sign, cw*sign], [c_zt, c_zt], off, SX)
        append_segmented(lines, 'C_PETE_CHAS', [ch_xf, ch_xr], [cw*sign, cw*sign], [c_zb, c_zb], off, SX)
    append_segmented(lines, 'C_PETE_CHAS', [ch_xr]*2, [-cw, cw], [c_zt, c_zt], off, SX)
    append_segmented(lines, 'C_PETE_CHAS', [ch_xr]*2, [-cw, cw], [c_zb, c_zb], off, SX)
    for sign in [-1, 1]:
        append_segmented(lines, 'C_WHEEL', [ch_xr, ch_xr], [0.5*sign, 1.25*sign], [0.9, 0.9], off, SX)
        append_segmented(lines, 'C_WHEEL', [ch_xr, ch_xr], [0.5*sign, 1.25*sign], [0.1, 0.1], off, SX)
        append_segmented(lines, 'C_WHEEL', [ch_xr, ch_xr], [1.25*sign, 1.25*sign], [0.9, 0.1], off, SX)
    
    # 5th Wheel Plateau (Z=1.1m clears trailer kingpin height perfectly)
    cx_5th, w_5th, z_5th = 2.7, 0.55, c_zt
    add_box(lines, 'C_CHROME', cx_5th, 0.0, z_5th+0.1, 1.0, w_5th*2, 0.2, off, SX)
    append_segmented(lines, 'C_CHROME', [cx_5th+0.5, cx_5th+1.1, cx_5th+1.1, cx_5th+0.5, cx_5th+0.5], [-w_5th, -w_5th, -0.2, -0.2, -w_5th], [z_5th+0.2, z_5th-0.1, z_5th-0.1, z_5th+0.2, z_5th+0.2], off, SX)
    append_segmented(lines, 'C_CHROME', [cx_5th+0.5, cx_5th+1.1, cx_5th+1.1, cx_5th+0.5, cx_5th+0.5], [w_5th, w_5th, 0.2, 0.2, w_5th], [z_5th+0.2, z_5th-0.1, z_5th-0.1, z_5th+0.2, z_5th+0.2], off, SX)

    cab_w = 1.15; cab_xf = -4.2; cab_xr = -2.0; slp_xf = -1.8; slp_xr = 1.0
    cab_zb = 1.0; cab_zm = 1.9; cab_zt = 2.8
    for sign in [-1, 1]:
        y = cab_w * sign
        append_segmented(lines, 'C_PETE_CAB', [cab_xr, cab_xf, cab_xf, cab_xr, cab_xr], [y]*5, [cab_zb, cab_zb, cab_zm, cab_zm, cab_zb], off, SX)
        append_segmented(lines, 'C_PETE_CAB', [cab_xr, cab_xf+0.1, cab_xf+0.1, cab_xr, cab_xr], [y]*5, [cab_zm, cab_zm, cab_zt, cab_zt, cab_zm], off, SX)
        append_segmented(lines, 'C_PETE_CAB', [slp_xr, slp_xf, slp_xf, slp_xr, slp_xr], [y]*5, [cab_zb, cab_zb, cab_zt, cab_zt, cab_zb], off, SX)
        add_cylinder(lines, 'C_CHROME', cab_xf, 1.1*sign, 1.4, length=0.85, radius=0.25, axis='z', rings=5, off=off, scale_x=SX)
    
    for x, z in [(cab_xf, cab_zm), (cab_xf+0.1, cab_zt), (cab_xr, cab_zt), (slp_xf, cab_zt), (slp_xr, cab_zt), (slp_xr, cab_zb)]:
        append_segmented(lines, 'C_PETE_CAB', [x, x], [-cab_w, cab_w], [z, z], off, SX)
        
    hood_xf, hood_w, hood_zt = -7.6, 0.85, 1.7
    for sign in [-1, 1]:
        y = hood_w * sign
        append_segmented(lines, 'C_PETE_CAB', [cab_xf, hood_xf], [y, y], [hood_zt, hood_zt], off, SX)
        append_segmented(lines, 'C_PETE_CAB', [cab_xf, hood_xf], [y, y], [cab_zb, cab_zb], off, SX)
        append_segmented(lines, 'C_PETE_CAB', [hood_xf, hood_xf], [y, y], [cab_zb, hood_zt], off, SX)
    append_segmented(lines, 'C_PETE_CAB', [hood_xf, hood_xf], [-hood_w, hood_w], [hood_zt, hood_zt], off, SX)
    append_segmented(lines, 'C_PETE_CAB', [cab_xf, hood_xf], [0, 0], [hood_zt, hood_zt], off, SX)
    add_box(lines, 'C_CHROME', hood_xf-0.1, 0.0, 0.6, dx=0.3, dy=2.4, dz=0.4, off=off, scale_x=SX)

    for sign in [-1, 1]:
        add_cylinder(lines, 'C_CHROME', -1.9, 1.25*sign, 0.9, 3.5, 0.15, axis='z', rings=10, off=off, scale_x=SX)
        add_cylinder(lines, 'C_CHROME', -3.7, 1.15*sign, 0.65, 3.6, 0.35, axis='x', rings=12, off=off, scale_x=SX)
        add_cylinder(lines, 'C_PETE_CHAS', -3.2, 1.15*sign, 0.65, 0.05, 0.36, axis='x', rings=2, off=off, scale_x=SX)

    xf_pts = np.linspace(-7.6, -4.2, 35)
    zf_pts = [0.52 + np.sqrt(max(0.001, 1.0**2 - (x - -6.4)**2)) * 0.8 if x < -6.4 else 
              (0.52 + np.sqrt(max(0.001, 1.0**2 - (x - -6.4)**2)) * 0.8)*(1-(x+6.4)) + 0.9*(x+6.4) if x < -5.4 else 0.9 for x in xf_pts]
    for sign in [-1, 1]:
        append_segmented(lines, 'C_PETE_CAB', list(xf_pts), list(np.full_like(xf_pts, hood_w*sign)), list(zf_pts), off, SX)
        append_segmented(lines, 'C_PETE_CAB', list(xf_pts), list(np.full_like(xf_pts, 1.25*sign)), list(zf_pts), off, SX)
        for i in range(len(xf_pts)): append_segmented(lines, 'C_PETE_CAB', [xf_pts[i]]*2, [hood_w*sign, 1.25*sign], [zf_pts[i]]*2, off, SX)

    # Typographic Overlay. Mapped explicitly on the Z/Y planes with X traversing dynamically
    draw_vector_text(lines, "SIM", -0.5, cab_w+0.05, 2.2, 0.3, 0.2, 0.06, 'C_LABEL', False, off)
    draw_vector_text(lines, "GARDEN", 0.4, cab_w+0.05, 1.7, 0.3, 0.2, 0.06, 'C_LABEL', False, off)
    draw_vector_text(lines, "SIM", 1.5, -cab_w-0.05, 2.2, 0.3, 0.2, 0.06, 'C_LABEL', True, off)
    draw_vector_text(lines, "GARDEN", 0.6, -cab_w-0.05, 1.7, 0.3, 0.2, 0.06, 'C_LABEL', True, off)


def generate_trailer_static(lines, off=(-10.2, 0, 0)):
    # Standardised width and alignment matching parameter requirements natively
    SX = -1.0
    w = 1.275; gn_front = -7.8; gn_rear = -4.7; gn_z_floor = 1.35; gn_z_roof = 1.6
    lines['C_TRL_BODY'].append(([gn_front, gn_rear, gn_rear, gn_front, gn_front], [-w, -w, w, w, -w], [gn_z_floor]*5))
    lines['C_TRL_BODY'].append(([gn_front, gn_rear, gn_rear, gn_front, gn_front], [-w, -w, w, w, -w], [gn_z_roof]*5))
    
    # Heavy 1.15m anchor Kingpin (sits comfortably above Peterbilt 1.10m plates)
    append_segmented(lines, 'C_CHROME', [-7.5, -7.5], [0, 0], [1.15, gn_z_floor], off, SX) 
    append_segmented(lines, 'C_CHROME', [-7.6, -7.4, -7.4, -7.6, -7.6], [-0.1, -0.1, 0.1, 0.1, -0.1], [1.15]*5, off, SX)
    
    # Gooseneck hydraulic towers relocated inside bounds
    for cx in [-7.2, -6.8]: 
        for iy in [-0.8, 0.8]: 
            append_segmented(lines, 'C_CHROME', [cx]*2, [iy]*2, [gn_z_roof, gn_z_roof+0.8], off, SX)
    
    tk_rear, tk_zb = -3.5, 0.4
    db_rear, z_bed = 3.5, tk_zb + 0.18
    for y_sign in [-1, 1]:
        append_segmented(lines, 'C_TRL_BODY', [gn_rear, tk_rear], [w*y_sign]*2, [gn_z_roof, z_bed], off, SX)
        append_segmented(lines, 'C_TRL_BODY', [gn_rear, tk_rear], [w*y_sign]*2, [gn_z_floor, tk_zb], off, SX)
        
    append_segmented(lines, 'C_TRL_BODY', [tk_rear, db_rear, db_rear, tk_rear, tk_rear], [-w, -w, w, w, -w], [tk_zb]*5, off, SX)
    append_segmented(lines, 'C_TRL_BODY', [tk_rear, db_rear, db_rear, tk_rear, tk_rear], [-w, -w, w, w, -w], [z_bed]*5, off, SX)
    for bx in np.linspace(tk_rear, db_rear, 20):
        append_segmented(lines, 'C_TRL_BED', [bx, bx], [-w, w], [z_bed, z_bed], off, SX)
        
    rb_front, z_bogie = 4.5, 1.05
    for y_sign in [-1, 1]:
        append_segmented(lines, 'C_TRL_BODY', [db_rear, rb_front], [w*y_sign]*2, [z_bed, z_bogie], off, SX)
        append_segmented(lines, 'C_TRL_BODY', [db_rear, rb_front], [w*y_sign]*2, [tk_zb, z_bogie-0.18], off, SX)
        
    bogie_rear, z_b_bot = 8.0, z_bogie - 0.18
    append_segmented(lines, 'C_TRL_BODY', [rb_front, bogie_rear, bogie_rear, rb_front, rb_front], [-w, -w, w, w, -w], [z_bogie]*5, off, SX)
    append_segmented(lines, 'C_TRL_BODY', [rb_front, bogie_rear, bogie_rear, rb_front, rb_front], [-w, -w, w, w, -w], [z_b_bot]*5, off, SX)
    
    # Ramps Stowed Vertical (90 deg upright deployment configuration)
    hx = bogie_rear; hz = z_bogie; rp = 90.0
    for sign in [-1, 1]:
        ry_center = w - 0.1 - 0.4
        ry_min, ry_max = ry_center - 0.4, ry_center + 0.4
        for s1, s2 in zip(np.linspace(0, 3.5, 8)[:-1], np.linspace(0, 3.5, 8)[1:]):
            x1t, _, z1t = rotate_y_pitch(hx+s1, ry_min, hz, hx, hz, rp)
            x2t, _, z2t = rotate_y_pitch(hx+s2, ry_min, hz, hx, hz, rp)
            x1ti, _, _ = rotate_y_pitch(hx+s1, ry_max, hz, hx, hz, rp)
            x2ti, _, _ = rotate_y_pitch(hx+s2, ry_max, hz, hx, hz, rp)
            append_segmented(lines, 'C_CHROME', [x1t, x2t, x2ti, x1ti, x1t], [ry_min*sign, ry_min*sign, ry_max*sign, ry_max*sign, ry_min*sign], [z1t, z2t, z2t, z1t, z1t], off, SX)
            x1b, _, z1b = rotate_y_pitch(hx+s1, ry_min, hz-0.15, hx, hz, rp)
            x2b, _, z2b = rotate_y_pitch(hx+s2, ry_min, hz-0.15, hx, hz, rp)
            append_segmented(lines, 'C_CHROME', [x1t, x1b], [ry_min*sign]*2, [z1t, z1b], off, SX)


def generate_dozer_static(lines, off=(-10.2, 0, 0.58)):
    # Tracks Oval securely locked into trailer drop-deck bounds matching scale payload requirements
    for t_y in [-1.45, 1.45]: # 0.5m overhang exactly mirrors actual engineering geometry
        rx = -1.6 + 0.5 * np.cos(np.linspace(np.pi/2, 3*np.pi/2, 12))
        rz =  0.6 + 0.5 * np.sin(np.linspace(np.pi/2, 3*np.pi/2, 12))
        bx = np.linspace(-1.6, 2.0, 15); bz = np.linspace(0.1, 0.1, 15)
        fx =  2.0 + 0.4 * np.cos(np.linspace(-np.pi/2, np.pi/2, 12))
        fz =  0.5 + 0.4 * np.sin(np.linspace(-np.pi/2, np.pi/2, 12))
        tx = np.linspace(2.0, -1.6, 15); tz = np.linspace(0.9, 1.1, 15)
        px = list(rx) + list(bx[1:]) + list(fx[1:]) + list(tx[1:])
        pz = list(rz) + list(bz[1:]) + list(fz[1:]) + list(tz[1:])
        tw = 0.35
        append_segmented(lines, 'C_DOZ_TRACK', px, [t_y - tw]*len(px), pz, off)
        append_segmented(lines, 'C_DOZ_TRACK', px, [t_y + tw]*len(px), pz, off)
        add_cylinder(lines, 'C_DOZ_TRACK', -1.6, t_y-0.2, 0.6, 0.4, 0.45, off=off)
        add_cylinder(lines, 'C_DOZ_TRACK',  2.0, t_y-0.2, 0.5, 0.4, 0.35, off=off)
        t_len = 45
        g_x = np.interp(np.linspace(0, len(px)-1, t_len), np.arange(len(px)), px)
        g_z = np.interp(np.linspace(0, len(px)-1, t_len), np.arange(len(px)), pz)
        for gx, gz in zip(g_x, g_z):
            append_segmented(lines, 'C_DOZ_TRACK', [gx, gx], [t_y - tw, t_y + tw], [gz, gz], off)
            append_segmented(lines, 'C_DOZ_TRACK', [gx, gx+0.05], [t_y - tw, t_y - tw], [gz, gz+0.05], off)

    add_box(lines, 'C_DOZ_BODY', 0.2, 0.0, 0.9, 4.0, 1.8, 0.8, off)
    extrude_profile(lines, 'C_DOZ_BODY', [(0.2, 1.3), (2.0, 1.3), (2.4, 1.2), (2.4, 1.8), (0.2, 2.0)], -0.7, 0.7, off)
    add_box(lines, 'C_DOZ_BODY', -1.2, 0.0, 1.6, 1.6, 1.7, 0.6, off)

    extrude_profile(lines, 'C_DOZ_ROPS', [(-1.3, 1.9), (0.2, 1.9), (0.2, 2.9), (-1.3, 2.9)], -0.8, 0.8, off)
    rx1, rx2, ry, rz1, rz2 = -1.5, 0.4, 0.9, 1.9, 3.1
    add_box(lines, 'C_DOZ_ROPS', (rx1+rx2)/2, 0.0, rz2, (rx2-rx1), ry*2, 0.1, off)
    for yp in [-ry, ry]:
        append_segmented(lines, 'C_DOZ_ROPS', [rx1, rx1], [yp, yp], [rz1, rz2], off)
        append_segmented(lines, 'C_DOZ_ROPS', [rx2, rx2], [yp, yp], [rz1, rz2], off)

    for sign in [-1, 1]:
        extrude_profile(lines, 'C_DOZ_BLADE', [(-1.0, 0.7), (2.8, 0.5), (3.0, 0.8), (2.8, 1.0), (-1.0, 0.9)], (1.6*sign)-0.1, (1.6*sign)+0.1, off)
        add_cylinder(lines, 'C_DOZ_BLADE', -1.0, 1.2*sign, 0.8, 0.4, 0.2, off=off)
        append_segmented(lines, 'C_CHROME', [0.8, 1.8], [0.8*sign, 1.2*sign], [2.0, 1.35], off)
        append_segmented(lines, 'C_CHROME', [1.8, 2.8], [1.2*sign, 1.6*sign], [1.4, 0.7], off)
        
    add_box(lines, 'C_DOZ_BLADE', 3.0, 0.0, 1.5, 0.2, 4.0, 0.2, off)
    add_box(lines, 'C_DOZ_BLADE', 2.9, 0.0, 0.6, 0.3, 4.0, 0.3, off)
    for sy in np.linspace(-1.9, 1.9, 11):
        extrude_profile(lines, 'C_DOZ_BLADE', [(2.9, 1.8), (3.0, 0.9), (3.3, 0.3), (3.6, 0.0), (3.4, 0.3), (3.2, 0.9), (3.1, 1.8)], sy-0.06, sy+0.06, off)

# ------------------------------------------------------------------
# PARALLEL GENERATOR DYNAMIC (WHEELS ROTATING FORWARD INTO +X)
# ------------------------------------------------------------------
def generate_dynamic_wheels(lines, rot_tract, rot_trail):
    # Wheels must run inversely across the array scale to spin backwards into the screen, matching +X momentum
    w_rot_t = -rot_tract
    w_rot_tr = -rot_trail
    SX, O_TRL = -1.0, (-10.2, 0, 0)
    
    # Tractor Wheels (Includes radius in positional args)
    for cx_steer in [-6.4]:
        for sign in [-1, 1]: 
            add_rotating_wheel(lines, cx_steer, 1.15*sign, 0.52, 0.52, 0.45, w_rot_t, rim_rad=0.5, off=(0,0,0), scale_x=SX)
    for dr_x in [2.0, 3.4]:
        for sign in [-1, 1]:
            add_rotating_wheel(lines, dr_x, 1.15*sign, 0.52, 0.52, 0.45, w_rot_t, rim_rad=0.5, off=(0,0,0), scale_x=SX)
            add_rotating_wheel(lines, dr_x, 0.65*sign, 0.52, 0.52, 0.45, w_rot_t, rim_rad=0.5, off=(0,0,0), scale_x=SX)
            
    # Trailer Wheels 
    for ax_x in [5.1, 6.4, 7.7]:
        for sign in [-1, 1]:
            add_rotating_wheel(lines, ax_x, 1.05*sign, 0.45, 0.45, 0.38, w_rot_tr, rim_rad=0.6, off=O_TRL, scale_x=SX)
            add_rotating_wheel(lines, ax_x, 0.55*sign, 0.45, 0.45, 0.38, w_rot_tr, rim_rad=0.6, off=O_TRL, scale_x=SX)

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    # Execute extreme macro-structure logic trace ONCE for O(1) loop speed
    static_rig = {'C_GRID': [], 'C_PETE_CAB': [], 'C_CHROME': [], 'C_PETE_CHAS': [], 'C_WHEEL': [], 'C_LABEL': [], 'C_LIGHTS': [],
                  'C_TRL_BODY': [], 'C_TRL_BED': [], 'C_DOZ_BODY': [], 'C_DOZ_BLADE': [], 'C_DOZ_ROPS': [], 'C_DOZ_TRACK': []}
                  
    gx_range = np.linspace(-25, 12, 38)
    gy_range = np.linspace(-3, 3, 13)
    for gx in gx_range: append_segmented(static_rig, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -3, 3), np.zeros_like(gx_range))
    for gy in gy_range: append_segmented(static_rig, 'C_GRID', np.clip(gx_range, -25, 12), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    generate_peterbilt_static(static_rig, off=(0,0,0))
    generate_trailer_static(static_rig, off=(-10.2,0,0))
    generate_dozer_static(static_rig, off=(-10.2,0,0.58)) 

    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = -5.0, 0.0, 2.5 
        
        # 0 Azimuth accurately maps the absolute right-side bounding profile in the painter array.
        azimuth = 0.0 + (stage * 360.0)

        rot_tract = stage * 12.0 * 2.0 * np.pi
        rot_trail = stage * 14.0 * 2.0 * np.pi

        yield (f, t_sec, azimuth, rot_tract, rot_trail, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, r_tract, r_trail, cx, cy, cz, static_rig = packet

    # Substrate generation isolated safely per core 
    local_rig = {k: v.copy() for k,v in static_rig.items()}
    generate_dynamic_wheels(local_rig, r_tract, r_trail)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    cam_span = 14.8
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID', C_GRID, 0.8, 0.4), ('C_WHEEL', C_WHEEL, 1.4, 1.0),
        ('C_PETE_CHAS', C_PETE_CHAS, 1.2, 1.0), ('C_PETE_CAB', C_PETE_CAB, 1.5, 1.0),
        ('C_CHROME', C_CHROME, 1.4, 1.0), ('C_LABEL', C_LABEL, 3.5, 1.0), ('C_LIGHTS', C_LIGHTS, 2.5, 1.0),
        ('C_TRL_BODY', C_TRL_BODY, 1.4, 1.0), ('C_TRL_BED', C_TRL_BED, 1.1, 1.0),
        ('C_DOZ_TRACK', C_DOZ_TRACK, 1.3, 1.0), ('C_DOZ_BODY', C_DOZ_BODY, 1.5, 1.0), 
        ('C_DOZ_BLADE', C_DOZ_BLADE, 1.4, 1.0), ('C_DOZ_ROPS', C_DOZ_ROPS, 1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in local_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=15.0)
            render_queue.append((np.mean(depth), u, v-1.5, c_val, lw, alpha))

    # ABSOLUTE Z-SORT
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 6.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.5, "LG-449t // MACRO-ENGINEERING TENSOR: HEAVY INDUSTRY KINEMATICS", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // TRIPLE MATRIX INTEGRATION", color=C_PETE_CAB, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+3.2, "[OPERATIONAL] CONTINUOUS TREAD VELOCITY SYNCHRONISATION", color=C_DOZ_BODY, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+2.0, f"CAMERA AZIMUTH    : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.8, "TRACTOR / TRAILER : VELOCITY LINKED ORBITAL ROTATION (FORWARD)", color=C_CHROME, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449t: INDUSTRIAL HEAVY HAUL KINEMATICS [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Triple-Matrix Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
