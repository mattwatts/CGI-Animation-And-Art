import time
import os
import subprocess
import gc
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

try:
    import cupy as cp
except ImportError:
    raise ImportError("CupY missing")

OUTPUT_DIR = "ikb_entropic_void_v3"
RESOLUTION = 1000
TOTAL_FRAMES = 900
GPU_DUTY_CYCLE = 0.6
INITIAL_SCALE = 160.0
TIME_STEP = 0.007

MACRO_PULSE_FREQ = 0.04
MICRO_PULSE_FREQ = 0.8
DRIFT_FREQ = 0.02
WARP_FREQ = 0.015
ENTROPY_RATE = 0.0015
GRAIN_INTENSITY = 0.05

# --- CUDA KERNEL: FBM (STRICT FLOAT) ---
entropic_kernel = r'''
extern "C" {

__device__ float fract(float x) { return x - floorf(x); }
__device__ float lerp(float a, float b, float t) { return a + t*(b-a); }

__device__ float hash(float n) { return fract(sinf(n) * 43758.5453123f); }

__device__ float noise(float x, float y, float z) {
    float p_x = floorf(x); float p_y = floorf(y); float p_z = floorf(z);
    float f_x = x - p_x;  float f_y = y - p_y;  float f_z = z - p_z;
    
    f_x = f_x*f_x*(3.0f-2.0f*f_x);
    f_y = f_y*f_y*(3.0f-2.0f*f_y);
    f_z = f_z*f_z*(3.0f-2.0f*f_z);
    
    float n = p_x + p_y*57.0f + p_z*113.0f;
    
    return lerp(lerp(lerp(hash(n+0.0f), hash(n+1.0f), f_x),
                   lerp(hash(n+57.0f), hash(n+58.0f), f_x), f_y),
              lerp(lerp(hash(n+113.0f), hash(n+114.0f), f_x),
                   lerp(hash(n+170.0f), hash(n+171.0f), f_x), f_y), f_z);
}

__device__ float fbm(float x, float y, float z) {
    float total = 0.0f;
    float amp = 1.0f;
    float freq = 1.0f;
    for(int i=0; i<4; i++) {
        total += noise(x*freq, y*freq, z*freq) * amp;
        freq *= 2.0f;
        amp *= 0.5f;
    }
    return total;
}

__global__ void entropic_warp_v3(
    float* output,
    int res,
    float scale,
    float time,
    float warp_amp,
    float breath
) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= res * res) return;

    int xi = idx % res;
    int yi = idx / res;

    float u = (xi / (float)res) * 2.0f - 1.0f;
    float v = (yi / (float)res) * 2.0f - 1.0f;
    
    float r = sqrtf(u*u + v*v);
    
    // Warp
    float u_c = u * (1.0f + warp_amp * r * r);
    float v_c = v * (1.0f + warp_amp * r * r);
    
    // Scale
    float S = (float)res / scale;
    float Xg = u_c * S;
    float Yg = v_c * S;
    
    float val = fbm(Xg, Yg, time); 
    val = (val - 1.0f) * breath;    
    
    output[idx] = val;
}
}
'''
noise_kernel = cp.RawKernel(entropic_kernel, 'entropic_warp_v3')

def get_drifting_cmap(frame_idx):
    drift = np.sin(frame_idx * DRIFT_FREQ)
    r_drift = 0.05 * (1 + drift)
    b_drift = 0.65 + 0.1 * drift
    colors = [(0.0, 0.0, 0.0), (r_drift, 0.18, b_drift), (0.5, 0.7, 1.0)]
    return LinearSegmentedColormap.from_list("EntropicVoid", colors)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    g_cpu = np.random.normal(0, GRAIN_INTENSITY, (RESOLUTION, RESOLUTION)).astype(np.float32)
    g_gpu = cp.asarray(g_cpu)
    
    print("Entropic Void v3.0 (Strict Float) starting...")
    
    for i in range(TOTAL_FRAMES):
        t0 = time.time()
        
        # Params
        z = i * TIME_STEP
        breath = 1.0 + 0.15 * np.sin(i * MACRO_PULSE_FREQ)
        shimmer = 1.0 + 0.4 * np.abs(np.sin(i * MICRO_PULSE_FREQ))
        warp = 0.12 * np.sin(i * WARP_FREQ)
        scale = INITIAL_SCALE * np.exp(-ENTROPY_RATE * i)
        
        # GPU
        d_out = cp.zeros(RESOLUTION*RESOLUTION, dtype=cp.float32)
        blocks = (RESOLUTION*RESOLUTION + 255) // 256
        noise_kernel((blocks,), (256,), (
            d_out, RESOLUTION, 
            cp.float32(scale), cp.float32(z), 
            cp.float32(warp), cp.float32(breath)
        ))
        
        d_out = d_out + (g_gpu.ravel() * shimmer)
        img = cp.asnumpy(d_out.reshape(RESOLUTION, RESOLUTION))
        del d_out
        cp.get_default_memory_pool().free_all_blocks()
        
        # Save
        plt.figure(figsize=(10, 10), dpi=100, facecolor='black')
        plt.axes([0, 0, 1, 1]).axis('off')
        plt.imshow(img, cmap=get_drifting_cmap(i), interpolation='bicubic', vmin=-0.6, vmax=0.6)
        plt.savefig(os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png"), facecolor='black')
        plt.close('all')
        del img
        gc.collect()
        
        dt = time.time() - t0
        print(f"Frame {i:03d}: {dt:.3f}s")
        if GPU_DUTY_CYCLE < 1.0: time.sleep(dt*(1.0/GPU_DUTY_CYCLE - 1.0))

    subprocess.run(['ffmpeg', '-y', '-framerate', '30', 
                    '-i', f'{OUTPUT_DIR}/frame_%04d.png',
                    '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p',
                    'klein_entropic_v3.mp4'], check=True)
