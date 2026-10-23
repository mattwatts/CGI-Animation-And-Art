"""
PROJECT: Logic Garden 408 (Numerical Relativity Tensor // Rogue Black Hole)
FORMAT: YouTube Shorts (1080x1920)
METADATA: NUMERICAL RELATIVITY, BLACK HOLE MERGER, GRAVITATIONAL KICK, ROGUE BLACK HOLE
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Gravity as explicit volumetric mesh deformation.
- Exact realisational aspect of Anisotropic Gravitational Waves and Recoil.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) Painter's Algorithm with Lambertian shading.
- HOTFIX: Strict mathematical clamp applied to chromatic anisotropy.
- HOTFIX: Spacetime substrate luminance jacked for absolute Event Horizon contrast.
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
OUT_DIR = "frames_408_rogue_bh"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_BH            = '#111115'  # Indestructible Black (Event Horizon)
C_FLAT_SPACE    = '#F8FAFC'  # Ultra-Bright Daylight Substrate (Maximum Contrast)
C_DEPTH         = '#00D2FF'  # High-Contrast Cyan (Gravity Well)
C_ENERGY        = '#DE008A'  # Deep Magenta (Gravitational Burst)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 3D ARCHITECTURAL GRID GENERATOR
# ------------------------------------------------------------------
GRID_SIZE = 1000.0
RES = 90  # 90x90 mapping equates to 8,100 polygon matrix
X_LN = np.linspace(-GRID_SIZE/2, GRID_SIZE/2, RES)
Y_LN = np.linspace(-GRID_SIZE/2, GRID_SIZE/2, RES)
X_GRID, Y_GRID = np.meshgrid(X_LN, Y_LN)

# Physics Variables
M1 = 2000.0  # Primary Mass
M2 = 1200.0  # Secondary Mass (Asymmetric to force the kick)
T_MERGE = 12.0
M_REMNANT = (M1 + M2) * 0.92  # 8% pure mass-energy conversion
KICK_VELOCITY = 180.0  # Representation of ~4000 km/s scaling
KICK_ANGLE = np.radians(45.0)

print(f"PHASE 1: SPACETIME TENSOR PRE-COMPILED [{RES*RES} NODES]")

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def rz(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def lerp_colour(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    return c1 * (1 - t) + c2 * t

def ease_out(t): 
    return np.clip(1.0 - (1.0 - np.clip(t, 0.0, 1.0))**3, 0.0, 1.0)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC CAMERA TENSOR
    M_cam = rx(-40.0) @ rz(np.radians(-30.0 + t_sec * 0.5)) # Slow orbital dolly track
    cam_dist = 1100.0 
    
    # 2. NUMERICAL RELATIVITY KINEMATICS
    bh_positions = []
    
    if t_sec < T_MERGE:
        # Phase 1: Inspiral
        # Frequency and radius driven by (T_m - t) decay algorithms
        time_left = T_MERGE - t_sec
        r_sep = 35.0 + 150.0 * (max(0.01, time_left / T_MERGE))**0.4
        theta = 50.0 * (1.0 - (max(0.01, time_left / T_MERGE))**0.6)
        
        # Barycenter math (Asymmetric orbiting)
        r1 = r_sep * (M2 / (M1 + M2))
        r2 = r_sep * (M1 / (M1 + M2))
        
        x1, y1 = r1 * np.cos(theta), r1 * np.sin(theta)
        x2, y2 = -r2 * np.cos(theta), -r2 * np.sin(theta)
        
        # Determine exact mesh deformation Z(x, y)
        d1 = np.sqrt((X_GRID - x1)**2 + (Y_GRID - y1)**2 + 80.0)
        d2 = np.sqrt((X_GRID - x2)**2 + (Y_GRID - y2)**2 + 60.0)
        Z_GRID = - (M1 / d1) - (M2 / d2)
        
        bh_positions = [(x1, y1, -M1/np.sqrt(80.0) - M2/np.sqrt((x1-x2)**2 + (y1-y2)**2 + 60.0), 32.0),
                        (x2, y2, -M2/np.sqrt(60.0) - M1/np.sqrt((x2-x1)**2 + (y2-y1)**2 + 80.0), 24.0)]
        
        energy_burst = 0.0
    else:
        # Phase 2 & 3: Merger & Rogue Recoil
        dt = t_sec - T_MERGE
        
        # Kick vector computation
        vx = KICK_VELOCITY * np.cos(KICK_ANGLE)
        vy = KICK_VELOCITY * np.sin(KICK_ANGLE)
        
        x_m = vx * dt
        y_m = vy * dt
        
        # Evaluate remnant deformation
        d3 = np.sqrt((X_GRID - x_m)**2 + (Y_GRID - y_m)**2 + 100.0)
        Z_GRID = - (M_REMNANT / d3)
        
        bh_positions = [(x_m, y_m, -M_REMNANT/np.sqrt(100.0), 40.0)]
        
        # 8% Mass-Energy Gravitational Wave Burst
        # Wave propagation speed across the mesh
        wave_radius = 280.0 * dt 
        wave_thickness = 40.0 + 30.0 * dt
        
        # Anisotropic Wave Emission logic (Stronger opposite to the kick to conserve momentum)
        R_dist = np.sqrt(X_GRID**2 + Y_GRID**2)
        R_ang = np.arctan2(Y_GRID, X_GRID)
        
        # Directional multiplier peaks at KICK_ANGLE + PI
        anisotropy = 1.0 + 0.9 * np.cos(R_ang - (KICK_ANGLE + np.pi))
        
        # Gaussian wave pulse
        wave_amp = 180.0 * np.exp(-dt*0.8) # Rapidly decaying amplitude
        W_GRID = anisotropy * wave_amp * np.exp(-((R_dist - wave_radius)**2) / (wave_thickness**2))
        
        Z_GRID += W_GRID
        energy_burst = np.clip(1.0 - dt*0.8, 0.0, 1.0) # Used for chromatic shifting

    # Capping the infinite mathematical depth so our arrays don't visually warp out of frame
    Z_GRID = np.maximum(Z_GRID, -250.0)

    # 3. O(N) QUADRILATERAL MATRIX COMPILATION
    faces = []
    face_colors = []
    centroids_z = []
    
    # Standardise Z scaling for visual impact
    Z_PLOT = Z_GRID * 1.5

    # Compute normals using gradient (highly optimised compared to 4-point cross products for a continuous mesh)
    dZdy, dZdx = np.gradient(Z_PLOT, Y_LN[1]-Y_LN[0], X_LN[1]-X_LN[0])
    
    # Build Quads
    for i in range(RES - 1):
        for j in range(RES - 1):
            x0, y0, z0 = X_GRID[i, j],   Y_GRID[i, j],   Z_PLOT[i, j]
            x1, y1, z1 = X_GRID[i+1, j], Y_GRID[i+1, j], Z_PLOT[i+1, j]
            x2, y2, z2 = X_GRID[i+1, j+1], Y_GRID[i+1, j+1], Z_PLOT[i+1, j+1]
            x3, y3, z3 = X_GRID[i, j+1], Y_GRID[i, j+1], Z_PLOT[i, j+1]
            
            quad_3d = np.array([
                [x0, y0, z0],
                [x1, y1, z1],
                [x2, y2, z2],
                [x3, y3, z3]
            ])
            
            # Map depth and energy into colours
            avg_z = (z0 + z1 + z2 + z3) / 4.0
            
            # Flat space is Bright White/Steel. Deeper is Cyan.
            depth_ratio = np.clip(abs(avg_z) / 150.0, 0.0, 1.0)
            base_col = lerp_colour(C_FLAT_SPACE, C_DEPTH, depth_ratio)
            
            # If wave bursts, inject Deep Magenta
            if t_sec > T_MERGE:
                # Approximate the wave intensity at this specific quad
                r_dist = np.sqrt(X_GRID[i,j]**2 + Y_GRID[i,j]**2)
                r_ang = np.arctan2(Y_GRID[i,j], X_GRID[i,j])
                aniso = 1.0 + 0.9 * np.cos(r_ang - (KICK_ANGLE + np.pi))
                w_int = aniso * np.exp(-((r_dist - wave_radius)**2) / (wave_thickness**2)) * energy_burst
                
                # STRICT MATHEMATICAL CLAMP TO PREVENT TRACEBACK
                w_int = np.clip(w_int, 0.0, 1.0)
                
                # Blend the violent energy
                base_col = base_col * (1 - w_int) + np.array(mcolors.to_rgb(C_ENERGY)) * w_int

            # Quick Normal estimation for Lambertian Shading
            nx, ny = -dZdx[i, j], -dZdy[i, j]
            nz = 1.0
            n_len = np.sqrt(nx**2 + ny**2 + nz**2)
            norm = np.array([nx, ny, nz]) / n_len
            
            # DIFFUSION CLAMP: Ensure shadows never drop below 0.7 luminance multiplier. Absolute contrast required.
            diff = 0.7 + 0.3 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            
            # Additional safety clamp prior to generating the face colour tensor
            f_col_safe = np.clip(base_col * diff, 0.0, 1.0)
            f_col = np.append(f_col_safe, 1.0)
            
            v_cam = np.einsum('ij,nj->ni', M_cam, quad_3d)
            v_cam[:, 2] += cam_dist
            
            # Valid Z clipping to prevent mathematical tear
            if np.any(v_cam[:, 2] < 10.0):
                continue
                
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            poly_2d = np.stack((px, py), axis=-1)
            
            faces.append(poly_2d)
            face_colors.append(f_col)
            centroids_z.append(np.mean(v_cam[:, 2]))

    # 4. SORT AND RENDER TENSORS
    sort_idx = np.argsort(centroids_z)[::-1] 
    sorted_faces = [faces[i] for i in sort_idx]
    sorted_fcs = [face_colors[i] for i in sort_idx]
    
    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.3, joinstyle='miter'))

    # 5. DRAW SINGULARITIES (Event Horizons)
    for (bx, by, bz, br) in bh_positions:
        # Plot circle precisely at depth location
        b_pt = np.array([[bx, by, bz*1.5]])
        v_c = np.einsum('ij,nj->ni', M_cam, b_pt)
        v_c[:, 2] += cam_dist
        px = 1800.0 * (v_c[:, 0] / v_c[:, 2])
        py = 1800.0 * (v_c[:, 1] / v_c[:, 2])
        
        # Scale physical horizon radius identically via Central Perspective maths
        visual_r = 1800.0 * (br / v_c[0, 2])
        
        ax.add_patch(plt.Circle((px[0], py[0]), visual_r, color=C_BH, zorder=100))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-408 :: NUMERICAL RELATIVITY TENSOR", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] ASYMMETRIC GRAVITATIONAL RECOIL", color=C_ENERGY, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = 0.0
    if t_sec < T_MERGE:
        state_msg = "PHASE 1: BINARY INSPIRAL MATRIX"
        state_col = C_DEPTH
        active_op = f"ORBITAL DECAY TRACE. T_MINUS: {(T_MERGE - t_sec):05.2f} S"
        prog = t_sec / T_MERGE
    elif t_sec < T_MERGE + 1.5:
        state_msg = "PHASE 2: THE MERGER & THE 8% MASS BURST"
        state_col = C_ENERGY
        active_op = "8% REST MASS CONVERTED TO GRAVITATIONAL RADIATION."
        prog = 1.0
    else:
        state_msg = "PHASE 3: ROGUE EJECTION MATRIX"
        state_col = C_TEXT
        active_op = "ANISOTROPIC RECOIL (KICK). V_ESC = 4000 KM/S."
        prog = 1.0

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: MOMENTUM CONSERVATION COMMANDS A PHYSICAL RECOIL.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-408: HIGH-CONTRAST RELATIVITY TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Spacetime mathematically deformed.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
