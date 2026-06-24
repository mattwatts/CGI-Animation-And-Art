"""
SOVEREIGN CODE: logic_garden_229b_starship_vanguard.py
SYSTEM: Python Multicore / O(1) Spatial Topology
SCENE: Logic Garden 229b (Relativistic Sustainment Tensor // Colony Vanguard)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, RELATIVISTIC VECTORS
HOTFIX: Continuous Slipstream Tensor / O(N*logN) Depth Sorting
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "STUDY"
DURATION = 10.0  # 10 Second Exact Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_229b_starship_vanguard"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL (HIGH-COHERENCE / WHITE BG) --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#D0D0D5'
C_STEEL     = '#707075'
C_CYAN      = '#00FFFF'
C_WHITE     = '#FFFFFF'
C_MANTIS    = '#00FF00'
C_AZURE     = '#007FFF'
C_DIM       = '#A0A0A5'

MAX_PARTICLES = 33000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg       = np.array(hex_to_rgba(C_BG)[:3])
c_text     = np.array(hex_to_rgba(C_TEXT)[:3])
c_titanium = np.array(hex_to_rgba(C_TITANIUM)[:3])
c_steel    = np.array(hex_to_rgba(C_STEEL)[:3])
c_cyan     = np.array(hex_to_rgba(C_CYAN)[:3])
c_mantis   = np.array(hex_to_rgba(C_MANTIS)[:3])

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
# BASE GEOMETRY ARRAYS: DETERMINISTIC ARCHITECTURE
# ------------------------------------------------------------------
np.random.seed(229) # Deterministic Architecture Lock

N_HABITAT = 5000
N_ENGINE  = 5000
N_PLUME   = 15000
N_DUST    = 8000

# 1. Biological Containment Toroids (Centrifugal Habitat) (Z: 20 to 80)
th_h = np.random.uniform(0, 2*np.pi, N_HABITAT)
phi_h = np.random.uniform(0, 2*np.pi, N_HABITAT)
r_major = 45.0
r_minor = np.random.uniform(0, 8.0, N_HABITAT)
x_h = (r_major + r_minor * np.cos(phi_h)) * np.cos(th_h)
y_h = (r_major + r_minor * np.cos(phi_h)) * np.sin(th_h)
z_h = r_minor * np.sin(phi_h) + np.random.choice([30, 60], N_HABITAT)

# 2. LG-229 Engine Bell & Structural Spine (Z: -40 to 90)
# Cylinder down the center
e_z = np.random.uniform(-40, 90, N_ENGINE)
e_th = np.random.uniform(0, 2*np.pi, N_ENGINE)
e_r = np.where(e_z < -10, 15 + (e_z + 10)**2 / 40.0, 10.0) # Bell flaring at bottom
x_e = e_r * np.cos(e_th)
y_e = e_r * np.sin(e_th)
z_e = e_z

# 3. Continuous Slipstream Tensor (Cosmic Dust & Distant Ships)
d_x = np.random.uniform(-300, 300, N_DUST)
# Distribute across a Y-axis vector volume of 8000 units
d_y = np.random.uniform(0, 8000, N_DUST) 
d_z = np.random.uniform(-150, 150, N_DUST)

# 4. Antimatter Plume (Eulerian Spallation)
# Initiates at engine bell (-40) and fires downward
p_y_base = np.random.uniform(0, 200, N_PLUME) # Base length of plume
p_th = np.random.uniform(0, 2*np.pi, N_PLUME)
p_r = np.random.uniform(0, 8) * (1 + p_y_base/20.0) # Expansion cone

# Array compilation (Dust and Plume remain dynamic in rendering loop)
base_colors = np.zeros((MAX_PARTICLES, 3))
base_sizes = np.ones(MAX_PARTICLES)

# Map static colors
base_colors[:N_HABITAT] = c_titanium
base_sizes[:N_HABITAT] = 3.0
base_colors[N_HABITAT:N_HABITAT+N_ENGINE] = c_steel
base_sizes[N_HABITAT:N_HABITAT+N_ENGINE] = 4.0

def render_frame(packet):
    f, phase_ratio, state_str, px, py, pz, colors, sizes = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # O(N) Depth Sorting Matrix [Heavy Thermodynamic Cost]
    sort_idx = np.argsort(pz)
    s_px = px[sort_idx]
    s_py = py[sort_idx]
    s_c = colors[sort_idx]
    s_s = sizes[sort_idx]

    ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_TEXT
    ax.text(-140, 240, "LG-229b :: RELATIVISTIC VANGUARD", color=ui_col, fontsize=18, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: 33K DATA POINTS // 10.0s O(1) LOOP", color=ui_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Phase-Locked Velocity Widget
    ax.text(-140, 210, "V_G: -8000 UNITS", color=ui_col, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 195, "PHASE-LOCKED TRANSIT", color=C_DIM, fontsize=9, fontname='monospace', zorder=80)

    # Payload Widget
    ax.text(-140, -200, "BIO-PAYLOAD: 10,000", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, -220, "STRUCTURAL INTEGRITY [ABSOLUTE LOCK]", color=ui_col, fontsize=9, fontname='monospace', zorder=80)
    
    ax.add_patch(plt.Rectangle((-140, -225), 280, 2, facecolor=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -225), 280 * phase_ratio, 2, facecolor=C_MANTIS, zorder=81))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

def generate_stream():
    V_SLIP = 8000.0
    for f in range(TOTAL_FRAMES):
        phase_ratio = f / float(TOTAL_FRAMES)
        
        # 1. Starship Geometry (Fixed in Center, rotating slowly for Study view)
        cam_rx = np.pi / 2.2 # Tilt to see down the Y axis
        cam_ry = 0.0
        cam_rz = phase_ratio * (2 * np.pi) # Full rotation over 10s for loop
        
        ship_x = np.concatenate([x_h, x_e])
        ship_y = np.concatenate([y_h, y_e])
        ship_z = np.concatenate([z_h, z_e])
        
        ship_pts = np.column_stack([ship_x, ship_y, ship_z])
        ship_rot = rotate_3d(ship_pts, cam_rx, cam_ry, cam_rz)

        # 2. Continuous Slipstream Tensor (The Universe moving backward)
        # We wrap the Y-velocity exactly modulus 8000 to guarantee endless loop
        dynamic_dust_y = (d_y - phase_ratio * V_SLIP) % 8000 - 4000 
        dust_pts = np.column_stack([d_x, d_z, dynamic_dust_y]) # Swap Y/Z to align with camera
        
        # 3. Dynamic Eulerian Spallation (Antimatter Plume)
        # Plume particles accelerate down the Y axis. Modulo keeps them flowing natively.
        plume_vel = 400.0
        dynamic_p_y = (p_y_base + phase_ratio * plume_vel) % 200
        dyn_p_r = np.random.uniform(0, 8, N_PLUME) * (1 + dynamic_p_y/20.0) 
        p_x = dyn_p_r * np.cos(p_th)
        p_z_coord = dyn_p_r * np.sin(p_th)
        
        plume_pts = np.column_stack([p_x, p_z_coord, -40 - dynamic_p_y])
        plume_rot = rotate_3d(plume_pts, cam_rx, cam_ry, 0) # Lock plume rotation to ship base
        
        # Matrix Assembly
        proj_x = np.concatenate([ship_rot[:, 0], dust_pts[:, 0], plume_rot[:, 0]])
        proj_y = np.concatenate([ship_rot[:, 2], dust_pts[:, 2], plume_rot[:, 2]]) # Z becomes visual Y
        z_depth = np.concatenate([ship_rot[:, 1], dust_pts[:, 1], plume_rot[:, 1]])

        # Compile dynamic colors
        c_dust = np.tile(c_text, (N_DUST, 1)) # Dust reads as structural black streaks
        c_plume = np.zeros((N_PLUME, 3))
        
        # Inverse gradient: Cyan at base, bleeding to White
        energy_ratio = np.clip(dynamic_p_y / 200.0, 0, 1)
        for i in range(N_PLUME):
            c_plume[i] = c_cyan * (1.0 - energy_ratio[i]) + np.array(hex_to_rgba(C_WHITE)[:3]) * energy_ratio[i]
            
        frame_colors = np.vstack([base_colors[:N_HABITAT+N_ENGINE], c_dust, c_plume])
        
        s_dust = np.ones(N_DUST) * 1.5
        s_plume = np.ones(N_PLUME) * 5.0
        frame_sizes = np.concatenate([base_sizes[:N_HABITAT+N_ENGINE], s_dust, s_plume])

        # Culling mask to save CPU glucose
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, phase_ratio, "NOMINAL", proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], frame_colors[cull_mask], frame_sizes[cull_mask])

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-229b: RELATIVISTIC VANGUARD [MODE: {RENDER_MODE}] [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
