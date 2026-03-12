import numpy as np
from PIL import Image, ImageDraw
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import os
import subprocess

class ColorEnum(Enum):
    RED = (220, 20, 60)
    BLUE = (30, 144, 255)
    GREEN = (34, 139, 34)
    YELLOW = (255, 215, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BROWN = (139, 69, 19)
    GRAY = (128, 128, 128)
    ORANGE = (255, 140, 0)
    PINK = (255, 192, 203)
    CYAN = (0, 255, 255)
    PURPLE = (128, 0, 128)
    LIME = (50, 205, 50)
    INDIGO = (75, 0, 130)

class PieceType(Enum):
    BRICK_1x1 = (1, 1, 1)
    BRICK_1x2 = (1, 2, 1)
    BRICK_2x2 = (2, 2, 1)
    BRICK_2x4 = (2, 4, 1)

@dataclass
class LEGOBlock:
    piece_type: PieceType
    color: ColorEnum
    position: Tuple[float, float, float]
    original_position: Tuple[float, float, float]
    index: int
    pixel_size: float = 25.0
    
    def get_dimensions(self) -> Tuple[float, float, float]:
        """Returns dimensions in world coordinates based on pixel size"""
        width, depth, height = self.piece_type.value
        return width * self.pixel_size, depth * self.pixel_size, height * self.pixel_size

class CongaLineRenderer:
    """Renders LEGO blocks forming a conga line"""
    
    ISOMETRIC_ANGLE = 30
    
    def __init__(self, width: int = 2000, height: int = 2000,
                 background_color: Tuple = (240, 240, 245), pixel_size: float = 25.0,
                 line_spacing: float = 0.3, line_speed: float = 1.5):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.pixel_size = pixel_size
        self.line_spacing = line_spacing
        self.line_speed = line_speed
        self.blocks: List[LEGOBlock] = []
        self.center_x = 0
        self.center_y = 0
    
    def add_block(self, block: LEGOBlock):
        self.blocks.append(block)
    
    def _get_resting_position(self, block_index: int, total_blocks: int) -> Tuple[float, float, float]:
        """Get the geometric resting position for a block in screen space"""
        # Arrange blocks in a circular pattern in the CENTER of the screen
        angle = (2 * math.pi * block_index) / total_blocks
        radius = 150  # pixels
        
        # Position in screen space (center is 1000, 1000)
        x = 1000 + radius * math.cos(angle)
        y = 1000 + radius * math.sin(angle)
        z = (block_index % 3) * 0.3
        
        return x, y, z
    
    def _get_conga_path(self, time: float, block_index: int) -> Tuple[float, float]:
        """Generate conga line path that fills the entire frame"""
        # Trail effect - each block follows the one ahead
        trail_delay = block_index * self.line_spacing
        adjusted_time = time - trail_delay
        
        # Speed control
        path_time = adjusted_time * self.line_speed
        
        # Create a serpentine path that covers the entire frame
        # Using multiple sine waves at different frequencies
        
        # Vertical movement (covers full height: 100 to 1900)
        vert_wave = math.sin(path_time * 0.4) * 900 + 1000
        
        # Horizontal movement (covers full width: 100 to 1900)
        horiz_wave = math.sin(path_time * 0.3 + block_index * 0.2) * 900 + 1000
        
        # Additional serpentine pattern
        serpentine_x = math.sin(path_time * 0.25) * 800 + 1000
        serpentine_y = math.cos(path_time * 0.2) * 800 + 1000
        
        # Combine movements
        x = (horiz_wave + serpentine_x) / 2
        y = (vert_wave + serpentine_y) / 2
        
        # Clamp to frame bounds with padding
        padding = 50
        x = max(padding, min(self.width - padding, x))
        y = max(padding, min(self.height - padding, y))
        
        return x, y
    
    def _interpolate_position(self, rest_pos: Tuple[float, float, float],
                             conga_pos: Tuple[float, float, float],
                             phase: float) -> Tuple[float, float, float]:
        """Smoothly interpolate between resting and conga positions"""
        # Ease-in-out function
        t = phase
        if t < 0.5:
            ease_t = 2 * t * t
        else:
            ease_t = 1 - 2 * (1 - t) ** 2
        
        x = rest_pos[0] + (conga_pos[0] - rest_pos[0]) * ease_t
        y = rest_pos[1] + (conga_pos[1] - rest_pos[1]) * ease_t
        z = rest_pos[2] + (conga_pos[2] - rest_pos[2]) * ease_t
        
        return x, y, z
    
    def _isometric_project(self, x: float, y: float, z: float) -> Tuple[float, float]:
        """Project 3D coordinates to 2D isometric"""
        iso_x = (x - y) * math.cos(math.radians(self.ISOMETRIC_ANGLE))
        iso_y = z + (x + y) * math.sin(math.radians(self.ISOMETRIC_ANGLE))
        return iso_x, iso_y
    
    def _project_and_scale(self, x: float, y: float, z: float) -> Tuple[float, float]:
        """Project 3D to screen coordinates"""
        iso_x, iso_y = self._isometric_project(x, y, z)
        
        # Center on screen
        screen_x = self.width / 2 + iso_x
        screen_y = self.height / 2 + iso_y
        
        return screen_x, screen_y
    
    def _clip_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """Clip coordinates to screen bounds"""
        x = max(0, min(self.width, x))
        y = max(0, min(self.height, y))
        return x, y
    
    def _draw_cube_face(self, x: float, y: float, z: float, width: float, depth: float,
                       height: float, color: Tuple, face: str):
        """Draw a single cube face in screen space (no isometric projection)"""
        
        # Draw rectangles directly in screen space
        if face == 'top':
            # Top face - visible flat
            rect_x = x
            rect_y = y
            rect_width = width
            rect_height = depth
            darken_factor = 0.0
        elif face == 'right':
            # Right face - simplified for screen space
            rect_x = x + width * 0.3
            rect_y = y + depth * 0.3
            rect_width = width * 0.4
            rect_height = height * 0.8
            darken_factor = 0.2
        elif face == 'left':
            # Left face - simplified for screen space
            rect_x = x - width * 0.2
            rect_y = y + depth * 0.3
            rect_width = width * 0.4
            rect_height = height * 0.8
            darken_factor = 0.4
        else:
            return
        
        # Apply shading
        darkened_color = tuple(int(c * (1 - darken_factor)) for c in color)
        
        # Clamp to screen
        rect_x1 = max(0, min(self.width, rect_x))
        rect_y1 = max(0, min(self.height, rect_y))
        rect_x2 = max(0, min(self.width, rect_x + rect_width))
        rect_y2 = max(0, min(self.height, rect_y + rect_height))
        
        if rect_x2 > rect_x1 and rect_y2 > rect_y1:
            self.draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], 
                              fill=darkened_color, outline=(0, 0, 0))
    
    def _draw_block_screen_space(self, block: LEGOBlock):
        """Draw block directly in screen space"""
        x, y, z = block.position
        width, depth, height = block.get_dimensions()
        
        # Convert pixel_size to screen pixels (direct mapping)
        width_px = width
        depth_px = depth
        height_px = height
        
        # Clamp position to screen
        x = max(0, min(self.width - width_px, x))
        y = max(0, min(self.height - depth_px, y))
        
        color = block.color.value
        
        # Draw block faces
        self._draw_cube_face(x, y, z, width_px, depth_px, height_px, color, 'top')
        self._draw_cube_face(x, y, z, width_px, depth_px, height_px, color, 'right')
        self._draw_cube_face(x, y, z, width_px, depth_px, height_px, color, 'left')
    
    def render_frame(self, time: float, total_duration: float) -> Image.Image:
        """Render a single frame"""
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        self.draw = ImageDraw.Draw(image, 'RGBA')
        
        total_blocks = len(self.blocks)
        
        # Timeline:
        # 0-15s: Formation phase
        # 15-105s: Conga dancing
        # 105-120s: Return to rest
        
        if time < 15:
            # Formation phase
            phase = time / 15.0
        elif time < 105:
            # Conga dancing phase
            phase = 1.0
        else:
            # Return to rest phase
            phase = 1.0 - (time - 105) / 15.0
        
        # Update block positions
        for block in self.blocks:
            # Get resting position (in screen space)
            rest_x, rest_y, rest_z = self._get_resting_position(block.index, total_blocks)
            
            # Get conga position (in screen space)
            conga_x, conga_y = self._get_conga_path(time, block.index)
            conga_z = 0.5 + 0.2 * math.sin(time * self.line_speed + block.index * 0.3)
            
            # Interpolate between rest and conga based on phase
            if phase < 1.0:
                # Formation phase
                x, y, z = self._interpolate_position(
                    (rest_x, rest_y, rest_z),
                    (conga_x, conga_y, conga_z),
                    phase
                )
            else:
                # Full conga phase
                x, y, z = conga_x, conga_y, conga_z
            
            block.position = (x, y, z)
        
        # Sort and draw blocks (painters algorithm)
        sorted_blocks = sorted(self.blocks, key=lambda b: b.position[2])
        
        for block in sorted_blocks:
            self._draw_block_screen_space(block)
        
        return image
    
    def save_frame(self, image: Image.Image, frame_num: int, output_dir: str):
        """Save frame to file"""
        filename = os.path.join(output_dir, f"frame_{frame_num:05d}.png")
        image.save(filename)

def build_geometric_structure(renderer: CongaLineRenderer, pixel_size: float = 25.0):
    """Build blocks in geometric arrangement"""
    colors = [ColorEnum.RED, ColorEnum.BLUE, ColorEnum.GREEN, 
              ColorEnum.YELLOW, ColorEnum.ORANGE, ColorEnum.PURPLE,
              ColorEnum.CYAN, ColorEnum.PINK, ColorEnum.BROWN, 
              ColorEnum.GRAY, ColorEnum.LIME, ColorEnum.INDIGO]
    
    # Create 20 blocks
    num_blocks = 20
    
    for i in range(num_blocks):
        color = colors[i % len(colors)]
        original_pos = (0, 0, 0)
        
        block = LEGOBlock(
            PieceType.BRICK_2x2,
            color,
            original_pos,
            original_pos,
            i,
            pixel_size=pixel_size
        )
        renderer.add_block(block)

def create_mp4_from_frames(frame_dir: str, output_file: str, fps: int = 30, bitrate: str = "8000k"):
    """Convert PNG frame sequence to MP4"""
    
    frame_pattern = os.path.join(frame_dir, "frame_%05d.png")
    
    command = [
        'ffmpeg',
        '-framerate', str(fps),
        '-i', frame_pattern,
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-b:v', bitrate,
        '-preset', 'medium',
        '-y',
        output_file
    ]
    
    print(f"\nCreating MP4 from frames...")
    
    try:
        subprocess.run(command, check=True)
        print(f"\nMP4 created successfully: {output_file}")
        
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating MP4: {e}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg first.")

def generate_conga_line_animation(output_dir: str = "lego_conga_frames", fps: int = 30, 
                                 pixel_size: float = 25.0, line_spacing: float = 0.3,
                                 line_speed: float = 1.5):
    """Generate conga line animation - 120 seconds at 30 fps
    
    Args:
        output_dir: Directory to save frame sequence
        fps: Frames per second
        pixel_size: Size of each LEGO stud in pixels (default: 25)
        line_spacing: Distance between blocks in conga line (default: 0.3)
        line_speed: Speed multiplier for conga line (default: 1.5)
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    renderer = CongaLineRenderer(width=2000, height=2000, pixel_size=pixel_size,
                                line_spacing=line_spacing, line_speed=line_speed)
    build_geometric_structure(renderer, pixel_size=pixel_size)
    
    # 120 seconds at 30 fps
    total_duration = 120.0
    total_frames = int(total_duration * fps)
    frame_time = 1.0 / fps
    
    print(f"Generating Conga Line Animation")
    print(f"{'='*60}")
    print(f"Resolution: {renderer.width}x{renderer.height} pixels")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {total_duration}s")
    print(f"FPS: {fps}")
    print(f"LEGO Pixel Size: {pixel_size}px per stud")
    print(f"Line Spacing: {line_spacing}")
    print(f"Line Speed: {line_speed}x")
    print(f"\nAnimation breakdown:")
    print(f"  Resting state:   0.0s - 0.0s   (initial)")
    print(f"  Formation:       0.0s - 15.0s  (450 frames)")
    print(f"  Conga dancing:   15.0s - 105.0s (2700 frames)")
    print(f"  Return to rest:  105.0s - 120.0s (450 frames)")
    print(f"{'='*60}\n")
    
    frame_num = 0
    current_time = 0
    
    # Generate all frames
    for i in range(total_frames):
        image = renderer.render_frame(current_time, total_duration)
        renderer.save_frame(image, frame_num, output_dir)
        
        if (i + 1) % 150 == 0 or i == 0:
            if current_time < 15:
                phase_name = f"FORMATION ({current_time / 15.0 * 100:.0f}%)"
            elif current_time < 105:
                phase_name = f"CONGA DANCING ({(current_time - 15) / 90.0 * 100:.0f}%)"
            else:
                phase_name = f"RETURN TO REST ({(current_time - 105) / 15.0 * 100:.0f}%)"
            
            print(f"Frame {frame_num:05d} ({i+1:4d}/{total_frames}) - {current_time:6.1f}s - {phase_name}")
        
        frame_num += 1
        current_time += frame_time
    
    # Loop closure
    first_frame_path = os.path.join(output_dir, "frame_00000.png")
    last_frame_path = os.path.join(output_dir, f"frame_{frame_num:05d}.png")
    
    if os.path.exists(first_frame_path):
        first_image = Image.open(first_frame_path)
        first_image.save(last_frame_path)
        print(f"Frame {frame_num:05d} - LOOP CLOSURE (identical to frame 0)")
    
    print(f"\n{'='*60}")
    print(f"Frame sequence complete!")
    print(f"Total frames generated: {frame_num + 1}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    output_mp4 = f"lego_conga_line_25px.mp4"
    create_mp4_from_frames(output_dir, output_mp4, fps=fps, bitrate="8000k")

if __name__ == "__main__":
    # Generate with 25px studs, spacing 0.3, speed 1.5x
    generate_conga_line_animation(
        output_dir="lego_conga_frames", 
        fps=30, 
        pixel_size=25.0,
        line_spacing=0.3,
        line_speed=1.5
    )
