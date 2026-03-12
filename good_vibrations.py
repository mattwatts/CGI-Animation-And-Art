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

class OtherworldlyWaveRenderer:
    """Renders LEGO blocks as otherworldly harmonic waveforms"""
    
    ISOMETRIC_ANGLE = 30
    
    def __init__(self, width: int = 2000, height: int = 2000,
                 background_color: Tuple = (10, 15, 30), pixel_size: float = 25.0,
                 wave_amplitude: float = 1.0, wave_frequency: float = 1.0):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.pixel_size = pixel_size
        self.wave_amplitude = wave_amplitude  # Controls vertical oscillation
        self.wave_frequency = wave_frequency  # Controls speed of waves
        self.blocks: List[LEGOBlock] = []
    
    def add_block(self, block: LEGOBlock):
        self.blocks.append(block)
    
    def _otherworldly_wave(self, block_index: int, total_blocks: int, time: float) -> Tuple[float, float, float]:
        """Generate otherworldly harmonic wave motion"""
        # Normalize block position along x-axis
        x_normalized = block_index / max(1, total_blocks - 1)
        
        # Distribute blocks across screen width with padding
        padding = 100
        x = padding + x_normalized * (self.width - 2 * padding)
        
        # Primary wave - deep harmonic oscillation
        primary_freq = 0.8 * self.wave_frequency
        primary_phase = x_normalized * math.pi * 4  # Multiple cycles across width
        primary_y = math.sin(time * primary_freq + primary_phase) * self.wave_amplitude * 300
        
        # Secondary wave - harmonic overtone (3x frequency)
        secondary_freq = 2.4 * self.wave_frequency
        secondary_phase = x_normalized * math.pi * 8
        secondary_y = math.sin(time * secondary_freq + secondary_phase) * self.wave_amplitude * 150
        
        # Tertiary wave - ethereal shimmer (5x frequency)
        tertiary_freq = 4.0 * self.wave_frequency
        tertiary_phase = x_normalized * math.pi * 12
        tertiary_y = math.sin(time * tertiary_freq + tertiary_phase) * self.wave_amplitude * 80
        
        # Combine harmonics
        y_offset = primary_y + secondary_y + tertiary_y
        y = self.height / 2 + y_offset
        
        # Clamp to screen
        y = max(50, min(self.height - 50, y))
        
        # Vertical phasing - blocks fade in/out as they move
        # Creates the effect of blocks emerging from and dissolving into the void
        phase_offset = x_normalized * 2 * math.pi
        phase_time = time * self.wave_frequency * 1.5
        depth_phase = math.sin(phase_time + phase_offset)
        
        # Z-coordinate controls opacity and scale
        z = depth_phase
        
        return x, y, z
    
    def _calculate_opacity(self, z_phase: float) -> float:
        """Calculate opacity based on phase (sine wave between 0 and 1)"""
        # Map sine wave (-1 to 1) to opacity (0.3 to 1.0)
        return 0.3 + (z_phase + 1) / 2 * 0.7
    
    def _draw_block_screen_space(self, block: LEGOBlock, opacity: float):
        """Draw block directly in screen space with opacity"""
        x, y, z = block.position
        width, depth, height = block.get_dimensions()
        
        # Clamp position to screen
        x = max(0, min(self.width - width, x))
        y = max(0, min(self.height - depth, y))
        
        color = block.color.value
        
        # Apply opacity to color
        opaque_color = tuple(int(c * opacity) for c in color)
        
        # Draw block as simple rectangles with opacity effect
        # Top face
        self.draw.rectangle(
            [x, y, x + width, y + depth],
            fill=opaque_color,
            outline=tuple(int(c * opacity * 0.7) for c in (50, 50, 50))
        )
        
        # Right face shadow
        shadow_color = tuple(int(c * opacity * 0.5) for c in (0, 0, 0))
        self.draw.rectangle(
            [x + width * 0.2, y + depth * 0.2, x + width, y + depth * 0.5],
            fill=shadow_color
        )
        
        # Left face shadow
        self.draw.rectangle(
            [x - width * 0.1, y + depth * 0.2, x + width * 0.3, y + depth * 0.5],
            fill=shadow_color
        )
    
    def render_frame(self, time: float) -> Image.Image:
        """Render a single frame of otherworldly waves"""
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        self.draw = ImageDraw.Draw(image, 'RGBA')
        
        total_blocks = len(self.blocks)
        
        # Update block positions based on harmonic waves
        for block in self.blocks:
            x, y, z = self._otherworldly_wave(block.index, total_blocks, time)
            block.position = (x, y, z)
        
        # Calculate opacity for each block based on phase
        block_opacities = []
        for block in self.blocks:
            opacity = self._calculate_opacity(block.position[2])
            block_opacities.append(opacity)
        
        # Sort and draw blocks by depth (z-phase)
        sorted_indices = sorted(range(total_blocks), key=lambda i: self.blocks[i].position[2])
        
        for idx in sorted_indices:
            block = self.blocks[idx]
            opacity = block_opacities[idx]
            self._draw_block_screen_space(block, opacity)
        
        # Add ethereal glow effect - draw faint traces of the wave path
        self._draw_wave_traces(time)
        
        return image
    
    def _draw_wave_traces(self, time: float):
        """Draw ethereal traces showing the wave path"""
        trace_points = []
        total_blocks = len(self.blocks)
        
        for i in range(total_blocks):
            x, y, z = self._otherworldly_wave(i, total_blocks, time)
            opacity = self._calculate_opacity(z)
            trace_color = (100, 150, 200, int(opacity * 50))  # Faint cyan trace
            
            # Draw small point
            radius = 2
            self.draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=trace_color
            )
        
        # Draw connecting lines between consecutive blocks
        for i in range(total_blocks - 1):
            x1, y1, z1 = self._otherworldly_wave(i, total_blocks, time)
            x2, y2, z2 = self._otherworldly_wave(i + 1, total_blocks, time)
            opacity1 = self._calculate_opacity(z1)
            opacity2 = self._calculate_opacity(z2)
            avg_opacity = (opacity1 + opacity2) / 2
            
            line_color = (100, 150, 200, int(avg_opacity * 30))
            self.draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)
    
    def save_frame(self, image: Image.Image, frame_num: int, output_dir: str):
        """Save frame to file"""
        filename = os.path.join(output_dir, f"frame_{frame_num:05d}.png")
        image.save(filename)

def build_wave_structure(renderer: OtherworldlyWaveRenderer, num_blocks: int = 40):
    """Build blocks for wave visualization"""
    colors = [ColorEnum.CYAN, ColorEnum.BLUE, ColorEnum.PURPLE, 
              ColorEnum.INDIGO, ColorEnum.PINK, ColorEnum.LIME,
              ColorEnum.YELLOW, ColorEnum.ORANGE, ColorEnum.GREEN]
    
    for i in range(num_blocks):
        color = colors[i % len(colors)]
        
        block = LEGOBlock(
            PieceType.BRICK_2x2,
            color,
            (0, 0, 0),
            (0, 0, 0),
            i,
            pixel_size=25.0
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

def generate_otherworldly_wave_animation(output_dir: str = "lego_wave_frames", fps: int = 30,
                                        duration: float = 120.0, wave_amplitude: float = 1.0,
                                        wave_frequency: float = 1.0):
    """Generate otherworldly wave animation
    
    Args:
        output_dir: Directory to save frames
        fps: Frames per second
        duration: Total duration in seconds
        wave_amplitude: Controls height of oscillation (1.0 = normal)
        wave_frequency: Controls speed of waves (1.0 = normal)
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    renderer = OtherworldlyWaveRenderer(
        width=2000, height=2000,
        background_color=(10, 15, 30),
        pixel_size=25.0,
        wave_amplitude=wave_amplitude,
        wave_frequency=wave_frequency
    )
    
    build_wave_structure(renderer, num_blocks=40)
    
    total_frames = int(duration * fps)
    frame_time = 1.0 / fps
    
    print(f"Generating Otherworldly Wave Animation")
    print(f"{'='*60}")
    print(f"Resolution: {renderer.width}x{renderer.height} pixels")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration}s")
    print(f"FPS: {fps}")
    print(f"Wave Amplitude: {wave_amplitude}x")
    print(f"Wave Frequency: {wave_frequency}x")
    print(f"Background: Deep void (10, 15, 30)")
    print(f"Blocks: 40 across cyan/blue/purple spectrum")
    print(f"{'='*60}\n")
    
    frame_num = 0
    current_time = 0
    
    for i in range(total_frames):
        image = renderer.render_frame(current_time)
        renderer.save_frame(image, frame_num, output_dir)
        
        if (i + 1) % 150 == 0 or i == 0:
            print(f"Frame {frame_num:05d} ({i+1:4d}/{total_frames}) - {current_time:6.1f}s")
        
        frame_num += 1
        current_time += frame_time
    
    # Loop closure
    first_frame_path = os.path.join(output_dir, "frame_00000.png")
    last_frame_path = os.path.join(output_dir, f"frame_{frame_num:05d}.png")
    
    if os.path.exists(first_frame_path):
        first_image = Image.open(first_frame_path)
        first_image.save(last_frame_path)
        print(f"Frame {frame_num:05d} - LOOP CLOSURE")
    
    print(f"\n{'='*60}")
    print(f"Frame sequence complete!")
    print(f"Total frames generated: {frame_num + 1}")
    print(f"{'='*60}\n")
    
    output_mp4 = "lego_otherworldly_wave.mp4"
    create_mp4_from_frames(output_dir, output_mp4, fps=fps, bitrate="8000k")

if __name__ == "__main__":
    # Generate otherworldly wave visualization
    generate_otherworldly_wave_animation(
        output_dir="lego_wave_frames",
        fps=30,
        duration=120.0,
        wave_amplitude=1.0,     # Control vertical oscillation
        wave_frequency=1.0      # Control speed of waves
    )
