"""
SOVEREIGN CODE: logic_garden_167_quadtree.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Spatial Partitioning (35 seconds)
SCENE: Logic Garden 167 (Spatial Indexing / The Quadtree vs O(N^2))
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_167_quadtree"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_RED     = '#FF0033'          # O(N^2) Brute Force Friction
C_CYAN    = '#00FFFF'          # Quadtree Bounding Boxes
C_MANTIS  = '#00FF00'          # Localized Quadtree Logic (Terminal Flow)
C_DIM     = '#1A1A24'          # Hardware Mesh

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & PHYSICS PRE-COMPILATION
# ------------------------------------------------------------------
N = 150  # Number of nodes per panel
np.random.seed(167)

# Pre-compile the entire 35-second kinetic trajectory
dt = 1.0 / FPS
px = np.random.uniform(0, 1000, (TOTAL_FRAMES, N))
py = np.random.uniform(0, 600, (TOTAL_FRAMES, N))
vx = np.random.uniform(-150, 150, N)
vy = np.random.uniform(-150, 150, N)

for f in range(1, TOTAL_FRAMES):
    px[f] = px[f-1] + vx * dt
    py[f] = py[f-1] + vy * dt
    
    # Bounding Box Deflections
    x_rebound = (px[f] <= 0) | (px[f] >= 1000)
    y_rebound = (py[f] <= 0) | (py[f] >= 600)
    vx[x_rebound] *= -1
    vy[y_rebound] *= -1
    px[f] = np.clip(px[f], 0, 1000)
    py[f] = np.clip(py[f], 0, 600)

MAX_BF_OPERATIONS = int(N * (N - 1) / 2)

# ------------------------------------------------------------------
# QUADTREE ARCHITECTURE (THE SPATIAL PARTITIONER)
# ------------------------------------------------------------------
class QuadTree:
    def __init__(self, x, y, w, h, capacity):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.children = []

    def subdivide(self):
        hw = self.w / 2
        hh = self.h / 2
        self.children.append(QuadTree(self.x, self.y, hw, hh, self.capacity))           # SW
        self.children.append(QuadTree(self.x + hw, self.y, hw, hh, self.capacity))      # SE
        self.children.append(QuadTree(self.x, self.y + hh, hw, hh, self.capacity))      # NW
        self.children.append(QuadTree(self.x + hw, self.y + hh, hw, hh, self.capacity)) # NE
        self.divided = True

    def insert(self, p):
        # p is a tuple (idx, x, y)
        if not (self.x <= p[1] <= self.x + self.w and self.y <= p[2] <= self.y + self.h):
            return False
            
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(p)
            return True
            
        if not self.divided:
            self.subdivide()
            
        for child in self.children:
            if child.insert(p):
                return True
        return False

    def get_leaves(self, leaves_list):
        if not self.divided:
            leaves_list.append((self.x, self.y, self.w, self.h, self.points))
        else:
            for child in self.children:
                child.get_leaves(leaves_list)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # Offset metrics for the 9:16 terminal
    TOP_Y = 1180
    BOT_Y = 220
    X_OFF = 40
    
    cur_px = px[f] + X_OFF
    cur_py = py[f]

    # -----------------------------------------------------------
    # 1. TOP PANEL: O(N²) BRUTE FORCE FLOOD
    # -----------------------------------------------------------
    # Generate all possible combination lines between nodes
    bf_lines = [[(cur_px[i], cur_py[i] + TOP_Y), (cur_px[j], cur_py[j] + TOP_Y)] 
                for i in range(N) for j in range(i+1, N)]
    
    lc_bf = LineCollection(bf_lines, color=hex_to_rgba(C_RED, 0.05), linewidths=1.0, zorder=1)
    ax.add_collection(lc_bf)
    
    ax.scatter(cur_px, cur_py + TOP_Y, s=15, c=C_TEXT, zorder=3)
    ax.add_patch(Rectangle((X_OFF, TOP_Y), 1000, 600, fill=False, edgecolor=C_DIM, lw=2, zorder=0))

    # -----------------------------------------------------------
    # 2. BOTTOM PANEL: THE QUADTREE BOUNDING BOXES
    # -----------------------------------------------------------
    # Rebuild tree for perfectly mapped topological tracking
    qt = QuadTree(X_OFF, BOT_Y, 1000.0, 600.0, capacity=6)
    for i in range(N):
        qt.insert((i, cur_px[i], cur_py[i] + BOT_Y))
        
    leaves = []
    qt.get_leaves(leaves)
    
    qt_lines = []
    qt_total_ops = 0
    
    # Render recursive boxes and calculate localized interactions
    for lx, ly, lw, lh, pts in leaves:
        # Draw rigid bounding box
        ax.add_patch(Rectangle((lx, ly), lw, lh, fill=False, edgecolor=hex_to_rgba(C_CYAN, 0.8), lw=1.5, zorder=2))
        
        # Connect nodes ONLY within their localized box
        num_local = len(pts)
        if num_local > 1:
            local_ops = int(num_local * (num_local - 1) / 2)
            qt_total_ops += local_ops
            for i in range(num_local):
                for j in range(i+1, num_local):
                    qt_lines.append([(pts[i][1], pts[i][2]), (pts[j][1], pts[j][2])])
    
    lc_qt = LineCollection(qt_lines, color=hex_to_rgba(C_MANTIS, 0.8), linewidths=2.0, zorder=3)
    ax.add_collection(lc_qt)
    
    ax.scatter(cur_px, cur_py + BOT_Y, s=15, c=C_TEXT, zorder=4)

    # -----------------------------------------------------------
    # 3. TELEMETRY WIDGETS
    # -----------------------------------------------------------
    # Top Terminal Data
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 167 :: SPATIAL INDEXING", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Brute Force Telemetry (Top)
    ax.text(0.04, 0.91, f"BRUTE FORCE ALGORITHM [O(N²)]", transform=ax.transAxes, color=C_RED, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.04, 0.89, f"GLOBAL COMPUTE: EVERY NODE EVALUATED", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.87, f"LATENCY CHECKS: {MAX_BF_OPERATIONS:>05d} / FRAME", transform=ax.transAxes, color=C_RED, fontsize=20, fontname='monospace')
    
    # Quadtree Telemetry (Middle)
    eff_reduction = 100.0 - ((qt_total_ops / MAX_BF_OPERATIONS) * 100)
    ax.text(0.04, 0.42, f"QUADTREE INDEXING [O(N log N)]", transform=ax.transAxes, color=C_CYAN, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.04, 0.40, f"LOCAL COMPUTE : SECTOR QUARANTINE", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.38, f"LATENCY CHECKS: {qt_total_ops:>05d} / FRAME", transform=ax.transAxes, color=C_MANTIS, fontsize=20, fontname='monospace', weight='bold')
    ax.text(0.04, 0.36, f"FRICTION CLEARED: -{eff_reduction:.1f}%", transform=ax.transAxes, color=C_CYAN, fontsize=18, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM METRIC:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=26, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (THERMODYNAMIC TIME MAPPING)
# ------------------------------------------------------------------
def generate_physics_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # State cycling for visual pacing
        if t_sec < 10.0:
            state = "[01] BRUTE FORCE FLOODING (UNBEARABLE LATENCY)"
            ui_col = C_RED
        elif t_sec < 25.0:
            state = "[02] QUADTREE DEPLOYED (NOISE QUARANTINED)"
            ui_col = C_CYAN
        else:
            state = "[03] TATHĀTĀ: COMPUTE ONLY WHAT YOU LOCALIZE"
            ui_col = C_MANTIS

        yield (f, t_sec, state, ui_col)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 167: SPATIAL INDEXING [CORES: {cpu_cores}]")
    print(f"Tracking Arithmetic Matrices across {TOTAL_FRAMES} kinematic states.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
