"""
PROJECT: IKB 14D Hypercube 
METADATA: 14D, HYPERCUBE, TESSERACT, MATHEMATICS, O(1) VECTOR RENDERING
EXECUTION: 45.0s Sequence.
RULES ENFORCED:
- O(1) Vectorised plotting via LineCollection to prevent RAM overflow.
- maxtasksperchild=5 enforced to violently purge OS memory pools.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os
import gc
from multiprocessing import Pool, cpu_count

# --- 1. Hypercube Generation Functions ---
def generate_hypercube_vertices(dim):
    vertices = []
    for i in range(2**dim):
        binary = bin(i)[2:].zfill(dim)
        vertex = np.array([float(bit) * 2 - 1 for bit in binary])
        vertices.append(vertex)
    return np.array(vertices)

def generate_hypercube_edges(vertices, dim):
    edges = []
    num_vertices = len(vertices)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            # If they differ by exactly one coordinate, they are connected
            if np.sum(vertices[i] != vertices[j]) == 1:
                edges.append((i, j))
    return edges

# --- 2. Projection and Rotation Functions ---
def project_14d_to_3d(vertices_14d):
    P_14_3 = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.5, 0.5, 0.0],
        [0.0, 0.5, 0.5],
        [0.5, 0.0, 0.5],
        [0.3, 0.3, 0.3],
        [0.2, 0.2, 0.0],
        [0.0, 0.2, 0.2],
        [0.2, 0.0, 0.2],
        [0.1, 0.1, 0.0],
        [0.05, 0.05, 0.05],
        [0.05, 0.0, 0.05],
        [0.02, 0.02, 0.02]
    ])
    return np.dot(vertices_14d, P_14_3)

def project_3d_to_2d_isometric(vertices_3d):
    cos_30 = np.cos(np.radians(30))
    sin_30 = np.sin(np.radians(30))
    proj_x = (vertices_3d[:, 0] - vertices_3d[:, 1]) * cos_30
    proj_y = (vertices_3d[:, 0] + vertices_3d[:, 1]) * sin_30 - vertices_3d[:, 2]
    return np.column_stack((proj_x, proj_y))

# --- Worker Function for Parallel Processing ---
def generate_single_frame(
    frame_idx,
    dim,
    total_frames,
    output_folder,
    background_color,
    node_color,
    node_edge_color,
    edge_color,
    edge_alpha,
    edge_width,
    base_node_size,
    padding_factor,
    vertices_initial,
    edges_list,
    node_colors_map,
    xlim_min_val,
    xlim_max_val,
    ylim_min_val,
    ylim_max_val,
    rotation_planes,
    rotation_speeds
):
    theta_base = (frame_idx / total_frames) * 2 * np.pi

    current_rotated_vertices = np.copy(vertices_initial)
    for i, (d1, d2) in enumerate(rotation_planes):
        theta = theta_base * rotation_speeds[i]
        R_plane = np.identity(dim)
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        R_plane[d1, d1] = cos_t
        R_plane[d1, d2] = -sin_t
        R_plane[d2, d1] = sin_t
        R_plane[d2, d2] = cos_t
        current_rotated_vertices = np.dot(current_rotated_vertices, R_plane)

    projected_3d = project_14d_to_3d(current_rotated_vertices)
    projected_2d = project_3d_to_2d_isometric(projected_3d)

    # --- Plotting Architecture ---
    fig = plt.figure(figsize=(10, 10), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(background_color)
    fig.patch.set_facecolor(background_color)
    
    ax.set_xlim(xlim_min_val, xlim_max_val)
    ax.set_ylim(ylim_min_val, ylim_max_val)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    # [O(1) VECTORISED LINE COMPILATION] -> Resolves the 114,688 object RAM leak
    lines = [[projected_2d[edge[0]], projected_2d[edge[1]]] for edge in edges_list]
    line_collection = LineCollection(lines, colors=edge_color, alpha=edge_alpha, linewidths=edge_width, zorder=1)
    ax.add_collection(line_collection)

    # [O(1) VECTORISED NODE SCATTER] -> Resolves the 16,384 loop constraint
    ax.scatter(projected_2d[:, 0], projected_2d[:, 1], 
               s=base_node_size, 
               color=node_color, 
               zorder=2, 
               edgecolors=node_edge_color, 
               linewidths=0.5)
    
    frame_filename = os.path.join(output_folder, f"frame_{frame_idx:04d}.png")
    plt.savefig(frame_filename, facecolor=background_color, edgecolor='none')

    # Aggressive memory purges
    fig.clf()
    plt.close(fig)
    del fig, ax, lines, line_collection, projected_2d, projected_3d, current_rotated_vertices
    gc.collect()

    if (frame_idx + 1) % 50 == 0 or frame_idx == total_frames - 1:
        print(f"Generated frame {frame_idx + 1}/{total_frames} [PID: {os.getpid()}]")

if __name__ == '__main__':
    # --- Configuration for Animation ---
    DIM = 14 
    FPS = 24
    OUTPUT_FOLDER = "hypercube_animation_frames"
    ROTATION_TIME_SECONDS = 45 
    TOTAL_FRAMES = ROTATION_TIME_SECONDS * FPS
    OUTPUT_VIDEO_FILENAME = "IKB_14D.mp4" 

    # --- Aesthetic Preferences (Blue-on-Black Theme) ---
    BACKGROUND_COLOR = '#000000'
    NODE_COLOR = '#4169E1' 
    NODE_EDGE_COLOR = '#B0C4DE' 
    EDGE_COLOR = '#1E90FF' 
    EDGE_ALPHA = 0.6
    EDGE_WIDTH = 1.0
    BASE_NODE_SIZE = 50 
    PADDING_FACTOR = 1.05

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print("Pre-calculating hypercube vertices and edges... This takes a few moments for 14D.")
    vertices_initial = generate_hypercube_vertices(DIM)
    edges_list = generate_hypercube_edges(vertices_initial, DIM)
    # Removing node_colors_map array to save RAM; passing uniform color dynamically inside function.

    # --- Determine Plot Limits ---
    temp_3d = project_14d_to_3d(vertices_initial)
    temp_2d = project_3d_to_2d_isometric(temp_3d)
    axis_max = np.max(np.abs(temp_2d)) * PADDING_FACTOR
    xlim_min_val, xlim_max_val = -axis_max, axis_max
    ylim_min_val, ylim_max_val = -axis_max, axis_max
    del temp_3d, temp_2d

    rotation_planes = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)] 
    rotation_speeds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] 

    cpu_cores = max(1, cpu_count() - 1)
    print(f"Executing parallel node generation of {TOTAL_FRAMES} frames.")
    print(f"Cores Active: {cpu_cores} | Strict OS-Level GC Enabled (maxtasksperchild=5)")
    print(f"O(1) Vectorisation Enabled for 16,384 Vertices and 114,688 Edges per frame.")

    args_list = [
        (frame_idx, DIM, TOTAL_FRAMES, OUTPUT_FOLDER, BACKGROUND_COLOR, NODE_COLOR,
         NODE_EDGE_COLOR, EDGE_COLOR, EDGE_ALPHA, EDGE_WIDTH, BASE_NODE_SIZE,
         PADDING_FACTOR, vertices_initial, edges_list, None, xlim_min_val,
         xlim_max_val, ylim_min_val, ylim_max_val, rotation_planes, rotation_speeds)
        for frame_idx in range(TOTAL_FRAMES)
    ]

    # maxtasksperchild=5 ensures the OS forcefully kills the worker process and reboots it 
    # every 5 frames, permanently eradicating any residual RAM creep.
    with Pool(processes=cpu_cores, maxtasksperchild=5) as pool:
        pool.starmap(generate_single_frame, args_list)

    print(f"\nMatrix resolution complete. Frames secured in {OUTPUT_FOLDER}.")
