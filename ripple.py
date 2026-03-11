import numpy as np
from PIL import Image, ImageDraw
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import os

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

class RipplingLEGORenderer:
    """Renders LEGO structures with rippling animation"""
    
    ISOMETRIC_ANGLE = 30
    
    def __init__(self, width: int = 2000, height: int = 2000,
                 background_color: Tuple = (240, 240, 245), padding: float = 0.05):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.padding = padding
        self.blocks: List[LEGOBlock] = []
        self.center_x = 0
        self.center_y = 0
    
    def add_block(self, block: LEGOBlock):
        self.blocks.append(block)
    
    def _ripple_effect(self, x: float, y: float, z: float, time: float, 
                      ripple_speed: float, ripple_amplitude: float) -> Tuple[float, float, float]:
        """Apply ripple effect to block position"""
        # Calculate distance from center
        dx = x - self.center_x
        dy = y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Create ripple wave
        wave = math.sin(distance * ripple_speed - time * ripple_speed * 2) * ripple_amplitude
        
        # Apply ripple to z position
        new_z = z + wave
        
        return x, y, new_z
    
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
        
        return min_x, max_x, min_y, max_y, min_z, max_z
    
    def _calculate_scale_and_offset(self):
        min_x, max_x, min_y, max_y, min_z, max_z = self._calculate_bounds()
        
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
        
        pad_x = self.width * self.padding
        pad_y = self.height * self.padding
        
        available_width = self.width - 2 * pad_x
        available_height = self.height - 2 * pad_y
        
        scale_x = available_width / iso_width if iso_width > 0 else 1
        scale_y = available_height / iso_height if iso_height > 0 else 1
        
        stud_size = min(scale_x, scale_y)
        
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
    
    def render_frame(self, time: float, ripple_speed: float, ripple_amplitude: float) -> Image.Image:
        """Render a single frame with ripple effect"""
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        self.draw = ImageDraw.Draw(image, 'RGBA')
        
        stud_size, offset_x, offset_y = self._calculate_scale_and_offset()
        
        # Apply ripple effect to all blocks
        for block in self.blocks:
            ox, oy, oz = block.original_position
            x, y, z = self._ripple_effect(ox, oy, oz, time, ripple_speed, ripple_amplitude)
            block.position = (x, y, z)
        
        # Sort and draw blocks
        sorted_blocks = sorted(self.blocks, key=lambda b: (b.position[0] + b.position[1], b.position[2]))
        
        for block in sorted_blocks:
            self._draw_block(block, stud_size, offset_x, offset_y)
        
        return image
    
    def save_frame(self, image: Image.Image, frame_num: int, output_dir: str):
        """Save frame to file"""
        filename = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
        image.save(filename)

def build_grid_structure(renderer: RipplingLEGORenderer, size: int = 6):
    """Build a simple grid structure for rippling"""
    colors = [ColorEnum.RED, ColorEnum.BLUE, ColorEnum.GREEN, 
              ColorEnum.YELLOW, ColorEnum.ORANGE, ColorEnum.PURPLE]
    
    center = size / 2
    
    for x in range(size):
        for y in range(size):
            z = 0
            color = colors[(x + y) % len(colors)]
            original_pos = (x * 2.5, y * 2.5, z)
            
            block = LEGOBlock(
                PieceType.BRICK_2x2,
                color,
                original_pos,
                original_pos
            )
            renderer.add_block(block)

def generate_animation_sequence(output_dir: str = "lego_ripple_frames", fps: int = 30):
    """Generate animation sequence with rippling"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize renderer
    renderer = RipplingLEGORenderer(width=2000, height=2000)
    build_grid_structure(renderer, size=7)
    
    # Animation parameters
    total_duration = 10.0  # seconds
    slow_phase = 2.0       # slow ripple phase
    crescendo_phase = 4.0  # accelerating ripple phase
    peak_phase = 1.0       # peak ripples
    stillness_phase = 3.0  # still phase
    
    total_frames = int(total_duration * fps)
    frame_time = 1.0 / fps
    
    slow_frames = int(slow_phase * fps)
    crescendo_frames = int(crescendo_phase * fps)
    peak_frames = int(peak_phase * fps)
    stillness_frames = int(stillness_phase * fps)
    
    print(f"Generating {total_frames} frames...")
    print(f"Slow phase: frames 0-{slow_frames}")
    print(f"Crescendo phase: frames {slow_frames}-{slow_frames + crescendo_frames}")
    print(f"Peak phase: frames {slow_frames + crescendo_frames}-{slow_frames + crescendo_frames + peak_frames}")
    print(f"Stillness phase: frames {slow_frames + crescendo_frames + peak_frames}-{total_frames}")
    
    frame_num = 0
    current_time = 0
    
    # Slow ripple phase
    for i in range(slow_frames):
        progress = i / slow_frames if slow_frames > 0 else 0
        ripple_speed = 0.5 + progress * 0.2
        ripple_amplitude = 0.3 + progress * 0.2
        
        image = renderer.render_frame(current_time, ripple_speed, ripple_amplitude)
        renderer.save_frame(image, frame_num, output_dir)
        
        print(f"Frame {frame_num:04d} - Slow phase (speed: {ripple_speed:.2f}, amp: {ripple_amplitude:.2f})")
        
        frame_num += 1
        current_time += frame_time
    
    # Crescendo phase - accelerating ripples
    for i in range(crescendo_frames):
        progress = i / crescendo_frames if crescendo_frames > 0 else 0
        # Quadratic acceleration
        acceleration = progress ** 1.5
        ripple_speed = 0.7 + acceleration * 2.0
        ripple_amplitude = 0.5 + acceleration * 1.5
        
        image = renderer.render_frame(current_time, ripple_speed, ripple_amplitude)
        renderer.save_frame(image, frame_num, output_dir)
        
        print(f"Frame {frame_num:04d} - Crescendo phase (speed: {ripple_speed:.2f}, amp: {ripple_amplitude:.2f})")
        
        frame_num += 1
        current_time += frame_time
    
    # Peak phase - maximum ripples
    for i in range(peak_frames):
        ripple_speed = 2.7
        ripple_amplitude = 2.0
        
        image = renderer.render_frame(current_time, ripple_speed, ripple_amplitude)
        renderer.save_frame(image, frame_num, output_dir)
        
        print(f"Frame {frame_num:04d} - Peak phase (speed: {ripple_speed:.2f}, amp: {ripple_amplitude:.2f})")
        
        frame_num += 1
        current_time += frame_time
    
    # Stillness phase - no ripples
    for i in range(stillness_frames):
        ripple_speed = 0.0
        ripple_amplitude = 0.0
        
        image = renderer.render_frame(current_time, ripple_speed, ripple_amplitude)
        renderer.save_frame(image, frame_num, output_dir)
        
        print(f"Frame {frame_num:04d} - Stillness phase")
        
        frame_num += 1
        current_time += frame_time
    
    # Ensure loop closure - fade back to frame 0 state
    # Duplicate first frame at end for smooth loop
    first_frame_path = os.path.join(output_dir, "frame_0000.png")
    last_frame_path = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
    
    if os.path.exists(first_frame_path):
        first_image = Image.open(first_frame_path)
        first_image.save(last_frame_path)
        print(f"Frame {frame_num:04d} - Loop closure (identical to frame 0)")
    
    print(f"\nAnimation sequence complete!")
    print(f"Total frames generated: {frame_num + 1}")
    print(f"Output directory: {output_dir}")
    print(f"To create video: ffmpeg -framerate {fps} -i {output_dir}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p lego_ripple.mp4")

if __name__ == "__main__":
    generate_animation_sequence(output_dir="ripple_frames", fps=30)
