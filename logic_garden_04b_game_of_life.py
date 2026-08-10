"""
PROJECT: Logic Garden 04b (Game of Life // Biokinetic Hardware Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CELLULAR AUTOMATA, DETERMINISM, EMERGENT GEOMETRY, CONWAYS GAME OF LIFE
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast Vibrant Geometry).
- Biological Phase-Locked Metaphor: Cells are born bright, mature into structure, and dissolve on death.
- Toroidal wrapping for absolute continuity.
- Australian spelling conventions enforced natively (Maths, Optimisation, Colour).
- Exact realisational aspect of machined blocks spanning an age matrix.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_04b_game_of_life"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BIOKINETIC PALETTE --------
C_BG            = '#FFFFFF'  # Pure Void
C_TEXT          = '#111115'
C_EDGE          = '#111115'  # Indestructible Black Bounds
C_NEWBORN       = '#FFD700'  # Cyber Yellow (Explosive Birth)
C_SURVIVOR      = '#0080FF'  # Azure Blue (Stable Biological Structure)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.8, -0.6])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(N) CELLULAR AUTOMATA ENGINE (WITH AGE MATRIX)
# ------------------------------------------------------------------
GRID_X = 40
GRID_Y = 70
TICKS_PER_SEC = 5.0
TOTAL_TICKS = int(DURATION * TICKS_PER_SEC) + 2

# Global state array memory matrices
G_STATES = np.zeros((TOTAL_TICKS, GRID_Y, GRID_X), dtype=np.int8)
G_AGES   = np.zeros((TOTAL_TICKS, GRID_Y, GRID_X), dtype=np.int32)

def pre_compute_automaton():
    print("PHASE 1: PRE-COMPUTING BIOKINETIC CHAOS MATRIX...")
    # Seed 42 for a highly active "soup"
    np.random.seed(42)
    current_grid = np.random.choice([0, 1], size=(GRID_Y, GRID_X), p=[0.75, 0.25])
    current_ages = np.zeros((GRID_Y, GRID_X), dtype=np.int32)
    
    G_STATES[0] = current_grid
    G_AGES[0] = current_ages
    
    # Exact Toroidal Conway Maths
    for t_step in range(1, TOTAL_TICKS):
        neighbors = (
            np.roll(current_grid, 1, axis=0) + np.roll(current_grid, -1, axis=0) +
            np.roll(current_grid, 1, axis=1) + np.roll(current_grid, -1, axis=1) +
            np.roll(np.roll(current_grid, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(current_grid, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(current_grid, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(current_grid, -1, axis=0), -1, axis=1)
        )
        
        # Conway's Rules of Optimisation
        birth = (current_grid == 0) & (neighbors == 3)
        survive = (current_grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        next_grid = np.zeros((GRID_Y, GRID_X), dtype=np.int8)
        next_ages = np.zeros((GRID_Y, GRID_X), dtype=np.int32)
        
        next_grid[birth | survive] = 1
        
        # Age progression
        next_ages[survive] = current_ages[survive] + 1
        next_ages[birth] = 0
        
        G_STATES[t_step] = next_grid
        G_AGES[t_step] = next_ages
        
        current_grid = next_grid
        current_ages = next_ages

    print(f"AUTOMATON COMPILED: {TOTAL_TICKS} Kinematic Epochs Extracted.")

# ------------------------------------------------------------------
# 3D PHYSICAL BLOCK GENERATOR
# ------------------------------------------------------------------
SPACING = 20.0
BLOCK_SIZE = 18.0 # Generates exactly 2.0 units of mechanical clearance
MAX_H = 45.0 # Taller extrusion to make the architecture pop

def get_base_faces():
    sz = BLOCK_SIZE / 2.0
    v = np.array([
        [-sz, -sz, 0], [ sz, -sz, 0], [ sz,  sz, 0], [-sz,  sz, 0], 
        [-sz, -sz, 1], [ sz, -sz, 1], [ sz,  sz, 1], [-sz,  sz, 1]  
    ])
    faces = [
        [v[0], v[1], v[5], v[4]], # Front
        [v[1], v[2], v[6], v[5]], # Right
        [v[2], v[3], v[7], v[6]], # Back
        [v[3], v[0], v[4], v[7]], # Left
        [v[4], v[5], v[6], v[7]], # Top
    ]
    # Slicing the 4-vertex quads into strict triangulated 3-vertex matrices
    tri_faces = []
    for f in faces:
        tri_faces.append([f[0], f[1], f[3]])
        tri_faces.append([f[1], f[2], f[3]])
    return np.array(tri_faces)

BASE_POLYS = get_base_faces()

# ------------------------------------------------------------------
# KINEMATIC MATH ENGINES
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def rz(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def ease_out_cubic(t):
    return 1 - (1 - t)**3

def rgb(hex_code):
    return np.array(mcolors.to_rgb(hex_code))

def mix(color_a, color_b, t):
    t_arr = np.clip(t, 0.0, 1.0)
    return color_a * (1.0 - t_arr) + color_b * t_arr

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    current_tick = int(t_sec * TICKS_PER_SEC)
    sub_tick = (t_sec * TICKS_PER_SEC) % 1.0
    
    kinematic_prog = ease_out_cubic(np.clip(sub_tick / 0.7, 0.0, 1.0))
    
    state_0 = G_STATES[current_tick]
    state_1 = G_STATES[min(current_tick + 1, TOTAL_TICKS - 1)]
    ages_0  = G_AGES[current_tick]

    # Pre-load base colours
    c_new = rgb(C_NEWBORN)
    c_sur = rgb(C_SURVIVOR)
    c_bg  = rgb(C_BG)

    active_polys = []
    active_colors = []
    total_alive_current = 0

    # Matrix Construction
    for y in range(GRID_Y):
        for x in range(GRID_X):
            s0 = state_0[y, x]
            s1 = state_1[y, x]
            
            if s0 == 0 and s1 == 0:
                continue
                
            cur_z = 0.0
            cur_color = c_bg
            
            if s0 == 0 and s1 == 1:
                # BIRTH: Erupts from void, transitioning White to Cyber Yellow
                cur_z = MAX_H * kinematic_prog
                cur_color = mix(c_bg, c_new, kinematic_prog)
                total_alive_current += 1
                
            elif s0 == 1 and s1 == 1:
                cur_z = MAX_H
                total_alive_current += 1
                if ages_0[y, x] == 0:
                    # MATURATION: Transforms from Cyber Yellow into Azure Blue
                    cur_color = mix(c_new, c_sur, kinematic_prog)
                else:
                    # STABLE ADULT: Deep, flawless Azure
                    cur_color = c_sur
                    
            elif s0 == 1 and s1 == 0:
                # DEATH: Smoothly dissolves back into the White void
                cur_z = MAX_H * (1.0 - kinematic_prog)
                origin_col = c_new if ages_0[y, x] == 0 else c_sur
                cur_color = mix(origin_col, c_bg, kinematic_prog)
                
            if cur_z < 0.5: continue
            
            cx = (x * SPACING) - ((GRID_X * SPACING) / 2.0)
            cy = (y * SPACING) - ((GRID_Y * SPACING) / 2.0)
            
            scaled_polys = BASE_POLYS.copy()
            scaled_polys[:, :, 2] *= cur_z 
            translated_polys = scaled_polys + np.array([cx, cy, 0])
            
            active_polys.extend(translated_polys)
            active_colors.extend([cur_color] * len(BASE_POLYS))

    # Master Camera Optics
    cam_hz = 15.0 + (t_sec * 2.0) 
    cam_pitch = -42.0 
    
    M_base = np.array([[1,0,0],[0,0,1],[0,1,0]])
    M_cam = rx(cam_pitch) @ rz(cam_hz) @ M_base

    cam_dist = 2000.0
    c_x, c_y, c_z = 0.0, 0.0, cam_dist

    if len(active_polys) > 0:
        M_ALL = np.array(active_polys)
        C_ALL = np.array(active_colors)

        def get_world_to_cam(polys):
            p_flat = polys.reshape(-1, 3)
            v_world = np.vstack((p_flat[:,0] - c_x, p_flat[:,1] - c_y, p_flat[:,2]))
            v_cam = M_cam @ v_world
            p_cam = v_cam.T.reshape(-1, 3, 3)
            return p_cam

        cam_polys = get_world_to_cam(M_ALL)
        
        centroids_z = np.mean(cam_polys[:, :, 2], axis=1)
        
        v1_edge = cam_polys[:, 1, :] - cam_polys[:, 0, :]
        v2_edge = cam_polys[:, 2, :] - cam_polys[:, 0, :]
        norms = np.cross(v1_edge, v2_edge)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        v_mask = norms[:, 2] > 0
        
        c_polys = cam_polys[v_mask]
        C_ALL = C_ALL[v_mask]
        c_centroids = centroids_z[v_mask]
        c_norms = norms[v_mask]

        if len(c_polys) > 0:
            diff = 0.35 + 0.65 * np.abs(np.dot(c_norms, LIGHT_DIR))
            
            final_rgba = np.zeros((len(c_polys), 4))
            final_rgba[:, :3] = C_ALL * diff[:, np.newaxis]
            final_rgba[:, 3] = 1.0

            z_safe = np.maximum(c_polys[:, :, 2] + cam_dist, 1.0)
            proj_x = 2200.0 * (c_polys[:, :, 0] / z_safe)
            proj_y = 2200.0 * (c_polys[:, :, 1] / z_safe) + 120
            proj_polys = np.stack((proj_x, proj_y), axis=-1)

            sort_idx = np.argsort(c_centroids)[::-1]

            # High-Contrast thick borders inject the pop effect natively
            col = PolyCollection(proj_polys[sort_idx], facecolors=final_rgba[sort_idx], edgecolors=C_EDGE, linewidths=1.0, joinstyle='miter', zorder=10)
            ax.add_collection(col)

    # 4. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [750, 750], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 890, "LG-04b :: THE DETERMINISTIC AUTOMATON", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-1.00] O(N) KINEMATIC EMERGENCE // CONWAY ALGORITHM", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    epoch_state = "MATHEMATICAL BIOLOGY GENERATING COMPLEX INFRASTRUCTURE"
    ax.text(-500, -780, f"PROTOCOL PHASE   : EMERGENT COMPLEXITY", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"ALGORITHMIC YIELD: T={current_tick:04d} // {total_alive_current:04d} ACTIVE BIOLOGICAL NODES", color=C_NEWBORN, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH  : {epoch_state}", color=C_SURVIVOR, fontsize=12, fontname='monospace', zorder=82)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    pre_compute_automaton()
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-04b: BIOKINETIC MATRIX [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. True emergent life generated.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
