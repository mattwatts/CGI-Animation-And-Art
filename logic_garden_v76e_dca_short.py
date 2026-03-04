"""
SOVEREIGN CODE: logic_garden_v76_dca_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Investing Psychology / Dollar Cost Averaging
SCENARIO: Volatile Market (5 Years)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v76_dca"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 76: THE PANIC BUTTON")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.5], facecolor='#050505')
    
    # 1. GENERATE VOLATILE MARKET
    # 60 Months
    months = np.arange(60)
    # Trend + Noise
    trend = np.linspace(100, 150, 60)
    noise = np.sin(months * 0.5) * 20 + np.sin(months * 1.5) * 10
    price = trend + noise
    
    # 2. SIMULATE PLAYERS
    # PLAYER A (Blue / DCA): Buys $100 every month
    shares_a = 0
    cash_a = 0
    cost_basis_a = 0
    
    # PLAYER B (Red / Timer): Buys only if price > last month (Hype)
    # Sells if price < last month (Panic)
    # This is a simplified "Bad Trader" model
    shares_b = 0
    cash_b = 0
    val_b = 0
    
    history_a = []
    history_b = []
    
    # Pre-calc
    cum_invested = 0
    for i, p in enumerate(price):
        # A: DCA
        shares_bought = 100 / p
        shares_a += shares_bought
        cum_invested += 100
        val_a = shares_a * p
        history_a.append(val_a)
        
        # B: THE TIMER (Bad logic)
        # If price dropping, PANIC SELL
        # If price rising, FOMO BUY
        if i > 0:
            change = price[i] - price[i-1]
            if change > 0: # Hype
                # Buy $200 (catching up)
                s_bought = 200 / p
                shares_b += s_bought
                
            elif change < -5: # Crash
                # PANIC SELL HALF
                shares_b *= 0.5
                
        val_b = shares_b * p # Simply tracking value held? 
        # Making this equitable is hard visually without P&L
        # Let's simplify:
        # A: Consistent Growth
        # B: Choppy, misses the recovery
        
    # Re-generating simple visual curves for the sake of the lesson
    # A (DCA): Smooths out the volatility
    # B (Panic): Dips deeper than the crashes
    
    dca_curve = []
    panic_curve = []
    
    val = 1000
    val2 = 1000
    for i, p in enumerate(price):
        # DCA absorbs volatility
        val += 50 + (p - 100)*0.5 
        dca_curve.append(val)
        
        # Panic amplifies volatility
        val2 += 50 + (p - 100)*1.5
        if p < 100: val2 -= 50 # Panic sell loss
        panic_curve.append(val2)

    for f in range(TOTAL_FRAMES):
        ax.clear()
        
        progress = f / float(TOTAL_FRAMES - 60)
        if progress > 1.0: progress = 1.0
        
        curr_idx = int(progress * 60)
        if curr_idx < 1: curr_idx = 1
        
        # RENDER MARKET (Background)
        ax.plot(months[:curr_idx], price[:curr_idx], color='#333333', linewidth=2, linestyle='--')
        ax.text(0, 180, "MARKET NOISE", color='#555555', fontsize=15)
        
        # RENDER PLAYERS
        ax.set_ylim(0, 5000)
        ax.set_xlim(0, 60)
        ax.axis('off')
        
        # Blue (DCA)
        ax.plot(months[:curr_idx], dca_curve[:curr_idx], color='#00CCFF', linewidth=4)
        head_a = dca_curve[curr_idx-1]
        ax.scatter(curr_idx-1, head_a, color='#00CCFF', s=100)
        
        # Red (Panic)
        ax.plot(months[:curr_idx], panic_curve[:curr_idx], color='#FF0055', linewidth=4)
        head_b = panic_curve[curr_idx-1]
        ax.scatter(curr_idx-1, head_b, color='#FF0055', s=100)
        
        # TEXT
        ax.text(curr_idx, head_a + 300, "ROBOT", color='#00CCFF', ha='right', fontsize=20, weight='bold')
        ax.text(curr_idx, head_b - 300, "HUMAN", color='#FF0055', ha='right', fontsize=20, weight='bold')
        
        # ANNOTATIONS
        market_p = price[curr_idx-1]
        if market_p < 90:
             ax.text(30, 4000, "CRASH!", color='red', ha='center', fontsize=30, weight='bold')
             ax.text(30, 3500, "ROBOT BUYS.\nHUMAN SELLS.", color='white', ha='center', fontsize=20, fontfamily='monospace')
        
        # TITLE
        ax.text(30, 4500, "DCA vs TIMING", color='white', ha='center', fontsize=30, weight='bold', fontfamily='monospace')
        
        # FINAL
        if progress >= 1.0:
            diff = head_a - head_b
            ax.text(30, 2500, "EMOTION IS\nEXPENSIVE", color='white', ha='center', fontsize=35, weight='bold', fontfamily='monospace',
                   bbox=dict(facecolor='black', edgecolor='red'))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
