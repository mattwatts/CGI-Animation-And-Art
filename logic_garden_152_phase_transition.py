"""
LOGIC GARDEN 152: THE ORCHESTRATED COLLAPSE (PHASE TRANSITION)
Engine: Decoupled Process Isolation (Raw PNG -> FFmpeg)
Base Frame: 2000x2000
Target Output: YouTube Shorts (1080x1920 via FORCEBOX)
FPS: 60 (Required for 30Hz Gamma Lock phase)
Duration: 20 seconds (1200 frames)
"""

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# =============================================================================
# COMPILE-TIME SAFETY & INDUSTRIAL PALETTE
# =============================================================================
np.random.seed(42)  # Absolute Determinism

C_VOID = '#000000'
C_ORGANIC = '#800080'  
C_DARK = '#220033'     
C_CYAN = '#00FFFF'     
C_GOLD = '#FFD700'     
C_MANTIS = '#39FF14'   

FPS = 60
TOTAL_FRAMES = 1200
N_NODES = 12000

# Strict matrix conversion
rgba_organic = np.array(to_rgba(C_ORGANIC))
rgba_mantis = np.array(to_rgba(C_MANTIS))
rgba_dark = np.array(to_rgba(C_DARK))
rgba_cyan = np.array(to_rgba(C_CYAN))
rgba_gold = np.array(to_rgba(C_GOLD))
rgba_void = np.array(to_rgba(C_VOID))

# =============================================================================
# TOPOLOGICAL ARCHITECTURE
# =============================================================================
theta = np.random.uniform(0, 2 * np.pi, N_NODES)
phi = np.arccos(1 - 2 * np.random.uniform(0, 1, N_NODES))
r = np.random.normal(15, 6, N_NODES)

X0 = r * np.sin(phi) * np.cos(theta)
Y0 = r * np.sin(phi) * np.sin(theta)
Z0 = r * np.cos(phi) + 10

GRID_STEP = 3.0
X_grid = np.round(X0 / GRID_STEP) * GRID_STEP
Y_grid = np.round(Y0 / GRID_STEP) * GRID_STEP
Z_grid = np.round(Z0 / GRID_STEP) * GRID_STEP

state = np.zeros(N_NODES, dtype=np.int8)

SOV_Y = -15
SOV_Z = -15
sov_x_bright = 4.0
sov_x_dark = -4.0

colors = np.tile(rgba_organic, (N_NODES, 1))
depth_mask = r < 12
colors[depth_mask] = rgba_dark

# =============================================================================
# RENDER ENVIRONMENT (2000x2000 RESOLUTION)
# =============================================================================
# 20.0 x 100 DPI = exactly 2000x2000 pixels
fig = plt.figure(figsize=(20.0, 20.0), dpi=100, facecolor=C_VOID)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor(C_VOID)
ax.axis('off')

# Keep framing consistent across the animation
ax.set_xlim([-30, 30])
ax.set_ylim([-30, 30])
ax.set_zlim([-20, 40])
ax.view_init(elev=10, azim=45)

init_sizes = np.full(N_NODES, 15.0)

scatter = ax.scatter(X0, Y0, Z0, c=colors, s=init_sizes, alpha=0.7, edgecolors='none')

sov_colors = np.array([rgba_void, rgba_void])
sov_edges = np.array([rgba_cyan, rgba_gold])
sov_sizes = np.array([200.0, 200.0])

scatter_sov = ax.scatter([sov_x_bright, sov_x_dark], [SOV_Y, SOV_Y], [SOV_Z, SOV_Z], 
                         c=sov_colors, s=sov_sizes, edgecolors=sov_edges, linewidths=2)

u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
nova_x = np.cos(u)*np.sin(v)
nova_y = np.sin(u)*np.sin(v)
nova_z = np.cos(v)

nova_surface = [ax.plot_wireframe(nova_x*0, nova_y*0, nova_z*0, color=C_MANTIS, alpha=0.0)]

# =============================================================================
# RUNTIME LOGIC
# =============================================================================
def compute_frame_logic(frame):
    global state, colors, nova_surface
    
    ax.view_init(elev=10 + np.sin(frame*0.005)*5, azim=45 + (frame * 0.15))
    
    noise_x = np.sin(frame * 0.05 + Y0) * 1.5
    noise_y = np.cos(frame * 0.04 + Z0) * 1.5
    noise_z = np.sin(frame * 0.06 + X0) * 2.0
    
    X = np.where(state == 0, X0 + noise_x, X_grid)
    Y = np.where(state == 0, Y0 + noise_y, Y_grid)
    Z = np.where(state == 0, Z0 + noise_z, Z_grid)
    
    # 30Hz Gamma Lock Sync
    if frame > 250 and frame < 450:
        if frame % 2 == 0:
            scatter_sov._facecolor3d = np.array([rgba_cyan, rgba_gold])
            scatter_sov._sizes3d = np.array([400.0, 400.0])
        else:
            scatter_sov._facecolor3d = np.array([rgba_void, rgba_void])
            scatter_sov._sizes3d = np.array([200.0, 200.0])
    elif frame >= 450:
        scatter_sov._facecolor3d = np.array([rgba_cyan, rgba_gold])
        scatter_sov._sizes3d = np.array([300.0, 300.0])

    nova_radius = 0.0
    if frame > 450:
        nova_radius = (frame - 450) * 0.25
        dist = np.sqrt(X0**2 + (Y0 - SOV_Y)**2 + (Z0 - SOV_Z)**2)
        
        new_crystallized = (dist <= nova_radius) & (state == 0)
        state[new_crystallized] = 1
        colors[state == 1] = rgba_mantis
        
        if nova_surface[0] is not None:
            nova_surface[0].remove()
            nova_surface[0] = None
            
        if nova_radius < 60:
            nova_surface[0] = ax.plot_wireframe(nova_x*nova_radius, 
                                                nova_y*nova_radius + SOV_Y, 
                                                nova_z*nova_radius + SOV_Z, 
                                                color=C_MANTIS, alpha=0.15)

    sizes = np.where(state == 0, 15.0, 30.0) 
    
    scatter._offsets3d = (X, Y, Z)
    scatter._sizes3d = sizes
    scatter._facecolor3d = colors

# =============================================================================
# BATCH EXECUTION & FFMPEG COMPILATION
# =============================================================================
if __name__ == '__main__':
    OUTPUT_DIR = "logic_garden_152b_frames"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Initiating Array Rendering Engine -> {OUTPUT_DIR}/")
    print("Simulating Target: 1200 Frames (20.0s @ 60FPS) in 2000x2000 PNG")
    
    # 1. GENERATE RAW PNG FRAMES
    for frame in range(TOTAL_FRAMES):
        compute_frame_logic(frame)
        
        filepath = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
        plt.savefig(filepath, facecolor=C_VOID, edgecolor='none', bbox_inches='tight', pad_inches=0)
        
        if frame % 60 == 0:
            print(f"Rendered: {frame}/{TOTAL_FRAMES} frames ({(frame/TOTAL_FRAMES)*100:.1f}%)")
            
    # 2. EXECUTE PROTOCOL: FORCEBOX COMPILATION
    output_video = "LG_152b_PHASE_TRANSITION.mp4"
    print(f"\nTerminal Green. Frame extraction complete.")
    print("Initiating FFmpeg Subprocess (FORCEBOX Protocol -> YouTube Shorts)...")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",  # Overwrite
        "-framerate", str(FPS),
        "-i", os.path.join(OUTPUT_DIR, "frame_%04d.png"),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        output_video
    ]
    
    subprocess.run(ffmpeg_cmd)
    print(f"Process Isolated. Video successfully compiled to: {output_video}")
