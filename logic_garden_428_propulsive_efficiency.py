"""
PROJECT: Logic Garden 428 (Exact Physical Construct // Propulsive Efficiency)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PROPULSIVE EFFICIENCY, TURBOFAN, TURBOJET, AERODYNAMICS, DAYLIGHT
EXECUTION: 24.0s Sequence. Active Kinematic Graphic Extrusion.
RULES ENFORCED: 
- O(1) Mathematical Interpolation of Propulsive Efficiency vs Mach.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Dynamic Hardware Scanner tracking and grading dominant systems.
- Purged Jargon. Australian spelling conventions.
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
OUT_DIR = "frames_428_propulsive_efficiency"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Passive Cartesian Grid
C_LIGHT     = '#E2E8F0'          # Ghost background lines
C_TRANS     = '#0F172A'          # Transonic Wall Overlay

# The 4 Engine Architectures
C_TP        = '#FF3300'          # Turboprop (Intense Red)
C_PF        = '#FFB300'          # Propfan / Unducted (Dense Amber)
C_TF        = '#005599'          # Turbofan (Deep Marine)
C_TJ        = '#1E293B'          # Turbojet (Carbon Slate)

# ------------------------------------------------------------------
# RIGID 1D PHYSICS DATASTREAMS (Exact Aerodynamic Yield Mapping)
# ------------------------------------------------------------------
M_BASE = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5])
# Efficiencies evaluated in strict percentages (0 to 100)
TP_BASE = np.array([82.0, 85.0, 84.0, 70.0, 20.0,  5.0,  0.0,  0.0,  0.0,  0.0,  0.0])
PF_BASE = np.array([75.0, 78.0, 81.0, 83.0, 80.0, 65.0, 40.0, 10.0,  0.0,  0.0,  0.0])
TF_BASE = np.array([55.0, 68.0, 75.0, 78.0, 80.0, 78.0, 73.0, 64.0, 52.0, 45.0, 38.0])
TJ_BASE = np.array([15.0, 25.0, 35.0, 45.0, 55.0, 60.0, 64.0, 72.0, 80.0, 88.0, 92.0])

# O(1) Interpolation at 6000 points for flawless line drawing
HI_RES_MACH = np.linspace(0.0, 2.5, 6000)
TP_Y = np.interp(HI_RES_MACH, M_BASE, TP_BASE)
PF_Y = np.interp(HI_RES_MACH, M_BASE, PF_BASE)
TF_Y = np.interp(HI_RES_MACH, M_BASE, TF_BASE)
TJ_Y = np.interp(HI_RES_MACH, M_BASE, TJ_BASE)

# ------------------------------------------------------------------
# GEOMETRY ENGINE (Data to Cartesian Pixel Translation)
# ------------------------------------------------------------------
GRAPH_W = 920.0
GRAPH_H = 900.0
MIN_X = -460.0 # Bounding Left
MIN_Y = -400.0 # Bounding Bottom

def map_m(m):
    return MIN_X + (m / 2.5) * GRAPH_W

def map_eff(e):
    return MIN_Y + (e / 100.0) * GRAPH_H

MAP_X_ARRAY = map_m(HI_RES_MACH)
MAP_TP = map_eff(TP_Y)
MAP_PF = map_eff(PF_Y)
MAP_TF = map_eff(TF_Y)
MAP_TJ = map_eff(TJ_Y)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec = packet
    
    # Scanner Logic Phase: 0 to 20 seconds maps Mach 0 to 2.5. Hold for 4s.
    scan_prog = np.clip(t_sec / 20.0, 0.0, 1.0)
    current_mach = scan_prog * 2.5
    
    # Smooth easing for the scanner beam
    m_eased = 2.5 * (1 - (1 - scan_prog)**3) # Ease out cubic
    current_mach = m_eased

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # ====================================================
    # 1. THE HARDWARE GRAPH MATRIX (Background Extrusion)
    # ====================================================
    
    # Outer Machined Borders
    ax.add_patch(patches.Rectangle((MIN_X, MIN_Y), GRAPH_W, GRAPH_H, fill=False, edgecolor=C_TEXT, lw=6, zorder=50))
    
    # Transonic Wall (Mach 0.8 to 1.2) - The barrier of physics
    ax.add_patch(patches.Rectangle((map_m(0.8), MIN_Y), map_m(1.2)-map_m(0.8), GRAPH_H, facecolor=C_TRANS, alpha=0.04, zorder=2))
    ax.plot([map_m(1.0), map_m(1.0)], [MIN_Y, MIN_Y+GRAPH_H], color=C_TEXT, lw=2, linestyle='dashed', alpha=0.3, zorder=3)
    ax.text(map_m(1.0), MIN_Y+GRAPH_H+20, "MACH 1.0 (SOUND BARRIER)", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=51)

    # Grid Lines (Horizontal % and Vertical Mach)
    for eff in [20, 40, 60, 80, 100]:
        e_y = map_eff(eff)
        ax.plot([MIN_X, MIN_X+GRAPH_W], [e_y, e_y], color=C_STEEL, lw=1.5, alpha=0.2, zorder=1)
        ax.text(MIN_X-15, e_y, f"{eff}%", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='right', va='center', zorder=51)
        
    for mac in [0.5, 1.0, 1.5, 2.0, 2.5]:
        m_x = map_m(mac)
        ax.plot([m_x, m_x], [MIN_Y, MIN_Y+GRAPH_H], color=C_STEEL, lw=1.5, alpha=0.2, zorder=1)
        ax.text(m_x, MIN_Y-30, f"M {mac:.1f}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', va='top', zorder=51)

    ax.text(MIN_X-30, MIN_Y + GRAPH_H/2, "PROPULSIVE EFFICIENCY YIELD (%)", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', rotation=90, zorder=51)

    # ====================================================
    # 2. KINEMATIC LINE TRACING
    # ====================================================
    # Find exact index in high-res array protecting limits
    idx_limit = np.searchsorted(HI_RES_MACH, current_mach)

    # Faint "Destiny" background tracking paths
    ax.plot(MAP_X_ARRAY, MAP_TP, color=C_TP, lw=6, alpha=0.10, zorder=5)
    ax.plot(MAP_X_ARRAY, MAP_PF, color=C_PF, lw=6, alpha=0.10, zorder=5)
    ax.plot(MAP_X_ARRAY, MAP_TF, color=C_TF, lw=6, alpha=0.10, zorder=5)
    ax.plot(MAP_X_ARRAY, MAP_TJ, color=C_TJ, lw=6, alpha=0.10, zorder=5)

    if idx_limit > 0:
        # Active Welded Architecture paths
        ax.plot(MAP_X_ARRAY[:idx_limit], MAP_TP[:idx_limit], color=C_TP, lw=8, zorder=15, solid_joinstyle='round', solid_capstyle='round')
        ax.plot(MAP_X_ARRAY[:idx_limit], MAP_PF[:idx_limit], color=C_PF, lw=8, zorder=16, solid_joinstyle='round', solid_capstyle='round')
        ax.plot(MAP_X_ARRAY[:idx_limit], MAP_TF[:idx_limit], color=C_TF, lw=8, zorder=17, solid_joinstyle='round', solid_capstyle='round')
        ax.plot(MAP_X_ARRAY[:idx_limit], MAP_TJ[:idx_limit], color=C_TJ, lw=8, zorder=18, solid_joinstyle='round', solid_capstyle='round')

    # ====================================================
    # 3. DYNAMIC HARDWARE SCANNER
    # ====================================================
    s_x = map_m(current_mach)
    ax.plot([s_x, s_x], [MIN_Y, MIN_Y+GRAPH_H], color=C_TEXT, lw=4, zorder=40)
    
    # Data extraction for HUD and dots
    dt_tp = np.interp(current_mach, HI_RES_MACH, TP_Y)
    dt_pf = np.interp(current_mach, HI_RES_MACH, PF_Y)
    dt_tf = np.interp(current_mach, HI_RES_MACH, TF_Y)
    dt_tj = np.interp(current_mach, HI_RES_MACH, TJ_Y)
    
    arr_vals = [dt_tp, dt_pf, dt_tf, dt_tj]
    arr_cols = [C_TP, C_PF, C_TF, C_TJ]
    max_idx = np.argmax(arr_vals)

    # Draw kinematic intersect flashes
    ax.scatter([s_x]*4, [map_eff(v) for v in arr_vals], s=300, facecolors=arr_cols, edgecolors=C_BG, linewidths=3, zorder=45)
    
    # Pulse the dominant line
    ax.scatter([s_x], [map_eff(arr_vals[max_idx])], s=800, facecolors=arr_cols[max_idx], edgecolors='none', alpha=0.3, zorder=44)

    # ====================================================
    # 4. JARGON-FREE DAYLIGHT TELEMETRY 
    # ====================================================
    # Top Architecture Enclosure
    ax.add_patch(plt.Rectangle((-540, 700), 1080, 260, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [700, 700], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-460, 880, "LG-428 :: PROPULSIVE EFFICIENCY TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, 830, "THE KINEMATICS OF THRUST // O(1) ENGINE ARCHITECTURE", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    
    if current_mach < 0.8: phase_str = "SUBSONIC (PROPELLER DOMINANCE)"
    elif current_mach < 1.2: phase_str = "TRANSONIC (COMPRESSIBILITY DRAG SHEAR)"
    else: phase_str = "SUPERSONIC (JET VELOCITY DOMINANCE)"
        
    ax.add_patch(plt.Rectangle((-460, 730), 920, 60, facecolor=C_TEXT, zorder=85))
    ax.text(0, 760, f"CURRENT AIRSPEED : MACH {current_mach:.2f} // {phase_str}", color=C_BG, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', zorder=86)

    # Bottom Live Telemetry Layout
    ax.add_patch(plt.Rectangle((-540, -960), 1080, 450, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [-510, -510], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-460, -580, "REAL-TIME EFFICIENCY YIELD :", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)

    # Dynamic Formatting Loop
    engines = [("TURBOPROP", C_TP), ("PROPFAN (UNDUCTED)", C_PF), ("TURBOFAN", C_TF), ("TURBOJET", C_TJ)]
    
    # Y-offsets for UI
    y_readouts = [-650, -710, -770, -830]
    
    for i in range(4):
        e_name, e_col = engines[i]
        e_val = arr_vals[i]
        
        # O(1) Status Labelling
        if e_val <= 0.5:
            status = "[COMPRESSIBILITY STALL]"
            v_str = "00.0"
            draw_col = C_STEEL
        else:
            v_str = f"{e_val:04.1f}"
            draw_col = e_col
            if i == max_idx:
                status = "[DOMINANT YIELD MATRIX]"
            else:
                status = ""
                
        # Draw explicit telemetry box
        ax.plot([-460, 460], [y_readouts[i]-20, y_readouts[i]-20], color=C_STEEL, lw=1, alpha=0.3, zorder=82)
        ax.text(-460, y_readouts[i], f"{e_name:<20}", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
        ax.text( -10, y_readouts[i], f"{v_str} %", color=draw_col, fontsize=24, fontname='monospace', weight='bold', zorder=82)
        ax.text( 200, y_readouts[i], f"{status}", color=draw_col, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-428: PROPULSIVE EFFICIENCY TENSOR (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    stream = [(f, f / float(FPS)) for f in range(TOTAL_FRAMES)]

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, stream, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerodynamic Physics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
