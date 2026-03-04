"""
SOVEREIGN CODE: logic_garden_v76_compound_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Financial Independence / Compound Interest
SCENARIO: The Cost of Waiting (Starting at 20 vs 30)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v76_short"
os.makedirs(OUT_DIR, exist_ok=True)

def calculate_compound(monthly, years, rate=0.08):
    months = years * 12
    balance = []
    curr = 0
    r_monthly = rate / 12
    for m in range(months):
        curr = (curr + monthly) * (1 + r_monthly)
        balance.append(curr)
    return balance

def run():
    print("LOGIC GARDEN 76: THE COST OF WAITING")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0.1, 0.2, 0.8, 0.6], facecolor='#050505') # Graph in middle
    
    # PARAMETERS
    # Person A: Starts age 20, Ends 60. $300/mo.
    # Person B: Starts age 30, Ends 60. $600/mo.
    
    AGE_START = 20
    AGE_END = 60
    TOTAL_YEARS = AGE_END - AGE_START
    TOTAL_MONTHS = TOTAL_YEARS * 12
    
    # Generate Data
    # A: Full run
    data_a = calculate_compound(300, TOTAL_YEARS) # 40 years
    
    # B: Delayed 10 years (120 months)
    zeros = [0] * 120
    data_b_growth = calculate_compound(600, TOTAL_YEARS - 10) # 30 years
    data_b = zeros + data_b_growth
    
    max_val = max(data_a[-1], data_b[-1])
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        
        # Timing: Map frames to Months
        # We want to scroll through time
        progress = f / float(TOTAL_FRAMES-60) # Save last 2s for static result
        if progress > 1.0: progress = 1.0
        
        current_month = int(progress * TOTAL_MONTHS)
        current_age = AGE_START + (current_month / 12.0)
        
        # Plot Logic
        ax.set_xlim(0, TOTAL_MONTHS)
        ax.set_ylim(0, max_val * 1.1)
        ax.axis('off')
        
        # Use full vectors up to current time
        if current_month > 1:
            indices = np.arange(current_month)
            
            # PLOT A (BLUE)
            ax.plot(indices, data_a[:current_month], color='#00CCFF', linewidth=4)
            # Head A
            val_a = data_a[current_month-1]
            ax.scatter(current_month-1, val_a, color='#00CCFF', s=100, zorder=10)
            
            # PLOT B (RED)
            if current_month > 120:
                ax.plot(indices[120:], data_b[120:current_month], color='#FF0055', linewidth=4)
                # Head B
                val_b = data_b[current_month-1]
                ax.scatter(current_month-1, val_b, color='#FF0055', s=100, zorder=10)
            else:
                val_b = 0
            
            # Gap Fill (Visualizing the Loss)
            if current_month > 120:
                ax.fill_between(indices[120:], data_a[120:current_month], data_b[120:current_month], 
                                color='#222222', alpha=0.5)

            # LIVE STATS (Top of Screen)
            # Fixed text position geometry
            ax.text(TOTAL_MONTHS*0.1, max_val, f"AGE: {int(current_age)}", color='white', fontsize=30, weight='bold', fontfamily='monospace')
            
            # A Label
            ax.text(TOTAL_MONTHS*0.5, max_val * 0.9, f"EARLY ($300): ${int(val_a):,}", color='#00CCFF', ha='right', fontsize=20, fontfamily='monospace', weight='bold')
            
            # B Label
            ax.text(TOTAL_MONTHS*0.5, max_val * 0.8, f"LATE ($600): ${int(val_b):,}", color='#FF0055', ha='right', fontsize=20, fontfamily='monospace', weight='bold')
            
            # The Lesson
            if current_age < 30:
                status = "STARTING EARLY..."
                col = '#00CCFF'
            elif current_age < 50:
                 status = "DOUBLING EFFORT..."
                 col = '#FF0055'
            else:
                 status = "MATH IS MERCILESS"
                 col = 'white'
            
            ax.text(TOTAL_MONTHS/2, max_val * 0.1, status, color=col, ha='center', fontsize=25, weight='bold', fontfamily='monospace')

        # FINAL POP (Last 60 frames)
        if progress >= 1.0:
            diff = data_a[-1] - data_b[-1]
            ax.text(TOTAL_MONTHS/2, max_val/2, f"THE GAP:\n${int(diff):,}", color='white', ha='center', fontsize=40, weight='bold', fontfamily='monospace',
                   bbox=dict(facecolor='black', alpha=0.8, edgecolor='white'))
            
            ax.text(TOTAL_MONTHS/2, max_val * 0.65, "YOU CANNOT\nCATCH UP", color='#FF0055', ha='center', fontsize=30, weight='bold', fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
