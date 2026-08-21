#!/usr/bin/env python3
"""
SciMSPT Phase 3.5: Advanced Scientific Visualization Video Generator
=====================================================================
Creates publication-quality explainer videos with:
- 3D-like scientific visualizations
- Domain-specific data/metrics
- Particle physics effects
- Professional KPI dashboards
- Research-grade imagery

Target Audience: Knowledgeable investors, researchers, domain experts
"""

import os
import sys
import json
import math
import random
import tempfile
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = BASE_DIR / "video-clips" / "phase3" / "startups"
AUDIO_DIR = BASE_DIR / "video-clips" / "phase3" / "audio"

VIDEO_WIDTH = 1280  # HD (optimized)
VIDEO_HEIGHT = 720
FPS = 24  # Optimized framerate

# Color Palettes - Scientific/Professional
COLORS = {
    'bg_deep': '#030712',
    'bg_primary': '#0a1628',
    'bg_secondary': '#111827',
    'quantum_cyan': '#00E5FF',
    'quantum_blue': '#3B82F6',
    'purple': '#A855F7',
    'pink': '#EC4899',
    'green': '#10B981',
    'gold': '#F59E0B',
    'orange': '#F97316',
    'red': '#EF4444',
    'white': '#FFFFFF',
    'text_primary': '#F1F5F9',
    'text_secondary': '#94A3B8',
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_font(size, bold=False):
    """Get font with fallback chain."""
    font_paths = [
        f"/usr/share/fonts/truetype/dejavu/{'DejaVuSans-Bold' if bold else 'DejaVuSans'}.ttf",
        f"/usr/share/fonts/truetype/freefont/{'FreeSansBold' if bold else 'FreeSans'}.ttf",
        f"/usr/share/fonts/truetype/liberation/{'LiberationSans-Bold' if bold else 'LiberationSans-Regular'}.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

# ============================================================================
# ADVANCED DRAWING FUNCTIONS
# ============================================================================

class ScientificRenderer:
    """Advanced renderer for scientific visualizations."""
    
    def __init__(self, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
        self.width = width
        self.height = height
        self.img = None
        self.draw = None
        
    def create_canvas(self, bg_color=None):
        """Create base canvas with gradient background."""
        bg = bg_color or COLORS['bg_deep']
        self.img = Image.new('RGB', (self.width, self.height), hex_to_rgb(bg))
        self.draw = ImageDraw.Draw(self.img)
        
        # Add subtle gradient overlay
        for y in range(self.height):
            alpha = int(15 * math.sin(y / self.height * math.pi))
            r, g, b = hex_to_rgb(COLORS['bg_primary'])
            self.draw.line([(0, y), (self.width, y)], fill=(min(255, r+alpha), min(255, g+alpha), min(255, b+alpha)))
        
        return self.img
    
    def draw_3d_sphere(self, cx, cy, radius, color, glow=True, highlight=True):
        """Draw a 3D-looking sphere with lighting effects."""
        # Outer glow
        if glow:
            for i in range(20, 0, -2):
                alpha = int(10 * (20-i) / 20)
                r, g, b = hex_to_rgb(color)
                glow_color = (min(255, r+alpha*3), min(255, g+alpha*3), min(255, b+alpha*3))
                self.draw.ellipse([cx-radius-i, cy-radius-i, cx+radius+i, cy+radius+i], 
                                 outline=glow_color)
        
        # Main sphere with gradient effect
        for dy in range(-radius, radius, 2):
            dist = abs(dy) / radius
            # Simulate 3D shading
            shade = 1 - (dist * 0.6)
            r, g, b = hex_to_rgb(color)
            shaded = (int(r * shade), int(g * shade), int(b * shade))
            
            # Calculate width at this y position
            if abs(dy) < radius:
                half_width = int(math.sqrt(radius**2 - dy**2))
                self.draw.line(
                    [(cx - half_width, cy + dy), (cx + half_width, cy + dy)],
                    fill=shaded,
                    width=2
                )
        
        # Highlight
        if highlight:
            hl_offset = radius // 3
            hl_radius = radius // 4
            for i in range(hl_radius, 0, -1):
                alpha = int(100 * (hl_radius - i) / hl_radius)
                self.draw.ellipse(
                    [cx - hl_offset - i, cy - hl_offset - i, 
                     cx - hl_offset + i, cy - hl_offset + i],
                    fill=(255, 255, 255, alpha) if alpha < 255 else (255, 255, 255)
                )
    
    def draw_quantum_circuit(self, x, y, width, height, gates=None, color=None):
        """Draw a quantum circuit diagram."""
        color = color or COLORS['quantum_cyan']
        line_color = hex_to_rgb(color)
        
        num_qubits = 4
        qubit_spacing = height // (num_qubits + 1)
        
        # Draw qubit lines
        for i in range(num_qubits):
            qy = y + qubit_spacing * (i + 1)
            self.draw.line([(x, qy), (x + width, qy)], fill=line_color, width=2)
            
            # Qubit label
            self.draw.text((x - 25, qy - 8), f"|q{i}⟩", fill=line_color, font=get_font(14))
        
        # Draw gates if provided
        if gates:
            gate_width = min(40, width // 6)
            for i, (qubit, gate_type, ctrl_qubit) in enumerate(gates):
                gx = x + 60 + i * (gate_width + 30)
                gy = y + qubit_spacing * (qubit + 1)
                
                if gate_type == 'H':
                    # Hadamard gate
                    self.draw.rectangle([gx-gate_width//2, gy-gate_width//2, gx+gate_width//2, gy+gate_width//2],
                                       outline=line_color, width=2)
                    self.draw.text((gx-5, gy-8), "H", fill=line_color, font=get_font(16, bold=True))
                
                elif gate_type == 'X':
                    # Pauli-X (NOT) gate
                    self.draw.ellipse([gx-gate_width//2, gy-gate_width//2, gx+gate_width//2, gy+gate_width//2],
                                     outline=line_color, width=2)
                    self.draw.line([(gx-gate_width//3, gy-gate_width//3), (gx+gate_width//3, gy+gate_width//3)],
                                   fill=line_color, width=2)
                    self.draw.line([(gx+gate_width//3, gy-gate_width//3), (gx-gate_width//3, gy+gate_width//3)],
                                   fill=line_color, width=2)
                
                elif gate_type == 'CNOT':
                    # CNOT gate
                    if ctrl_qubit is not None:
                        cgy = y + qubit_spacing * (ctrl_qubit + 1)
                        # Control dot
                        self.draw.ellipse([gx-5, cgy-5, gx+5, cgy+5], fill=line_color)
                        # Connection line
                        self.draw.line([(gx, cgy), (gx, gy)], fill=line_color, width=2)
                        # Target (X gate circle)
                        self.draw.ellipse([gx-gate_width//2, gy-gate_width//2, gx+gate_width//2, gy+gate_width//2],
                                         outline=line_color, width=2)
                        self.draw.line([(gx-gate_width//3, gy), (gx+gate_width//3, gy)], fill=line_color, width=2)
                
                elif gate_type == 'RZ':
                    # Rotation gate
                    self.draw.ellipse([gx-gate_width//2, gy-gate_width//2, gx+gate_width//2, gy+gate_width//2],
                                     outline=line_color, width=2)
                    self.draw.text((gx-12, gy-8), "Rz", fill=line_color, font=get_font(14, bold=True))
                
                elif gate_type == 'MEASURE':
                    # Measurement
                    self.draw.line([(gx-gate_width//2, gy), (gx, gy-gate_width//3)], fill=line_color, width=2)
                    self.draw.line([(gx, gy-gate_width//3), (gx+gate_width//2, gy)], fill=line_color, width=2)
                    self.draw.polygon([(gx-gate_width//4, gy+5), (gx+gate_width//4, gy+5), (gx, gy+15)], fill=line_color)
    
    def draw_molecule_3d(self, cx, cy, scale=1.0, molecule_type='drug'):
        """Draw a 3D-looking molecular structure."""
        atoms = []
        bonds = []
        
        if molecule_type == 'drug':
            # Drug-like molecule (simplified benzene ring with functional groups)
            atoms = [
                (cx, cy-80*scale, 'C', COLORS['quantum_cyan']),      # Carbon
                (cx+70*scale, cy-40*scale, 'C', COLORS['quantum_cyan']),
                (cx+70*scale, cy+40*scale, 'C', COLORS['quantum_cyan']),
                (cx, cy+80*scale, 'C', COLORS['quantum_cyan']),
                (cx-70*scale, cy+40*scale, 'C', COLORS['quantum_cyan']),
                (cx-70*scale, cy-40*scale, 'C', COLORS['quantum_cyan']),
                (cx, cy, 'N', COLORS['purple']),                      # Nitrogen center
                (cx+120*scale, cy, 'O', COLORS['red']),               # Oxygen
                (cx-120*scale, cy, 'O', COLORS['red']),               # Oxygen
                (cx, cy+140*scale, 'H', COLORS['white']),             # Hydrogen
            ]
            bonds = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0),  # Ring
                     (0,6), (1,6), (3,6), (4,6),                  # To center
                     (1,7), (5,8), (3,9)]                         # Functional groups
        elif molecule_type == 'protein':
            # Alpha helix representation
            for i in range(8):
                angle = i * 0.8
                x = cx + math.cos(angle) * 80 * scale
                y = cy + (i - 4) * 35 * scale + math.sin(angle) * 30 * scale
                color = COLORS['green'] if i % 2 == 0 else COLORS['purple']
                atoms.append((x, y, 'AA', color))
            bonds = [(i, i+1) for i in range(len(atoms)-1)]
        elif molecule_type == 'dna':
            # DNA double helix (simplified)
            for i in range(10):
                angle = i * 0.63
                offset = (i - 5) * 30 * scale
                
                x1 = cx + math.cos(angle) * 50 * scale
                y1 = cy + offset
                x2 = cx + math.cos(angle + math.pi) * 50 * scale
                y2 = cy + offset
                
                atoms.append((x1, y1, 'P', COLORS['quantum_cyan']))
                atoms.append((x2, y2, 'P', COLORS['pink']))
                if i < 9:
                    bonds.append((i*2, i*2+2))  # Strand 1
                    bonds.append((i*2+1, i*2+3))  # Strand 2
                    bonds.append((i*2, i*2+1))  # Base pair
        
        # Draw bonds first (behind atoms)
        for i, j in bonds:
            if i < len(atoms) and j < len(atoms):
                x1, y1, _, _ = atoms[i]
                x2, y2, _, _ = atoms[j]
                
                # 3D bond effect
                self.draw.line([(x1, y1), (x2, y2)], fill=hex_to_rgb(COLORS['text_secondary']), width=3)
        
        # Draw atoms as 3D spheres
        for ax, ay, atom_type, color in atoms:
            radius = 18 if atom_type in ['C', 'N', 'O'] else 12
            self.draw_3d_sphere(ax, ay, radius, color, glow=(atom_type != 'H'))
            
            # Atom label
            font_size = 14 if atom_type in ['P', 'AA'] else 16
            self.draw.text((ax-font_size//3, ay-font_size//2), atom_type, 
                          fill=hex_to_rgb(COLORS['bg_deep']) if color != COLORS['white'] else hex_to_rgb(COLORS['bg_deep']),
                          font=get_font(font_size, bold=True))
    
    def draw_energy_landscape(self, x, y, width, height, data_points=None):
        """Draw a 3D-like energy landscape/surface plot."""
        # Create gradient background for the plot area
        self.draw.rectangle([x, y, x+width, y+height], fill=hex_to_rgb(COLORS['bg_secondary']))
        
        # Grid lines
        grid_color = tuple(int(c * 0.3) for c in hex_to_rgb(COLORS['quantum_cyan']))
        for i in range(0, width, 40):
            alpha = int(30 + 20 * math.sin(i / width * math.pi))
            self.draw.line([(x+i, y), (+x+i, y+height)], fill=(*grid_color[:3],), width=1)
        for i in range(0, height, 40):
            self.draw.line([(x, y+i), (x+width, y+i)], fill=(*grid_color[:3],), width=1)
        
        # Energy surface (simulated potential energy surface)
        points = []
        num_points = 60
        for i in range(num_points):
            px = x + (i / num_points) * width
            
            # Complex energy function with multiple minima
            t = i / num_points * 4 * math.pi
            
            if data_points is None:
                # Default: VQE-style convergence to ground state
                base_energy = 150 + 80 * math.exp(-t/2) * math.cos(t * 3)
                noise = 20 * math.sin(t * 7) * math.exp(-t/3)
                py = y + height/2 + base_energy + noise
            else:
                py = y + height - (data_points[i] if i < len(data_points) else height/2)
            
            py = max(y, min(y+height, py))
            points.append((px, py))
        
        # Draw filled area under curve
        if len(points) > 2:
            fill_points = points + [(points[-1][0], y+height), (points[0][0], y+height)]
            
            # Gradient fill
            for i in range(len(points)-1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                
                # Calculate color based on position
                progress = i / len(points)
                r = int(hex_to_rgb(COLORS['quantum_cyan'])[0] * (1-progress*0.5))
                g = int(hex_to_rgb(COLORS['quantum_cyan'])[1] * (1-progress*0.3))
                b = int(hex_to_rgb(COLORS['quantum_cyan'])[2])
                
                self.draw.polygon([
                    (x1, y1), (x2, y2), (x2, y+height), (x1, y+height)
                ], fill=(r, g, b, 100))
            
            # Main curve line with glow
            for gw in range(6, 0, -2):
                alpha = int(50 * (6-gw) / 6)
                glow_color = (*hex_to_rgb(COLORS['quantum_cyan'])[:3],)
                for i in range(len(points)-1):
                    self.draw.line([points[i], points[i+1]], fill=glow_color, width=gw)
            
            # Points on curve
            for i, (px, py) in enumerate(points[::5]):
                self.draw_3d_sphere(px, py, 6, COLORS['quantum_cyan'], glow=True)
        
        # Axis labels
        axis_color = hex_to_rgb(COLORS['text_secondary'])
        self.draw.text((x, y+height+10), "Molecular Configuration", fill=axis_color, font=get_font(12))
        
        # Rotate Y-axis label
        self.draw.text((x-20, y+height//2), "Energy", fill=axis_color, font=get_font(12))
        
        # Ground state marker
        if points:
            min_y = min(p[1] for p in points)
            min_x = [p[0] for p in points if p[1] == min_y][0]
            self.draw.line([(min_x, min_y), (min_x, y+height)], 
                          fill=hex_to_rgb(COLORS['green']), width=2)
            self.draw.text((min_x+5, min_y-15), "Ground State |ψ₀⟩", 
                          fill=hex_to_rgb(COLORS['green']), font=get_font(11, bold=True))
    
    def draw_probability_cloud(self, cx, cy, radius, num_particles=80, color=None):
        """Draw a quantum probability distribution particle cloud."""
        color = color or COLORS['quantum_cyan']
        
        particles = []
        for _ in range(num_particles):
            # Gaussian distribution for quantum probability
            r = random.gauss(0, radius/2.5)
            theta = random.uniform(0, 2 * math.pi)
            
            px = cx + r * math.cos(theta)
            py = cy + r * math.sin(theta)
            
            # Probability density (higher near center)
            dist = math.sqrt((px-cx)**2 + (py-cy)**2)
            prob = math.exp(-(dist/radius)**2 * 2)
            
            size = max(1, int(prob * 4))
            alpha = int(prob * 180)
            
            particles.append((px, py, size, alpha, prob))
        
        # Sort by probability (draw low prob first)
        particles.sort(key=lambda p: p[4])
        
        # Draw particles
        for px, py, size, alpha, prob in particles:
            r, g, b = hex_to_rgb(color)
            
            # Color variation based on probability
            if prob > 0.7:
                particle_color = (r, g, b)
            elif prob > 0.4:
                particle_color = (int(r*0.8), int(g*0.9), b)
            else:
                particle_color = (int(r*0.6), int(g*0.7), int(b*0.9))
            
            if size > 1:
                self.draw.ellipse([px-size, py-size, px+size, py+size], fill=particle_color)
            else:
                self.draw.point((px, py), fill=particle_color)
        
        # Central bright spot
        self.draw_3d_sphere(cx, cy, 8, color, glow=True)
    
    def draw_kpi_dashboard(self, x, y, width, height, kpis, title="Key Performance Indicators"):
        """Draw an executive KPI dashboard."""
        # Background panel with glass effect
        padding = 24
        panel_rect = [x, y, x+width, y+height]
        
        # Panel shadow
        self.draw.rectangle([panel_rect[0]+4, panel_rect[1]+4, panel_rect[2]+4, panel_rect[3]+4],
                           fill=(0, 0, 0, 100))
        
        # Main panel
        self.draw.rounded_rectangle(panel_rect, radius=16, fill=hex_to_rgb(COLORS['bg_secondary']))
        self.draw.rounded_rectangle(panel_rect, radius=16, outline=hex_to_rgb(COLORS['quantum_cyan']), width=2)
        
        # Title bar
        title_bar_height = 44
        self.draw.rounded_rectangle(
            [x+2, y+2, x+width-2, y+title_bar_height],
            radius=14,
            fill=tuple(int(c*0.15) for c in hex_to_rgb(COLORS['quantum_cyan']))
        )
        
        # Title text
        self.draw.text((x+padding, y+12), title, fill=hex_to_rgb(COLORS['quantum_cyan']), 
                      font=get_font(18, bold=True))
        
        # KPI cards
        if not kpis:
            return
            
        kpi_width = (width - padding*2 - 24) // min(len(kpis), 3)
        kpi_height = 90
        kpi_start_y = y + title_bar_height + 20
        
        for i, kpi in enumerate(kpis):
            row = i // 3
            col = i % 3
            kpi_x = x + padding + col * (kpi_width + 12)
            kpi_y = kpi_start_y + row * (kpi_height + 12)
            
            # Card background
            card_rect = [kpi_x, kpi_y, kpi_x+kpi_width, kpi_y+kpi_height]
            self.draw.rounded_rectangle(card_rect, radius=12, fill=hex_to_rgb(COLORS['bg_primary']))
            self.draw.rounded_rectangle(card_rect, radius=12, 
                                       outline=tuple(int(c*0.3) for c in hex_to_rgb(kpi.get('color', COLORS['quantum_cyan']))),
                                       width=1)
            
            # KPI value
            value_text = str(kpi.get('value', ''))
            self.draw.text((kpi_x+12, kpi_y+12), value_text, 
                          fill=hex_to_rgb(kpi.get('color', COLORS['quantum_cyan'])),
                          font=get_font(28, bold=True))
            
            # KPI label
            self.draw.text((kpi_x+12, kpi_y+50), kpi.get('label', ''), 
                          fill=hex_to_rgb(COLORS['text_secondary']),
                          font=get_font(13))
            
            # Trend indicator (if present)
            trend = kpi.get('trend')
            if trend:
                trend_color = COLORS['green'] if trend > 0 else COLORS['red']
                trend_symbol = '↑' if trend > 0 else '↓'
                self.draw.text((kpi_x+kpi_width-30, kpi_y+15), f"{trend_symbol}{abs(trend)}%",
                              fill=hex_to_rgb(trend_color),
                              font=get_font(14, bold=True))
    
    def draw_wave_function(self, cx, cy, width, height, n_states=3):
        """Draw quantum wave functions with interference patterns."""
        colors = [COLORS['quantum_cyan'], COLORS['purple'], COLORS['pink']]
        
        for state in range(n_states):
            points = []
            amplitude = height * (0.3 - state * 0.08)
            frequency = 2 + state * 1.5
            phase = state * math.pi / 4
            
            for i in range(width):
                px = cx - width/2 + i
                # Wave function ψ(x) = A*sin(kx + φ)*exp(-x²/2σ²)
                x_norm = (i - width/2) / (width/2)
                envelope = math.exp(-x_norm**2 * 2)
                wave = amplitude * math.sin(i * frequency * 0.05 + phase) * envelope
                py = cy + wave - (state - n_states/2) * 40
                points.append((px, py))
            
            # Draw wave
            if len(points) > 1:
                color = colors[state % len(colors)]
                
                # Glow effect
                for gw in range(4, 0, -1):
                    for i in range(len(points)-1):
                        alpha = int(40 * (4-gw) / 4)
                        r, g, b = hex_to_rgb(color)
                        self.draw.line([points[i], points[i+1]], 
                                      fill=(min(255,r+alpha), min(255,g+alpha), min(255,b+alpha)), 
                                      width=gw)
                
                # Main line
                for i in range(len(points)-1):
                    self.draw.line([points[i], points[i+1]], fill=hex_to_rgb(color), width=2)
        
        # Labels
        self.draw.text((cx-width/2, cy+height/2+20), "Position (x)", 
                      fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(11))
        self.draw.text((cx-width/2-40, cy-10), "ψ(x)", 
                      fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(11))
    
    def draw_progress_arc(self, cx, cy, radius, progress, color, label="", value=""):
        """Draw a circular progress indicator with 3D effect."""
        # Background arc
        self.draw.arc([cx-radius, cy-radius, cx+radius, cy+radius], 0, 360,
                     fill=hex_to_rgb(COLORS['bg_secondary']), width=12)
        
        # Progress arc
        end_angle = -90 + (progress * 3.6)  # Start from top
        start_angle = -90
        
        # Glow effect
        for gw in range(radius+8, radius, -2):
            alpha = int(30 * (radius+8-gw) / 8)
            r, g, b = hex_to_rgb(color)
            self.draw.arc([cx-gw, cy-gw, cx+gw, cy+gw], start_angle, end_angle,
                         fill=(min(255,r+alpha), min(255,g+alpha), min(255,b+alpha)), width=4)
        
        # Main arc
        self.draw.arc([cx-radius, cy-radius, cx+radius, cy+radius], start_angle, end_angle,
                     fill=hex_to_rgb(color), width=12)
        
        # Center text
        if value:
            self.draw.text((cx-25, cy-12), value, fill=hex_to_rgb(color), font=get_font(20, bold=True))
        if label:
            self.draw.text((cx-30, cy+25), label, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(11))


# ============================================================================
# VIDEO GENERATION FUNCTIONS
# ============================================================================

def generate_tts(text, output_path, voice="en-US-GuyNeural"):
    """Generate TTS audio using edge-tts."""
    try:
        cmd = ["edge-tts", "--voice", voice, "--text", text, "--write-media", str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        return result.returncode == 0
    except Exception as e:
        print(f"TTS error: {e}")
        return False


def generate_quantum_therapeutics_video():
    """
    Generate advanced Quantum Therapeutics video with:
    - 3D molecular visualizations
    - Quantum circuit diagrams  
    - VQE energy landscapes
    - KPI dashboard
    - Probability clouds
    - Wave function animations
    """
    
    print("=" * 60)
    print("Generating Advanced: Quantum Therapeutics Explainer")
    print("=" * 60)
    
    renderer = ScientificRenderer()
    output_path = OUTPUT_DIR / "quantum_therapeutics_explainer.mp4"
    audio_path = AUDIO_DIR / "quantum_therapeutics_narration.wav"
    
    # Enhanced narration with specific KPIs and technical details
    narration = """
    Quantum Therapeutics represents a paradigm shift in computational drug discovery.
    Their Variational Quantum Eigensolver platform achieves a validated 40-fold speedup 
    in molecular energy calculations compared to classical methods.
    
    Key performance indicators demonstrate exceptional market positioning: 
    94% validation accuracy across 12 peer-reviewed publications, 
    4.2 million dollars in seed funding, 
    and partnerships with three major pharmaceutical companies.
    
    The platform leverages NISQ-era quantum hardware to simulate drug-target binding 
    at the orbital electron level, reducing compound screening time from months to days.
    
    Their proprietary error mitigation techniques achieve chemical accuracy 
    of within 1 kilocalorie per mole—surpassing the gold standard for pharmaceutical applications.
    
    Current pipeline includes programs in oncology, neurodegenerative diseases, 
    and rare genetic disorders with combined addressable market exceeding 80 billion dollars.
    """
    
    # Generate TTS
    print("Generating TTS narration...")
    generate_tts(narration, audio_path, voice="en-US-AriaNeural")
    
    # Define video scenes
    total_duration = 45  # 45 seconds (optimized)
    frames_data = []
    
    # Scene timing (in frames at 30fps)
    fps = FPS
    
    # ===== SCENE 1: Title Card (0-6s) =====
    scene_frames = int(fps * 6)
    for frame_i in range(scene_frames):
        progress = frame_i / scene_frames
        img = renderer.create_canvas()
        draw = renderer.draw
        
        # Animated background particles
        for p in range(15):
            px = (frame_i * (p + 1) * 17 + p * 100) % VIDEO_WIDTH
            py = (frame_i * (p + 1) * 13 + p * 80) % VIDEO_HEIGHT
            size = 2 + math.sin(frame_i * 0.05 + p) * 2
            alpha = int(abs(math.sin(frame_i * 0.03 + p * 0.5)) * 100)
            r, g, b = hex_to_rgb(COLORS['quantum_cyan'])
            draw.ellipse([px-size, py-size, px+size, py+size], 
                        fill=(min(255, r+alpha), g, b))
        
        # Company logo with glow animation
        logo_pulse = 1 + 0.1 * math.sin(frame_i * 0.1)
        logo_size = int(80 * logo_pulse)
        
        # Logo background circle
        draw.ellipse([VIDEO_WIDTH//2-logo_size-20, 160-logo_size-20, 
                     VIDEO_WIDTH//2+logo_size+20, 160+logo_size+20],
                    fill=tuple(int(c*0.1) for c in hex_to_rgb(COLORS['quantum_cyan'])))
        
        draw.ellipse([VIDEO_WIDTH//2-logo_size, 160-logo_size, 
                     VIDEO_WIDTH//2+logo_size, 160+logo_size],
                    fill=hex_to_rgb(COLORS['quantum_cyan']))
        draw.text((VIDEO_WIDTH//2-25, 145), "QT", fill=hex_to_rgb(COLORS['bg_deep']), 
                 font=get_font(48, bold=True))
        
        # Company name with fade-in
        name_alpha = min(255, int(progress * 255 * 2))
        draw.text((VIDEO_WIDTH//2-220, 280), "QUANTUM THERAPEUTICS", 
                 fill=(*hex_to_rgb(COLORS['white']),), font=get_font(52, bold=True))
        
        # Tagline
        tagline = "Quantum-Accelerated Drug Discovery Platform"
        tagline_width = draw.textlength(tagline, font=get_font(22))
        draw.text((VIDEO_WIDTH//2-tagline_width//2, 350), tagline,
                 fill=hex_to_rgb(COLORS['quantum_cyan']), font=get_font(22))
        
        # Subtitle with tech keywords
        keywords = ["VQE Algorithms", "Molecular Simulation", "NISQ Hardware"]
        kw_start_x = VIDEO_WIDTH//2 - 200
        for i, kw in enumerate(keywords):
            kw_x = kw_start_x + i * 150
            kw_alpha = max(0, min(255, int((progress - 0.3) * 255 * 2))) if progress > 0.3 else 0
            draw.rounded_rectangle([kw_x, 420, kw_x+130, 455], radius=20,
                                  fill=tuple(int(c*0.15) for c in hex_to_rgb(COLORS['purple'])),
                                  outline=hex_to_rgb(COLORS['purple']))
            draw.text((kw_x+15, 428), kw, fill=hex_to_rgb(COLORS['text_primary']), font=get_font(13))
        
        # Progress bar
        draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * (frame_i / (total_duration*fps))), VIDEO_HEIGHT],
                       fill=hex_to_rgb(COLORS['quantum_cyan']))
        
        frames_data.append(img)
    
    # ===== SCENE 2: The Problem & Solution (6-15s) =====
    scene_frames = int(fps * 9)
    for frame_i in range(scene_frames):
        progress = frame_i / scene_frames
        img = renderer.create_canvas()
        draw = renderer.draw
        
        # Section header
        draw.text((60, 50), "THE QUANTUM ADVANTAGE IN DRUG DISCOVERY", 
                 fill=hex_to_rgb(COLORS['quantum_cyan']), font=get_font(32, bold=True))
        draw.line([(60, 95), (600, 95)], fill=hex_to_rgb(COLORS['quantum_cyan']), width=3)
        
        # Left side: Classical vs Quantum comparison
        box_y = 130
        box_h = 380
        
        # Classical box
        draw.rounded_rectangle([60, box_y, 450, box_y+box_h], radius=16,
                              fill=hex_to_rgb(COLORS['bg_secondary']),
                              outline=hex_to_rgb(COLORS['red']), width=2)
        draw.text((80, box_y+20), "CLASSICAL COMPUTING", fill=hex_to_rgb(COLORS['red']), 
                 font=get_font(18, bold=True))
        
        classical_issues = [
            ("Months", "Screening Time"),
            ("Limited", "Molecular Accuracy"),
            ("Exponential", "Scaling Cost"),
            ("Approximate", "Solutions Only")
        ]
        for i, (value, label) in enumerate(classical_issues):
            iy = box_y + 60 + i * 75
            draw.text((90, iy), value, fill=hex_to_rgb(COLORS['text_primary']), font=get_font(24, bold=True))
            draw.text((90, iy+28), label, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14))
            # X mark
            draw.text((340, iy+5), "✗", fill=hex_to_rgb(COLORS['red']), font=get_font(24))
        
        # VS divider
        vs_x = VIDEO_WIDTH // 2 - 20
        draw.ellipse([vs_x-30, box_y+box_h//2-30, vs_x+30, box_y+box_h//2+30],
                    fill=hex_to_rgb(COLORS['bg_primary']), outline=hex_to_rgb(COLORS['gold']), width=2)
        draw.text((vs_x-12, box_y+box_h//2-18), "VS", fill=hex_to_rgb(COLORS['gold']), 
                 font=get_font(20, bold=True))
        
        # Quantum box
        qx = vs_x + 60
        draw.rounded_rectangle([qx, box_y, qx+390, box_y+box_h], radius=16,
                              fill=hex_to_rgb(COLORS['bg_secondary']),
                              outline=hex_to_rgb(COLORS['green']), width=2)
        draw.text((qx+20, box_y+20), "QUANTUM COMPUTING", fill=hex_to_rgb(COLORS['green']), 
                 font=get_font(18, bold=True))
        
        quantum_benefits = [
            ("Days", "Screening Time"),
            ("Chemical", "Level Accuracy"),
            ("Polynomial", "Resource Scaling"),
            ("Exact", "Ground States")
        ]
        for i, (value, label) in enumerate(quantum_benefits):
            iy = box_y + 60 + i * 75
            draw.text((qx+30, iy), value, fill=hex_to_rgb(COLORS['text_primary']), font=get_font(24, bold=True))
            draw.text((qx+30, iy+28), label, fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14))
            # Checkmark
            draw.text((qx+330, iy+5), "✓", fill=hex_to_rgb(COLORS['green']), font=get_font(24))
        
        # Speedup callout (animated)
        speedup_scale = 1 + 0.1 * math.sin(frame_i * 0.15)
        speedup_size = int(120 * speedup_scale)
        draw.ellipse([VIDEO_WIDTH//2-speedup_size, 550-speedup_size, 
                     VIDEO_WIDTH//2+speedup_size, 550+speedup_size],
                    fill=tuple(int(c*0.1) for c in hex_to_rgb(COLORS['gold'])))
        draw.text((VIDEO_WIDTH//2-50, 535), "40×", fill=hex_to_rgb(COLORS['gold']), 
                 font=get_font(56, bold=True))
        draw.text((VIDEO_WIDTH//2-65, 595), "SPEEDUP", fill=hex_to_rgb(COLORS['text_secondary']), 
                 font=get_font(16, bold=True))
        
        # Progress bar
        current_frame = int(fps * 6) + frame_i
        draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * (current_frame / (total_duration*fps))), VIDEO_HEIGHT],
                       fill=hex_to_rgb(COLORS['quantum_cyan']))
        
        frames_data.append(img)
    
    # ===== SCENE 3: VQE Technology Deep Dive (15-28s) =====
    scene_frames = int(fps * 13)
    for frame_i in range(scene_frames):
        progress = frame_i / scene_frames
        img = renderer.create_canvas()
        draw = renderer.draw
        
        # Header
        draw.text((60, 40), "VARIATIONAL QUANTUM EIGENSOLVER TECHNOLOGY", 
                 fill=hex_to_rgb(COLORS['purple']), font=get_font(28, bold=True))
        draw.line([(60, 78), (700, 78)], fill=hex_to_rgb(COLORS['purple']), width=3)
        
        # Quantum Circuit Diagram (left side)
        circuit_x, circuit_y = 80, 110
        circuit_w, circuit_h = 500, 250
        
        # Circuit background
        draw.rounded_rectangle([circuit_x-10, circuit_y-10, circuit_x+circuit_w+10, circuit_y+circuit_h+10],
                              radius=12, fill=hex_to_rgb(COLORS['bg_secondary']))
        draw.text((circuit_x, circuit_y-30), "Ansatz Circuit Architecture", 
                 fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14))
        
        # Animate circuit gates appearing
        gates = [
            (0, 'H', None),
            (1, 'H', None),
            (0, 'RZ', None),
            (1, 'RZ', None),
            (0, 'CNOT', 1),
            (0, 'RZ', None),
            (1, 'RZ', None),
            (0, 'CNOT', 1),
            (0, 'MEASURE', None),
            (1, 'MEASURE', None),
        ]
        
        visible_gates = int(len(gates) * min(1, progress * 1.5))
        renderer.draw_quantum_circuit(circuit_x, circuit_y+20, circuit_w, circuit_h, 
                                    gates[:visible_gates], COLORS['purple'])
        
        # Energy Landscape (right side)
        landscape_x = 650
        landscape_y = 100
        landscape_w = 550
        landscape_h = 260
        
        # Generate animated energy data
        energy_data = []
        for i in range(60):
            t = i / 60 * 4 * math.pi
            convergence = min(1, progress * 2)
            base = 150 + 80 * math.exp(-t/2) * math.cos(t * 3) * (1 - convergence * 0.7)
            noise = 20 * math.sin(t * 7) * math.exp(-t/3) * (1 - convergence)
            energy_data.append(base + noise + frame_i * 0.5)
        
        draw.text((landscape_x, landscape_y-25), "Convergence to Ground State |ψ₀⟩", 
                 fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14))
        renderer.draw_energy_landscape(landscape_x, landscape_y, landscape_w, landscape_h, energy_data)
        
        # Wave Function Visualization (bottom left)
        wave_x, wave_y = 80, 400
        draw.rounded_rectangle([wave_x-10, wave_y-10, wave_x+580, wave_y+180], radius=12,
                              fill=hex_to_rgb(COLORS['bg_secondary']))
        draw.text((wave_x, wave_y-5), "Molecular Orbital Wave Functions", 
                 fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14))
        renderer.draw_wave_function(wave_x + 290, wave_y + 85, 500, 100, n_states=3)
        
        # Molecule 3D (bottom right)
        mol_x, mol_y = 720, 400
        draw.rounded_rectangle([mol_x-10, mol_y-10, mol_x+480, mol_y+180], radius=12,
                              fill=hex_to_rgb(COLORS['bg_secondary']))
        draw.text((mol_x, mol_y-5), "Drug-Target Binding Simulation", 
                 fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(14))
        
        # Rotate molecule slowly
        rotation = frame_i * 0.02
        renderer.draw_molecule_3d(mol_x + 230, mol_y + 90, scale=1.2, molecule_type='drug')
        
        # Progress bar
        current_frame = int(fps * 15) + frame_i
        draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * (current_frame / (total_duration*fps))), VIDEO_HEIGHT],
                       fill=hex_to_rgb(COLORS['quantum_cyan']))
        
        frames_data.append(img)
    
    # ===== SCENE 4: KPI Dashboard (28-42s) =====
    scene_frames = int(fps * 14)
    for frame_i in range(scene_frames):
        progress = frame_i / scene_frames
        img = renderer.create_canvas()
        draw = renderer.draw
        
        # Header
        draw.text((60, 40), "VALIDATED PERFORMANCE METRICS", 
                 fill=hex_to_rgb(COLORS['green']), font=get_font(32, bold=True))
        draw.line([(60, 82), (520, 82)], fill=hex_to_rgb(COLORS['green']), width=3)
        
        # Main KPI Dashboard
        kpis = [
            {"value": "94%", "label": "Validation Accuracy", "color": COLORS['quantum_cyan'], "trend": 3},
            {"value": "$4.2M", "label": "Seed Funding Raised", "color": COLORS['green'], "trend": 15},
            {"value": "12", "label": "Peer-Reviewed Papers", "color": COLORS['purple'], "trend": 8},
            {"value": "40×", "label": "Computational Speedup", "color": COLORS['gold'], "trend": 25},
            {"value": "<1", "label": "kcal/mol Chemical Accuracy", "color": COLORS['pink'], "trend": -5},
            {"value": "3", "label": "Pharma Partnerships", "color": COLORS['orange'], "trend": 50},
        ]
        
        # Animated reveal of KPIs
        visible_kpis = int(len(kpis) * min(1, progress * 1.5))
        renderer.draw_kpi_dashboard(80, 110, VIDEO_WIDTH-160, 320, kpis[:visible_kpis], "Executive Summary")
        
        # Circular progress indicators (bottom section)
        metrics = [
            ("94%", 0.94, COLORS['quantum_cyan'], "Accuracy"),
            ("40×", 0.85, COLORS['gold'], "Speedup"),
            ("$4.2M", 0.72, COLORS['green'], "Funding"),
        ]
        
        circle_start_x = 300
        for i, (label, value, color, name) in enumerate(metrics):
            cx = circle_start_x + i * 450
            cy = 560
            anim_progress = min(1, max(0, (progress - 0.3) * 2)) if progress > 0.3 else 0
            
            renderer.draw_progress_arc(cx, cy, 70, value * anim_progress, color, name, 
                                      label if anim_progress > 0.5 else "")
        
        # Market opportunity callout
        if progress > 0.6:
            alpha = min(255, int((progress - 0.6) * 2 * 255))
            draw.rounded_rectangle([VIDEO_WIDTH//2-250, 680, VIDEO_WIDTH//2+250, 750], radius=16,
                                  fill=tuple(int(c*0.1) for c in hex_to_rgb(COLORS['purple'])),
                                  outline=hex_to_rgb(COLORS['purple']))
            draw.text((VIDEO_WIDTH//2-180, 700), "$80B+", fill=hex_to_rgb(COLORS['purple']), 
                     font=get_font(36, bold=True))
            draw.text((VIDEO_WIDTH//2-100, 740), "Addressable Market Opportunity", 
                     fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(16))
        
        # Progress bar
        current_frame = int(fps * 28) + frame_i
        draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * (current_frame / (total_duration*fps))), VIDEO_HEIGHT],
                       fill=hex_to_rgb(COLORS['quantum_cyan']))
        
        frames_data.append(img)
    
    # ===== SCENE 5: Quantum Probability Cloud (42-52s) =====
    scene_frames = int(fps * 10)
    for frame_i in range(scene_frames):
        progress = frame_i / scene_frames
        img = renderer.create_canvas()
        draw = renderer.draw
        
        # Header
        draw.text((60, 40), "QUANTUM STATE VISUALIZATION", 
                 fill=hex_to_rgb(COLORS['pink']), font=get_font(32, bold=True))
        draw.line([(60, 82), (500, 82)], fill=hex_to_rgb(COLORS['pink']), width=3)
        
        # Large probability cloud (center)
        cloud_cx = VIDEO_WIDTH // 2
        cloud_cy = VIDEO_HEIGHT // 2 + 30
        
        # Animated expansion
        expansion = 1 + 0.2 * math.sin(progress * math.pi)
        cloud_radius = int(250 * expansion)
        
        # Multiple overlapping probability clouds
        renderer.draw_probability_cloud(cloud_cx - 150, cloud_cy, int(cloud_radius * 0.7), 
                                      150, COLORS['quantum_cyan'])
        renderer.draw_probability_cloud(cloud_cx + 150, cloud_cy, int(cloud_radius * 0.7), 
                                      150, COLORS['purple'])
        renderer.draw_probability_cloud(cloud_cx, cloud_cy - 50, int(cloud_radius * 0.9), 
                                      200, COLORS['pink'])
        
        # Quantum state labels
        draw.text((cloud_cx-180, cloud_cy-cloud_radius-60), "|ψ₀⟩ Ground State", 
                 fill=hex_to_rgb(COLORS['quantum_cyan']), font=get_font(16, bold=True))
        draw.text((cloud_cx+100, cloud_cy-cloud_radius-60), "|ψ₁⟩ Excited State", 
                 fill=hex_to_rgb(COLORS['purple']), font=get_font(16, bold=True))
        
        # Superposition equation
        eq_y = cloud_cy + cloud_radius + 80
        draw.text((VIDEO_WIDTH//2-200, eq_y), "|ψ⟩ = α|ψ₀⟩ + β|ψ₁⟩", 
                 fill=hex_to_rgb(COLORS['text_primary']), font=get_font(28, bold=True))
        draw.text((VIDEO_WIDTH//2-120, eq_y+40), "Quantum Superposition Principle", 
                 fill=hex_to_rgb(COLORS['text_secondary']), font=get_font(16))
        
        # Measurement probabilities
        if progress > 0.4:
            prob_alpha = min(1, (progress - 0.4) * 2.5)
            draw.rounded_rectangle([VIDEO_WIDTH//2-200, eq_y+80, VIDEO_WIDTH//2+200, eq_y+160], 
                                  radius=12, fill=hex_to_rgb(COLORS['bg_secondary']))
            draw.text((VIDEO_WIDTH//2-170, eq_y+95), "P(|ψ₀⟩) = |α|² = 73%", 
                     fill=hex_to_rgb(COLORS['quantum_cyan']), font=get_font(18, bold=True))
            draw.text((VIDEO_WIDTH//2-170, eq_y+125), "P(|ψ₁⟩) = |β|² = 27%", 
                     fill=hex_to_rgb(COLORS['purple']), font=get_font(18, bold=True))
        
        # Progress bar
        current_frame = int(fps * 42) + frame_i
        draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * (current_frame / (total_duration*fps))), VIDEO_HEIGHT],
                       fill=hex_to_rgb(COLORS['quantum_cyan']))
        
        frames_data.append(img)
    
    # ===== SCENE 6: Call to Action (52-60s) =====
    scene_frames = int(fps * 8)
    for frame_i in range(scene_frames):
        progress = frame_i / scene_frames
        img = renderer.create_canvas()
        draw = renderer.draw
        
        # Final branding
        logo_pulse = 1 + 0.15 * math.sin(frame_i * 0.12)
        logo_size = int(60 * logo_pulse)
        
        draw.ellipse([VIDEO_WIDTH//2-logo_size-15, 180-logo_size-15, 
                     VIDEO_WIDTH//2+logo_size+15, 180+logo_size+15],
                    outline=hex_to_rgb(COLORS['quantum_cyan']), width=3)
        draw.ellipse([VIDEO_WIDTH//2-logo_size, 180-logo_size, 
                     VIDEO_WIDTH//2+logo_size, 180+logo_size],
                    fill=hex_to_rgb(COLORS['quantum_cyan']))
        draw.text((VIDEO_WIDTH//2-18, 168), "QT", fill=hex_to_rgb(COLORS['bg_deep']), 
                 font=get_font(36, bold=True))
        
        # Taglines with staggered appearance
        taglines = [
            ("QUANTUM THERAPEUTICS", 36, COLORS['white'], 240),
            ("Redefining Drug Discovery", 24, COLORS['quantum_cyan'], 295),
            ("From Months to Days. From Approximate to Exact.", 18, COLORS['text_secondary'], 340),
        ]
        
        for text, size, color, y_pos in taglines:
            alpha = min(1, progress * 1.5)
            if alpha > 0:
                tw = draw.textlength(text, font=get_font(size))
                tx = VIDEO_WIDTH//2 - tw//2
                draw.text((tx, y_pos), text, fill=hex_to_rgb(color), font=get_font(size, bold=True))
        
        # Contact/CTA
        if progress > 0.5:
            cta_alpha = min(1, (progress - 0.5) * 2)
            btn_width, btn_height = 280, 56
            btn_x = VIDEO_WIDTH//2 - btn_width//2
            btn_y = 420
            
            # Button glow
            glow_size = int(10 * math.sin(frame_i * 0.1))
            draw.rounded_rectangle([btn_x-glow_size, btn_y-glow_size, 
                                   btn_x+btn_width+glow_size, btn_y+btn_height+glow_size],
                                  radius=28, fill=tuple(int(c*0.2) for c in hex_to_rgb(COLORS['quantum_cyan'])))
            
            # Button
            draw.rounded_rectangle([btn_x, btn_y, btn_x+btn_width, btn_y+btn_height], 
                                  radius=28, fill=hex_to_rgb(COLORS['quantum_cyan']))
            draw.text((btn_x+45, btn_y+16), "EXPLORE RESEARCH →", 
                     fill=hex_to_rgb(COLORS['bg_deep']), font=get_font(18, bold=True))
        
        # Footer info
        draw.text((VIDEO_WIDTH//2-180, VIDEO_HEIGHT-80), "www.quantumtherapeutics.scimspt.io", 
                 fill=hex_to_rgb(COLORS['text_muted']), font=get_font(14))
        draw.text((VIDEO_WIDTH//2-100, VIDEO_HEIGHT-55), "Seed Stage • Series A Opening Q1 2026", 
                 fill=hex_to_rgb(COLORS['text_muted']), font=get_font(13))
        
        # Final progress bar
        current_frame = int(fps * 52) + frame_i
        draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * (current_frame / (total_duration*fps))), VIDEO_HEIGHT],
                       fill=hex_to_rgb(COLORS['quantum_cyan']))
        
        frames_data.append(img)
    
    # Assemble video with FFmpeg
    print(f"Assembling video from {len(frames_data)} frames...")
    
    with tempfile.TemporaryDirectory() as frame_dir:
        # Save all frames
        for i, frame in enumerate(frames_data):
            frame_path = Path(frame_dir) / f"frame_{i:05d}.png"
            frame.save(frame_path, 'PNG', optimize=True)
            
            if (i+1) % 100 == 0:
                print(f"  Saved frame {i+1}/{len(frames_data)}")
        
        # Ensure audio exists
        if not Path(audio_path).exists():
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", str(total_duration), "-acodec", "pcm_s16le", str(audio_path)
            ], capture_output=True)
        
        # FFmpeg assembly command
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", f"{frame_dir}/frame_%05d.png",
            "-i", str(audio_path),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            size_mb = Path(output_path).stat().st_size / (1024*1024)
            print(f"\n✓ Quantum Therapeutics video created!")
            print(f"  Duration: {total_duration}s")
            print(f"  Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
            print(f"  File size: {size_mb:.1f} MB")
            print(f"  Output: {output_path}")
            return True
        else:
            print(f"✗ FFmpeg error: {result.stderr[:500]}")
            return False


def main():
    """Main entry point for advanced video generation."""
    print("\n" + "="*70)
    print("SCIMSPT PHASE 3.5: ADVANCED SCIENTIFIC VIDEO GENERATOR")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate Quantum Therapeutics video
    success = generate_quantum_therapeutics_video()
    
    print("\n" + "="*70)
    if success:
        print("GENERATION COMPLETE")
    else:
        print("GENERATION FINISHED WITH WARNINGS")
    print("="*70)
    
    return success


if __name__ == "__main__":
    main()
