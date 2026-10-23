"""
PROJECT: Logic Garden 453x (Exact Physical Construct // Universal GLB Batch Parser - LINUX HOTFIX 41)
FORMAT: YouTube Shorts (1080x1920)
METADATA: GLB, 3D PARSER, WIREFRAME, PYTHON, BATCH AUTOMATION
EXECUTION: 24.0s Sequence per payload. True Continuous Vector Architecture.
RULES ENFORCED:
- Autonomous Batching: Scans directory, sorts all payloads by byte mass (ascending).
- The 4-Byte Alignment Vanguard: Natively forces bitwise memory snapping to 4-byte bounds `(curr_pos + 3) & ~3` circumventing unpadded GLB JSON integer traps.
- The Integer Pointer Suture: Restores exact array addressing for glTF mesh nodes natively.
- The Triangulation Suture: Eradicates Index Frame-Shift hallucinations by validating (-1, 3) geometric matrices securely.
- Linux OOM Shield: FFmpeg strictly throttled to 2 threads, preset fast, protecting OS RAM.
"""

import os
# Force Linux RAM to flush immediately on process end
os.environ["MALLOC_TRIM_THRESHOLD_"] = "0"

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection
import multiprocessing as mp
import trimesh
import subprocess
import glob
import sys
import gc
import json
import struct
import base64
import io

try:
    trimesh.constants.tol.merge = 1e-30
    trimesh.constants.tol.zero = 1e-30
    trimesh.tol.merge = 1e-30
    trimesh.tol.zero = 1e-30
except:
    pass

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#94A3B8'

MESH_PALETTE = [
    '#334155', # Heavy Slate
    '#005599', # Deep Marine
    '#1E293B', # Carbon Slate
    '#94A3B8', # Slate Aluminium
    '#CA8A04'  # Kapton Gold
]

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

# ------------------------------------------------------------------
# .GLB UNIVERSAL BARE-METAL EXTRACTOR 
# ------------------------------------------------------------------
def safe_transform(transform):
    if transform is None: return np.eye(4)
    if np.isnan(transform).any() or np.isinf(transform).any():
        return np.eye(4)
    try:
        if abs(np.linalg.det(transform[:3, :3])) < 1e-20:
            t_salvage = np.eye(4)
            t_salvage[:3, 3] = transform[:3, 3] 
            return t_salvage
    except Exception:
        return np.eye(4)
    return transform

def extract_from_geom(geom, transform):
    lines = []
    verts = None

    if hasattr(geom, 'vertices') and getattr(geom, 'vertices') is not None and len(geom.vertices) > 0:
        verts = np.array(geom.vertices)
    elif isinstance(geom, dict) and 'vertices' in geom:
        verts = np.array(geom['vertices'])
    elif isinstance(geom, np.ndarray) and len(geom.shape) == 2 and geom.shape[1] == 3:
        verts = geom

    if verts is None or len(verts) == 0:
        return lines

    verts = trimesh.transformations.transform_points(verts, transform)
    extracted_edges = False

    if hasattr(geom, 'faces') and getattr(geom, 'faces') is not None and len(geom.faces) > 0:
        edges = trimesh.geometry.faces_to_edges(geom.faces)
        edges = np.unique(np.sort(edges, axis=1), axis=0) 
        lines.extend(verts[edges].tolist())
        extracted_edges = True
    elif isinstance(geom, dict) and 'faces' in geom and len(geom['faces']) > 0:
        edges = trimesh.geometry.faces_to_edges(np.array(geom['faces']))
        edges = np.unique(np.sort(edges, axis=1), axis=0) 
        lines.extend(verts[edges].tolist())
        extracted_edges = True
    elif hasattr(geom, 'edges') and getattr(geom, 'edges') is not None and len(geom.edges) > 0:
        lines.extend(verts[geom.edges].tolist())
        extracted_edges = True
    elif hasattr(geom, 'entities') and getattr(geom, 'entities') is not None:
        for entity in geom.entities:
            if hasattr(entity, 'points'): 
                pts = entity.points
                for i in range(len(pts)-1):
                    lines.append([verts[pts[i]], verts[pts[i+1]]])
                extracted_edges = True

    if not extracted_edges and len(verts) > 0:
        bbox_span = np.max(np.max(verts, axis=0) - np.min(verts, axis=0)) if len(verts) > 0 else 1.0
        cs = max(0.001, bbox_span * 0.0005) # Micro-point connection (eradicates XYZ cartesian visuals) 
        for v in verts:
            x, y, z = v
            lines.append([[x, y, z], [x+cs, y+cs, z+cs]])

    return lines

def native_polyglot_ripper(binary_payload):
    """The Polyglot Substrate Protocol. Rigid Mathematical Boundary Snapping via Bitwise Alignment."""
    raw_e = []
    try:
        bin_data = b""
        gltf = None
        header = binary_payload[:4]

        # Valid GLB Vector (The Primary Index Lock)
        if header == b'glTF': 
            stream = io.BytesIO(binary_payload)
            stream.read(12) 
            c1_header = stream.read(8)
            if len(c1_header) == 8:
                c1_len, c1_type = struct.unpack('<II', c1_header)
                js_bytes = stream.read(c1_len)
                js_str = js_bytes.decode('utf-8', errors='ignore').split('\x00')[0].strip()
                try: gltf = json.loads(js_str)
                except Exception: pass
            
            # THE 4-BYTE ALIGNMENT VANGUARD
            curr_pos = stream.tell()
            aligned_pos = (curr_pos + 3) & ~3  # Snaps precisely to the 4-byte sector matrix
            
            if aligned_pos + 8 <= len(binary_payload):
                c2_header = binary_payload[aligned_pos:aligned_pos+8]
                c2_len, c2_type = struct.unpack('<II', c2_header)
                if c2_type == 0x004E4942: # BIN\0 exactly specifies pure binary
                    bin_data = binary_payload[aligned_pos+8 : ]
                else: 
                    # If format is totally corrupt, engage native find override
                    bin_idx = binary_payload.find(b'BIN\x00', curr_pos)
                    if bin_idx != -1:
                        bin_data = binary_payload[bin_idx+4 : ]
                    else:
                        bin_data = binary_payload[aligned_pos:]
            else:
                bin_data = binary_payload[aligned_pos:]

        # Base64 Socket / External Text Payload 
        else: 
            brace_count = 0
            json_end_idx = -1
            in_string = False
            escape = False
            for i, b in enumerate(binary_payload):
                if b == 0x22 and not escape: 
                    in_string = not in_string
                if not in_string:
                    if b == 0x7B: 
                        brace_count += 1
                    elif b == 0x7D: 
                        brace_count -= 1
                        if brace_count == 0:
                            json_end_idx = i + 1
                            break
                if b == 0x5C and not escape: 
                    escape = True
                else:
                    escape = False
            
            if json_end_idx > 0:
                js_str = binary_payload[:json_end_idx].decode('utf-8', errors='ignore').split('\x00')[0].strip()
                try: gltf = json.loads(js_str)
                except Exception: pass
                
                bin_data = binary_payload[json_end_idx:] 
                while len(bin_data) > 0 and bin_data[0] in [0x20, 0x09, 0x0A, 0x0D]:
                    bin_data = bin_data[1:]

        if not gltf: 
            return [], bin_data

        # Absolute Multi-Buffer Synchronisation Substrate
        bin_buffers = {}
        if len(bin_data) > 0: bin_buffers[0] = bin_data

        for b_i, b_spec in enumerate(gltf.get('buffers', [])):
            uri = b_spec.get('uri', '')
            if uri.startswith('data:'):
                b64_str = uri.split(',', 1)[1]
                bin_buffers[b_i] = base64.b64decode(b64_str)
            else:
                if b_i not in bin_buffers:
                    bin_buffers[b_i] = bin_data

        def get_arr(acc_idx):
            acc = gltf['accessors'][acc_idx]
            if 'bufferView' not in acc: return None
                
            bv = gltf['bufferViews'][acc['bufferView']]
            offset = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
            count, comp, typ = acc['count'], acc['componentType'], acc['type']
            
            dt_char = {5120:'b', 5121:'B', 5122:'h', 5123:'H', 5125:'I', 5126:'f'}.get(comp, 'f')
            n_comp = {'VEC3':3, 'VEC2':2, 'VEC4':4, 'SCALAR':1, 'MAT4':16}.get(typ, 1)
            unpack_fmt = f"<{n_comp}{dt_char}"
            item_size = struct.calcsize(unpack_fmt) // n_comp
            
            b_idx = bv.get('buffer', 0)
            target_bin = bin_buffers.get(b_idx, b"")
            if not target_bin: return None

            stride = bv.get('byteStride')
            if stride is None or stride == 0:
                stride = item_size * n_comp
            
            arr = None
            try:
                if stride == item_size * n_comp:
                    dt_np = np.dtype((np.dtype('<' + dt_char), n_comp))
                    if offset + count * stride <= len(target_bin):
                        arr = np.frombuffer(target_bin, dtype=dt_np, count=count, offset=offset).copy()
                else:
                    dt_base = np.dtype('<' + dt_char)
                    s_dt = np.dtype({'names': ['v'], 'formats': [(dt_base, n_comp)], 'itemsize': stride})
                    if offset + count * stride <= len(target_bin):
                        arr = np.frombuffer(target_bin, dtype=s_dt, count=count, offset=offset)['v'].copy()
            except Exception:
                pass

            if arr is None: 
                temp_a = []
                for i in range(count):
                    ptr = offset + i * stride
                    if ptr + (item_size * n_comp) <= len(target_bin):
                        temp_a.append(struct.unpack_from(unpack_fmt, target_bin, ptr))
                    else:
                        break
                if len(temp_a) == 0: return None
                arr = np.array(temp_a, dtype=np.float64)
                    
            arr = arr.astype(np.float64)
            if acc.get('normalized', False): 
                if comp in [5120, 5122]: 
                    max_v = 127 if comp == 5120 else 32767
                    arr = np.maximum(arr / float(max_v), -1.0)
                else: 
                    max_v = 255 if comp == 5121 else (65535 if comp == 5123 else 4294967295)
                    arr = arr / float(max_v)
            return arr

        node_mats = {}
        def eval_node(idx, parent_m):
            node = gltf.get('nodes', [])[idx]
            m = np.eye(4)
            if 'matrix' in node:
                m = np.array(node['matrix']).reshape(4,4).T
            else:
                t = node.get('translation', [0,0,0])
                s = node.get('scale', [1,1,1])
                q = node.get('rotation', [0,0,0,1])
                if abs(s[0]) < 1e-10 or abs(s[1]) < 1e-10 or abs(s[2]) < 1e-10:
                    s = [1.0, 1.0, 1.0]

                tm = np.eye(4); tm[:3,3] = t
                sm = np.diag([s[0], s[1], s[2], 1.0])
                x,y,z,w = q[0],q[1],q[2],q[3]
                xx,yy,zz = x**2, y**2, z**2
                rm = np.array([
                    [1-2*(yy+zz), 2*(x*y-z*w), 2*(x*z+y*w), 0],
                    [2*(x*y+z*w), 1-2*(xx+zz), 2*(y*z-x*w), 0],
                    [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(xx+yy), 0],
                    [0,0,0,1]
                ])
                m = tm @ rm @ sm
                
            world_m = safe_transform(parent_m @ m)
            node_mats[idx] = world_m
            for child in node.get('children', []): eval_node(child, world_m)

        if 'nodes' in gltf:
            child_set = set(c for node in gltf['nodes'] for c in node.get('children',[]))
            for i in range(len(gltf['nodes'])):
                if i not in child_set: eval_node(i, np.eye(4))
        else:
            node_mats = {0: np.eye(4)}

        meshes_found = 0
        def extract_mesh(mesh_cfg, w_mat):
            nonlocal meshes_found
            meshes_found += 1
            for prim in mesh_cfg.get('primitives', []):
                acc = prim.get('attributes', {}).get('POSITION')
                if acc is None: continue
                v = get_arr(acc)
                if v is None or len(v) == 0: continue
                
                v = (w_mat @ np.hstack((v, np.ones((len(v),1)))).T).T[:,:3]
                ind = prim.get('indices')
                mode = prim.get('mode', 4)  
                
                idx_arr = get_arr(ind) if ind is not None else None
                
                if ind is not None and idx_arr is not None:
                    idx = idx_arr.flatten().astype(int)
                    v_len = len(v)
                    
                    if mode == 1: 
                        idx = idx[:len(idx) - (len(idx)%2)].reshape(-1, 2)
                        idx = idx[np.all(idx < v_len, axis=1)]
                        for pair in idx:
                            raw_e.append([v[pair[0]], v[pair[1]]])
                    elif mode == 4: 
                        idx = idx[:len(idx) - (len(idx)%3)].reshape(-1, 3)
                        # The Triangulation Suture: Prevent index out-of-bounds matrix collapse natively
                        idx = idx[np.all(idx < v_len, axis=1)]
                        for tri in idx:
                            raw_e.extend([[v[tri[0]], v[tri[1]]], [v[tri[1]], v[tri[2]]], [v[tri[2]], v[tri[0]]]])
                    elif mode == 0: 
                        idx = idx[idx < v_len]
                        bbox_span = np.max(np.max(v, axis=0) - np.min(v, axis=0)) if len(v) > 0 else 1.0
                        cs = max(0.001, bbox_span * 0.0005)
                        for i_p in idx:
                            x, y, z = v[i_p]
                            raw_e.append([[x,y,z], [x+cs,y+cs,z+cs]])
                    else:  
                        idx = idx[idx < v_len]
                        for i in range(len(idx)-1): raw_e.append([v[idx[i]], v[idx[i+1]]])
                else:
                    if mode == 1:
                        for i in range(0, len(v)-1, 2): raw_e.append([v[i], v[i+1]])
                    elif mode == 4:
                        for i in range(0, len(v)-2, 3):
                            raw_e.extend([[v[i], v[i+1]], [v[i+1], v[i+2]], [v[i+2], v[i]]])
                    else:
                        bbox_span = np.max(np.max(v, axis=0) - np.min(v, axis=0)) if len(v) > 0 else 1.0
                        cs = max(0.001, bbox_span * 0.0005)
                        for pt in v:
                            x, y, z = pt
                            raw_e.append([[x,y,z], [x+cs,y+cs,z+cs]])

        if node_mats:
            for n_idx, w_mat in node_mats.items():
                if 'mesh' in gltf['nodes'][n_idx]:
                    extract_mesh(gltf['meshes'][gltf['nodes'][n_idx]['mesh']], w_mat)
        else:
            for mesh in gltf.get('meshes', []):
                extract_mesh(mesh, np.eye(4))
                
        print(f"      [SUTURE SENTINEL] Matrix cracked natively. Total glTF component meshes unpacked: {meshes_found}")
        return raw_e, bin_data
    except Exception as e:
        print(f"      [POLYGLOT EXTRACTOR ERROR] Absolute native mathematical failure: {e}")
        return [], b""

def get_extent(edge_list):
    if not edge_list or len(edge_list) == 0: 
        return 0.0
    flat = np.array(edge_list).reshape(-1, 3)
    valid = flat[~np.isnan(flat).any(axis=1)]
    if len(valid) == 0: 
        return 0.0
    return float(np.max(np.max(valid, axis=0) - np.min(valid, axis=0)))

def ingest_glb_payload(filepath):
    raw_edges = []
    extent_eval = 0.0
    scene = None
    extracted_bin_data = b""
    
    with open(filepath, 'rb') as f:
        binary_payload = f.read()

    # TIER I: THE IDENTITY STRIPPER (Native Extension Mask Override)
    print("      [INGESTION] Routing pure Python Alien Geometry Identifier...")
    formats_to_test = ['glb', 'gltf', 'stl', 'ply', 'obj', 'off', 'dae']
    
    for fmt in formats_to_test:
        try:
            stream = io.BytesIO(binary_payload)
            test_scene = trimesh.load(stream, file_type=fmt, force=None)
            
            temp_edges = []
            if isinstance(test_scene, trimesh.Trimesh):
                 temp_edges.extend(extract_from_geom(test_scene, np.eye(4)))
            elif hasattr(test_scene, 'graph') and hasattr(test_scene.graph, 'nodes_geometry'):
                for node_name in test_scene.graph.nodes_geometry:
                    transform, geometry_name = test_scene.graph.get(node_name)
                    transform = safe_transform(transform)
                    geom = test_scene.geometry.get(geometry_name)
                    if geom is not None:
                        temp_edges.extend(extract_from_geom(geom, transform))
                        
            if get_extent(temp_edges) <= 0.0 and hasattr(test_scene, 'geometry'):
                for geom in test_scene.geometry.values():
                    temp_edges.extend(extract_from_geom(geom, np.eye(4)))
            
            test_extent = get_extent(temp_edges)
            if test_extent > 0.0:
                raw_edges = temp_edges
                extent_eval = test_extent
                scene = test_scene
                print(f"      [IDENTITY STRIPPER] Extracted securely. File identity forcibly re-mapped to: {fmt.upper()}")
                break
        except Exception:
            pass

    # TIER II: True Polyglot Substrate Protocol
    if extent_eval <= 0.0:
        print("      [INGESTION BYPASS] Typology bounds yielded zero. Forcing The Native Polyglot Core...")
        raw_edges, extracted_bin_data = native_polyglot_ripper(binary_payload)
        extent_eval = get_extent(raw_edges)

    # TIER III: Fallback Draco Interception System
    if extent_eval <= 0.0:
        try:
            print("      [TIER 3 ACTIVATED] Explicitly triggering Force-Draco Trimesh backend execution.")
            trimesh.constants.tol.merge = 1e-30
            trimesh.constants.tol.zero = 1e-30
            stream = io.BytesIO(binary_payload)
            scene = trimesh.load(stream, file_type='glb', force='scene', process=True) 
            raw_edges = []
            if hasattr(scene, 'graph') and hasattr(scene.graph, 'nodes_geometry'):
                for node_name in scene.graph.nodes_geometry:
                    transform, geometry_name = scene.graph.get(node_name)
                    transform = safe_transform(transform)
                    geom = scene.geometry.get(geometry_name)
                    if geom is not None:
                        raw_edges.extend(extract_from_geom(geom, transform))
            extent_eval = get_extent(raw_edges)
        except Exception: pass

    # TIER IV: Mesh Fallback Extrusion
    if extent_eval <= 0.0:
        print("      [SINGULARITY BYPASS] Topologies corrupt. Forcing pure Trimesh Mesh execution.")
        try:
            stream = io.BytesIO(binary_payload)
            mesh = trimesh.load(stream, file_type='glb', force='mesh', process=False)
            raw_edges = extract_from_geom(mesh, np.eye(4))
            extent_eval = get_extent(raw_edges)
        except Exception: pass

    if extent_eval <= 0.0:
        print("      [FATAL] Complete Pipeline Blockage. Topology evaluates natively as purely dead mathematics.")
        return None, None

    edges_array = np.array(raw_edges)
    total_raw_edges = len(edges_array)

    MAX_ALLOWABLE_EDGES = 15000
    decimation_step = int(np.ceil(total_raw_edges / float(MAX_ALLOWABLE_EDGES)))
    
    if decimation_step > 1:
        edges_array = edges_array[::decimation_step]
        print(f"      [OOM SHUTTLE] True physical edges natively mapped: {total_raw_edges}. Decimated organically (1-in-{decimation_step}).")

    flat_verts = edges_array.reshape(-1, 3)
    valid_verts = flat_verts[~np.isnan(flat_verts).any(axis=1)]
    min_b = np.min(valid_verts, axis=0)
    max_b = np.max(valid_verts, axis=0)
    true_centroid = (min_b + max_b) / 2.0

    scale_factor = 10.0 / extent_eval
    normalized_edges = (edges_array - true_centroid) * scale_factor
    print(f"      [NORMALISATION] Matrix cleanly stabilised boundary by factor of {scale_factor:.2e}")

    lines_output = {'C_GRID': []}
    for c in MESH_PALETTE:
        lines_output[c] = []

    for i, edge in enumerate(normalized_edges):
        col_key = MESH_PALETTE[i % len(MESH_PALETTE)]
        lines_output[col_key].append(([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], [edge[0][2], edge[1][2]]))

    # Ground Tracking Frame
    z_floor = (min_b[2] - true_centroid[2]) * scale_factor - 1.0 
    grid_radii = [2.5, 4.0, 6.0]
    for r_p in grid_radii:
        t_p = np.linspace(0, 2*np.pi, 32, endpoint=False)
        for i in range(len(t_p)-1):
            xs = [r_p * np.cos(t_p[i]), r_p * np.cos(t_p[i+1])]
            ys = [r_p * np.sin(t_p[i]), r_p * np.sin(t_p[i+1])]
            zs = [z_floor, z_floor]
            lines_output['C_GRID'].append((xs, ys, zs))

    cam_span = 5.0 * 1.30
    
    del raw_edges
    del edges_array
    del flat_verts
    del normalized_edges
    if scene is not None: del scene
    gc.collect()
    
    return lines_output, cam_span

# ------------------------------------------------------------------
# MASTER RENDERER HOOK & WORKER INITIALIZER
# ------------------------------------------------------------------
GLOBAL_LINES = None
GLOBAL_CAM_SPAN = None
GLOBAL_TARGET_NAME = None
GLOBAL_OUT_DIR = None

def init_worker(lines_bundle, span_bundle, name_bundle, out_bundle):
    global GLOBAL_LINES, GLOBAL_CAM_SPAN, GLOBAL_TARGET_NAME, GLOBAL_OUT_DIR
    GLOBAL_LINES = lines_bundle
    GLOBAL_CAM_SPAN = span_bundle
    GLOBAL_TARGET_NAME = name_bundle
    GLOBAL_OUT_DIR = out_bundle

def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        yield (f, t_sec, 115.0 - (stage * 360.0), 0.0, 0.0, 0.0)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN)
    ax.set_ylim(-GLOBAL_CAM_SPAN * 1.777, GLOBAL_CAM_SPAN * 1.777)

    render_queue = []
    
    for xl, yl, zl in GLOBAL_LINES['C_GRID']:
        u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
        render_queue.append((np.mean(depth), [(u[0], v[0]), (u[1], v[1])], C_GRID, 1.0, 0.4))
            
    for col_key in MESH_PALETTE:
        if col_key in GLOBAL_LINES:
            for xl, yl, zl in GLOBAL_LINES[col_key]:
                u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
                render_queue.append((np.mean(depth), [(u[0], v[0]), (u[1], v[1])], col_key, 1.25, 0.9))

    render_queue.sort(key=lambda item: item[0], reverse=True)
    
    if render_queue:
        segments = [rq[1] for rq in render_queue]
        colors = [mcolors.to_rgba(rq[2], alpha=rq[4]) for rq in render_queue]
        linewidths = [rq[3] for rq in render_queue]
        lc = LineCollection(segments, colors=colors, linewidths=linewidths)
        ax.add_collection(lc)

    ui_t = GLOBAL_CAM_SPAN * 1.45
    ax.add_patch(patches.Rectangle((-GLOBAL_CAM_SPAN, ui_t), GLOBAL_CAM_SPAN*2, GLOBAL_CAM_SPAN*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_t + GLOBAL_CAM_SPAN*0.08, "LG-453x // MACRO-ENGINEERING TENSOR: STRUCTURAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_t + GLOBAL_CAM_SPAN*0.02, f"EXPLICIT TRUE-SCALE BASE LOGIC // FILE: {GLOBAL_TARGET_NAME.upper()}", color=MESH_PALETTE[0], fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ui_b = -GLOBAL_CAM_SPAN * 1.777
    ax.add_patch(patches.Rectangle((-GLOBAL_CAM_SPAN, ui_b), GLOBAL_CAM_SPAN*2, GLOBAL_CAM_SPAN*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN], [ui_b + GLOBAL_CAM_SPAN*0.35, ui_b + GLOBAL_CAM_SPAN*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=MESH_PALETTE[1], fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.02, f"TOPOLOGICAL YIELD: THE 4-BYTE ALIGNMENT VANGUARD SECURE", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(GLOBAL_OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    
    plt.close("all")
    fig.clf()
    del fig
    gc.collect()
    
    return f

# ------------------------------------------------------------------
# BATCH ORCHESTRATION & AUTOMATED FFMPEG PIPELINE
# ------------------------------------------------------------------
def process_batch():
    glb_files = glob.glob("*.glb")
    if not glb_files:
        print("[FATAL] Zero .glb payloads detected in the active working directory.")
        sys.exit(1)

    glb_files.sort(key=lambda f: os.path.getsize(f))
    
    cpu_cores = max(1, mp.cpu_count() // 2)
    print(f"LG-453x: AUTONOMOUS BATCH PIPELINE ENGAGED [THROTTLED CORES: {cpu_cores}]")
    print(f"Payloads detected: {len(glb_files)} (Sorted efficiently by byte mass)")

    for idx, filepath in enumerate(glb_files):
        filename = os.path.basename(filepath)
        basename, _ = os.path.splitext(filename)
        out_mp4 = f"{basename}.mp4"
        
        GLOBAL_TARGET_NAME = filename
        GLOBAL_OUT_DIR = f"frames_{basename}"
        os.makedirs(GLOBAL_OUT_DIR, exist_ok=True)

        size_mb = os.path.getsize(filepath) / (1024*1024)
        print(f"\n[{idx+1}/{len(glb_files)}] PARSING PAYLOAD: {filename} ({size_mb:.2f} MB)")
        
        lines, cam_span = ingest_glb_payload(filepath)
        
        if lines is None:
            continue
        
        print(f"      Initiating Core Pool -> Rendering {TOTAL_FRAMES} frames...")
        
        with mp.Pool(processes=cpu_cores, maxtasksperchild=180, 
                     initializer=init_worker, 
                     initargs=(lines, cam_span, GLOBAL_TARGET_NAME, GLOBAL_OUT_DIR)) as pool:
            
            for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
                if finished_frame % 60 == 0:
                    print(f"      Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

        print(f"      Graphic Topology Yield Complete. Forcing FFmpeg compilation for {out_mp4}...")
        
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-framerate', '60', 
            '-i', f'{GLOBAL_OUT_DIR}/frame_%04d.png',
            '-threads', '2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            '-preset', 'fast', '-tune', 'animation',
            '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:white',
            out_mp4
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"      [SUCCESS] Binary Video Output Secure: {out_mp4}")
        except subprocess.CalledProcessError as e:
            print(f"      [FATAL] FFmpeg pipeline collapsed securely on file: {filename}. Error: {e}")
            
        lines = None
        gc.collect()

    print("\n[OPERATIONAL] MASTER BATCH EXECUTION COMPLETED.")

if __name__ == "__main__":
    mp.freeze_support()
    process_batch()
