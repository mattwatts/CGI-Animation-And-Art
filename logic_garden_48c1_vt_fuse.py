"""
PROJECT: Logic Garden 48c (Variable Time Proximity Fuse)
FORMAT: YouTube Shorts (1080x1920)
METADATA: VT FUSE, RADAR, DOPPLER SHIFT, ARTILLERY, KINEMATICS, DAYLIGHT PROTOCOL
EXECUTION: 10.0s Sequence. True Physical Erasure.
RULES ENFORCED:
- 10.0s Temporal Compression: Eradicates dead air, explosive delivery.
- Daylight Palette (White Substrate / High-Contrast Steel & Brass).
- Exact Realisational Aspect: Camera pulled back, target pulverised by tungsten.
- True RF Wave Propagation overlaid with an active Beat-Frequency Oscilloscope.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_48c_vt_fuse"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST PHOTOREALISTIC PALETTE --------
C_BG        = '#FFFFFF'       # Daylight Protocol Baseline
C_TEXT      = '#111115'       # Indestructible Black (UI / Outlines)
C_STEEL     = '#334155'       # Shell Casing / Aircraft Hull
C_BRASS     = '#B87333'       # Driving Band / Fuse Module
C_TUNGSTEN  = '#111115'       # High-Density Shrapnel 
C_TX        = '#005599'       # Transmission Wave (Deep Marine)
C_RX        = '#FFB300'       # Echo Return Wave (Dense Amber)
C_FIRE      = '#DE008A'       # Detonation Core / High-Temp Fragmentation
C_GUI       = '#64748B'       # Telemetry Matrix

MAX_SHRAPNEL = 15000

def hex_to_rgba(h, a=1.0):
    h = h.lstrip('#')
    return [int(h[0:2],16)/255.0, int(h[2:4],16)/255.0, int(h[4:6],16)/255.0, a]

c_shrapnel = np.array(hex_to_rgba(C_TUNGSTEN)[:3])
c_fire     = np.array(hex_to_rgba(C_FIRE)[:3])

# ------------------------------------------------------------------
# RIGID 2D ORDNANCE DRAFTING 
# ------------------------------------------------------------------
def generate_shell_polygon(cx, cy, scale=1.0):
    width = 25.0 * scale
    length = 100.0 * scale
    
    body = [
        (cx - width, cy - length),
        (cx + width, cy - length),
        (cx + width, cy + length*0.2),
        (cx - width, cy + length*0.2)
    ]
    
    ogive_L = []
    ogive_R = []
    steps = 15
    for i in range(steps + 1):
        t = i / float(steps)
        r = width * (1.0 - t**1.5)
        h = cy + length*0.2 + (length * 0.8 * t)
        ogive_L.append((cx - r, h))
        ogive_R.insert(0, (cx + r, h))
        
    return body[:3] + ogive_R + ogive_L + [body[3]]

# ------------------------------------------------------------------
# MULTICORE RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_life, tx_waves, rx_waves, shell_pos, tgt_pos, tgt_alpha, beat_amp, detonated, det_pos, det_time = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # Mathematical View Frustum (Pulled back to reveal the closure)
    cam_x = shell_pos[0]
    cam_y = shell_pos[1] + 1500.0 if not detonated else det_pos[1] + 1500.0
    cam_w = 3000.0
    cam_h = cam_w * (1920.0 / 1080.0)
    
    ax.set_xlim(cam_x - cam_w/2, cam_x + cam_w/2)
    ax.set_ylim(cam_y - cam_h/2, cam_y + cam_h/2)
    
    # 1. RENDER CONTINUOUS-WAVE RADAR
    for w in tx_waves:
        ax.add_patch(Circle((w[0], w[1]), w[2], fill=False, edgecolor=C_TX, lw=2.0, alpha=max(0, 1.0 - w[2]/1500.0), zorder=5))
    for w in rx_waves:
        ax.add_patch(Circle((w[0], w[1]), w[2], fill=False, edgecolor=C_RX, lw=3.0, alpha=max(0, 1.0 - w[2]/1500.0), zorder=6))

    # 2. RENDER THE TARGET (AIRCRAFT) - TARGET ERASURE TENSOR
    if tgt_alpha > 0.01:
        hx, hy = tgt_pos
        # Bomber Geometry fades dynamically during spallation intersection
        ax.add_patch(Ellipse((hx, hy), 120, 400, angle=15, facecolor=C_STEEL, edgecolor=C_TEXT, lw=3, alpha=tgt_alpha, zorder=10)) 
        ax.add_patch(Polygon([(hx-40, hy+40), (hx-280, hy-100), (hx-240, hy-160), (hx+20, hy-20)], facecolor=C_STEEL, edgecolor=C_TEXT, lw=3, alpha=tgt_alpha, zorder=9)) 
        ax.add_patch(Polygon([(hx+40, hy-20), (hx+280, hy+80), (hx+240, hy+140), (hx-20, hy+40)], facecolor=C_STEEL, edgecolor=C_TEXT, lw=3, alpha=tgt_alpha, zorder=11))
        ax.add_patch(Circle((hx, hy+150), 30, facecolor=C_BG, edgecolor=C_TEXT, lw=2, alpha=tgt_alpha, zorder=12))

    # 3. RENDER THE ORDNANCE (VT SHELL)
    if not detonated:
        sx, sy = shell_pos
        shell_poly = generate_shell_polygon(sx, sy, 1.5)
        ax.add_patch(Polygon(shell_poly, facecolor=C_STEEL, edgecolor=C_TEXT, lw=3, zorder=20))
        # Brass proximity nose cone
        ax.add_patch(Polygon(shell_poly[-6:-2], facecolor=C_BRASS, edgecolor=C_TEXT, lw=2, zorder=21))
        # Driving band
        ax.add_patch(Rectangle((sx-37.5, sy-110), 75, 18, facecolor=C_BRASS, edgecolor=C_TEXT, lw=2, zorder=21))

    # 4. KINEMATIC SPALLATION TENSOR (The Fragmentation)
    active = p_life > 0
    if np.any(active):
        s_px = px[active]
        s_py = py[active]
        s_life = p_life[active]
        
        # Colour calculation: Fire core cools rapidly into Tungsten black
        colors = np.zeros((len(s_px), 4))
        for i, l in enumerate(s_life):
            if l > 0.85:
                # Still hot
                colors[i] = [c_fire[0], c_fire[1], c_fire[2], l]
            else:
                # Black fragmentation
                colors[i] = [c_shrapnel[0], c_shrapnel[1], c_shrapnel[2], l]
            
        # Heavy Tungsten sizes to physically obscure the target underneath
        sizes = 10.0 + (s_life * 25.0)
        ax.scatter(s_px, s_py, s=sizes, color=colors, edgecolors='none', zorder=30)
        
        # Expanding HE Shockwave Array
        exp_age = t_sec - det_time
        if exp_age < 0.3:
            r_fire = 150 + (exp_age * 5000)
            r_core = 80 + (exp_age * 4500)
            a_fire = max(0.0, 1.0 - (exp_age / 0.3))
            ax.add_patch(Circle((det_pos[0], det_pos[1]), r_fire, facecolor=C_FIRE, alpha=a_fire*0.8, zorder=25))
            ax.add_patch(Circle((det_pos[0], det_pos[1]), r_core, facecolor=C_BG, alpha=a_fire*0.95, zorder=26))

    # 5. INDUSTRIAL HUD & TELEMETRY
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=80))
    ax.text(0.04, 0.965, "LG-48c :: THE VARIABLE TIME (VT) FUSE", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(Rectangle((0, 0), 1.0, 0.18, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=80))
    
    ax.text(0.04, 0.14, f"STATE: {state_str}", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=81)
    ax.text(0.04, 0.11, f"DOPPLER AMPLITUDE: {beat_amp*100:05.1f}V", transform=ax.transAxes, color=C_RX if not detonated else C_FIRE, fontsize=14, fontname='monospace', weight='bold', zorder=81)

    # 6. MATHEMATICAL OSCILLOSCOPE (Beat Frequency)
    osc_x = np.linspace(0.04, 0.96, 500)
    beat_freq = 15.0 + (beat_amp * 50.0)
    osc_y = 0.05 + np.sin((osc_x * beat_freq) + (f * 0.2)) * 0.04 * beat_amp
    if detonated: 
        osc_y = np.ones_like(osc_x) * 0.05 # Immediate Post-Detonation Flatline
        
    ax.plot(osc_x, osc_y, transform=ax.transAxes, color=C_TEXT, lw=2.5, zorder=81)
    # Target Threshold Trip-Line
    ax.plot([0.04, 0.96], [0.05 + (0.04 * 0.85), 0.05 + (0.04 * 0.85)], transform=ax.transAxes, color=C_FIRE, lw=1.5, linestyle='--', zorder=81)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    px = np.zeros(MAX_SHRAPNEL)
    py = np.zeros(MAX_SHRAPNEL)
    vx = np.zeros(MAX_SHRAPNEL)
    vy = np.zeros(MAX_SHRAPNEL)
    p_life = np.zeros(MAX_SHRAPNEL)
    
    tx_waves = []
    rx_waves = []
    
    shell_pos = np.array([0.0, -1000.0])
    shell_v = np.array([0.0, 750.0]) # Violent closing velocity
    
    target_pos = np.array([400.0, 4200.0])
    target_v = np.array([-80.0, -250.0]) # Target diving in
    
    detonated = False
    det_pos = np.array([0.0, 0.0])
    det_time = 0.0
    tgt_alpha = 1.0
    speed_of_light = 3500.0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        state = "ASCENT BALLISTICS // CONTINUOUS WAVE TX"
        beat_amp = 0.0
        dist = np.linalg.norm(shell_pos - target_pos) if not detonated else np.linalg.norm(det_pos - target_pos)
        
        # ---- PHASE 1: ACQUISITION ----
        if not detonated:
            if f % 4 == 0:
                tx_waves.append([shell_pos[0], shell_pos[1], 10.0])
                
            beat_amp = np.clip(1.0 - (dist / 2200.0), 0.0, 1.0)**3.0
            if beat_amp > 0.2:
                state = "INTERFERENCE // DOPPLER SHIFT DETECTED"
            
            # Absolute Mathematical Threshold Override
            if beat_amp > 0.85:
                detonated = True
                det_time = t_sec
                det_pos = np.copy(shell_pos)
                
                # Execute Spallation
                angles = np.random.normal(np.pi/2, 0.5, MAX_SHRAPNEL) # High volume forward cone
                speeds = np.random.uniform(1200.0, 3600.0, MAX_SHRAPNEL) # Out-accelerates the aircraft
                
                px[...] = shell_pos[0] + np.random.uniform(-10, 10, MAX_SHRAPNEL)
                py[...] = shell_pos[1] + np.random.uniform(-10, 10, MAX_SHRAPNEL)
                vx[...] = np.cos(angles) * speeds + shell_v[0]
                vy[...] = np.sin(angles) * speeds + shell_v[1]
                p_life[...] = 1.0

        # ---- PHASE 2: TARGET ERASURE TENSOR ----
        else:
            state = "PROXIMITY THRESHOLD EXCEEDED // KINEMATIC ERASURE"
            beat_amp = 1.0
            # Bomber fades to zero instantly as the cloud overtakes it
            tgt_alpha = max(0.0, 1.0 - (t_sec - det_time) * 2.5)

        # O(1) Kinematics Operations
        if not detonated:
            shell_pos += shell_v * dt
        
        # Target always translates, physics do not pause upon shell death
        target_pos += target_v * dt

        # RF Continuity Matrix
        alive_tx = []
        for w in tx_waves:
            w[2] += speed_of_light * dt
            # If target acts as mirror
            if tgt_alpha > 0.1 and abs(dist - w[2]) < 100.0:
                if np.random.random() < 0.9: 
                    rx_waves.append([target_pos[0], target_pos[1], 10.0])
            if w[2] < 2200.0:
                alive_tx.append(w)
        tx_waves = alive_tx
        
        alive_rx = []
        for w in rx_waves:
            w[2] += speed_of_light * dt
            if w[2] < 2200.0:
                alive_rx.append(w)
        rx_waves = alive_rx

        # Thermodynamics Particle Engine (Shrapnel Fade)
        active = p_life > 0
        if np.any(active):
            px[active] += vx[active] * dt
            py[active] += vy[active] * dt
            p_life[active] -= 1.0 / (FPS * 3.5) # 3.5s drift retention

        yield (f, t_sec, state, np.copy(px), np.copy(py), np.copy(p_life), tx_waves, rx_waves, np.copy(shell_pos), np.copy(target_pos), tgt_alpha, beat_amp, detonated, np.copy(det_pos), det_time)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-48c: PHOTOREALISTIC TARGET ERASURE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Compression Duration: {DURATION}s | Erasure Nodes: {MAX_SHRAPNEL}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Matrix Resolved: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
