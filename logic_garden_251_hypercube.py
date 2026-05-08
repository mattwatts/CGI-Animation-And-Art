"""
SOVEREIGN CODE: logic_garden_251_hypercube.py
SYSTEM: Python Multicore / O(1) Tesseract Shadow Projection
SCENE: Logic Garden 251 (The Hypercube Shadow / Dimensional Cascade)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: 4D to 2D Orthogonal Topography / O(N^4) Cognitive CPU Clamp

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 17.5s flow cycle.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
DURATION = 17.5
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_251_hypercube"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # The Dimensional Shadow
C_AZURE     = '#007FFF'        # Cascading Higher Dimensions
C_MAGENTA   = '#FF0055'        # Cognitive Friction / 4D Load
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Axis HUD
C_CYAN      = '#00E5FF'        # 4D Horizon

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])

# ------------------------------------------------------------------
# 4D TESSERACT GENERATOR (16 Vertices, 32 Edges)
# ------------------------------------------------------------------
def generate_tesseract():
    v = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                for w in [-1, 1]:
                    v.append([x, y, z, w])
    v = np.array(v)
    edges = []
    for i in range(16):
        for j in range(i + 1, 16):
            # Connect if they differ in exactly one coordinate
            if np.sum(np.abs(v[i] - v[j])) == 2:
                edges.append((i, j))
    return v, np.array(edges)

base_v, base_edges = generate_tesseract()
NUM_CUBES = 9 # The 9 Hypercubes of Cognitive Height

# ------------------------------------------------------------------
# 4D ROTATION TENSORS
# ------------------------------------------------------------------
def rotate_4d(pts, xw, yw, zw, xy, xz, yz):
    # Rotate in the 6 primary planes of 4D space
    R_xw = np.array([[np.cos(xw),0,0,-np.sin(xw)], [0,1,0,0], [0,0,1,0], [np.sin(xw),0,0,np.cos(xw)]])
    R_yw = np.array([[1,0,0,0], [0,np.cos(yw),0,-np.sin(yw)], [0,0,1,0], [0,np.sin(yw),0,np.cos(yw)]])
    R_zw = np.array([[1,0,0,0], [0,1,0,0], [0,0,np.cos(zw),-np.sin(zw)], [0,0,np.sin(zw),np.cos(zw)]])
    
    R_xy = np.array([[np.cos(xy),-np.sin(xy),0,0], [np.sin(xy),np.cos(xy),0,0], [0,0,1,0], [0,0,0,1]])
    R_xz = np.array([[np.cos(xz),0,-np.sin(xz),0], [0,1,0,0], [np.sin(xz),0,np.cos(xz),0], [0,0,0,1]])
    R_yz = np.array([[1,0,0,0], [0,np.cos(yz),-np.sin(yz),0], [0,np.sin(yz),np.cos(yz),0], [0,0,0,1]])
    
    # Apply chained rotation matrix
    R_combined = R_xw @ R_yw @ R_zw @ R_xy @ R_xz @ R_yz
    return pts @ R_combined.T

# Perspective projection 4D -> 3D
def project_4d_to_3d(pts_4d, distance=2.5):
    w = pts_4d[:, 3:4]
    factor = distance / (distance - w)
    return pts_4d[:, 0:3] * factor

# Isometric projection 3D -> 2D
def project_3d_to_2d(pts_3d):
    rx, ry = np.pi/6, np.pi/4
    # Rotation matrices
    Rx = np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]])
    rotated = pts_3d @ Ry.T @ Rx.T
    return rotated[:, 0:2]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, segments, seg_colors, seg_widths, shadow_active, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Background Aligning Grid (HUD anchor for tracing 2D plane)
        if shadow_active:
            for g_line in np.linspace(-150, 150, 9):
                ax.plot([-130, 130], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
                ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # High-Fidelity Line Collection Rendering
        lc = LineCollection(segments, colors=seg_colors, linewidths=seg_widths, capstyle='round', zorder=10)
        ax.add_collection(lc)

        # Tathata Phase-Lock UI
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -140, "TATHĀTĀ: DIMENSIONAL SHADOW", color=C_MANTIS, fontsize=13, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, -165, "[INFINITE MATH COMPRESSED TO O(1)]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 6.5 else (C_TEXT if t_sec < 14.8 else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-251 :: THE HYPERCUBE SHADOW", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: 4D-CASCADE TO 2D-PROXY / SUBSTRATE MAPPING", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE VERTICAL DIMENSION [O(N^4) LOAD]"
    if 6.5 <= t_sec < 9.5: obj_str = "TOPOLOGICAL PUSH [FLATTENING]"
    elif 9.5 <= t_sec < 14.8: obj_str = "THE ARISING SHADOW [2D PROJECTION]"
    elif is_tathata: obj_str = "ABSOLUTE BEDROCK [PHASE COHERENCE]"

    if t_sec < 6.5 or t_sec > 7.5: # Clean omission during the flash
        ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
        
        # CPU Load Metric
        metric_label = "COGNITIVE CPU HEAT [4D LOAD]" if t_sec < 9.5 else "SUBSTRATE RESONANCE [O(1)]"
        ax.text(-140, -205, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
        ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
        
        heat = 1.0 - (t_sec / 9.5) if t_sec < 9.5 else 1.0
        if is_tathata: heat = 1.0
        val_w = 280 * np.clip(heat, 0, 1)
        ax.add_patch(plt.Rectangle((-140, -210), val_w, 4, facecolor=ui_col, zorder=81))

        # Phase Text Box
        ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
        ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        shadow_active = False
        
        # Global 4D tracking parameters
        xw = t_sec * 0.8
        yw = t_sec * 0.5
        zw = t_sec * 1.1
        xy = t_sec * 0.4
        xz = 0.0
        yz = 0.0

        all_segments = []
        all_colors = []
        all_widths = []

        # -------------------------------------------------------------
        # THE 4D CASCADE KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 6.5:
            # PHASE 1: THE VERTICAL CASCADE (O(N^4) Cognitive Heat)
            state = "PHASE 1 :: COGNITIVE BURNOUT"
            
            for i in range(NUM_CUBES):
                scale = 35.0 - (i * 3.0)
                y_offset = (i * 30.0) - 120.0
                
                # Each hypercube rotates slightly offset to create a cascading effect
                v_rot = rotate_4d(base_v * scale, xw+i*0.1, yw, zw+i*0.2, xy, xz, yz)
                v_3d = project_4d_to_3d(v_rot, distance=150.0)
                
                # Apply vertical offset BEFORE 2D isometric projection
                v_3d[:, 1] += y_offset
                v_2d = project_3d_to_2d(v_3d)
                
                # Append edges
                for e in base_edges:
                    all_segments.append([v_2d[e[0]], v_2d[e[1]]])
                    comp_idx = i / NUM_CUBES
                    # Heavy coloring representing cognitive friction
                    color = hex_to_rgba(C_AZURE) if comp_idx > 0.5 else hex_to_rgba(C_MAGENTA)
                    color[3] = 0.6 # Alpha
                    all_colors.append(color)
                    all_widths.append(1.5 + (1.0 * comp_idx))
                    
        elif t_sec < 9.5:
            # PHASE 2: TOPOLOGICAL PUSH (Vector Collapse)
            state = "PHASE 2 :: ALGORITHM FLATTENING"
            prog = (t_sec - 6.5) / 3.0
            ease = prog ** 3 
            shadow_active = True
            
            if t_sec > 9.3:
                is_flash = True if f % 3 == 0 else False

            for i in range(NUM_CUBES):
                scale = 35.0 - (i * 3.0)
                # The vertical dimension physically collapses into the Y=0 baseplate
                y_offset = ((i * 30.0) - 120.0) * (1 - ease)
                
                v_rot = rotate_4d(base_v * scale, xw+i*0.1, yw, zw+i*0.2, xy, xz, yz)
                v_3d = project_4d_to_3d(v_rot, distance=150.0)
                v_3d[:, 1] += y_offset
                v_2d = project_3d_to_2d(v_3d)
                
                for e in base_edges:
                    all_segments.append([v_2d[e[0]], v_2d[e[1]]])
                    
                    # Colors transition beautifully from Magenta/Azure directly to pure Black (C_TEXT)
                    b_r, b_g, b_b, _ = hex_to_rgba(C_TEXT)
                    comp_idx = i / NUM_CUBES
                    s_r, s_g, s_b, _ = hex_to_rgba(C_AZURE) if comp_idx > 0.5 else hex_to_rgba(C_MAGENTA)
                    
                    r = s_r * (1 - ease) + b_r * ease
                    g = s_g * (1 - ease) + b_g * ease
                    b = s_b * (1 - ease) + b_b * ease
                    
                    all_colors.append([r, g, b, 0.6 + (0.3 * ease)])
                    all_widths.append(1.5 + (0.5 * ease))
                    
        elif t_sec < 14.8:
            # PHASE 3: THE ARISING SHADOW (Absolute Zen Geometry)
            state = "PHASE 3 :: DIMENSIONAL SHADOW ARISING"
            shadow_active = True
            
            for i in range(NUM_CUBES):
                scale = 35.0 - (i * 3.0)
                # Completely flattened
                v_rot = rotate_4d(base_v * scale, xw+i*0.1, yw, zw+i*0.2, xy, xz, yz)
                v_3d = project_4d_to_3d(v_rot, distance=150.0)
                v_3d[:, 1] = 0.0 # Bounding projection
                v_2d = project_3d_to_2d(v_3d)
                
                for e in base_edges:
                    all_segments.append([v_2d[e[0]], v_2d[e[1]]])
                    # High contrast C_TEXT mandala rendering
                    all_colors.append(hex_to_rgba(C_TEXT, alpha=0.85))
                    all_widths.append(1.0 + (i * 0.15)) # Depth mapping via line weight width

        else:
            # PHASE 4: TATHĀTĀ (Absolute Phase Lock)
            state = "TATHĀTĀ :: STARK REALITY LOCKED"
            is_tathata = True
            shadow_active = True
            
            # The 4D rotation instantly halts at t=14.8s
            xw_lock, yw_lock, zw_lock = 14.8 * 0.8, 14.8 * 0.5, 14.8 * 1.1
            xy_lock = 14.8 * 0.4
            
            for i in range(NUM_CUBES):
                scale = 35.0 - (i * 3.0)
                v_rot = rotate_4d(base_v * scale, xw_lock+i*0.1, yw_lock, zw_lock+i*0.2, xy_lock, xz, yz)
                v_3d = project_4d_to_3d(v_rot, distance=150.0)
                v_3d[:, 1] = 0.0 
                v_2d = project_3d_to_2d(v_3d)
                
                for e in base_edges:
                    all_segments.append([v_2d[e[0]], v_2d[e[1]]])
                    # Colors snap perfectly to Mantis Green
                    all_colors.append(hex_to_rgba(C_MANTIS, alpha=0.9))
                    all_widths.append(1.5 + (i * 0.2))
            
            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, state, all_segments, all_colors, all_widths, shadow_active, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 251: THE HYPERCUBE SHADOW [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: 4D Tesseract Flattening Array mapped to O(1) Bounding Matrix")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Dimensional Hierarchy Severed. Shadow Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
