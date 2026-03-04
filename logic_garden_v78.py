"""
SOVEREIGN CODE: logic_garden_v78_boolean_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Logic Gates
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import itertools

FPS, DURATION = 30, 16 
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v78_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 78: BOOLEAN (SHORT FORMAT)")
    states = list(itertools.product([0, 1], repeat=2))
    
    fig = plt.figure(figsize=(9, 16), facecolor='#222222')
    
    col_off, col_on = '#444444', '#00FF00'
    
    for f in range(TOTAL_FRAMES):
        fig.clf()
        
        # Determine State
        state_idx = (f // 120) % 4
        A, B = states[state_idx]
        
        cA = col_on if A else col_off
        cB = col_on if B else col_off
        
        # --- HEADER (INPUTS) ---
        ax_h = fig.add_axes([0, 0.85, 1, 0.15], facecolor='#111111')
        ax_h.axis('off')
        ax_h.text(0.3, 0.5, f"A={A}", color=cA, fontsize=40, weight='bold', ha='center', va='center')
        ax_h.text(0.7, 0.5, f"B={B}", color=cB, fontsize=40, weight='bold', ha='center', va='center')
        
        # --- 1. AND GATE (Top) ---
        ax1 = fig.add_axes([0.1, 0.6, 0.8, 0.2], facecolor='#222222')
        ax1.axis('off')
        res_and = A and B
        cRes = col_on if res_and else col_off
        
        ax1.text(0.5, 0.8, "AND (BOTH)", color='white', ha='center', fontsize=15)
        # Visual
        circle = plt.Circle((0.5, 0.4), 0.2, color='#333333', ec='white')
        ax1.add_patch(circle)
        ax1.add_patch(plt.Rectangle((0.4, 0.3), 0.2, 0.2, color=cRes)) # LED
        
        # --- 2. OR GATE (Mid) ---
        ax2 = fig.add_axes([0.1, 0.35, 0.8, 0.2], facecolor='#222222')
        ax2.axis('off')
        res_or = A or B
        cRes = col_on if res_or else col_off
        
        ax2.text(0.5, 0.8, "OR (ANY)", color='white', ha='center', fontsize=15)
        rect = plt.Rectangle((0.3, 0.2), 0.4, 0.4, color='#333333', ec='white')
        ax2.add_patch(rect)
        ax2.add_patch(plt.Rectangle((0.4, 0.3), 0.2, 0.2, color=cRes)) # LED

        # --- 3. XOR GATE (Low) ---
        ax3 = fig.add_axes([0.1, 0.1, 0.8, 0.2], facecolor='#222222')
        ax3.axis('off')
        res_xor = A ^ B
        cRes = col_on if res_xor else col_off
        
        ax3.text(0.5, 0.8, "XOR (ONLY ONE)", color='white', ha='center', fontsize=15)
        poly = plt.Polygon([[0.3, 0.2], [0.7, 0.2], [0.5, 0.6]], color='#333333', ec='white')
        ax3.add_patch(poly)
        ax3.add_patch(plt.Rectangle((0.45, 0.25), 0.1, 0.1, color=cRes)) # LED

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#222222')
        
    plt.close(fig)

if __name__ == "__main__": run()
