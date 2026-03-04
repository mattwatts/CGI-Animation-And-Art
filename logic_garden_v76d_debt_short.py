"""
SOVEREIGN CODE: logic_garden_v76_debt_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: High Interest Debt / Snowball Method
SCENARIO: $10k Credit Card Debt (20% APR)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v76_debt"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 76: DEBT TRAP")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0.15, 0.2, 0.7, 0.6], facecolor='#050505')
    
    # PARAMETERS
    PRINCIPAL = 10000
    RATE = 0.20 # 20% APR
    MONTHLY_RATE = RATE / 12
    
    # Strategy A: Minimum (2% of balance or $100)
    # Strategy B: Attack ($400 fixed)
    
    # Pre-simulate to find max time
    path_a = []
    path_b = []
    interest_a = []
    interest_b = []
    
    curr_a = PRINCIPAL
    curr_b = PRINCIPAL
    cum_int_a = 0
    cum_int_b = 0
    
    months = 0
    # Simulate 5 years (60 months)
    MAX_MONTHS = 60
    
    for m in range(MAX_MONTHS):
        path_a.append(curr_a)
        path_b.append(curr_b)
        interest_a.append(cum_int_a)
        interest_b.append(cum_int_b)
        
        # Calc Interest
        int_a = curr_a * MONTHLY_RATE
        int_b = curr_b * MONTHLY_RATE
        
        cum_int_a += int_a
        cum_int_b += int_b
        
        # Calc Payment
        pay_a = max(200, curr_a * 0.02) # Min payment floor
        pay_b = 400 # Fixed Attack
        
        # Apply
        if curr_a > 0: curr_a = curr_a + int_a - pay_a
        if curr_b > 0: curr_b = curr_b + int_b - pay_b
        
        if curr_a < 0: curr_a = 0
        if curr_b < 0: curr_b = 0
        
    for f in range(TOTAL_FRAMES):
        ax.clear()
        
        progress = f / float(TOTAL_FRAMES - 60)
        if progress > 1.0: progress = 1.0
        
        curr_idx = int(progress * MAX_MONTHS)
        if curr_idx >= MAX_MONTHS: curr_idx = MAX_MONTHS - 1
        
        # DATA
        bal_a = path_a[curr_idx]
        bal_b = path_b[curr_idx]
        wasted_a = interest_a[curr_idx]
        wasted_b = interest_b[curr_idx]
        
        # RENDER
        ax.set_ylim(0, 15000) # Headroom for interest pile
        ax.set_xlim(0, 3)
        ax.axis('off')
        
        # LEFT (MINIMUM)
        # The Debt
        plt.Rectangle((0.5, 0), 0.8, bal_a, color='#FF0000').set_label('Debt')
        ax.add_patch(plt.Rectangle((0.5, 0), 0.8, bal_a, color='#FF0000'))
        
        # The Waste (Interest Accumulator - shown as "Trash" at bottom? 
        # Actually better to show it "Growing" on top to show total cost?
        # Let's show it as a grey pile BENEATH the floor y=0 using negative?
        # No, let's stack it on top to show "Total Burden"
        # Or distinct pile behind. Distinct pile behind is better.
        
        # Render Debt Bar
        ax.add_patch(plt.Rectangle((0.5, 0), 0.8, bal_a, color='#FF0000'))
        # Render Waste (Ghost Bar rising from floor behind)
        ax.add_patch(plt.Rectangle((0.5, 0), 0.8, wasted_a, color='#444444', alpha=0.5, zorder=0))
        
        # RIGHT (ATTACK)
        ax.add_patch(plt.Rectangle((1.7, 0), 0.8, bal_b, color='#00FF00'))
        ax.add_patch(plt.Rectangle((1.7, 0), 0.8, wasted_b, color='#444444', alpha=0.5, zorder=0))

        # TEXT VALUES
        ax.text(0.9, bal_a + 500, f"${int(bal_a):,}", color='#FF0000', ha='center', fontsize=20, fontfamily='monospace', weight='bold')
        ax.text(2.1, bal_b + 500, f"${int(bal_b):,}", color='#00FF00', ha='center', fontsize=20, fontfamily='monospace', weight='bold')
        
        # Waste Label
        if wasted_a > 1000:
            ax.text(0.9, wasted_a, f"WASTE:\n${int(wasted_a):,}", color='#888888', ha='center', fontsize=15, fontfamily='monospace')

        # LABELS
        ax.text(0.9, -1500, "MINIMUM\n($200)", color='white', ha='center', fontsize=18, fontfamily='monospace')
        ax.text(2.1, -1500, "ATTACK\n($400)", color='white', ha='center', fontsize=18, fontfamily='monospace')
        
        # HUD
        ax.text(1.5, 14000, "THE DEBT TRAP", color='white', ha='center', fontsize=30, weight='bold', fontfamily='monospace')
        ax.text(1.5, 13000, f"MONTH: {curr_idx}", color='#AAAAAA', ha='center', fontsize=20, fontfamily='monospace')

        # VICTORY STATE
        if bal_b == 0 and progress < 1.0:
            ax.text(2.1, 5000, "FREEDOM", color='#00FF00', ha='center', fontsize=25, weight='bold', rotation=45, bbox=dict(facecolor='black'))
            
        if progress >= 1.0:
             # Final comparison
             ax.text(1.5, 7500, "INTEREST\nEATS YOU ALIVE", color='white', ha='center', fontsize=35, weight='bold', fontfamily='monospace',
                    bbox=dict(facecolor='black', edgecolor='red'))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
