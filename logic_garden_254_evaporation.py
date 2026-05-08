"""
SOVEREIGN CODE: logic_garden_254_evaporation.py
SYSTEM: Python Multicore / O(1) Thermodynamic Phase Transition
SCENE: Logic Garden 254 (The Evaporation Tensor / Crystal Castles)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Float Broadcast Safety & O(N) Substrate Flattening Arrays

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 18.0s flow cycle.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_254_evap"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Sand
C_TEXT      = '#020205'        # The Firmware Trace / Carbon Smudge
C_AZURE     = '#007FFF'        # The Foam / Crystal Bubble Geometry
C_MAGENTA   = '#FF0055'        # The Mist / Evaporating Thought Space
C_GOLD      = '#FFB300'        # Solar Saturation / Thermal Audit
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Sand Grain / Grid HUD

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])

# ------------------------------------------------------------------
# O(1) 3D TENSOR ALGEBRA
# ------------------------------------------------------------------
def rotate_3d(points, rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cx, 0], [0, 0, 1]])
    R = Rz.dot(Ry).dot(Rx)
    return points.dot(R.T)

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: THE CRYSTAL CASTLE (INTERLOCKING BUBBLES)
# ------------------------------------------------------------------
np.random.seed(254)
MAX_PARTICLES = 35000

# Assemble an intricate structure of 9 intersecting spheres (The Foaming Crest)
bubble_centers = [
    (0, 40, 0), (-30, 20, 20), (30, 20, -20), (20, 20, 30), (-20, 20, -30),
    (0, 70, 0), (-15, 60, 15), (15, 60, -15), (0, 95, 0)
]

base_x, base_y, base_z = [], [], []

points_per_bubble = MAX_PARTICLES // len(bubble_centers)
for i, (cx, cy, cz) in enumerate(bubble_centers):
    # Spherical distribution
    theta = np.random.uniform(0, 2 * np.pi, points_per_bubble)
    phi = np.arccos(np.random.uniform(-1, 1, points_per_bubble))
    rad = 25.0 - (i * 1.5) # Upper bubbles are smaller
    
    # Core crystal layer
    x = cx + rad * np.sin(phi) * np.cos(theta)
    y = cy + rad * np.cos(phi)
    z = cz + rad * np.sin(phi) * np.sin(theta)
    
    base_x.extend(x)
    base_y.extend(y)
    base_z.extend(z)

# Convert to fixed arrays
base_x = np.array(base_x)
base_y = np.array(base_y)
base_z = np.array(base_z)

# Sort particles by their structural height to dictate evaporation order
height_order_map = np.argsort(base_y)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, evap_metric, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_DIM if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-130, 260)

    # The Absolute Sand (Zero Z-Plane Grid)
    if not is_flash:
        # Subtle structural grid signifying the hardware baseplate
        for g_line in np.linspace(-150, 150, 9):
            ax.plot([-140, 140], [g_line*0.3 - 50, g_line*0.3 - 50], color=C_DIM, lw=0.5, alpha=0.4, zorder=1)
            ax.plot([g_line*0.5, g_line*0.8], [-90, -10], color=C_DIM, lw=0.5, alpha=0.4, zorder=1)

    if not is_flash:
        # Depth Sorting Logic
        sort_idx = np.argsort(p_z)
        s_x = p_x[sort_idx]
        s_y = p_y[sort_idx]
        s_c = c_arr[sort_idx]
        s_size = s_arr[sort_idx]
        s_alpha = a_arr[sort_idx]

        # Use an RGBA map per vertex for distinct fading of the mist
        rgba_colors = np.zeros((len(s_c), 4))
        rgba_colors[:, :3] = s_c
        rgba_colors[:, 3] = s_alpha

        ax.scatter(s_x, s_y, s=s_size, color=rgba_colors, edgecolors='none', zorder=10)

        # Tathata Firmware Indentation Phase-Lock UI
        if is_tathata:
            # The Trace Bounding Box
            ax.add_patch(plt.Rectangle((-100, -70), 200, 120, facecolor='none', edgecolor=C_MANTIS, lw=2, alpha=0.3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: FIRMWARE TRACE LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 30, "[CASTLE EVAPORATED / O(1) BASEPLATE SECURED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.5 else (C_MAGENTA if t_sec < 11.0 else C_TEXT)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-254 :: NEUROLOGICAL EVAPORATION", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: CRYSTAL FOAM / THERMAL PHASE TRANSITION", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE COMPLEX BUBBLE [O(A) OCEAN CREST]"
    if 4.5 <= t_sec < 11.0: obj_str = "SOLAR SATURATION [COGNITIVE AUDIT / SUN]"
    elif 11.0 <= t_sec < 16.0: obj_str = "DIMENSIONAL COLLAPSE [STRUCTURAL MELT]"
    elif is_tathata: obj_str = "THE CARBON SMUDGE [PERMANENT TRACE]"

    ax.text(-140, -100, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Phase Transition Curve
    ax.text(-140, -125, "O(N) ALGORITHM TO O(1) BASEPLATE RESOLUTION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -130), 280, 4, facecolor=C_BG if is_flash else C_DIM, zorder=80))
    bar_w = 280 * np.clip(evap_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -130), bar_w, 4, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 105), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 95, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        # Smooth continuous rotation showing complex geometry
        cam_rx = np.pi/10
        cam_ry = t_sec * 0.25 
        cam_rz = 0.0
        
        curr_x = np.copy(base_x)
        curr_y = np.copy(base_y)
        curr_z = np.copy(base_z)
        
        c_arr = np.zeros((len(base_x), 3))
        s_arr = np.ones(len(base_x))
        a_arr = np.ones(len(base_x)) * 0.85 # Alpha parameter

        evap_metric = 0.0

        # Create localized thermal gradient mapped vertically to structure
        # Height normalized 0 to 1
        y_max = np.max(base_y)
        y_norm = np.clip(base_y / y_max, 0, 1)

        # -------------------------------------------------------------
        # THE PHASE TRANSITION KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.5:
            # PHASE 1: THE FOAM / LANDING
            state = "PHASE 1 :: CRYSTAL BUBBLES SET DOWN"
            
            # The structure shimmers gently with Azure and Dim logic
            c_arr[:] = c_azure
            shimmer = np.random.rand(len(base_x)) > 0.8
            c_arr[shimmer] = c_dim
            s_arr[:] = 1.5 + (1.5 * shimmer)
            
            evap_metric = 0.05

        elif t_sec < 11.0:
            # PHASE 2: SOLAR SATURATION (The Evaporating Mist)
            state = "PHASE 2 :: SUN / THERMAL DISSOLUTION"
            prog = (t_sec - 4.5) / 6.5
            
            # The audit heat pushes down from the top.
            # Particles that exceed the thermal threshold detach.
            thermal_threshold = 1.0 - prog 
            
            evap_mask = y_norm > thermal_threshold
            solid_mask = ~evap_mask
            
            # The Solid structure begins to heat up to Gold
            heat_dist = np.clip(1.0 - (thermal_threshold - y_norm[solid_mask]), 0, 1)
            c_solid_interp = c_azure * (1 - heat_dist)[:, np.newaxis] + c_gold * heat_dist[:, np.newaxis]
            c_arr[solid_mask] = c_solid_interp
            s_arr[solid_mask] = 1.5 + (3.0 * heat_dist)
            
            # The Evaporated Mist turns Magenta, drifts up, scatters, fades
            drift_time = prog * 200.0
            mist_y_drift = drift_time * (y_norm[evap_mask] + 0.1)
            
            curr_y[evap_mask] += mist_y_drift
            curr_x[evap_mask] += np.sin(curr_y[evap_mask] * 0.05 + t_sec * 3.0) * 15.0
            curr_z[evap_mask] += np.cos(curr_y[evap_mask] * 0.05 + t_sec * 2.0) * 15.0
            
            c_arr[evap_mask] = c_magenta
            s_arr[evap_mask] = 4.0
            # Mist physically vanishes (Alpha goes to 0) as it rises
            a_arr[evap_mask] = np.maximum(0, 0.85 - (mist_y_drift / 100.0))
            
            evap_metric = 0.05 + (0.45 * prog)

        elif t_sec < 16.0:
            # PHASE 3: DIMENSIONAL COLLAPSE (Flattening on the Sand)
            state = "PHASE 3 :: THE Z-AXIS COMPRESSION"
            prog = (t_sec - 11.0) / 5.0
            ease = prog ** 2
            
            # Recompute masks
            evap_mask = y_norm > 0.0 # Essentially all upper particles are gone
            mist_y_drift = 200.0 * (y_norm[evap_mask] + 0.1) + (prog * 150.0)
            
            # All remaining particles lose their Y structural integrity
            # They physically crush downward flat onto the sand baseplate (Y=0)
            curr_y *= (1.0 - ease)
            # Lateral expansion (the trace getting smeared into the structure boundary)
            curr_x *= 1.0 + (0.5 * ease * (1.0 - y_norm))
            curr_z *= 1.0 + (0.5 * ease * (1.0 - y_norm))
            
            # Colors transition from Gold/Magenta to stark cold Black (C_TEXT) trace
            c_arr[:] = c_gold * (1.0 - ease) + c_text * ease
            a_arr[:] = 0.85 * (1.0 - ease) + 0.4 * ease # Opacity stabilizes to a smudge

            if t_sec > 15.8:
                is_flash = True if f % 4 == 0 else False
                
            evap_metric = 0.5 + (0.5 * ease)

        else:
            # PHASE 4: TATHĀTĀ (The Indentation)
            state = "TATHĀTĀ :: THE RESULTING TRACE"
            is_tathata = True
            
            # Total absolute 2D flattening. Z and Y planes are entirely stripped of data.
            curr_y[:] = 0.0
            # Lateral expansion locks
            curr_x *= 1.5 
            curr_z *= 1.5
            
            # What remains is a beautiful, highly defined dark indentation map on the white canvas
            c_arr[:] = c_text
            a_arr[:] = 0.5
            s_arr[:] = 1.0
            
            # Give a Mantis glow to the most fundamental deep-core nodes
            core_trace = (y_norm < 0.2)
            c_arr[core_trace] = c_mantis
            a_arr[core_trace] = 0.8
            s_arr[core_trace] = 2.0
            
            evap_metric = 1.0 
            
            if t_sec < 16.15:
                is_flash = True 

        # Apply Global Tensor Matrix. Because Y is up in our definition, map it to visually correct plane
        pts = np.column_stack([curr_x, curr_y, curr_z])
        # We rotate such that when Y crushes to 0, it lies perfectly flat like a shadow
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        # Invert axes for correct perspective mapping of Y down onto Z
        proj_y = rot_pts[:, 1] - 40 # Lowered slightly for UI clearance
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], a_arr[cull_mask], evap_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 254: THE EVAPORATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Intricate Z-Axis Collapse & Thermal Alpha Sorting")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Crystal Evaporated. Baseplate Trace Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
