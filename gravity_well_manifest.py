import numpy as np
from PIL import Image
import scipy.ndimage
import os
import sys

# --- CONFIGURATION NODE ---
INPUT_FILENAME = "tardis.png"  # Target File
OUTPUT_DIR = "render_sequence"
TOTAL_FRAMES = 240
FPS = 60

# Physics Parameters
WAVE_AMPLITUDE = 30.0    # Maximum pixel displacement
WAVE_FREQUENCY = 0.05    # Tightness of the rings
WAVE_SPEED = 0.2         # Phase velocity
DECAY_FACTOR = 0.005     # How fast the gravity well fades at edges (Gaussian sigma)

# Sequence Timeline (in frames)
# [Still] -> [Ramp Up] -> [Sustain Ripple] -> [Ramp Down] -> [Still]
T_START_RAMP = 30
T_END_RAMP = 90
T_START_DECAY = 150
T_END_DECAY = 210

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def smoothstep(edge0, edge1, x):
    """Hermite interpolation for glass-smooth transitions."""
    x = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return x * x * (3 - 2 * x)

def apply_gravity_well(image_array, intensity, time_phase):
    """
    Applies a radial sine-wave distortion weighted by distance (Gravity Well).
    Returns the distorted image array.
    """
    h, w, channels = image_array.shape
    center_y, center_x = h / 2.0, w / 2.0

    # 1. Create the Coordinate Grid (The 'Fabric of Space')
    # We use float32 for "Industrial" precision without "Heavy Industry" memory cost
    y, x = np.indices((h, w), dtype=np.float32)
    
    # 2. Convert to Polar Coordinates relative to center
    dx = x - center_x
    dy = y - center_y
    radius = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)

    # 3. Calculate the Displacement ('The Ripple')
    # A sine wave travels outwards (-time_phase), dampened by distance (exp decay)
    # The 'intensity' controls the global amplitude (0.0 to 1.0)
    distortion = np.sin(radius * WAVE_FREQUENCY - time_phase) 
    damping = np.exp(-radius * DECAY_FACTOR)
    
    offset_r = intensity * WAVE_AMPLITUDE * distortion * damping

    # 4. Map back to Source Coordinate Space (Inverse Mapping)
    # New sample coordinates = Original coordinates - displacement
    # We subtract because we are "pulling" the pixels to the new location
    source_r = radius - offset_r
    
    map_x = center_x + source_r * np.cos(theta)
    map_y = center_y + source_r * np.sin(theta)

    # 5. Sampling ('The Synthesiser')
    # We loop through channels to handle RGB/RGBA correctly
    distorted_image = np.zeros_like(image_array)
    
    for c in range(channels):
        # Order=1 (Bilinear) is fast; Order=3 (Bicubic) is "Glass Smooth"
        # mode='reflect' mirrors the edges to fill the void, preventing black borders
        distorted_image[:, :, c] = scipy.ndimage.map_coordinates(
            image_array[:, :, c], 
            [map_y, map_x], 
            order=1, 
            mode='reflect'
        )
        
    return distorted_image

def main():
    print(f"[*] Initializing Protocol: Gravity Well Ripple")
    ensure_dir(OUTPUT_DIR)

    # Ingestion
    try:
        img = Image.open(INPUT_FILENAME).convert('RGB')
        img_data = np.array(img)
        print(f"[*] Signal Acquired: {INPUT_FILENAME} {img_data.shape}")
    except FileNotFoundError:
        print(f"[!] Critical Failure: '{INPUT_FILENAME}' not found in local sector.")
        sys.exit(1)

    # Execution Loop
    for frame in range(TOTAL_FRAMES):
        # Calculate Time Phase (Linear Flow)
        t = frame
        
        # Calculate Intensity (The Envelope)
        intensity = 0.0
        
        if frame < T_START_RAMP:
             # Phase 1: Still
            intensity = 0.0
        elif T_START_RAMP <= frame < T_END_RAMP:
            # Phase 2: Ramp Up (Smoothstep)
            intensity = smoothstep(T_START_RAMP, T_END_RAMP, frame)
        elif T_END_RAMP <= frame < T_START_DECAY:
            # Phase 3: Sustain Max
            intensity = 1.0
        elif T_START_DECAY <= frame < T_END_DECAY:
            # Phase 4: Ramp Down (Smoothstep Inverse)
            intensity = 1.0 - smoothstep(T_START_DECAY, T_END_DECAY, frame)
        else:
            # Phase 5: Still
            intensity = 0.0

        # Optimization: Skip processing if intensity is effectively zero
        if intensity < 0.001:
            result_data = img_data
        else:
            # Shift phase over time to animate the ripple
            phase = frame * WAVE_SPEED
            result_data = apply_gravity_well(img_data, intensity, phase)

        # Output Node
        out_name = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
        Image.fromarray(result_data.astype(np.uint8)).save(out_name)
        
        # Flight Recorder Log
        sys.stdout.write(f"\r[>] Rendering Frame: {frame}/{TOTAL_FRAMES} | Intensity: {intensity:.4f}")
        sys.stdout.flush()

    print("\n[*] Sequence Complete. Ready for stitching.")

if __name__ == "__main__":
    main()
