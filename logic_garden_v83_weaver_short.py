"""
SOVEREIGN CODE: logic_garden_v83_weaver_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Differential Diagnosis / Bayesian Filter
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v83_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 83: THE WEAVER")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000')
    
    # 100 Diseases with attributes
    # x, y, is_fever, is_stiff, is_rash
    points = []
    for _ in range(100):
        points.append({
            'x': random.uniform(-8, 8),
            'y': random.uniform(-12, 12),
            'fever': random.random() < 0.5,
            'stiff': random.random() < 0.3, # Rarer
            'rash': random.random() < 0.4,
            'active': True
        })
        
    # Force one "Gold" cluster
    target = points[0]
    target['fever'] = True; target['stiff'] = True; target['rash'] = True
    target['x'] = 0; target['y'] = 0
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        filter_text = "ALL DIAGNOSES"
        
        # APPLY FILTERS CHRONOLOGICALLY
        if f > 60:
            filter_text = "+ INPUT: FEVER"
            for p in points: 
                if not p['fever']: p['active'] = False
        
        if f > 180:
            filter_text = "+ INPUT: NECK STIFFNESS"
            for p in points:
                if not p['stiff']: p['active'] = False
                
        if f > 300:
            filter_text = "+ INPUT: RASH"
            for p in points:
                if not p['rash']: p['active'] = False
                
        # RENDER
        count = 0
        for p in points:
            if p['active']:
                count += 1
                col = '#444444' # Grey default
                size = 100
                
                # Highlight the survivor(s) at end
                if f > 300: 
                    col = '#FFD700' # Gold
                    size = 300
                    
                ax.scatter(p['x'], p['y'], s=size, color=col)
                
        # HUD
        ax.text(0, 14, "BAYESIAN FILTER", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        ax.text(0, 12, filter_text, color='#00FFFF', ha='center', fontsize=20, fontfamily='monospace')
        ax.text(0, -14, f"POSSIBILITIES: {count}", color='white', ha='center', fontsize=20, fontfamily='monospace')
        
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
