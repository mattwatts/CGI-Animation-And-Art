"""
PROJECT: Logic Garden 431 (Exact Physical Construct // Dual Rotary Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: WANKEL ROTARY, RADIAL ENGINE, KINEMATICS, DAYLIGHT, THERMODYNAMICS
EXECUTION: 12.0s Seamless Endless Loop. True 2D High-Density Construct.
RULES ENFORCED: 
- O(1) Epitrochoid geometric envelope & Reuleaux Rotor plotting.
- True Master-Articulating rod geometric intersection mapping.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcol
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_431_dual_rotary"
os.makedirs(OUT_DIR, exist_ok=True)
REVS_PER_LOOP = 6.0  # Universal mechanical clock

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black Borders
C_STEEL     = '#94A3B8'          # Steel Casing / Exhaust Phase
C_CRANE     = '#1E293B'          # Carbon Slate (Pistons / Rotor)
C_MASTER    = '#DE008A'          # Deep Magenta (Master Kinematics)
C_ARTIC     = '#005599'          # Deep Marine (Articulating Rods & Intake Phase)
C_COMP      = '#00C853'          # Jade (Compression Phase)
C_POWER     = '#FF3300'          # Intense Red (Combustion/Power Phase)
C_AMBER     = '#FFB300'          # Amber (Crankshaft Webs / Spark)
C_HOUSING   = '#F8FAFC'          # Light Substrate Base

# ------------------------------------------------------------------
# O(1) MACRO PHYSICS ENGINE (DUAL KINEMATICS)
# ------------------------------------------------------------------

# --- WANKEL PARAMETERS (Top) ---
WANKEL_C = np.array([0.0, 420.0])
R_GEN = 210.0      # Generative Radius
E_ECC = 35.0       # Eccentricity Offset

# --- RADIAL PARAMETERS (Bottom) ---
RADIAL_C = np.array([0.0, -420.0])
R_CRANK = 70.0     # Crank Throw
L_MASTER = 260.0   # Master Rod Length
R_HUB = 48.0       # Articulating Hub Radius
L_ARTIC = 212.0    # Articulating Rod Length (L_MASTER - R_HUB)
R_CYL = 35.0       # Cylinder Inner Radius
CYL_H = 140.0      # Cylinder Cutaway Height
NUM_CYL = 7

# Cylinder absolute angles (Cyl 0 is Top Dead Vertical)
PHI = [math.pi/2 + i * (2*math.pi / NUM_CYL) for i in range(NUM_CYL)]
# Operational Stroke Offset to ensure proper 4-Stroke sequence (0, 2pi alternating)
PSI = [0, 2*math.pi, 0, 2*math.pi, 0, 2*math.pi, 0]

def get_bezier_curve(p0, p1, p_ctrl, steps=20):
    """ O(1) Quadratic Bezier for Reuleaux Rotor sweeping edge """
    t = np.linspace(0, 1, steps)
    t = t[:, np.newaxis]
    return (1-t)**2 * p0 + 2*(1-t)*t * p_ctrl + t**2 * p1

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_seq = f / TOTAL_FRAMES
        
        # Universal System Clock (radians)
        theta_crank = t_seq * REVS_PER_LOOP * 2 * math.pi
        
        yield (f, theta_crank)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, theta_crank = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # ==================================================================
    # MODULE 1: WANKEL ROTARY ENGINE (EPITROCHOID MATRIX)
    # ==================================================================
    # 1. Base Epitrochoid Housing Geometry
    t_ep = np.linspace(0, 2*math.pi, 360)
    # 90-degree phase shift applied to lock the "pinch" to the Y-axis.
    ep_x = R_GEN * np.cos(t_ep) - E_ECC * np.cos(3*t_ep) + WANKEL_C[0]
    ep_y = R_GEN * np.sin(t_ep) + E_ECC * np.sin(3*t_ep) + WANKEL_C[1]
    
    ax.fill(ep_x, ep_y, color=C_HOUSING, zorder=1)
    ax.plot(ep_x, ep_y, color=C_TEXT, lw=4, zorder=30)
    
    # Thermodynamic Fluid Masking (Drawing colored phase wedges underneath the rotor)
    alpha_rotor = theta_crank / 3.0
    
    # Calculate Rotor Vertices
    v_pts = []
    for k in range(3):
        v_ang = alpha_rotor + k * (2*math.pi/3) + math.pi/2 # aligned with epitrochoid shift
        vx = E_ECC * math.cos(theta_crank+math.pi/2) + R_GEN * math.cos(v_ang) + WANKEL_C[0]
        vy = E_ECC * math.sin(theta_crank+math.pi/2) + R_GEN * math.sin(v_ang) + WANKEL_C[1]
        v_pts.append(np.array([vx, vy]))
    v_pts.append(v_pts[0]) # Loop for drawing

    # Eccentric Shaft Center
    ecc_cx = E_ECC * math.cos(theta_crank+math.pi/2) + WANKEL_C[0]
    ecc_cy = E_ECC * math.sin(theta_crank+math.pi/2) + WANKEL_C[1]

    # Evaluate Phase Colors (Interpolating chamber volume logic)
    for k in range(3):
        # Angle of chamber center relative to operation
        mid_ang = (alpha_rotor + k * (2*math.pi/3) + math.pi/3) % (2*math.pi)
        
        c_phase = C_STEEL
        if mid_ang < math.pi/2: c_phase = C_POWER
        elif mid_ang < math.pi: c_phase = C_STEEL # Exhaust
        elif mid_ang < 3*math.pi/2: c_phase = C_ARTIC # Intake (Deep Marine)
        else: c_phase = C_COMP
        
        # Determine filling polygon. A rough wedge stretching to epitrochoid bounds
        poly_pts = [np.array([ecc_cx, ecc_cy])]
        arc_angs = np.linspace(alpha_rotor + k*(2*math.pi/3), alpha_rotor + (k+1)*(2*math.pi/3), 15)
        for aa in arc_angs:
            e_ax = R_GEN * math.cos(aa+math.pi/2) - E_ECC * math.cos(3*(aa+math.pi/2)) + WANKEL_C[0]
            e_ay = R_GEN * math.sin(aa+math.pi/2) + E_ECC * math.sin(3*(aa+math.pi/2)) + WANKEL_C[1]
            poly_pts.append(np.array([e_ax, e_ay]))
        ax.add_patch(patches.Polygon(poly_pts, facecolor=c_phase, edgecolor='none', alpha=0.7, zorder=2))

    # Construct the Reuleaux Rotor Edges
    rotor_poly = []
    for k in range(3):
        p0 = v_pts[k]
        p1 = v_pts[k+1]
        mid = (p0 + p1) / 2.0
        # Normal vector pushed outward to form the geometric bulge
        norm = mid - np.array([ecc_cx, ecc_cy])
        norm = norm / np.linalg.norm(norm)
        p_ctrl = mid + norm * (R_GEN * 0.165) # Tuned envelope bulge
        curve = get_bezier_curve(p0, p1, p_ctrl, steps=15)
        rotor_poly.extend(curve)
        
    ax.add_patch(patches.Polygon(rotor_poly, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=10))
    
    # Internal Gearing & Drive Shaft
    ax.add_patch(patches.Circle((ecc_cx, ecc_cy), 55, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=11))
    ax.add_patch(patches.Circle((WANKEL_C[0], WANKEL_C[1]), 35, facecolor=C_STEEL, edgecolor=C_TEXT, lw=3, zorder=12))
    ax.add_patch(patches.Circle((ecc_cx, ecc_cy), E_ECC, facecolor=C_MASTER, edgecolor=C_TEXT, lw=2, zorder=13)) # Eccentric Pin

    # Base Station Geometrics & Spark Plug
    ax.add_patch(patches.Circle((WANKEL_C[0], WANKEL_C[1]+160), 10, facecolor=C_TEXT, zorder=31))
    # Combustion Flash Logic
    if ((theta_crank % (2*math.pi)) < 0.2) or ((theta_crank % (2*math.pi)) > 2*math.pi - 0.2):
        ax.add_patch(patches.Circle((WANKEL_C[0], WANKEL_C[1]+155), 35, facecolor=C_AMBER, alpha=0.8, edgecolor='none', zorder=32))

    # ==================================================================
    # MODULE 2: 7-CYLINDER RADIAL AERO-ENGINE
    # ==================================================================
    # Crankshaft Pin Position
    pin_x = R_CRANK * math.cos(theta_crank+math.pi/2) + RADIAL_C[0]
    pin_y = R_CRANK * math.sin(theta_crank+math.pi/2) + RADIAL_C[1]
    
    # Pre-render Background Cylinders & Hardware
    for i in range(NUM_CYL):
        dx = math.cos(PHI[i])
        dy = math.sin(PHI[i])
        
        c_base_x = RADIAL_C[0] + dx * 130
        c_base_y = RADIAL_C[1] + dy * 130
        
        pt0 = [c_base_x + dy*R_CYL, c_base_y - dx*R_CYL]
        pt1 = [c_base_x - dy*R_CYL, c_base_y + dx*R_CYL]
        pt2 = [pt1[0] + dx*CYL_H, pt1[1] + dy*CYL_H]
        pt3 = [pt0[0] + dx*CYL_H, pt0[1] + dy*CYL_H]
        
        ax.add_patch(patches.Polygon([pt0, pt1, pt2, pt3], fill=True, facecolor=C_HOUSING, edgecolor=C_TEXT, lw=3, zorder=1))

    # Solve Master Rod Kinematics (Cylinder 0)
    # Line from P to Y-axis. px^2 + (py - Pcyl_y)^2 = L^2
    m_dx_c = pin_x - RADIAL_C[0]
    m_dy_c = pin_y - RADIAL_C[1]
    
    dist_to_piston_0 = m_dy_c + math.sqrt(L_MASTER**2 - m_dx_c**2)
    pist_0_x = RADIAL_C[0]
    pist_0_y = RADIAL_C[1] + dist_to_piston_0
    
    # Current Absolute Angle of the Master Rod
    ang_master = math.atan2(pist_0_y - pin_y, pist_0_x - pin_x)

    ax.plot([pin_x, pist_0_x], [pin_y, pist_0_y], color=C_MASTER, lw=12, solid_capstyle='round', zorder=15)
    ax.plot([pin_x, pist_0_x], [pin_y, pist_0_y], color=C_TEXT, lw=2, zorder=16) # Inlay groove

    # Master Hub Base
    ax.add_patch(patches.Circle((pin_x, pin_y), R_HUB+10, facecolor=C_MASTER, edgecolor=C_TEXT, lw=3, zorder=14))

    # Resolve Articulating Rods & Pistons
    for i in range(NUM_CYL):
        cyl_dx = math.cos(PHI[i])
        cyl_dy = math.sin(PHI[i])
        
        pist_x, pist_y = 0.0, 0.0
        
        if i == 0:
            pist_x, pist_y = pist_0_x, pist_0_y
        else:
            # Articulating Hub Pin offset relative to Master Rod axis
            phi_rel = i * (2*math.pi / NUM_CYL)
            ang_pin = ang_master - math.pi/2 + phi_rel
            
            hx = pin_x + R_HUB * math.cos(ang_pin)
            hy = pin_y + R_HUB * math.sin(ang_pin)
            
            # Intersection with cylinder radial vector
            # (h_xc + d*cyl_dx)^2 + (h_yc + d*cyl_dy)^2 = L_ARTIC^2
            h_xc = hx - RADIAL_C[0]
            h_yc = hy - RADIAL_C[1]
            
            A = 1.0
            B = -2.0 * (h_xc * cyl_dx + h_yc * cyl_dy)
            C = h_xc**2 + h_yc**2 - L_ARTIC**2
            
            det = B**2 - 4*A*C
            d_val = (-B + math.sqrt(det)) / 2.0
            
            pist_x = RADIAL_C[0] + d_val * cyl_dx
            pist_y = RADIAL_C[1] + d_val * cyl_dy
            
            ax.plot([hx, pist_x], [hy, pist_y], color=C_ARTIC, lw=8, solid_capstyle='round', zorder=10)
            ax.add_patch(patches.Circle((hx, hy), 6, facecolor=C_TEXT, zorder=15))
        
        # Piston Block
        ax.add_patch(patches.Rectangle((pist_x - dy*25, pist_y + dx*25), 50, 30, 
            angle=math.degrees(PHI[i])-90, facecolor=C_CRANE, edgecolor=C_TEXT, lw=2, 
            rotation_point=(pist_x, pist_y), zorder=12))
            
        # Draw Thermodynamic Cycle Colours in Cylinder Head
        sim_ang = (theta_crank - PHI[i] + PSI[i]) % (4*math.pi)
        c_chamber = C_BG
        heat_alpha = 0.0
        spark = False
        
        if sim_ang < math.pi: 
            c_chamber = C_POWER
            heat_alpha = 1.0 - (sim_ang/math.pi)*0.5
            if sim_ang < 0.3: spark = True
        elif sim_ang < 2*math.pi:
            c_chamber = C_STEEL
            heat_alpha = 0.4
        elif sim_ang < 3*math.pi:
            c_chamber = C_ARTIC
            heat_alpha = 0.4
        else:
            c_chamber = C_COMP
            heat_alpha = 0.4 + ((sim_ang-3*math.pi)/math.pi)*0.4
            
        # Piston displacement calculations for volume colouring
        # Top of cylinder is approx R_CRANK + L_MASTER + 30
        max_reach = R_CRANK + L_MASTER + 60
        dist_c = math.sqrt((pist_x-RADIAL_C[0])**2 + (pist_y-RADIAL_C[1])**2)
        vol_len = max(max_reach - dist_c, 5)
        
        v_px = pist_x + cyl_dx * 35
        v_py = pist_y + cyl_dy * 35
        
        poly_vol = [
            [v_px + cyl_dy*R_CYL, v_py - cyl_dx*R_CYL],
            [v_px - cyl_dy*R_CYL, v_py + cyl_dx*R_CYL],
            [v_px - cyl_dy*R_CYL + cyl_dx*vol_len, v_py + cyl_dx*R_CYL + cyl_dy*vol_len],
            [v_px + cyl_dy*R_CYL + cyl_dx*vol_len, v_py - cyl_dx*R_CYL + cyl_dy*vol_len]
        ]
        ax.add_patch(patches.Polygon(poly_vol, facecolor=c_chamber, alpha=heat_alpha, edgecolor='none', zorder=2))
        
        # Spark Indicator
        spark_loc_x = RADIAL_C[0] + cyl_dx * max_reach
        spark_loc_y = RADIAL_C[1] + cyl_dy * max_reach
        ax.plot([spark_loc_x, spark_loc_x+cyl_dx*10], [spark_loc_y, spark_loc_y+cyl_dy*10], color=C_TEXT, lw=4, zorder=21)
        if spark:
            ax.add_patch(patches.Circle((spark_loc_x, spark_loc_y), 25, facecolor=C_AMBER, alpha=0.9, edgecolor='none', zorder=25))

    # Main Crankshaft Weights & Axis
    ax.add_patch(patches.Circle((RADIAL_C[0], RADIAL_C[1]), 35, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=12))
    weight_poly = [
        [RADIAL_C[0] - pin_y + RADIAL_C[1], RADIAL_C[1] + pin_x - RADIAL_C[0]],
        [RADIAL_C[0] + pin_y - RADIAL_C[1], RADIAL_C[1] - pin_x + RADIAL_C[0]],
        [RADIAL_C[0] - m_dx_c*0.8, RADIAL_C[1] - m_dy_c*0.8]
    ]
    ax.add_patch(patches.Polygon(weight_poly, facecolor=C_AMBER, edgecolor=C_TEXT, lw=3, zorder=11))
    ax.add_patch(patches.Circle((pin_x, pin_y), 15, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=16))

    # ==================================================================
    # MODULE 3: ABSOLUTE DAYLIGHT TELEMETRY
    # ==================================================================
    # Top Separation Bar
    ax.add_patch(plt.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [800, 800], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-460, 890, "LG-431 :: DUAL ROTARY KINEMATICS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, 840, "[TOP MATRIX]: O(1) WANKEL EPITROCHOID ROTARY", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    # Middle Division
    ax.plot([-460, 460], [0, 0], color=C_TEXT, lw=3, linestyle='dotted', zorder=81)
    ax.text(-460, -35, "[BTM MATRIX]: 7-CYLINDER RADIAL AERO-ENGINE (RECIPROCATING)", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    # Bottom Display
    ax.add_patch(plt.Rectangle((-540, -960), 1080, 200, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [-760, -760], color=C_TEXT, lw=6, zorder=81)
    
    crank_rpm = 30.0 * REVS_PER_LOOP # Visual RPM scale tracking mathematical loop
    ax.text(-460, -820, f"UNIVERSAL KINEMATIC SHAFT: {crank_rpm:04.0f} RPM", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, -870, f"WANKEL ROTOR YIELD       : {crank_rpm/3.0:04.0f} RPM", color=C_MASTER, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, -920, f"RADIAL 4-STROKE FIRING   : TRUE 1-3-5-7-2-4-6", color=C_ARTIC, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-431: DUAL ROTARY KINEMATICS (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    stream = generate_stream()

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, stream, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Trans-Rotational Mechanics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
