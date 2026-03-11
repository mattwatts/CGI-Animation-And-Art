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
    
    def get_dimensions(self) -> Tuple[float, float, float]:
        return self.piece_type.value

class EscherTwirlingRenderer:
    """Renders LEGO blocks twirling in an Escher landscape within frame bounds"""
    
    ISOMETRIC_ANGLE = 30
    
    def __init__(self, width: int = 2000, height: int = 2000,
                 background_color: Tuple = (240, 240, 245), padding: float = 0.08):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.padding = padding
        self.blocks: List[LEGOBlock] = []
        self.center_x = 0
        self.center_y = 0
        self.safe_radius = 0  # Will be calculated
    
    def add_block(self, block: LEGOBlock):
        self.blocks.append(block)
    
    def _escher_landscape_transform(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Apply Escher landscape transformation to create impossible geometry"""
        # Normalize to center
        dx = x - self.center_x
        dy = y - self.center_y
        
        # Spiral gravity well
        radius = math.sqrt(dx**2 + dy**2) + 0.1
        angle = math.atan2(dy, dx)
        
        # Create impossible staircase effect
        stair_factor = (x + y) * 0.15
        z_escher = z + math.sin(stair_factor) * 2 + math.cos(angle * 2) * 1.5
        
        # Möbius twist effect
        twist = angle + (radius * 0.25)
        new_x = self.center_x + radius * math.cos(twist)
        new_y = self.center_y + radius * math.sin(twist)
        
        return new_x, new_y, z_escher
    
    def _twirl_effect(self, x: float, y: float, z: float, time: float, 
                     twirl_speed: float) -> Tuple[float, float, float]:
        """Apply twirling effect around center within safe bounds"""
        # Calculate distance from center
        dx = x - self.center_x
        dy = y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Constrain distance to safe radius
        if distance > self.safe_radius:
            distance = self.safe_radius
        
        # Current angle
        angle = math.atan2(dy, dx)
        
        # Apply twirl rotation - slow, graceful rotation
        twirl_angle = angle + time * twirl_speed
        
        # Maintain constrained distance while rotating
        new_x = self.center_x + distance * math.cos(twirl_angle)
        new_y = self.center_y + distance * math.sin(twirl_angle)
        
        # Add vertical bobbing motion synchronized with twirl
        bob_z = z + math.sin(time * twirl_speed * 0.7) * 1.0
        
        return new_x, new_y, bob_z
    
    def _isometric_project(self, x: float, y: float, z: float) -> Tuple[float, float]:
        iso_x = (x - y) * math.cos(math.radians(self.ISOMETRIC_ANGLE))
        iso_y = z + (x + y) * math.sin(math.radians(self.ISOMETRIC_ANGLE))
        return iso_x, iso_y
    
    def _calculate_bounds(self) -> Tuple[float, float, float, float, float, float]:
        if not self.blocks:
            return 0, 1, 0, 1, 0, 1
        
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        min_z = float('inf')
        max_z = float('-inf')
        
        for block in self.blocks:
            x, y, z = block.original_position
            width, depth, height = block.get_dimensions()
            
            min_x = min(min_x, x)
            max_x = max(max_x, x + width)
            min_y = min(min_y, y)
            max_y = max(max_y, y + depth)
            min_z = min(min_z, z)
            max_z = max(max_z, z + height)
        
        self.center_x = (min_x + max_x) / 2
        self.center_y = (min_y + max_y) / 2
        
        # Calculate safe radius based on bounds
        max_dx = max(abs(max_x - self.center_x), abs(min_x - self.center_x))
        max_dy = max(abs(max_y - self.center_y), abs(min_y - self.center_y))
        self.safe_radius = math.sqrt(max_dx**2 + max_dy**2) * 0.9  # 90% of max radius
        
        return min_x, max_x, min_y, max_y, min_z, max_z
    
    def _calculate_scale_and_offset(self):
        """Calculate scale to fit within frame with padding"""
        min_x, max_x, min_y, max_y, min_z, max_z = self._calculate_bounds()
        
        # Include some Z variation in calculation
        corners_3d = [
            (min_x, min_y, min_z),
            (max_x, min_y, min_z),
            (min_x, max_y, min_z),
            (max_x, max_y, min_z),
            (min_x, min_y, max_z),
            (max_x, min_y, max_z),
            (min_x, max_y, max_z),
            (max_x, max_y, max_z),
        ]
        
        corners_2d = [self._isometric_project(x, y, z) for x, y, z in corners_3d]
        
        iso_xs = [c[0] for c in corners_2d]
        iso_ys = [c[1] for c in corners_2d]
        
        iso_min_x = min(iso_xs)
        iso_max_x = max(iso_xs)
        iso_min_y = min(iso_ys)
        iso_max_y = max(iso_ys)
        
        iso_width = iso_max_x - iso_min_x
        iso_height = iso_max_y - iso_min_y
        
        # Padding to keep content within frame
        pad_x = self.width * self.padding
        pad_y = self.height * self.padding
        
        # Available space
        available_width = self.width - 2 * pad_x
        available_height = self.height - 2 * pad_y
        
        # Calculate scale to fit
        scale_x = available_width / iso_width if iso_width > 0 else 1
        scale_y = available_height / iso_height if iso_height > 0 else 1
        
        # Use smaller scale to maintain aspect ratio and fit within frame
        stud_size = min(scale_x, scale_y)
        
        # Center offset
        scaled_width = iso_width * stud_size
        scaled_height = iso_height * stud_size
        
        offset_x = (self.width - scaled_width) / 2 - iso_min_x * stud_size
        offset_y = (self.height - scaled_height) / 2 - iso_min_y * stud_size
        
        return stud_size, offset_x, offset_y
    
    def _project_and_scale(self, x: float, y: float, z: float, stud_size: float,
                          offset_x: float, offset_y: float) -> Tuple[float, float]:
        iso_x, iso_y = self._isometric_project(x, y, z)
        screen_x = iso_x * stud_size + offset_x
        screen_y = iso_y * stud_size + offset_y
        return screen_x, screen_y
    
    def _draw_cube_face(self, x: float, y: float, z: float, width: float, depth: float,
                       height: float, color: Tuple, face: str, stud_size: float,
                       offset_x: float, offset_y: float):
        
        if face == 'top':
            corners_3d = [
                (x, y, z + height),
                (x + width, y, z + height),
                (x + width, y + depth, z + height),
                (x, y + depth, z + height),
            ]
            darken_factor = 0.0
        elif face == 'right':
            corners_3d = [
                (x + width, y, z),
                (x + width, y + depth, z),
                (x + width, y + depth, z + height),
                (x + width, y, z + height),
            ]
            darken_factor = 0.2
        elif face == 'left':
            corners_3d = [
                (x, y, z),
                (x, y, z + height),
                (x, y + depth, z + height),
                (x, y + depth, z),
            ]
            darken_factor = 0.4
        else:
            return
        
        corners_2d = [self._project_and_scale(cx, cy, cz, stud_size, offset_x, offset_y)
                     for cx, cy, cz in corners_3d]
        
        darkened_color = tuple(int(c * (1 - darken_factor)) for c in color)
        
        self.draw.polygon(corners_2d, fill=darkened_color, outline=(0, 0, 0))
    
    def _draw_block(self, block: LEGOBlock, stud_size: float, offset_x: float, 
                   offset_y: float):
        x, y, z = block.position
        width, depth, height = block.get_dimensions()
        color = block.color.value
        
        self._draw_cube_face(x, y, z, width, depth, height, color, 'top', stud_size, offset_x, offset_y)
        self._draw_cube_face(x, y, z, width, depth, height, color, 'right', stud_size, offset_x, offset_y)
        self._draw_cube_face(x, y, z, width, depth, height, color, 'left', stud_size, offset_x, offset_y)
    
    def render_frame(self, time: float, twirl_speed: float, loop_duration: float) -> Image.Image:
        """Render a single frame with twirling blocks within frame bounds"""
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        self.draw = ImageDraw.Draw(image, 'RGBA')
        
        stud_size, offset_x, offset_y = self._calculate_scale_and_offset()
        
        # Normalize time to 0-1 for seamless looping
        normalized_time = (time % loop_duration) / loop_duration
        
        # Apply Escher landscape and twirl effects
        for block in self.blocks:
            ox, oy, oz = block.original_position
            
            # First apply Escher landscape transformation
            ex, ey, ez = self._escher_landscape_transform(ox, oy, oz)
            
            # Then apply twirl effect (constrained to safe radius)
            tx, ty, tz = self._twirl_effect(ex, ey, ez, normalized_time * loop_duration, twirl_speed)
            
            block.position = (tx, ty, tz)
        
        # Sort and draw blocks
        sorted_blocks = sorted(self.blocks, key=lambda b: (b.position[0] + b.position[1], b.position[2]))
        
        for block in sorted_blocks:
            self._draw_block(block, stud_size, offset_x, offset_y)
        
        return image
    
    def save_frame(self, image: Image.Image, frame_num: int, output_dir: str):
        """Save frame to file"""
        filename = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
        image.save(filename)

def build_escher_grid_structure(renderer: EscherTwirlingRenderer):
    """Build a grid structure in Escher landscape"""
    colors = [ColorEnum.RED, ColorEnum.BLUE, ColorEnum.GREEN, 
              ColorEnum.YELLOW, ColorEnum.ORANGE, ColorEnum.PURPLE,
              ColorEnum.CYAN, ColorEnum.PINK, ColorEnum.BROWN, 
              ColorEnum.GRAY, ColorEnum.LIME, ColorEnum.INDIGO]
    
    # Create a circular grid centered for better twirling
    grid_width = 5
    grid_height = 10
    
    for x in range(grid_width):
        for y in range(grid_height):
            z = 0
            color = colors[(x + y) % len(colors)]
            original_pos = (x * 2.2, y * 1.8, z)
            
            block = LEGOBlock(
                PieceType.BRICK_2x2,
                color,
                original_pos,
                original_pos
            )
            renderer.add_block(block)

def create_mp4_from_frames(frame_dir: str, output_file: str, fps: int = 30, bitrate: str = "8000k"):
    """Convert PNG frame sequence to MP4 using ffmpeg"""
    
    frame_pattern = os.path.join(frame_dir, "frame_%04d.png")
    
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
    print(f"Command: {' '.join(command)}\n")
    
    try:
        subprocess.run(command, check=True)
        print(f"\nMP4 created successfully: {output_file}")
        
        # Get file size
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating MP4: {e}")
        print("Make sure ffmpeg is installed: brew install ffmpeg (macOS) or sudo apt install ffmpeg (Linux)")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg first.")

def generate_twirling_animation(output_dir: str = "lego_escher_frames", fps: int = 30, duration: float = 15.0):
    """Generate seamlessly looping twirling animation at 2000x2000 resolution"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize renderer at 2000x2000 resolution with safe padding
    renderer = EscherTwirlingRenderer(width=2000, height=2000, padding=0.12)
    build_escher_grid_structure(renderer)
    
    # Animation parameters
    loop_duration = duration  # Full loop duration in seconds
    twirl_speed = (2 * math.pi) / loop_duration  # One full rotation per loop_duration
    
    total_frames = int(duration * fps)
    frame_time = 1.0 / fps
    
    print(f"Generating Escher Twirling Animation")
    print(f"{'='*60}")
    print(f"Resolution: 2000x2000 pixels")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration}s")
    print(f"FPS: {fps}")
    print(f"Twirl speed: {twirl_speed:.4f} rad/s ({360 * twirl_speed / (2 * math.pi):.1f}°/s)")
    print(f"Action: WITHIN FRAME BOUNDS")
    print(f"Seamless loop: YES (start and end frames identical)")
    print(f"{'='*60}\n")
    
    frame_num = 0
    current_time = 0
    
    # Generate all frames
    for i in range(total_frames):
        image = renderer.render_frame(current_time, twirl_speed, loop_duration)
        renderer.save_frame(image, frame_num, output_dir)
        
        if (i + 1) % 30 == 0 or i == 0:
            rotation_degrees = (current_time * twirl_speed * 180 / math.pi) % 360
            print(f"Frame {frame_num:04d} ({i+1:3d}/{total_frames}) - Rotation: {rotation_degrees:6.1f}°")
        
        frame_num += 1
        current_time += frame_time
    
    # Add final frame - identical to frame 0 for seamless loop
    first_frame_path = os.path.join(output_dir, "frame_0000.png")
    last_frame_path = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
    
    if os.path.exists(first_frame_path):
        first_image = Image.open(first_frame_path)
        first_image.save(last_frame_path)
        print(f"Frame {frame_num:04d} - LOOP CLOSURE (identical to frame 0)")
    
    print(f"\n{'='*60}")
    print(f"Frame sequence complete!")
    print(f"Total frames generated: {frame_num + 1}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    # Create MP4 from frames
    output_mp4 = "lego_escher_twirl.mp4"
    create_mp4_from_frames(output_dir, output_mp4, fps=fps, bitrate="8000k")

if __name__ == "__main__":
    generate_twirling_animation(output_dir="lego_escher_frames", fps=30, duration=15.0)
