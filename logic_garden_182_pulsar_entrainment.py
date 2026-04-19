"""
SOVEREIGN CODE: logic_garden_182_pulsar_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / 3D Numpy Dipole Array (17.5 seconds)
SCENE: Logic Garden 182 (The Cosmic Clock / Pulsar Entrainment)
HOTFIX: O(1) Particle Swarms, 60 FPS Photic Driving, Neon Pop Physics
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_182_pulsar"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'
C_CYAN    = '#00FFFF'          # Radiation Jet (North)
C_MAGENTA = '#FF00FF'          # Radiation Jet (South)
C_GOLD    = '#FFD700'          # Core / Oscilloscope High
C_MANTIS  = '#00FF00'          # Terminal Data Flow

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE 3D DIPOLE ARRAY (15,000 NODES)
# ------------------------------------------------------------------
np.random.seed(182)
N_POINTS = 15000

# Dipole Formula: r = R0 * sin^2(theta)
# We generate particles along these field lines.
theta = np.random.uniform(0.1, np.pi-0.1, N_POINTS)
phi = np.random.uniform(0, 2*np.pi, N_POINTS)
R0 = np.random.uniform(100, 1200, N_POINTS) # Scale of the lines

r = R0 * (np.sin(theta)**2)

# Spherical to Cartesian (Base Magnetic Frame)
base_x = r * np.sin(theta) * np.cos(phi)
base_y = r * np.cos(theta)
base_z = r * np.sin(theta) * np.sin(phi)

# Create Jet Swarm (High velocity particles exiting the poles)
N_JETS = 3000
jet_z_base = np.random.normal(0, 50, N_JETS)
jet_r = np.random.uniform(0, 80, N_JETS)
jet_phi = np.random.uniform(0, 2*np.pi, N_JETS)
jet_y = np.random.uniform(100, 2500, N_JETS) * np.random.choice([-1, 1], N_JETS) # Up and Down
jet_x = jet_r * np.cos(jet_phi) * (np.abs(jet_y)/300) # Cone shape
jet_z = jet_r * np.sin(jet_phi) * (np.abs(jet_y)/300)

base_x = np.concatenate([base_x, jet_x])
base_y = np.concatenate([base_y, jet_y])
base_z = np.concatenate([base_z, jet_z])

TOTAL_NODES = N_POINTS + N_JETS

# Math Functions for 3D Rotation
def rotate_z(x, y, z, angle):
    nx = x * np.cos(angle) - y * np.sin(angle)
    ny = x * np.sin(angle) + y * np.cos(angle)
    return nx, ny, z

def rotate_y(x, y, z, angle):
    nx = x * np.cos(angle) + z * np.sin(angle)
    nz = -x * np.sin(angle) + z * np.cos(angle)
    return nx, y, nz

def rotate_x(x, y, z, angle):
    ny = y * np.cos(angle) - z * np.sin(angle)
    nz = y * np.sin(angle) + z * np.cos(angle)
    return x, ny, nz

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, pz, signal, signal_hist, flash_intensity = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Entrainment Flash (Alters Background)
    bg_phase = C_TEXT if flash_intensity > 0.9 else C_VOID
    fig.patch.set_facecolor(bg_phase)
    ax.set_facecolor(bg_phase)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # Center Screen
    CX, CY = 540, 960

    # 1. DEPTH SORTING & RENDERING THE 3D ARRAY
    # Sort by Z to draw back-to-front (O(N log N) but fast in numpy)
    sort_idx = np.argsort(pz)
    sx = px[sort_idx]
    sy = py[sort_idx]
    sz = pz[sort_idx]

    # Calculate Color and Alpha based on Z and position
    z_norm = np.clip((sz + 1000) / 2000, 0, 1) # 0 (back) to 1 (front)
    
    # Split color arrays (Cyan for North/Upper, Magenta for South/Lower based on internal Y)
    # We use sy to determine color (it's orthographic)
    colors = np.where(sy[:, None] > 0, 
                      np.array(hex_to_rgba(C_CYAN)[:3]), 
                      np.array(hex_to_rgba(C_MAGENTA)[:3]))
    
    # Construct RGBA tensor
    rgba_tensor = np.zeros((TOTAL_NODES, 4))
    rgba_tensor[:, :3] = colors
    # Alpha modulated by Z-depth and global flash
    rgba_tensor[:, 3] = z_norm * 0.8 * (1.0 - flash_intensity)

    # Scatter massive array
    ax.scatter(CX + sx, CY + sy, s=6, c=rgba_tensor, edgecolors='none', zorder=2)

    # 2. THE NEUTRON CORE
    core_glow = 30 + (250 * flash_intensity)
    ax.scatter([CX], [CY], s=core_glow**2, c=C_VOID if flash_intensity>0.9 else C_TEXT, edgecolors=C_CYAN, lw=2, zorder=5)

    # 3. LENS FLARE / BEAM IMPACT
    if flash_intensity > 0.1:
        ax.axhline(CY, color=C_TEXT if flash_intensity < 0.9 else C_CYAN, lw=20 * flash_intensity, alpha=flash_intensity, zorder=6)
        ax.axvline(CX, color=C_TEXT if flash_intensity < 0.9 else C_CYAN, lw=20 * flash_intensity, alpha=flash_intensity, zorder=6)
        # Giant geometric blast
        ax.add_patch(Circle((CX, CY), 1500 * flash_intensity, color=C_CYAN, fill=False, lw=10, alpha=flash_intensity, zorder=7))

    # 4. THE SCOPE (TELEMETRY WIDGET)
    # Bottom HUD background
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.20, transform=ax.transAxes, color=bg_phase, alpha=0.9, zorder=10))
    ax.plot([0, 1], [0.20, 0.20], transform=ax.transAxes, color=C_CYAN, lw=2, zorder=10)
    
    # Oscilloscope Math
    hist_x = np.linspace(40, 1040, len(signal_hist))
    hist_y = 100 + (np.array(signal_hist) * 200) # Base 100, max 300
    
    # Draw Graph
    ax.plot(hist_x, hist_y, color=C_MANTIS if flash_intensity < 0.8 else C_VOID, lw=4, zorder=11)
    ax.fill_between(hist_x, 100, hist_y, color=C_MANTIS, alpha=0.2 * (1.0-flash_intensity), zorder=10)
    
    # Scanner Head
    current_x = hist_x[-1]
    current_y = hist_y[-1]
    ax.scatter([current_x], [current_y], s=200, c=C_GOLD, zorder=12)

    # Text Overlay
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=C_CYAN, lw=2)
    ax.text(0.04, 0.965, "LG-182 :: THE COSMIC CLOCK / NEUTRON ENTRAINMENT", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')
    
    txt_col = C_TEXT if flash_intensity < 0.9 else C_VOID
    ax.text(0.04, 0.16, "RADIO FLUX TENSOR:", transform=ax.transAxes, color=C_DIM if flash_intensity>0.9 else C_TEXT, fontsize=20, fontname='monospace', zorder=11)
    ax.text(0.04, 0.13, f"{state_str}", transform=ax.transAxes, color=C_MANTIS if flash_intensity < 0.9 else C_VOID, fontsize=24, fontname='monospace', weight='bold', zorder=11)
    ax.text(0.80, 0.16, f"SIG: {signal:.3f}", transform=ax.transAxes, color=txt_col, fontsize=22, fontname='monospace', weight='bold', zorder=11)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# THERMODYNAMIC PHYSICS STREAM (KINEMATICS)
# ------------------------------------------------------------------
def generate_stream():
    # Exactly 0.4 Hz rotation -> 2.5 seconds per pulse
    # 17.5 duration / 2.5 = Exactly 7 complete flashes (Perfect Loop)
    SPIN_FREQ = 0.4 
    TILT_ANGLE = np.radians(45) # 45 degree magnetic offset
    
    signal_history = [0.0] * 120 # Rolling window

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # 1. Kinematic Rotation
        spin_angle = 2 * np.pi * SPIN_FREQ * t_sec
        
        # Apply Tilt (Rotate around X)
        x1, y1, z1 = rotate_x(base_x, base_y, base_z, TILT_ANGLE)
        
        # Apply Spin (Rotate around Y)
        px, py, pz = rotate_y(x1, y1, z1, spin_angle)
        
        # 2. Photonic Driving (Flash detection)
        # The beam points exactly at the camera when the tilted Y-axis enters the +Z vector
        # Magnetic Y vector calculation:
        my_z = np.sin(TILT_ANGLE) * np.sin(spin_angle)
        
        # Sharpness of beam
        raw_signal = max(0, my_z)
        signal = raw_signal ** 12.0 # Extremely sharp exponential trigger
        
        flash_intensity = signal
        signal_history.append(signal)
        signal_history.pop(0)
        
        # Status Parsing
        state_str = "TATHĀTĀ: CHAOS COMPRESSED TO ARCHITECTURE." if signal < 0.1 else "CRITICAL: O(1) PHOTIC DRIVING ACTIVE."

        yield (f, t_sec, state_str, px, py, pz, signal, list(signal_history), flash_intensity)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 182: THE COSMIC CLOCK [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {TOTAL_NODES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
