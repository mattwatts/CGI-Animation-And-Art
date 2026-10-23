"""
PROJECT: LG-456a Gemini Suit Compiler. --- Logic Garden 451v (Exact Physical Construct // Gemini G4C GLB Exporter)
FORMAT: Binary (.glb)
EXECUTION: True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe extraction bypassing all 3rd-party rendering (Trimesh/Matplotlib).
- The 4-Byte Alignment Vanguard: JSON and BIN chunks manually aligned to 4-byte bounds natively.
- Mode 1 Geometry: Writes directly as GL_LINES ensuring line-segment parity with LG-453x.
- Grid Substrate Purge: Only writes the spacesuit matrix.
"""

import numpy as np
import struct
import json
import os

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE (MATHEMATICAL PRIMITIVES)
# ------------------------------------------------------------------
def append_segmented(lines_dict, key, xs, ys, zs):
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5)
    for i in range(4):
        append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

def add_sym_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    add_box(lines_dict, col, cx, cy, cz, dx, dy, dz)
    if abs(cy) > 0.001:
        add_box(lines_dict, col, cx, -cy, cz, dx, dy, dz)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius*np.cos(t); iy = cy + radius*np.sin(t); iz = np.full_like(t, cz + s)
        elif axis == 'y':
            ix = cx + radius*np.cos(t); iy = np.full_like(t, cy + s); iz = cz + radius*np.sin(t)
        elif axis == 'x':
            ix = np.full_like(t, cx + s); iy = cy + radius*np.cos(t); iz = cz + radius*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = np.full_like(steps, cy + radius*np.sin(a))
            sz = cz + steps
        elif axis == 'y':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = cy + steps
            sz = np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'x':
            sx = cx + steps
            sy = np.full_like(steps, cy + radius*np.cos(a))
            sz = np.full_like(steps, cz + radius*np.sin(a))
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_sym_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis, rings, t_count)
    if abs(cy) > 0.001:
        add_cylinder(lines_dict, col, cx, -cy, cz, length, radius, axis, rings, t_count)

def add_sphere(lines_dict, col, cx, cy, cz, radius, rings=8, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_s = radius * np.cos(p)
        z_s = radius * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_s*np.cos(t); iy = cy + r_s*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        r_s = radius * np.cos(p)
        ix = cx + r_s*np.cos(a); iy = cy + r_s*np.sin(a); iz = cz + radius*np.sin(p)
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_sym_sphere(lines_dict, col, cx, cy, cz, radius, rings=8, t_count=16):
    add_sphere(lines_dict, col, cx, cy, cz, radius, rings, t_count)
    if abs(cy) > 0.001:
        add_sphere(lines_dict, col, cx, -cy, cz, radius, rings, t_count)

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_x = rx * np.cos(p); r_y = ry * np.cos(p); z_s = rz * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_x*np.cos(t); iy = cy + r_y*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        c_p = np.cos(p); s_p = np.sin(p)
        ix = cx + rx * c_p * np.cos(a); iy = cy + ry * c_p * np.sin(a); iz = cz + rz * s_p
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_sym_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
    add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings, t_count)
    if abs(cy) > 0.001:
        add_ellipsoid(lines_dict, col, cx, -cy, cz, rx, ry, rz, rings, t_count)

def add_ribbed_strut(lines_dict, col, p1, p2, radius, rings=10, t_count=12, rib_freq=6.0, rib_depth=0.15):
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    length = np.linalg.norm(v)
    if length < 0.001: return
    v_dir = v / length
    not_v = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(v_dir, not_v)) > 0.99: not_v = np.array([0.0, 1.0, 0.0])
    n1 = np.cross(v_dir, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_dir, n1)
    
    steps = np.linspace(0, length, rings)
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for s in steps:
        r_mod = radius * (1.0 + rib_depth * np.cos((s / length) * rib_freq * 2 * np.pi))
        center = p1 + v_dir * s
        ix = center[0] + r_mod * (np.cos(t)*n1[0] + np.sin(t)*n2[0])
        iy = center[1] + r_mod * (np.cos(t)*n1[1] + np.sin(t)*n2[1])
        iz = center[2] + r_mod * (np.cos(t)*n1[2] + np.sin(t)*n2[2])
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for s in steps:
            r_mod = radius * (1.0 + rib_depth * np.cos((s / length) * rib_freq * 2 * np.pi))
            nx = r_mod * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
            ny = r_mod * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
            nz = r_mod * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
            sx.append(p1[0] + nx + v_dir[0] * s)
            sy.append(p1[1] + ny + v_dir[1] * s)
            sz.append(p1[2] + nz + v_dir[2] * s)
        append_segmented(lines_dict, col, sx, sy, sz)

def add_sym_ribbed_strut(lines_dict, col, p1, p2, radius, rings=10, t_count=12, rib_freq=6.0, rib_depth=0.15):
    add_ribbed_strut(lines_dict, col, p1, p2, radius, rings, t_count, rib_freq, rib_depth)
    if abs(p1[1]) > 0.001 or abs(p2[1]) > 0.001:
        sp1 = (p1[0], -p1[1], p1[2])
        sp2 = (p2[0], -p2[1], p2[2])
        add_ribbed_strut(lines_dict, col, sp1, sp2, radius, rings, t_count, rib_freq, rib_depth)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (GEMINI G4C SPACECRAFT SUIT)
# ------------------------------------------------------------------
def generate_geminisuit_static():
    lines = {
        'C_SUIT': [], 'C_HELMET': [], 'C_HARDWARE': [], 
        'C_VISOR': [], 'C_DETAILS': [], 'C_HARNESS': [], 'C_GRID': []
    }

    H_Z = 1.70
    add_sphere(lines, 'C_HELMET', cx=0.0, cy=0.0, cz=H_Z, radius=0.13, rings=8, t_count=16)
    add_ellipsoid(lines, 'C_VISOR', cx=0.06, cy=0.0, cz=H_Z+0.01, rx=0.11, ry=0.15, rz=0.09, rings=8, t_count=20)
    add_cylinder(lines, 'C_DETAILS', cx=0.0, cy=0.0, cz=H_Z-0.15, length=0.04, radius=0.12, axis='z', rings=2, t_count=20)

    add_ellipsoid(lines, 'C_SUIT', cx=0.0, cy=0.0, cz=1.28, rx=0.12, ry=0.22, rz=0.28, rings=8, t_count=20)
    add_ellipsoid(lines, 'C_SUIT', cx=0.0, cy=0.0, cz=0.95, rx=0.13, ry=0.19, rz=0.16, rings=6, t_count=16)

    add_box(lines, 'C_HARDWARE', cx=0.12, cy=0.0, cz=1.16, dx=0.05, dy=0.14, dz=0.10)
    add_cylinder(lines, 'C_HARDWARE', cx=0.15, cy=-0.05, cz=1.06, length=0.10, radius=0.02, axis='z', rings=2, t_count=8)
    add_cylinder(lines, 'C_HARDWARE', cx=0.15, cy=0.05, cz=1.06, length=0.10, radius=0.02, axis='z', rings=2, t_count=8)

    add_sym_cylinder(lines, 'C_HARNESS', cx=0.11, cy=0.09, cz=1.05, length=0.45, radius=0.02, axis='z', rings=4, t_count=8)

    SH_R = (0.0, -0.24, 1.45)
    ELBOW_R = (0.08, -0.28, 1.15)
    WRIST_R = (0.20, -0.22, 0.95)
    add_sym_ribbed_strut(lines, 'C_SUIT', SH_R, ELBOW_R, radius=0.07, rings=12, t_count=12, rib_freq=9.0, rib_depth=0.05)
    add_sym_ribbed_strut(lines, 'C_SUIT', ELBOW_R, WRIST_R, radius=0.06, rings=12, t_count=12, rib_freq=11.0, rib_depth=0.05)
    
    add_sym_sphere(lines, 'C_DETAILS', *WRIST_R, 0.045, rings=4, t_count=10) 
    add_sym_ellipsoid(lines, 'C_DETAILS', cx=0.25, cy=-0.21, cz=0.88, rx=0.05, ry=0.04, rz=0.07, rings=6, t_count=12) 

    HIP_R = (0.0, -0.14, 0.90)
    KNEE_R = (0.06, -0.16, 0.50)
    ANKLE_R = (0.0, -0.14, 0.12)
    
    add_sym_ribbed_strut(lines, 'C_SUIT', HIP_R, KNEE_R, radius=0.10, rings=16, t_count=16, rib_freq=12.0, rib_depth=0.04)
    add_sym_ribbed_strut(lines, 'C_SUIT', KNEE_R, ANKLE_R, radius=0.08, rings=16, t_count=16, rib_freq=14.0, rib_depth=0.04)

    add_sym_box(lines, 'C_DETAILS', cx=0.06, cy=-0.14, cz=0.06, dx=0.18, dy=0.08, dz=0.12)

    return lines


# ------------------------------------------------------------------
# GLB BARE-METAL COMPILER
# ------------------------------------------------------------------
def compile_native_glb(output_filename):
    print("[GLB COMPILER] Calculating pure physical matrices...")
    static_rig = generate_geminisuit_static()
    
    vertices = []
    
    # We dynamically strip the C_GRID. Only physical geometry applies to the GLB matrix. 
    for c_key, segments in static_rig.items():
        if c_key == 'C_GRID': continue
        
        for xl, yl, zl in segments:
            # Segment mapping to exact vertices (P1, P2)
            vertices.append((float(xl[0]), float(yl[0]), float(zl[0])))
            vertices.append((float(xl[1]), float(yl[1]), float(zl[1])))

    if not vertices:
        print("[FATAL] Computed vectors yielded zero physical volume.")
        return

    # Pack into physical binary struct <3f (FLOAT LE VEC3)
    bin_data = bytearray()
    min_b = [float('inf'), float('inf'), float('inf')]
    max_b = [float('-inf'), float('-inf'), float('-inf')]
    
    for v in vertices:
        for i in range(3):
            if v[i] < min_b[i]: min_b[i] = v[i]
            if v[i] > max_b[i]: max_b[i] = v[i]
        bin_data.extend(struct.pack('<3f', v[0], v[1], v[2]))

    total_vertices = len(vertices)

    # Bare-Metal glTF 2.0 Mapping. mode = 1 establishes pure Line Segments. 
    gltf = {
        "asset": {"version": "2.0", "generator": "LG-451v Bare-Metal Tensor Compiler"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "mode": 1}]}],
        "accessors": [{
            "bufferView": 0,
            "byteOffset": 0,
            "componentType": 5126, 
            "count": total_vertices,
            "type": "VEC3",
            "max": max_b,
            "min": min_b
        }],
        "bufferViews": [{
            "buffer": 0,
            "byteOffset": 0,
            "byteLength": len(bin_data),
            "target": 34962 
        }],
        "buffers": [{
            "byteLength": len(bin_data)
        }]
    }
    
    json_str = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
    
    # THE 4-BYTE ALIGNMENT VANGUARD
    while len(json_str) % 4 != 0: json_str += b' '
    while len(bin_data) % 4 != 0: bin_data += b'\x00'
    
    # Payload Construction Baseplate
    glb_magic = b'glTF'
    glb_version = 2
    
    json_chunk_header = struct.pack('<II', len(json_str), 0x4E4F534A) # 'JSON'
    bin_chunk_header = struct.pack('<II', len(bin_data), 0x004E4942) # 'BIN\0'
    
    total_length = 12 + 8 + len(json_str) + 8 + len(bin_data)
    header = struct.pack('<4sII', glb_magic, glb_version, total_length)
    
    with open(output_filename, 'wb') as f:
        f.write(header)
        f.write(json_chunk_header)
        f.write(json_str)
        f.write(bin_chunk_header)
        f.write(bin_data)
        
    print(f"[SUCCESS] Pure geometry locked. Escaped to: {output_filename}")
    print(f"[METRICS] True VEC3 Points Processed: {total_vertices} (Aligned accurately to Mode 1 LINE boundaries)")


if __name__ == "__main__":
    compile_native_glb("logic_garden_451v_gemini_suit.glb")
