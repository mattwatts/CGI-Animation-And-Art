"""
SOVEREIGN CODE: logic_garden_v76_inflation_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Inflation / Purchasing Power
SCENARIO: $10k Invested vs $10k Cash (20 Years)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v76_inflation"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 76: INFLATION")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0.15, 0.2, 0.7, 0.6], facecolor='#050505')
    
    # PARAMETERS
    START_VAL = 10000
    YEARS = 20
    MONTHS = YEARS * 12
    
    # GROWS: 7% return
    # SHRINKS: 3% inflation decay
    
    val_invest = [START_VAL]
    val_cash = [START_VAL]
    
    for m in range(MONTHS):
        # Invest: Compounding Up
        val_invest.append(val_invest[-1] * (1 + 0.07/12))
        # Cash: Compounding Down (Purchasing Power)
        val_cash.append(val_cash[-1] * (1 - 0.03/12))
        
    for f in range(TOTAL_FRAMES):
        ax.clear()
        
        # TIME MAPPING
        progress = f / float(TOTAL_FRAMES - 60) # Leave 2s at end
        if progress > 1.0: progress = 1.0
        
        curr_idx = int(progress * MONTHS)
        curr_year = int(curr_idx / 12)
        
        v_inv = val_invest[curr_idx]
        v_csh = val_cash[curr_idx]
        
        # RENDER BARS
        ax.set_ylim(0, 40000) # Max growth approx 38k
        ax.set_xlim(0, 3)
        ax.axis('off')
        
        # Left Bar (Invested)
        rect_inv = plt.Rectangle((0.5, 0), 0.8, v_inv, color='#00CCFF')
        ax.add_patch(rect_inv)
        
        # Right Bar (Cash)
        # We start at 10k. As it shrinks, we visualize the "Ghost" of what was lost
        rect_cash = plt.Rectangle((1.7, 0), 0.8, v_csh, color='#FF4500')
        ax.add_patch(rect_cash)
        
        # The "Lost Value" Ghost (Outline)
        rect_ghost = plt.Rectangle((1.7, v_csh), 0.8, START_VAL - v_csh, edgecolor='#333333', hatch='//', facecolor='none', linewidth=2)
        ax.add_patch(rect_ghost)
        
        # TEXT LABELS
        # Values
        ax.text(0.9, v_inv + 1000, f"${int(v_inv):,}", color='#00CCFF', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        ax.text(2.1, v_csh + 1000, f"${int(v_csh):,}", color='#FF4500', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        
        # Base Labels
        ax.text(0.9, -2000, "ASSET\n(+7%)", color='white', ha='center', fontsize=20, fontfamily='monospace')
        ax.text(2.1, -2000, "CASH\n(-3%)", color='white', ha='center', fontsize=20, fontfamily='monospace')
        
        # HUD
        ax.text(1.5, 38000, f"YEAR: {curr_year}", color='white', ha='center', fontsize=30, weight='bold', fontfamily='monospace')
        ax.text(1.5, 36000, "THE SILENT THIEF", color='#AAAAAA', ha='center', fontsize=20, fontfamily='monospace')

        # FINAL MESSAGE
        if progress >= 1.0:
            ax.text(1.5, 20000, "SAFE IS RISKY", color='white', ha='center', fontsize=40, weight='bold', fontfamily='monospace',
                   bbox=dict(facecolor='black', edgecolor='red', boxstyle='round,pad=0.5'))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
