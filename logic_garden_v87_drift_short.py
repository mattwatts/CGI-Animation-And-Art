"""
SOVEREIGN CODE: logic_garden_v87_drift_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Cushing's Triad / Pre-Code Warning
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from collections import deque

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v87_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 87: THE DRIFT")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    
    # 3 Subplots vertically
    ax1 = fig.add_axes([0.1, 0.7, 0.8, 0.2], facecolor='#111111') # BP
    ax2 = fig.add_axes([0.1, 0.4, 0.8, 0.2], facecolor='#111111') # HR
    ax3 = fig.add_axes([0.1, 0.1, 0.8, 0.2], facecolor='#111111') # RR
    
    # Data Buffers
    window = 100
    bp_data = deque([120]*window, maxlen=window)
    hr_data = deque([80]*window, maxlen=window)
    rr_data = deque([16]*window, maxlen=window)
    
    curr_bp = 120.0
    curr_hr = 80.0
    
    for f in range(TOTAL_FRAMES):
        # Update Data (The Trend)
        if f > 30:
            # Cushing's Trend: BP Up, HR Down
            curr_bp += 0.2 + np.random.normal(0, 1) # Noise
            curr_hr -= 0.15 + np.random.normal(0, 1)
            
            # RR becomes irregular (Widening sine)
            rr_val = 16 + np.sin(f*0.1) * (f/50) # Amplitude grows (Cheyne-Stokes-ish)
        else:
            rr_val = 16
            
        bp_data.append(curr_bp)
        hr_data.append(curr_hr)
        rr_data.append(rr_val)
        
        # RENDER BP
        ax1.clear(); ax1.set_xticks([]); ax1.set_facecolor('#111111')
        ax1.set_ylim(100, 220)
        ax1.plot(bp_data, color='#FF0000', linewidth=3)
        ax1.text(0, 200, f"SYS BP: {int(curr_bp)} ^", color='#FF0000', fontsize=15, weight='bold')
        
        # RENDER HR
        ax2.clear(); ax2.set_xticks([]); ax2.set_facecolor('#111111')
        ax2.set_ylim(40, 100)
        ax2.plot(hr_data, color='#00FFFF', linewidth=3)
        ax2.text(0, 90, f"HR: {int(curr_hr)} v", color='#00FFFF', fontsize=15, weight='bold')
        
        # RENDER RR
        ax3.clear(); ax3.set_xticks([]); ax3.set_facecolor('#111111')
        ax3.set_ylim(0, 40)
        ax3.plot(rr_data, color='#FFFF00', linewidth=3)
        ax3.text(0, 35, "RESPIRATION: IRREGULAR", color='#FFFF00', fontsize=15, weight='bold')
        
        # VISUAL JAW (Arrows between plot 1 and 2)
        # We draw this on the figure coordinates? No, can't easily cross axes.
        # Just stick to graphs.
        
        # HUD
        fig.text(0.5, 0.95, "CUSHING'S TRIAD", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        
        # ALERT
        if curr_bp > 180 and curr_hr < 50:
             fig.text(0.5, 0.65, "HERNIATION IMMINENT", color='red', ha='center', fontsize=20, weight='bold', bbox=dict(facecolor='black'))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
