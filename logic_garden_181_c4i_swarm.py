"""
SOVEREIGN CODE: logic_garden_181_c4i_swarm.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Topological Warfare Matrix (18.0 seconds)
SCENE: Logic Garden 181 (The JADC2 Swarm vs. The Hierarchical Hub)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 18.0                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_181_c4i"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Slain / Inactive Matrix
C_GOLD    = '#FFD700'          # Legacy C4I Hierarchy
C_MANTIS  = '#00FF00'          # JADC2 Distributed Mesh
C_CYAN    = '#00FFFF'          # Sensor Ping / Data Flow
C_RED     = '#FF0033'          # Thermodynamic Friction / Hub Overload
C_ORANGE  = '#FF5500'          # Hypersonic Kinetic Vector

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE TWO ALGORITHMS
# ------------------------------------------------------------------
np.random.seed(181)

# --- TOP MATRIX: HIERARCHICAL C4I (LEGACY) ---
# Hub at (540, 1500), 3 sub-hubs, 9 edge sensors
legacy_nodes = [(540, 1600)] # 0: Main Hub
sub_hubs = [(240, 1400), (540, 1400), (840, 1400)] # 1, 2, 3
edge_nodes = [
    (140, 1200), (240, 1200), (340, 1200),
    (440, 1200), (540, 1200), (640, 1200),
    (740, 1200), (840, 1200), (940, 1200)
]
legacy_nodes.extend(sub_hubs)
legacy_nodes.extend(edge_nodes)

legacy_edges = [
    (0, 1), (0, 2), (0, 3), # Hub to Sub-hubs
    (1, 4), (1, 5), (1, 6), # Sub 1 to Edges
    (2, 7), (2, 8), (2, 9), # Sub 2 to Edges
    (3, 10), (3, 11), (3, 12) # Sub 3 to Edges
]

# --- BOTTOM MATRIX: JADC2 DISTRIBUTED MESH (SWARM) ---
mesh_nodes = []
# Generate an organic but evenly spaced lattice 
for _ in range(30):
    wx = np.random.randint(150, 930)
    wy = np.random.randint(200, 800)
    mesh_nodes.append((wx, wy))
    
# Connect nodes if within a certain radius (KNN style) to form a fluid mesh
mesh_edges = []
CONNECTION_RADIUS = 280
for i in range(len(mesh_nodes)):
    for j in range(i+1, len(mesh_nodes)):
        dist = np.sqrt((mesh_nodes[i][0]-mesh_nodes[j][0])**2 + (mesh_nodes[i][1]-mesh_nodes[j][1])**2)
        if dist < CONNECTION_RADIUS:
            mesh_edges.append((i, j))

# Define attack targets
legacy_target = 0 # The Hub
mesh_target = 15  # A central node in the mesh

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, ui_col, t_phase, ping_rad, hub_heat, threat_y, legacy_alive, mesh_alive = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)

    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)
    
    # Midline Separator
    ax.axhline(1000, color=C_DIM, lw=4, zorder=1)

    # ==========================================
    # MATRIX A: LEGACY C4I HIERARCHY
    # ==========================================
    # Draw Edges
    for u, v in legacy_edges:
        n1, n2 = legacy_nodes[u], legacy_nodes[v]
        col = C_GOLD if legacy_alive else C_DIM
        ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color=col, lw=1.5, alpha=0.5, zorder=2)
        
    # Draw Data Ping 
    if t_phase == 1 and legacy_alive:
        # Ping originates at edge node 4, travels to sub 1, then to hub
        ping_path = [legacy_nodes[4], legacy_nodes[1], legacy_nodes[0]]
        # Animate along path based on modulo
        progress = (t_sec * 2) % 3 
        idx = int(progress)
        next_idx = min(idx + 1, 2)
        rem = progress - idx
        px = ping_path[idx][0] + (ping_path[next_idx][0] - ping_path[idx][0]) * rem
        py = ping_path[idx][1] + (ping_path[next_idx][1] - ping_path[idx][1]) * rem
        ax.scatter([px], [py], s=200, c=C_CYAN, zorder=5)
        
    # Draw Nodes
    for i, node in enumerate(legacy_nodes):
        if not legacy_alive:
            col = C_DIM
            size = 40
        else:
            col = C_RED if i == 0 and hub_heat > 0 else C_GOLD
            size = 200 + (300 * hub_heat) if i == 0 else (100 if i in [1, 2, 3] else 40)
        ax.scatter([node[0]], [node[1]], s=size, c=col, zorder=4)
        
    # Draw Label
    ax.text(0.04, 0.90, "HIERARCHICAL C4I. MULTI-DOMAIN KINETIC VULNERABILITY.", transform=ax.transAxes, color=C_GOLD if legacy_alive else C_DIM, fontsize=18, fontname='monospace')

    # ==========================================
    # MATRIX B: JADC2 DISTRIBUTED MESH
    # ==========================================
    # Draw Edges
    for u, v in mesh_edges:
        if mesh_alive[u] and mesh_alive[v]:
            n1, n2 = mesh_nodes[u], mesh_nodes[v]
            # If ping is active, highlight nearest edges to active nodes
            edge_col = C_MANTIS
            alpha = 0.3
            if t_phase == 1:
                if (ping_rad % 1.0) > 0.5: # Pulse effect
                    edge_col = C_CYAN
                    alpha = 0.8
            ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color=edge_col, lw=1.5, alpha=alpha, zorder=2)
            
    # Draw Data Ripple (Phase-Coherence)
    if t_phase == 1:
        # Mesh processes data as a wave of coherence immediately across all nodes
        center_mesh = mesh_nodes[15] # Start near middle
        ax.scatter([center_mesh[0]], [center_mesh[1]], s=(ping_rad*1000)**2 % 50000, facecolors='none', edgecolors=C_CYAN, lw=4, alpha=max(0, 1.0 - (ping_rad*1000)**2%50000/50000), zorder=3)

    # Draw Nodes
    for i, node in enumerate(mesh_nodes):
        if mesh_alive[i]:
            size = 40
            col = C_MANTIS
            # Pulse Nodes
            if t_phase == 1 and np.sin(i*123 + t_sec*10) > 0.8:
                col = C_CYAN
                size = 100
            ax.scatter([node[0]], [node[1]], s=size, c=col, zorder=4)
        else:
            ax.scatter([node[0]], [node[1]], s=40, c=C_DIM, zorder=4)

    # Draw Label
    ax.text(0.04, 0.48, "JADC2 MESH. DISTRIBUTED LETHALITY / ZERO HUB REQUIRED.", transform=ax.transAxes, color=C_MANTIS, fontsize=18, fontname='monospace')

    # ==========================================
    # KINETIC THREAT VECTOR (Z-AXIS HYPERSONIC)
    # ==========================================
    if t_phase >= 2:
        # Threat against Top (Hub)
        if threat_y > 1600:
            ax.plot([540, 540], [1920, threat_y], color=C_ORANGE, lw=8, zorder=6)
            ax.scatter([540], [threat_y], s=400, c=C_TEXT, edgecolors=C_ORANGE, lw=3, zorder=7)
        if threat_y <= 1600 and threat_y > 1500: # Impact Bloom Top
            ax.scatter([540], [1600], s=8000, facecolors='none', edgecolors=C_RED, lw=8, zorder=8)
            ax.scatter([540], [1600], s=3000, c=C_RED, edgecolors='none', alpha=0.6, zorder=9)

        # Threat against Bottom (Mesh Node 15)
        tx, ty = mesh_nodes[mesh_target]
        adjusted_ty = ty + (1600 - threat_y) # Matches fall rate
        if adjusted_ty > ty:
            ax.plot([tx, tx], [1000, adjusted_ty], color=C_ORANGE, lw=8, zorder=6)
            ax.scatter([tx], [adjusted_ty], s=400, c=C_TEXT, edgecolors=C_ORANGE, lw=3, zorder=7)
        if adjusted_ty <= ty and adjusted_ty > ty-100: # Impact Bloom Bottom
            ax.scatter([tx], [ty], s=4000, facecolors='none', edgecolors=C_RED, lw=8, zorder=8)
            ax.scatter([tx], [ty], s=1000, c=C_RED, edgecolors='none', alpha=0.6, zorder=9)

    # ==========================================
    # TELEMETRY WIDGETS
    # ==========================================
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LG-181 :: ARCHITECTURAL OBSOLESCENCE", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.08, "SYSTEM TOPOLOGY STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    pulse = ui_col if (f % 10 < 5) or t_phase == 4 else C_TEXT
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# TOPOLOGICAL PHYSICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    legacy_alive = True
    mesh_alive = [True] * 30
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        hub_heat = 0.0
        ping_rad = 0.0
        threat_y = 2000
        
        # Phase 1: Normal Operations (Friction vs C_CYAN Coherence)
        if t_sec < 6.0:
            t_phase = 1
            ui_col = C_CYAN
            state = "[01] ROUTING SENSOR DATA // C4I HUB LATENCY DETECTED"
            ping_rad = t_sec % 1.0
            
            # The Legacy hub glows RED showing thermodynamic processing drag
            if (t_sec * 2) % 3 > 1.5:
                hub_heat = ((t_sec * 2) % 3) - 1.5 
                
        # Phase 2: Hypersonic Strike
        elif t_sec < 10.0:
            t_phase = 2
            ui_col = C_ORANGE
            state = "[02] CRITICAL: MULTI-DOMAIN KINETIC VECTOR INBOUND"
            
            # Drops rapidly 
            threat_y = 1920 - ((t_sec - 6.0) / 4.0) ** 3 * 1000

        # Phase 3: Impact & Array Erasure
        elif t_sec < 14.0:
            t_phase = 3
            ui_col = C_RED
            threat_y = 1600 - ((t_sec - 10.0) / 1.0) * 1000 # Continues downward past impact
            
            if t_sec > 10.1:
                legacy_alive = False # Hub dies, entire tree dies
                mesh_alive[15] = False # Only target node dies
                
            state = "[03] O(1) ARRAY ERASURE // LEGACY C4I SYSTEM KILLED"

        # Phase 4: Mesh Rerouting / Survival
        else:
            t_phase = 4
            ui_col = C_MANTIS
            state = "TATHĀTĀ: CENTRALIZATION IS OBSOLETE. SWARM REROUTE COMPLETE."

        yield (f, t_sec, state, ui_col, t_phase, ping_rad, hub_heat, threat_y, legacy_alive, mesh_alive)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 181: ARCHITECTURAL OBSOLESCENCE [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
