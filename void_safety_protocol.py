import numpy as np
import os
import time
import subprocess
import multiprocessing
import gc
import sys
from PIL import Image

# [so-100] INDUSTRIALIST CONFIGURATION (SAFE MODE)
VOID_CONFIG = {
    # -- CANVAS --
    "WIDTH": 1920,
    "HEIGHT": 1080,
    "FPS": 30,
    "DURATION_SEC": 10,
    
    # -- SAFETY PROTOCOLS --
    # CRITICAL: Keep this LOW (2 or 3) to prevent RAM saturation.
    "CORES": 2,  
    
    # -- I/O --
    "OUTPUT_DIR": "void_safe_render",
    "VIDEO_FILENAME": "void_fluid_safe.mp4",
    
    # -- PHYSICS --
    "COLOR_DEEP": np.array([0, 5, 20], dtype=np.float32),
    "COLOR_IKB":  np.array([0, 47, 167], dtype=np.float32),
    "COLOR_CYAN": np.array([0, 100, 255], dtype=np.float32),
}

def render_frame_safe(frame_data):
    """
    Optimized Worker Node.
    Uses float32 and in-place operations to minimize RAM footprint.
    """
    idx, total_frames, cfg = frame_data
    
    # Time (Linear)
    t = np.float32((idx / total_frames) * cfg['DURATION_SEC'])
    
    width = cfg['WIDTH']
    height = cfg['HEIGHT']
    
    try:
        # 1. ALLOCATE COORDINATES (FLOAT32)
        # We perform aspect correction immediately
        aspect = np.float32(width / height)
        
        # Create grid directly in float32
        x = np.linspace(-aspect, aspect, width, dtype=np.float32)
        y = np.linspace(-1.0, 1.0, height, dtype=np.float32)
        X, Y = np.meshgrid(x, y) # Allocates 2 arrays
        
        # 2. DOMAIN WARPING (Reuse memory where possible)
        # Warp 1 (Base Flow)
        # We use explicit temporary variables to avoid keeping large intermediates
        
        # qx = X + 2.0 * sin(...)
        # We calculate the modifier first, then add X
        modifier = Y * 2.0
        modifier += (t * 0.2)
        np.sin(modifier, out=modifier) # In-place sin
        modifier *= 2.0
        X += modifier # In-place add (X is now warped qx)
        
        # qy = Y + 2.0 * cos(...)
        modifier = X * 2.4 # Note: X is already warped, this adds turbulence
        modifier -= (t * 0.3)
        np.cos(modifier, out=modifier)
        modifier *= 2.0
        Y += modifier # In-place add (Y is now warped qy)
        
        # Warp 2 (Turbulence) - modifying X/Y further
        # r_x calculation using current Y
        turb_mod = Y * 3.5
        turb_mod += (t * 0.4)
        np.sin(turb_mod, out=turb_mod)
        # We need to store r_x separately because we need original X for r_y? 
        # Actually in fluid sim, iterative warping is fine.
        X += turb_mod 
        
        # r_y calculation
        turb_mod = X * 3.2 # Uses the doubly warped X, increasing chaos
        turb_mod += (t * 0.4)
        np.cos(turb_mod, out=turb_mod)
        Y += turb_mod
        
        # 3. PIGMENT DENSITY (Fractal Sum)
        # val = 0.5 * sin(X*4 + ...)
        val = X * 4.0
        val += (t * 0.1)
        np.sin(val, out=val)
        val *= 0.5
        
        # Add layer 2
        layer2 = Y * 8.3
        layer2 -= (t * 0.2)
        np.sin(layer2, out=layer2)
        layer2 *= 0.25
        val += layer2
        
        # Add layer 3 (Interference)
        layer3 = X + Y
        layer3 *= 12.7
        layer3 += (t * 0.5)
        np.cos(layer3, out=layer3)
        layer3 *= 0.125
        val += layer3
        
        # Normalize roughly [0, 1]
        val *= 0.5
        val += 0.5
        
        # Clean up coordinates to free RAM
        del X, Y, modifier, turb_mod, layer2, layer3
        
        # 4. COLOR MAPPING
        # Pulse
        pulse = 0.5 + 0.5 * np.sin(t * 0.5 * 2 * np.pi)
        
        # Hermite Interpolation (Smoothstep) for Deep -> IKB
        # t = clip((x - edge0) / (edge1 - edge0), 0, 1)
        # edge0=0.0, edge1=0.6
        mix_factor = np.clip(val / 0.6, 0.0, 1.0)
        mix_factor = mix_factor * mix_factor * (3.0 - 2.0 * mix_factor) # Smoothstep
        
        # Pre-calc colors (Normalized 0-1)
        c_deep = cfg['COLOR_DEEP'] / 255.0
        c_ikb  = cfg['COLOR_IKB'] / 255.0
        c_cyan = cfg['COLOR_CYAN'] / 255.0
        
        # Alloc Output Image (H, W, 3) - float32
        out_img = np.zeros((height, width, 3), dtype=np.float32)
        
        # Broadcast mixing: Deep -> IKB
        # out = (1-mix) * deep + mix * ikb
        # rewritten: deep + mix * (ikb - deep)
        out_img[:] = c_deep
        delta_c = c_ikb - c_deep
        
        # Apply mix_factor (broadcasting height x width x 1 against h x w x 3)
        mix_broad = mix_factor[..., np.newaxis]
        out_img += mix_broad * delta_c
        
        # Highlights (IKB -> Cyan)
        # Edge0=0.75, Edge1=1.0
        mix_high = np.clip((val - 0.75) / 0.25, 0.0, 1.0)
        mix_high = mix_high * mix_high * (3.0 - 2.0 * mix_high)
        
        # Modulate highlights by pulse
        pulse_mod = 0.6 + 0.4 * pulse
        mix_high *= pulse_mod
        
        delta_high = c_cyan - out_img # Difference from current pixel to Cyan
        mix_high_broad = mix_high[..., np.newaxis]
        
        # Apply highlights
        out_img += mix_high_broad * delta_high
        
        # 5. GRAIN (Texture)
        # Generate grain directly into a temp buffer
        noise = np.random.normal(0, 0.035, (height, width)).astype(np.float32)
        out_img += noise[..., np.newaxis]
        
        del noise, mix_factor, mix_high, mix_broad, mix_high_broad, val
        
        # 6. SAVE
        out_img = np.clip(out_img, 0.0, 1.0)
        out_img *= 255.0
        
        img = Image.fromarray(out_img.astype(np.uint8))
        filepath = os.path.join(cfg['OUTPUT_DIR'], f"frame_{idx:04d}.png")
        img.save(filepath, compress_level=0)
        
        del out_img, img
        gc.collect() # Force cleanup
        
        return None
        
    except Exception as e:
        return f"Error: {e}"

def compile_video(cfg):
    print(f"\n > [The Synthesiser] Binding artifacts with FFmpeg...")
    input_pattern = os.path.join(cfg['OUTPUT_DIR'], "frame_%04d.png")
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(cfg['FPS']),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p",
        "-crf", "16",
        "-preset", "slow",
        "-tune", "grain",
        "-movflags", "+faststart",
        cfg['VIDEO_FILENAME']
    ]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(f" > [Target Acquired] {cfg['VIDEO_FILENAME']}")
    except subprocess.CalledProcessError as e:
        print(f" > [Error] FFmpeg failed: {e.stderr.decode()}")

def main():
    total_frames = VOID_CONFIG['FPS'] * VOID_CONFIG['DURATION_SEC']
    os.makedirs(VOID_CONFIG['OUTPUT_DIR'], exist_ok=True)
    
    print(f"--- VOID GENERATOR (SAFETY PROTOCOL) ---")
    print(f" > Target: {VOID_CONFIG['WIDTH']}x{VOID_CONFIG['HEIGHT']}")
    print(f" > Cores:  {VOID_CONFIG['CORES']} (Throttled for Stability)")
    
    jobs = [(i, total_frames, VOID_CONFIG) for i in range(total_frames)]
    
    start_time = time.time()
    
    # Use Pool with constrained cores
    with multiprocessing.Pool(processes=VOID_CONFIG['CORES']) as pool:
        results = pool.imap_unordered(render_frame_safe, jobs, chunksize=1)
        
        for i, _ in enumerate(results):
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (total_frames - (i + 1)) / (rate + 1e-5)
            
            # Simple Progress
            sys.stdout.write(f"\r > Rendering Frame {i+1}/{total_frames} | {rate:.2f} FPS | ETA: {remaining:.0f}s")
            sys.stdout.flush()
            
    print(f"\n > Render Complete. Time: {time.time() - start_time:.2f}s")
    compile_video(VOID_CONFIG)

if __name__ == "__main__":
    main()
