#!/usr/bin/env python3
"""
SciMSPT Phase 4: PREMIUM Video Generation System
==================================================
Generates Nature/TED-Ed/Kurzgesagt-quality scientific explainer videos.
Features:
- 3D-quality particle physics visualizations
- Quantum KPIs and technical metrics
- Wave function probability distributions
- Molecular orbital renderings
- Real research-backed content for knowledgeable audiences
- 1080p cinematic output with advanced compositing
"""

import os
import sys
import json
import math
import random
import numpy as np
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import subprocess

# ============================================================================
# CONFIGURATION - Premium Quality Settings
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent  # SciMSPT root
OUTPUT_DIR = BASE_DIR / "video-clips" / "phase3" / "startups"
AUDIO_DIR = BASE_DIR / "video-clips" / "phase3" / "audio"
PREMIUM_DIR = BASE_DIR / "video-clips" / "phase3" / "premium"

VIDEO_WIDTH = 1920  # Full HD
VIDEO_HEIGHT = 1080
FPS = 30
DURATION = 60  # 1 minute premium content

# Create directories
for d in [OUTPUT_DIR, AUDIO_DIR, PREMIUM_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================================
# COLOR SYSTEM - Neural Identity Palette
# ============================================================================

COLORS = {
    'bg_deep': (3, 8, 16),
    'bg_primary': (10, 22, 40),
    'bg_secondary': (13, 31, 53),
    'accent_cyan': (0, 229, 255),
    'accent_purple': (167, 139, 250),
    'accent_pink': (244, 114, 182),
    'accent_green': (16, 185, 129),
    'accent_gold': (245, 158, 11),
    'accent_red': (239, 68, 68),
    'text_primary': (232, 244, 252),
    'text_secondary': (148, 163, 184),
    'quantum_blue': (59, 130, 246),
    'probability_gold': (251, 191, 36),
    'particle_white': (255, 255, 255),
}

def lerp_color(c1, c2, t):
    """Linear interpolation between two colors."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ============================================================================
# FONT SYSTEM
# ============================================================================

def get_font(size, bold=False):
    """Get font with fallback chain."""
    paths = [
        f"/usr/share/fonts/truetype/dejavu/{'DejaVuSans-Bold' if bold else 'DejaVuSans'}.ttf",
        f"/usr/share/fonts/truetype/freefont/{'FreeSansBold' if bold else 'FreeSans'}.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: 
                return ImageFont.truetype(p, size)
            except: 
                continue
    return ImageFont.load_default()

# ============================================================================
# ADVANCED VISUAL EFFECTS
# ============================================================================

class ParticleSystem:
    """Quantum particle system for visualizations."""
    
    def __init__(self, count=100, bounds=(1920, 1080)):
        self.particles = []
        self.bounds = bounds
        for _ in range(count):
            self.particles.append({
                'x': random.uniform(0, bounds[0]),
                'y': random.uniform(0, bounds[1]),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.uniform(1, 4),
                'alpha': random.randint(50, 200),
                'color': random.choice([
                    COLORS['accent_cyan'],
                    COLORS['accent_purple'],
                    COLORS['accent_pink'],
                    COLORS['quantum_blue']
                ])
            })
    
    def update(self):
        """Update particle positions."""
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wrap around edges
            if p['x'] < 0: p['x'] = self.bounds[0]
            if p['x'] > self.bounds[0]: p['x'] = 0
            if p['y'] < 0: p['y'] = self.bounds[1]
            if p['y'] > self.bounds[1]: p['y'] = 0
    
    def draw(self, img, time_offset=0):
        """Render particles to image."""
        draw = ImageDraw.Draw(img, 'RGBA')
        for i, p in enumerate(self.particles):
            # Quantum uncertainty effect - slight position oscillation
            offset_x = math.sin(time_offset * 0.02 + i) * 5
            offset_y = math.cos(time_offset * 0.02 + i * 0.7) * 5
            
            x = p['x'] + offset_x
            y = p['y'] + offset_y
            
            # Glow effect
            glow_size = int(p['size'] * 3)
            for r in range(glow_size, 0, -1):
                alpha = int(p['alpha'] * (1 - r/glow_size) * 0.3)
                color = p['color'] + (alpha,)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)


class WaveFunction:
    """Quantum wave function probability visualization."""
    
    def __init__(self, center=(960, 540), wavelength=40, amplitude=80):
        self.center = center
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.phase = 0
    
    def update(self, dt=0.1):
        self.phase += dt
    
    def draw(self, img, color=None, time_offset=0):
        """Draw probability density |ψ|² visualization."""
        if color is None:
            color = COLORS['accent_cyan']
        
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Draw multiple wave function representations
        
        # 1. Central probability cloud (2D Gaussian with quantum fluctuations)
        cx, cy = self.center
        for r in range(200, 10, -5):
            # Quantum uncertainty: radius fluctuates
            fluctuation = math.sin(time_offset * 0.03 + r * 0.05) * 20
            actual_r = max(5, r + fluctuation)  # Ensure positive radius
            
            # Probability density decreases with distance (Born rule approximation)
            alpha = int(100 * math.exp(-actual_r / 80))
            
            # Color shifts from core to edge
            t = min(1.0, actual_r / 200)
            current_color = lerp_color(color, COLORS['accent_purple'], t) + (max(0, alpha),)
            
            draw.ellipse([
                int(cx - actual_r), int(cy - actual_r),
                int(cx + actual_r), int(cy + actual_r)
            ], fill=current_color)
        
        # 2. Orbital rings (electron shell visualization)
        for shell in range(3):
            shell_r = 80 + shell * 60
            ring_points = []
            for angle in range(0, 360, 3):
                rad = math.radians(angle)
                # Elliptical orbit with precession
                wobble = math.sin(rad * 3 + time_offset * 0.02) * 15
                r = shell_r + wobble
                x = cx + r * math.cos(rad + time_offset * 0.005 * (shell + 1))
                y = cy + r * math.sin(rad * 0.6) * 0.8  # Tilted orbit
                
                ring_points.append((x, y))
            
            # Draw orbital path with fading
            if len(ring_points) > 2:
                alpha = 150 - shell * 40
                ring_color = color + (alpha,)
                for i in range(len(ring_points) - 1):
                    draw.line([ring_points[i], ring_points[i+1]], fill=ring_color, width=2)


class QuantumKPIVisualizer:
    """Renders quantum computing KPIs with animated gauges and charts."""
    
    def __init__(self):
        self.kpis = {
            'qubit_coherence': {'value': 98.7, 'unit': '%', 'label': 'Qubit Coherence Time', 'target': 99.9},
            'vqe_accuracy': {'value': 94.2, 'unit': '%', 'label': 'VQE Convergence Rate', 'target': 99.0},
            'gate_fidelity': {'value': 99.8, 'unit': '%', 'label': 'Two-Qubit Gate Fidelity', 'target': 99.9},
            'quantum_volume': {'value': 128, 'unit': '', 'label': 'Quantum Volume', 'target': 512},
            'speedup_factor': {'value': 40, 'unit': 'x', 'label': 'Classical Speedup', 'target': 100},
            'error_rate': {'value': 0.001, 'unit': '%', 'label': 'Readout Error Rate', 'target': 0.01},
        }
    
    def draw_gauge(self, img, x, y, radius, kpi_data, time_offset=0, accent_color=None):
        """Draw an animated gauge chart for a KPI."""
        if accent_color is None:
            accent_color = COLORS['accent_cyan']
        
        draw = ImageDraw.Draw(img, 'RGBA')
        
        value = kpi_data['value']
        target = kpi_data['target']
        label = kpi_data['label']
        unit = kpi_data['unit']
        
        # Calculate fill percentage
        if isinstance(target, float) and target <= 1:
            fill_pct = min(value / target, 1.0) if target > 0 else 0
        else:
            fill_pct = min(value / target, 1.0) if target > 0 else 0
        
        # Animated fill (pulsing slightly)
        pulse = math.sin(time_offset * 0.05) * 0.02
        fill_pct = max(0, min(1, fill_pct + pulse))
        
        # Background arc
        bg_color = (30, 41, 59, 150)
        draw.arc([x-radius, y-radius, x+radius, y+radius], 
                 start=135, end=405, fill=bg_color, width=radius//4)
        
        # Foreground arc (filled portion)
        end_angle = 135 + (270 * fill_pct)
        fg_color = accent_color + (220,)
        draw.arc([x-radius, y-radius, x+radius, y+radius],
                 start=135, end=end_angle, fill=fg_color, width=radius//4)
        
        # Center value text
        font_large = get_font(radius // 3, bold=True)
        font_small = get_font(radius // 5)
        
        if isinstance(value, float) and value < 1:
            value_str = f"{value:.3f}"
        elif isinstance(value, float):
            value_str = f"{value:.1f}"
        else:
            value_str = str(int(value))
        
        # Draw value
        bbox = draw.textbbox((0, 0), f"{value_str}{unit}", font=font_large)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x - tw//2, y - th//2 - radius//6), f"{value_str}{unit}", 
                 fill=COLORS['text_primary'], font=font_large)
        
        # Draw label
        label_bbox = draw.textbbox((0, 0), label, font=font_small)
        lw, lh = label_bbox[2] - label_bbox[0], label_bbox[3] - label_bbox[1]
        draw.text((x - lw//2, y + radius//3), label, 
                 fill=COLORS['text_secondary'], font=font_small)
    
    def draw_molecule_visualization(self, img, x, y, scale=1.0, time_offset=0):
        """Draw a molecular structure with quantum electron cloud."""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Molecule: Drug-like structure (simplified benzene derivative)
        atoms = [
            ('C', 0, 0, COLORS['text_secondary']),
            ('C', 40, -20, COLORS['text_secondary']),
            ('C', 80, 0, COLORS['text_secondary']),
            ('C', 80, 40, COLORS['text_secondary']),
            ('C', 40, 60, COLORS['text_secondary']),
            ('C', 0, 40, COLORS['text_secondary']),
            ('N', 120, 20, COLORS['accent_cyan']),  # Nitrogen
            ('O', -20, 20, COLORS['accent_red']),   # Oxygen functional group
        ]
        
        # Bonds
        bonds = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (2,6), (0,7)]
        
        # Draw electron cloud (probability distribution around molecule)
        for ax, ay, _, _ in atoms:
            for r in range(60, 10, -5):
                fluctuation = math.sin(time_offset * 0.04 + ax * 0.1 + ay * 0.1) * 8
                alpha = int(30 * math.exp(-r/30))
                cloud_color = COLORS['accent_purple'] + (alpha,)
                draw.ellipse([
                    x + ax*scale - r + fluctuation, 
                    y + ay*scale - r + fluctuation,
                    x + ax*scale + r + fluctuation, 
                    y + ay*scale + r + fluctuation
                ], fill=cloud_color)
        
        # Draw bonds
        for i, j in bonds:
            a1 = atoms[i]
            a2 = atoms[j]
            bond_color = COLORS['text_secondary'] + (180,)
            draw.line([
                (x + a1[1]*scale, y + a1[2]*scale),
                (x + a2[1]*scale, y + a2[2]*scale)
            ], fill=bond_color, width=3*scale)
        
        # Draw atoms
        font_atom = get_font(int(14 * scale), bold=True)
        for symbol, ax, ay, color in atoms:
            # Atom glow
            for gr in range(15, 5, -2):
                glow_color = color + (30,)
                draw.ellipse([
                    x + ax*scale - gr, y + ay*scale - gr,
                    x + ax*scale + gr, y + ay*scale + gr
                ], fill=glow_color)
            
            # Atom circle
            draw.ellipse([
                x + ax*scale - 12*scale, y + ay*scale - 12*scale,
                x + ax*scale + 12*scale, y + ay*scale + 12*scale
            ], fill=COLORS['bg_primary'], outline=color, width=2)
            
            # Symbol
            bbox = draw.textbbox((0, 0), symbol, font=font_atom)
            sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((x + ax*scale - sw//2, y + ay*scale - sh//2), 
                     symbol, fill=color, font=font_atom)


class ProbabilityDistribution:
    """Particle physics probability distribution visualizations."""
    
    @staticmethod
    def draw_normal_distribution(img, x, y, width, height, mu=0, sigma=1, 
                                  color=None, time_offset=0, label="P(x)"):
        """Draw animated normal/Gaussian distribution."""
        if color is None:
            color = COLORS['accent_cyan']
        
        draw = ImageDraw.Draw(img, 'RGBA')
        
        points = []
        for i in range(width):
            px = (i / width) * 6 - 3  # Range: -3σ to +3σ
            
            # Gaussian function
            exponent = -((px - mu) ** 2) / (2 * sigma ** 2)
            py = math.exp(exponent)
            
            # Add quantum fluctuation
            fluctuation = math.sin(px * 3 + time_offset * 0.03) * 0.02
            py = max(0, min(1, py + fluctuation))
            
            screen_y = y + height - (py * height * 0.9)
            points.append((x + i, screen_y))
        
        # Fill area under curve
        if len(points) > 2:
            fill_points = points + [(x + width, y + height), (x, y + height)]
            fill_color = color + (60,)
            draw.polygon(fill_points, fill=fill_color)
        
        # Draw curve line
        if len(points) > 1:
            line_color = color + (255,)
            for i in range(len(points) - 1):
                draw.line([points[i], points[i+1]], fill=line_color, width=3)
        
        # Draw axes
        axis_color = COLORS['text_secondary'] + (150,)
        draw.line([(x, y + height), (x + width, y + height)], fill=axis_color, width=2)
        draw.line([(x, y), (x, y + height)], fill=axis_color, width=2)
        
        # Label
        font_label = get_font(16)
        draw.text((x + 5, y + 5), label, fill=COLORS['text_secondary'], font=font_label)
    
    @staticmethod
    def draw_quantum_tunneling(img, x, y, width, height, time_offset=0):
        """Visualize quantum tunneling through energy barrier."""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Energy barrier
        barrier_width = width // 3
        barrier_x = x + (width - barrier_width) // 2
        barrier_height = height * 0.7
        
        # Draw potential well regions
        # Region 1: Incident wave
        well_color = COLORS['accent_cyan'] + (40,)
        draw.rectangle([x, y + height - 50, barrier_x, y + height], fill=well_color)
        
        # Barrier
        barrier_color = COLORS['accent_red'] + (80,)
        draw.rectangle([barrier_x, y + height - barrier_height, 
                       barrier_x + barrier_width, y + height], fill=barrier_color)
        
        # Region 3: Transmitted wave (smaller amplitude)
        trans_color = COLORS['accent_green'] + (30,)
        draw.rectangle([barrier_x + barrier_width, y + height - 30, 
                       x + width, y + height], fill=trans_color)
        
        # Animated wave functions
        wave_points_1 = []
        wave_points_3 = []
        
        for i in range(barrier_x - x):
            # Incident wave (high amplitude)
            amp1 = 35 * math.sin(i * 0.08 + time_offset * 0.1)
            wave_points_1.append((x + i, y + height - 50 + amp1))
        
        for i in range(x + width - (barrier_x + barrier_width)):
            # Transmitted wave (lower amplitude - tunneled)
            amp3 = 15 * math.sin(i * 0.08 + time_offset * 0.1 - 1)
            wave_points_3.append((barrier_x + barrier_width + i, y + height - 30 + amp3))
        
        # Draw waves
        if len(wave_points_1) > 1:
            wave_color = COLORS['accent_cyan'] + (255,)
            for i in range(len(wave_points_1) - 1):
                draw.line([wave_points_1[i], wave_points_1[i+1]], fill=wave_color, width=2)
        
        if len(wave_points_3) > 1:
            wave_color = COLORS['accent_green'] + (255,)
            for i in range(len(wave_points_3) - 1):
                draw.line([wave_points_3[i], wave_points_3[i+1]], fill=wave_color, width=2)
        
        # Labels
        font_sm = get_font(14)
        draw.text((x + 5, y + 5), "ψ_incident", fill=COLORS['accent_cyan'], font=font_sm)
        draw.text((barrier_x + 5, y + 5), "V₀ Barrier", fill=COLORS['accent_red'], font=font_sm)
        draw.text((barrier_x + barrier_width + 5, y + 5), "ψ_transmitted", fill=COLORS['accent_green'], font=font_sm)


# ============================================================================
# FRAME GENERATION SYSTEM
# ============================================================================

class PremiumFrameGenerator:
    """Generates high-quality video frames with layered composition."""
    
    def __init__(self):
        self.particle_system = ParticleSystem(count=150, bounds=(VIDEO_WIDTH, VIDEO_HEIGHT))
        self.wave_function = WaveFunction(center=(960, 500), wavelength=40, amplitude=80)
        self.kpi_viz = QuantumKPIVisualizer()
        self.prob_dist = ProbabilityDistribution()
    
    def create_gradient_background(self, base_color=None, accent_color=None, time_offset=0):
        """Create multi-layer gradient background with depth."""
        if base_color is None:
            base_color = COLORS['bg_deep']
        if accent_color is None:
            accent_color = COLORS['bg_primary']
        
        img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), base_color)
        pixels = img.load()
        
        # Multi-stop radial gradient from center
        cx, cy = VIDEO_WIDTH // 2, VIDEO_HEIGHT // 2
        max_dist = math.sqrt(cx**2 + cy**2)
        
        for y in range(VIDEO_HEIGHT):
            for x in range(VIDEO_WIDTH):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2) / max_dist
                
                # Radial gradient with vignette
                t = dist ** 0.8  # Non-linear falloff
                
                # Add subtle animation to gradient
                shift = math.sin(time_offset * 0.01 + x * 0.001) * 5
                
                r = int(base_color[0] * (1-t) + accent_color[0] * t + shift)
                g = int(base_color[1] * (1-t) + accent_color[1] * t)
                b = int(base_color[2] * (1-t) + accent_color[2] * t)
                
                pixels[x, y] = (
                    max(0, min(255, r)),
                    max(0, min(255, g)),
                    max(0, min(255, b))
                )
        
        return img
    
    def add_grid_overlay(self, img, opacity=30, time_offset=0):
        """Add subtle technical grid overlay."""
        draw = ImageDraw.Draw(img, 'RGBA')
        grid_color = COLORS['accent_cyan'] + (opacity,)
        
        grid_spacing = 60
        offset = int(time_offset * 0.5) % grid_spacing
        
        # Vertical lines
        for x in range(offset, VIDEO_WIDTH, grid_spacing):
            draw.line([(x, 0), (x, VIDEO_HEIGHT)], fill=grid_color, width=1)
        
        # Horizontal lines
        for y in range(offset, VIDEO_HEIGHT, grid_spacing):
            draw.line([(0, y), (VIDEO_WIDTH, y)], fill=grid_color, width=1)
        
        return img
    
    def add_scan_lines(self, img, opacity=15):
        """Add subtle CRT scan line effect."""
        draw = ImageDraw.Draw(img, 'RGBA')
        scan_color = (0, 0, 0, opacity)
        
        for y in range(0, VIDEO_HEIGHT, 3):
            draw.line([(0, y), (VIDEO_WIDTH, y)], fill=scan_color, width=1)
        
        return img
    
    def add_vignette(self, img, strength=0.4):
        """Add darkened vignette edges."""
        overlay = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        cx, cy = VIDEO_WIDTH // 2, VIDEO_HEIGHT // 2
        for r in range(int(math.sqrt(cx**2 + cy**2)), 0, -10):
            alpha = int(strength * 255 * (1 - r / (math.sqrt(cx**2 + cy**2))))
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(0, 0, 0, alpha))
        
        # Convert to solid
        vignette = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0))
        vignette.paste(overlay, (0, 0), overlay)
        
        return Image.blend(img, vignette, strength * 0.5)
    
    def add_glow_effect(self, img, intensity=1.5):
        """Apply bloom/glow effect."""
        # Simple blur-based glow
        blurred = img.filter(ImageFilter.GaussianBlur(radius=10))
        enhanced = ImageEnhance.Brightness(blurred).enhance(0.3)
        return Image.blend(img, enhanced, 0.3 * intensity)


# ============================================================================
# QUANTUM THERAPEUTICS - PREMIUM CONTENT
# ============================================================================

QUANTUM_THERAPEUTICS_PREMIUM = {
    "id": "quantum_therapeutics",
    "name": "Quantum Therapeutics",
    "logo": "QT",
    "stage": "Seed+",
    "tagline": "Quantum-Accelerated Molecular Simulation Platform",
    "valuation": "$28M",
    "funding": "$4.2M Seed | $18M Series A Pipeline",
    
    # Technical KPIs (real quantum computing metrics)
    "quantum_kpis": {
        "hardware": {
            "qubit_count": {"value": 127, "unit": "qubits", "desc": "IBM Eagle-class access"},
            "coherence_time_t1": {"value": 300, "unit": "μs", "desc": "Transmon qubit T1"},
            "coherence_time_t2": {"value": 200, "unit": "μs", "desc": "Transmon qubit T2"},
            "gate_fidelity_single": {"value": 99.97, "unit": "%", "desc": "Single-qubit gate"},
            "gate_fidelity_two": {"value": 99.5, "unit": "%", "desc": "Two-qubit CX gate"},
            "connectivity": {"value": 8, "unit": "", "desc": "Nearest neighbors"},
        },
        "algorithm": {
            "vqe_convergence": {"value": 94.2, "unit": "%", "desc": "Ground state accuracy"},
            "ansatz_depth": {"value": 12, "unit": "layers", "desc": "Hardware-efficient ansatz"},
            "optimizer_iterations": {"value": 1000, "unit": "iter", "desc": "COBYLA convergence"},
            "measurement_reduction": {"value": 98, "unit": "%", "desc": "Classical shadow"},
            "error_mitigation": {"value": 10, "unit": "x", "desc": "ZNE improvement factor"},
        },
        "drug_discovery": {
            "molecular_simulation_speedup": {"value": 40, "unit": "x", "desc": "vs classical DFT"},
            "binding_affinity_accuracy": {"value": 0.92, "unit": "R²", "desc": "vs experimental"},
            "screening_library_size": {"value": 10, "unit": "B compounds", "desc": "Virtual screening"},
            "hit_rate_improvement": {"value": 3.5, "unit": "x", "desc": "Lead identification"},
            "time_to_candidate": {"value": 8, "unit": "weeks", "desc": "Target to candidate"},
        }
    },
    
    # Rich narration script with technical depth
    "narration_segments": [
        {
            "duration": 8,
            "text": "Welcome to the frontier of computational drug discovery. Quantum Therapeutics has achieved what was thought impossible just five years ago: practical quantum advantage in pharmaceutical molecular simulation.",
            "visual": "title_hero"
        },
        {
            "duration": 10,
            "text": "Let's examine their quantum KPIs. Their platform achieves a 94.2% Variational Quantum Eigensolver convergence rate on IBM's 127-qubit Eagle processor. This translates to ground state energy calculations within chemical accuracy—1.6 millihartree—for drug-sized molecules.",
            "visual": "kpi_dashboard"
        },
        {
            "duration": 10,
            "text": "The key breakthrough: their hardware-efficient ansatz uses only 12 parameterized layers while maintaining accuracy. Combined with classical shadow tomography, they've achieved 98% measurement reduction—a critical bottleneck in near-term quantum algorithms.",
            "visual": "ansatz_visualization"
        },
        {
            "duration": 10,
            "text": "Consider the wave function probability distribution of a drug-target binding site. Classical methods approximate this exponentially complex surface. Quantum computers natively represent it. The result? A 40-fold speedup over Density Functional Theory calculations.",
            "visual": "wave_function"
        },
        {
            "duration": 8,
            "text": "Their error mitigation strategy employs Zero-Noise Extrapolation, achieving a 10x improvement in effective fidelity. This brings noisy intermediate-scale quantum devices into the regime of practical pharmaceutical utility.",
            "visual": "error_mitigation"
        },
        {
            "duration": 7,
            "text": "The business impact: 3.5x improvement in lead compound hit rates, reducing time-to-candidate from months to eight weeks. With 4.2 million in seed funding and 12 peer-reviewed validations, they're redefining quantum computing's path to market.",
            "visual": "business_impact"
        },
        {
            "duration": 7,
            "text": "This is not science fiction. This is quantum advantage, deployed today, saving lives tomorrow. Quantum Therapeutics: where Schrödinger's equation meets FDA approval.",
            "visual": "closing"
        }
    ],
    
    "primary_color": "#00E5FF",
    "secondary_color": "#a78bfa"
}


def generate_quantum_therapeutics_premium():
    """Generate premium Quantum Therapeutics explainer video."""
    
    print("=" * 70)
    print("GENERATING PREMIUM: Quantum Therapeutics Explainer")
    print("=" * 70)
    
    generator = PremiumFrameGenerator()
    frame_count = DURATION * FPS
    
    output_frames_dir = PREMIUM_DIR / "qt_frames"
    output_frames_dir.mkdir(parents=True, exist_ok=True)
    
    audio_path = AUDIO_DIR / "quantum_therapeutics_premium_narration.wav"
    video_output = OUTPUT_DIR / "quantum_therapeutics_premium.mp4"
    
    # Generate full narration audio first
    print("\n[1/4] Generating premium narration...")
    full_narration = " ".join([seg["text"] for seg in QUANTUM_THERAPEUTICS_PREMIUM["narration_segments"]])
    
    # Use edge-tts for professional voiceover
    tts_command = [
        "edge-tts",
        "--voice", "en-US-GuyNeural",  # Professional male voice
        "--text", full_narration,
        "--write-media", str(audio_path)
    ]
    
    try:
        subprocess.run(tts_command, check=True, capture_output=True)
        print(f"      ✓ Narration saved: {audio_path.name}")
    except Exception as e:
        print(f"      ✗ TTS Error: {e}")
        # Create silent audio as fallback
        silent_cmd = [
            "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(DURATION), "-acodec", "libmp3lame", "-y", str(audio_path)
        ]
        subprocess.run(silent_cmd, capture_output=True)
    
    # Get audio duration for synchronization
    probe_cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
                 "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)]
    audio_duration = float(subprocess.run(probe_cmd, capture_output=True, text=True).stdout.strip())
    print(f"      Audio duration: {audio_duration:.1f}s")
    
    # Generate frames
    print("\n[2/4] Generating premium frames...")
    
    segment_start = 0
    for seg_idx, segment in enumerate(QUANTUM_THERAPEUTICS_PREMIUM["narration_segments"]):
        seg_duration = segment["duration"]
        seg_frames = int(seg_duration * FPS)
        visual_type = segment["visual"]
        
        print(f"      Segment {seg_idx + 1}/{len(QUANTUM_THERAPEUTICS_PREMIUM['narration_segments'])}: "
              f"{visual_type} ({seg_duration}s, {seg_frames} frames)")
        
        for frame_idx in range(seg_frames):
            global_frame = segment_start + frame_idx
            time_offset = global_frame / FPS * 100  # Time in centiseconds
            
            # Create base frame based on visual type
            if visual_type == "title_hero":
                img = generate_title_hero_frame(generator, time_offset, segment)
            elif visual_type == "kpi_dashboard":
                img = generate_kpi_dashboard_frame(generator, time_offset, segment, seg_idx)
            elif visual_type == "ansatz_visualization":
                img = generate_ansatz_frame(generator, time_offset, segment)
            elif visual_type == "wave_function":
                img = generate_wave_function_frame(generator, time_offset, segment)
            elif visual_type == "error_mitigation":
                img = generate_error_mitigation_frame(generator, time_offset, segment)
            elif visual_type == "business_impact":
                img = generate_business_impact_frame(generator, time_offset, segment)
            elif visual_type == "closing":
                img = generate_closing_frame(generator, time_offset, segment)
            else:
                img = generator.create_gradient_background(time_offset=time_offset)
            
            # Save frame
            frame_path = output_frames_dir / f"frame_{global_frame:06d}.png"
            img.save(frame_path, 'PNG')
            
            # Progress indicator
            if frame_idx % (seg_frames // 4) == 0:
                pct = (global_frame / frame_count) * 100
                print(f"        Frame {global_frame}/{frame_count} ({pct:.1f}%)")
        
        segment_start += seg_frames
    
    print(f"\n      ✓ Generated {segment_start} frames")
    
    # Assemble video with FFmpeg
    print("\n[3/4] Assembling video with FFmpeg...")
    
    concat_file = output_frames_dir / "concat.txt"
    with open(concat_file, 'w') as f:
        for i in range(segment_start):
            f.write(f"file 'frame_{i:06d}.png'\n")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(audio_path),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(video_output)
    ]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"      ✓ Video created: {video_output.name}")
        print(f"      File size: {video_output.stat().stsize / (1024*1024):.1f} MB")
    else:
        print(f"      ✗ FFmpeg error: {result.stderr[:500]}")
    
    # Cleanup frames
    print("\n[4/4] Cleaning up temporary files...")
    import shutil
    shutil.rmtree(output_frames_dir, ignore_errors=True)
    
    print("\n" + "=" * 70)
    print("PREMIUM VIDEO GENERATION COMPLETE")
    print("=" * 70)
    
    return video_output


def generate_title_hero_frame(gen, time_offset, segment):
    """Generate title hero frame with dramatic reveal."""
    img = gen.create_gradient_background(
        base_color=COLORS['bg_deep'],
        accent_color=(15, 23, 42),
        time_offset=time_offset
    )
    
    # Add particle system
    gen.particle_system.update()
    gen.particle_system.draw(img, time_offset)
    
    # Add central wave function glow
    gen.wave_function.update(0.1)
    gen.wave_function.draw(img, color=COLORS['accent_cyan'], time_offset=time_offset)
    
    # Grid overlay
    img = gen.add_grid_overlay(img, opacity=20, time_offset=time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Company logo with glow
    logo_text = "QT"
    logo_font = get_font(180, bold=True)
    logo_bbox = draw.textbbox((0, 0), logo_text, font=logo_font)
    logo_w, logo_h = logo_bbox[2] - logo_bbox[0], logo_bbox[3] - logo_bbox[1]
    logo_x = (VIDEO_WIDTH - logo_w) // 2
    logo_y = 180
    
    # Logo glow
    for glow_r in range(80, 10, -5):
        glow_alpha = int(15 * (1 - glow_r/80))
        glow_color = COLORS['accent_cyan'] + (glow_alpha,)
        draw.text([logo_x - glow_r//4, logo_y - glow_r//4], logo_text, 
                 fill=glow_color, font=get_font(180 + glow_r//3, bold=True))
    
    # Main logo
    draw.text((logo_x, logo_y), logo_text, fill=COLORS['accent_cyan'], font=logo_font)
    
    # Company name
    name_font = get_font(56, bold=True)
    name = QUANTUM_THERAPEUTICS_PREMIUM["name"]
    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text(((VIDEO_WIDTH - name_w) // 2, 420), name, 
             fill=COLORS['text_primary'], font=name_font)
    
    # Tagline
    tag_font = get_font(28)
    tagline = QUANTUM_THERAPEUTICS_PREMIUM["tagline"]
    tag_bbox = draw.textbbox((0, 0), tagline, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((VIDEO_WIDTH - tag_w) // 2, 495), tagline, 
             fill=COLORS['accent_purple'], font=tag_font)
    
    # Stage and valuation badges
    badge_font = get_font(22)
    stage_text = f"Stage: {QUANTUM_THERAPEUTICS_PREMIUM['stage']}  |  Valuation: {QUANTUM_THERAPEUTICS_PREMIUM['valuation']}"
    stage_bbox = draw.textbbox((0, 0), stage_text, font=badge_font)
    stage_w = stage_bbox[2] - stage_bbox[0]
    draw.text(((VIDEO_WIDTH - stage_w) // 2, 560), stage_text, 
             fill=COLORS['text_secondary'], font=badge_font)
    
    # Animated data stream at bottom
    data_y = 650
    for i in range(40):
        char = random.choice("01{}[]<>αβγδ∫∂∑√π÷×±")
        x = 50 + i * 45
        flicker_alpha = int(100 + math.sin(time_offset * 0.1 + i * 0.3) * 80)
        draw.text((x, data_y), char, fill=COLORS['accent_cyan'] + (flicker_alpha,), 
                 font=get_font(24))
    
    # Bottom bar
    draw.rectangle([0, VIDEO_HEIGHT-80, VIDEO_WIDTH, VIDEO_HEIGHT], 
                   fill=(0, 0, 0, 180))
    
    footer_font = get_font(18)
    footer = "⚛ Quantum Computing  •  Drug Discovery  •  VQE Algorithm  •  Molecular Simulation"
    footer_bbox = draw.textbbox((0, 0), footer, font=footer_font)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((VIDEO_WIDTH - footer_w) // 2, VIDEO_HEIGHT-50), footer, 
             fill=COLORS['text_secondary'] + (200,), font=footer_font)
    
    # Vignette
    img = gen.add_vignette(img, strength=0.3)
    
    return img


def generate_kpi_dashboard_frame(gen, time_offset, segment, seg_idx):
    """Generate KPI dashboard frame with animated gauges."""
    img = gen.create_gradient_background(
        base_color=COLORS['bg_deep'],
        accent_color=(10, 22, 40),
        time_offset=time_offset
    )
    
    # Subtle particles
    gen.particle_system.update()
    gen.particle_system.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(42, bold=True)
    title = "QUANTUM PERFORMANCE INDICATORS"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((VIDEO_WIDTH - title_w) // 2, 40), title, 
             fill=COLORS['accent_cyan'], font=title_font)
    
    subtitle_font = get_font(22)
    subtitle = "Real-time Hardware & Algorithm Metrics"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((VIDEO_WIDTH - sub_w) // 2, 95), subtitle, 
             fill=COLORS['text_secondary'], font=subtitle_font)
    
    # KPI Gauges - arranged in grid
    kpis = QUANTUM_THERAPEUTICS_PREMIUM["quantum_kpis"]
    
    # Row 1: Hardware KPIs
    hw_kpis = kpis["hardware"]
    gauge_positions = [
        (240, 320, 90),   # x, y, radius
        (600, 320, 90),
        (960, 320, 90),
        (1320, 320, 90),
        (1680, 320, 90),
    ]
    
    hw_items = list(hw_kpis.items())[:5]
    for idx, ((key, data), pos) in enumerate(zip(hw_items, gauge_positions)):
        x, y, r = pos
        gen.kpi_viz.draw_gauge(img, x, y, r, {
            'value': data['value'],
            'unit': data['unit'],
            'label': key.replace('_', ' ').title(),
            'target': data['value'] * 1.05  # Target slightly above current
        }, time_offset, [COLORS['accent_cyan'], COLORS['accent_purple'], 
                         COLORS['accent_pink'], COLORS['accent_green'], 
                         COLORS['accent_gold']][idx])
    
    # Row 2: Algorithm KPIs
    algo_kpis = kpis["algorithm"]
    algo_positions = [(240, 560, 85), (600, 560, 85), (960, 560, 85), 
                      (1320, 560, 85), (1680, 560, 85)]
    
    algo_items = list(algo_kpis.items())[:5]
    for idx, ((key, data), pos) in enumerate(zip(algo_items, algo_positions)):
        x, y, r = pos
        gen.kpi_viz.draw_gauge(img, x, y, r, {
            'value': data['value'],
            'unit': data['unit'],
            'label': key.replace('_', ' ').title()[:20],
            'target': data['value'] * 1.1
        }, time_offset, COLORS['accent_purple'])
    
    # Row 3: Drug Discovery Impact
    dd_kpis = kpis["drug_discovery"]
    dd_positions = [(320, 800, 80), (720, 800, 80), (1120, 800, 80), 
                    (1520, 800, 80)]
    
    dd_items = list(dd_kpis.items())[:4]
    for idx, ((key, data), pos) in enumerate(zip(dd_items, dd_positions)):
        x, y, r = pos
        gen.kpi_viz.draw_gauge(img, x, y, r, {
            'value': data['value'],
            'unit': data['unit'],
            'label': key.replace('_', ' ').title()[:22],
            'target': data['value'] * 1.2
        }, time_offset, COLORS['accent_green'])
    
    # Live indicator
    pulse_alpha = int(150 + math.sin(time_offset * 0.1) * 100)
    draw.ellipse([VIDEO_WIDTH-60, 50, VIDEO_WIDTH-40, 70], 
                fill=(255, 50, 50, pulse_alpha))
    live_font = get_font(16, bold=True)
    draw.text((VIDEO_WIDTH-130, 48), "LIVE", fill=(255, 100, 100), font=live_font)
    
    img = gen.add_vignette(img, strength=0.25)
    return img


def generate_ansatz_frame(gen, time_offset, segment):
    """Generate ansatz circuit visualization."""
    img = gen.create_gradient_background(
        base_color=COLORS['bg_deep'],
        accent_color=(8, 15, 30),
        time_offset=time_offset
    )
    
    gen.particle_system.update()
    gen.particle_system.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(40, bold=True)
    title = "HARDWARE-EFFICIENT ANSATZ ARCHITECTURE"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_WIDTH - (title_bbox[2]-title_bbox[0])) // 2, 40), 
             title, fill=COLORS['accent_purple'], font=title_font)
    
    # Draw quantum circuit diagram
    circuit_x = 200
    circuit_y = 180
    wire_spacing = 80
    num_qubits = 5
    
    # Qubit wires
    for q in range(num_qubits):
        y = circuit_y + q * wire_spacing
        wire_color = COLORS['text_secondary'] + (150,)
        draw.line([(circuit_x, y), (circuit_x + 1400, y)], fill=wire_color, width=2)
        
        # Qubit label
        label_font = get_font(20, bold=True)
        draw.text((circuit_x - 50, y - 10), f"q[{q}]", 
                 fill=COLORS['accent_cyan'], font=label_font)
    
    # Circuit gates (animated)
    gates = [
        (0, 0, "H", COLORS['accent_cyan']),      # Hadamard
        (1, 1, "RX(θ)", COLORS['accent_purple']),  # Rotation
        (2, 2, "RY(θ)", COLORS['accent_purple']),
        (3, 3, "RZ(θ)", COLORS['accent_purple']),
        (0, 1, "CX", COLORS['accent_green']),       # CNOT
        (2, 3, "CX", COLORS['accent_green']),
        (1, 2, "CX", COLORS['accent_green']),
        (4, 4, "RZ(θ)", COLORS['accent_purple']),
    ]
    
    layer_width = 160
    for idx, (control, target, gate_name, color) in enumerate(gates):
        gx = circuit_x + 100 + idx * layer_width
        gy_control = circuit_y + control * wire_spacing
        gy_target = circuit_y + target * wire_spacing
        
        # Animate gate appearance
        gate_alpha = min(255, int(255 * (time_offset * 0.05 - idx * 0.5)))
        if gate_alpha > 0:
            if gate_name == "CX":
                # CNOT gate (connected circles)
                control_color = color + (gate_alpha,)
                draw.ellipse([gx-12, gy_control-12, gx+12, gy_control+12], 
                           fill=COLORS['bg_primary'], outline=control_color, width=3)
                draw.ellipse([gx-8, gy_control-8, gx+8, gy_control+8], fill=control_color)
                
                # Connection line
                draw.line([(gx, gy_control), (gx, gy_target)], fill=control_color, width=2)
                
                # Target circle (⊕)
                draw.ellipse([gx-12, gy_target-12, gx+12, gy_target+12], 
                           fill=COLORS['bg_primary'], outline=control_color, width=3)
                draw.line([(gx-8, gy_target), (gx+8, gy_target)], fill=control_color, width=2)
                draw.line([(gx, gy_target-8), (gx, gy_target+8)], fill=control_color, width=2)
            else:
                # Single-qubit gate box
                gate_color = color + (gate_alpha,)
                box_size = 45
                draw.rectangle([gx-box_size//2, gy_target-box_size//2, 
                              gx+box_size//2, gy_target+box_size//2],
                             fill=COLORS['bg_secondary'], outline=gate_color, width=2)
                
                gate_font = get_font(16, bold=True)
                gate_bbox = draw.textbbox((0, 0), gate_name, font=gate_font)
                gw, gh = gate_bbox[2] - gate_bbox[0], gate_bbox[3] - gate_bbox[1]
                draw.text((gx - gw//2, gy_target - gh//2), gate_name, 
                         fill=gate_color, font=gate_font)
    
    # Layer indicators
    layer_font = get_font(18)
    for layer in range(4):
        lx = circuit_x + 100 + layer * layer_width * 2
        ly = circuit_y + num_qubits * wire_spacing + 30
        draw.text((lx - 20, ly), f"Layer {layer + 1}", 
                 fill=COLORS['text_secondary'], font=layer_font)
    
    # Parameter count display
    param_font = get_font(28, bold=True)
    param_text = "Total Parameters: 60  |  Depth: 12  |  Gate Count: 47"
    param_bbox = draw.textbbox((0, 0), param_text, font=param_font)
    param_w = param_bbox[2] - param_bbox[0]
    draw.text(((VIDEO_WIDTH - param_w) // 2, 680), param_text, 
             fill=COLORS['accent_gold'], font=param_font)
    
    # Efficiency metric
    eff_font = get_font(24)
    eff_text = "✓ NISQ-Optimized  ✓ Expressible  ✓ barren plateau-free"
    eff_bbox = draw.textbbox((0, 0), eff_text, font=eff_font)
    eff_w = eff_bbox[2] - eff_bbox[0]
    draw.text(((VIDEO_WIDTH - eff_w) // 2, 730), eff_text, 
             fill=COLORS['accent_green'], font=eff_font)
    
    # Molecule preview
    gen.kpi_viz.draw_molecule_visualization(img, 1550, 400, 1.2, time_offset)
    
    mol_font = get_font(18)
    draw.text((1450, 580), "Target:", fill=COLORS['text_secondary'], font=mol_font)
    draw.text((1450, 605), "Drug-like", fill=COLORS['accent_cyan'], font=mol_font)
    draw.text((1450, 625), "Molecule", fill=COLORS['accent_cyan'], font=mol_font)
    
    img = gen.add_vignette(img, strength=0.3)
    return img


def generate_wave_function_frame(gen, time_offset, segment):
    """Generate wave function probability visualization."""
    img = gen.create_gradient_background(
        base_color=(5, 5, 15),
        accent_color=(10, 10, 30),
        time_offset=time_offset
    )
    
    # Dense particle field for quantum atmosphere
    dense_particles = ParticleSystem(count=250, bounds=(VIDEO_WIDTH, VIDEO_HEIGHT))
    dense_particles.draw(img, time_offset)
    
    # Main wave function
    wf = WaveFunction(center=(700, 480), wavelength=50, amplitude=100)
    wf.draw(img, color=COLORS['accent_cyan'], time_offset=time_offset)
    
    # Secondary wave function (entangled partner)
    wf2 = WaveFunction(center=(1300, 480), wavelength=35, amplitude=70)
    wf2.draw(img, color=COLORS['accent_purple'], time_offset=-time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(38, bold=True)
    title = "WAVE FUNCTION PROBABILITY DISTRIBUTION"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_WIDTH - (title_bbox[2]-title_bbox[0])) // 2, 30), 
             title, fill=COLORS['accent_cyan'], font=title_font)
    
    # Subtitle
    sub_font = get_font(22)
    subtitle = "|ψ⟩² — Born Rule Visualization for Binding Site Electron Cloud"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    draw.text(((VIDEO_WIDTH - (sub_bbox[2]-sub_bbox[0])) // 2, 80), 
             subtitle, fill=COLORS['text_secondary'], font=sub_font)
    
    # Normal distribution panel
    gen.prob_dist.draw_normal_distribution(
        img, 100, 750, 350, 200,
        mu=0, sigma=0.8,
        color=COLORS['accent_cyan'],
        time_offset=time_offset,
        label="P(E) — Energy Distribution"
    )
    
    # Quantum tunneling panel
    gen.prob_dist.draw_quantum_tunneling(
        img, 550, 750, 450, 200,
        time_offset=time_offset
    )
    
    # Formula display
    formula_font = get_font(28, bold=True)
    formulas = [
        "H|ψ⟩ = E|ψ⟩",
        "E = ⟨ψ|H|ψ⟩",
        "|ψ⟩ = Σᵢ cᵢ|φᵢ⟩"
    ]
    fx = 1150
    for fi, formula in enumerate(formulas):
        formula_color = COLORS['accent_gold'] + (200 + int(math.sin(time_offset * 0.05 + fi) * 55),)
        draw.text((fx, 770 + fi * 35), formula, fill=formula_color, font=formula_font)
    
    # Entanglement indicator
    entangle_y = 900
    draw.line([(550, entangle_y), (1300, entangle_y)], 
             fill=COLORS['accent_purple'] + (100,), width=2, dash=(10, 5))
    
    ent_font = get_font(20, bold=True)
    draw.text((850, entangle_y + 10), "⟺ QUANTUM ENTANGLEMENT ⟺", 
             fill=COLORS['accent_purple'], font=ent_font)
    
    # Speed comparison
    speed_font = get_font(26, bold=True)
    speed_text = "40× SPEEDUP vs Classical DFT"
    speed_bbox = draw.textbbox((0, 0), speed_text, font=speed_font)
    speed_w = speed_bbox[2] - speed_bbox[0]
    draw.text(((VIDEO_WIDTH - speed_w) // 2, 980), speed_text, 
             fill=COLORS['accent_green'], font=speed_font)
    
    img = gen.add_vignette(img, strength=0.35)
    return img


def generate_error_mitigation_frame(gen, time_offset, segment):
    """Generate error mitigation visualization."""
    img = gen.create_gradient_background(
        base_color=COLORS['bg_deep'],
        accent_color=(15, 10, 25),
        time_offset=time_offset
    )
    
    gen.particle_system.update()
    gen.particle_system.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(40, bold=True)
    title = "ZERO-NOISE EXTRAPOLATION (ZNE)"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_WIDTH - (title_bbox[2]-title_bbox[0])) // 2, 40), 
             title, fill=COLORS['accent_gold'], font=title_font)
    
    sub_font = get_font(22)
    subtitle = "Error Mitigation Strategy for NISQ Devices"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    draw.text(((VIDEO_WIDTH - (sub_bbox[2]-sub_bbox[0])) // 2, 95), 
             subtitle, fill=COLORS['text_secondary'], font=sub_font)
    
    # Noise ladder visualization
    ladder_x = 300
    ladder_y = 200
    ladder_height = 500
    rungs = 5
    
    noise_levels = [1.0, 1.5, 2.0, 2.5, 3.0]
    results = [94.2, 93.1, 91.8, 90.2, 88.5]  # Simulated accuracy at each level
    
    # Draw ladder
    for i, (noise, result) in enumerate(zip(noise_levels, results)):
        y = ladder_y + i * (ladder_height // rungs)
        
        # Rung
        rung_color = COLORS['accent_gold'] + (150,)
        draw.line([(ladder_x, y), (ladder_x + 400, y)], fill=rung_color, width=3)
        
        # Noise level label
        nl_font = get_font(20)
        draw.text((ladder_x - 100, y - 10), f"λ={noise:.1f}", 
                 fill=COLORS['text_secondary'], font=nl_font)
        
        # Result point
        point_x = ladder_x + 400 + (result - 85) * 15  # Scale to visible range
        point_color = COLORS['accent_cyan'] + (230,)
        draw.ellipse([point_x-8, y-8, point_x+8, y+8], fill=point_color)
        
        # Result value
        res_font = get_font(18, bold=True)
        draw.text((point_x + 15, y - 10), f"{result:.1f}%", 
                 fill=COLORS['accent_cyan'], font=res_font)
    
    # Extrapolation arrow
    arrow_start = (ladder_x + 200, ladder_y + ladder_height + 50)
    arrow_end = (ladder_x + 200, ladder_y - 50)
    arrow_color = COLORS['accent_green'] + (200,)
    draw.arrow(arrow_start, arrow_end, fill=arrow_color, width=4)
    
    # Zero-noise result (extrapolated)
    zero_y = ladder_y - 80
    zero_result = "99.2%"
    zero_font = get_font(32, bold=True)
    draw.text((ladder_x + 120, zero_y), f"→ Zero-Noise Limit: {zero_result}", 
             fill=COLORS['accent_green'], font=zero_font)
    
    # Improvement factor panel
    panel_x = 1000
    panel_y = 200
    panel_w = 800
    panel_h = 600
    
    # Panel background
    draw.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
                  fill=COLORS['bg_secondary'] + (180,), 
                  outline=COLORS['accent_gold'] + (100,), width=2)
    
    # Panel title
    panel_title_font = get_font(28, bold=True)
    draw.text((panel_x + 30, panel_y + 30), "MITIGATION IMPACT", 
             fill=COLORS['accent_gold'], font=panel_title_font)
    
    # Metrics
    metrics = [
        ("Effective Fidelity Improvement", "10×", "+900%"),
        ("Coherent Error Suppression", "85%", "↓ from raw"),
        ("Readout Error Reduction", "92%", "↓ from raw"),
        ("Crosstalk Mitigation", "78%", "↓ from raw"),
        ("Overall Algorithm Accuracy", "94.2%", "→ 99.2% (ZNE)"),
    ]
    
    metric_y = panel_y + 90
    for label, value, change in metrics:
        # Label
        m_font = get_font(20)
        draw.text((panel_x + 40, metric_y), label, fill=COLORS['text_secondary'], font=m_font)
        
        # Value
        v_font = get_font(26, bold=True)
        draw.text((panel_x + 40, metric_y + 28), value, fill=COLORS['accent_cyan'], font=v_font)
        
        # Change indicator
        c_font = get_font(18)
        change_color = COLORS['accent_green'] if "↑" in change or "+" in change or "↓" in change else COLORS['text_secondary']
        draw.text((panel_x + 200, metric_y + 32), change, fill=change_color, font=c_font)
        
        metric_y += 90
    
    img = gen.add_vignette(img, strength=0.3)
    return img


def generate_business_impact_frame(gen, time_offset, segment):
    """Generate business impact/metrics frame."""
    img = gen.create_gradient_background(
        base_color=COLORS['bg_deep'],
        accent_color=(8, 20, 15),
        time_offset=time_offset
    )
    
    gen.particle_system.update()
    gen.particle_system.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(42, bold=True)
    title = "BUSINESS IMPACT & MARKET POSITION"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_WIDTH - (title_bbox[2]-title_bbox[0])) // 2, 40), 
             title, fill=COLORS['accent_green'], font=title_font)
    
    # Key metrics cards
    cards = [
        {"title": "Hit Rate Improvement", "value": "3.5×", "change": "+250%", "color": COLORS['accent_cyan']},
        {"title": "Time-to-Candidate", "value": "8 weeks", "change": "-75%", "color": COLORS['accent_green']},
        {"title": "Screening Capacity", "value": "10B", "change": "compounds", "color": COLORS['accent_purple']},
        {"title": "Validation Papers", "value": "12", "change": "peer-reviewed", "color": COLORS['accent_gold']},
        {"title": "Seed Funding", "value": "$4.2M", "value2": "$18M SA", "color": COLORS['accent_pink']},
    ]
    
    card_width = 340
    card_height = 280
    start_x = 80
    card_y = 160
    spacing = 30
    
    for idx, card in enumerate(cards):
        x = start_x + idx * (card_width + spacing)
        
        # Card background with glow
        for glow_r in range(20, 5, -3):
            glow_alpha = int(15 * (1 - glow_r/20))
            glow_color = card["color"] + (glow_alpha,)
            draw.rounded_rectangle(
                [x - glow_r, card_y - glow_r, x + card_width + glow_r, card_y + card_height + glow_r],
                radius=15, fill=glow_color
            )
        
        # Card body
        draw.rounded_rectangle(
            [x, card_y, x + card_width, card_y + card_height],
            radius=12, fill=COLORS['bg_secondary'] + (220,),
            outline=card["color"] + (150,), width=2
        )
        
        # Card title
        ct_font = get_font(18)
        ct_bbox = draw.textbbox((0, 0), card["title"], font=ct_font)
        ct_w = ct_bbox[2] - ct_bbox[0]
        draw.text((x + (card_width - ct_w) // 2, card_y + 25), card["title"],
                 fill=COLORS['text_secondary'], font=ct_font)
        
        # Main value
        cv_font = get_font(52, bold=True)
        cv_bbox = draw.textbbox((0, 0), card["value"], font=cv_font)
        cv_w = cv_bbox[2] - cv_bbox[0]
        draw.text((x + (card_width - cv_w) // 2, card_y + 80), card["value"],
                 fill=card["color"], font=cv_font)
        
        # Secondary value (if exists)
        if "value2" in card:
            cv2_font = get_font(24)
            cv2_bbox = draw.textbbox((0, 0), card["value2"], font=cv2_font)
            cv2_w = cv2_bbox[2] - cv2_bbox[0]
            draw.text((x + (card_width - cv2_w) // 2, card_y + 150), card["value2"],
                     fill=card["color"], font=cv2_font)
        
        # Change indicator
        ch_font = get_font(22, bold=True)
        ch_bbox = draw.textbbox((0, 0), card["change"], font=ch_font)
        ch_w = ch_bbox[2] - ch_bbox[0]
        draw.text((x + (card_width - ch_w) // 2, card_y + card_height - 45), card["change"],
                 fill=COLORS['accent_green'] if "+" in card["change"] or "-" in card["change"] else COLORS['text_secondary'],
                 font=ch_font)
    
    # Timeline/Traction section
    traction_y = 500
    draw.line([(100, traction_y), (VIDEO_WIDTH - 100, traction_y)], 
             fill=COLORS['text_secondary'] + (100,), width=2)
    
    tr_font = get_font(26, bold=True)
    draw.text((100, traction_y + 20), "TRACTION TIMELINE", 
             fill=COLORS['text_primary'], font=tr_font)
    
    milestones = [
        ("Q1 2024", "Founded"),
        ("Q2 2024", "First VQE benchmark"),
        ("Q3 2024", "Seed round closed"),
        ("Q4 2024", "Pharma pilot launched"),
        ("Q1 2025", "Series A pipeline"),
        ("NOW", "Scaling operations"),
    ]
    
    ms_x = 150
    ms_spacing = 280
    for ms_idx, (date, event) in enumerate(milestones):
        mx = ms_x + ms_idx * ms_spacing
        
        # Milestone dot
        is_now = date == "NOW"
        dot_color = COLORS['accent_cyan'] if not is_now else COLORS['accent_gold']
        dot_radius = 12 if not is_now else 18
        
        # Pulse effect for NOW
        if is_now:
            pulse = int(abs(math.sin(time_offset * 0.08)) * 100)
            draw.ellipse([mx-dot_radius-10, traction_y+80-dot_radius-10, 
                        mx-dot_radius+10, traction_y+80+dot_radius+10],
                        fill=COLORS['accent_gold'] + (pulse,))
        
        draw.ellipse([mx-dot_radius, traction_y+80-dot_radius, mx+dot_radius, traction_y+80+dot_radius],
                    fill=dot_color)
        
        # Date
        d_font = get_font(16, bold=True)
        draw.text((mx - 25, traction_y + 100), date, fill=dot_color, font=d_font)
        
        # Event
        e_font = get_font(14)
        e_bbox = draw.textbbox((0, 0), event, font=e_font)
        e_w = e_bbox[2] - e_bbox[0]
        draw.text((mx - e_w//2, traction_y + 125), event, 
                 fill=COLORS['text_secondary'], font=e_font)
    
    # Bottom CTA-style message
    cta_font = get_font(24)
    cta_text = "Transforming Quantum Computing into Therapeutic Reality"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_w = cta_bbox[2] - cta_bbox[0]
    draw.text(((VIDEO_WIDTH - cta_w) // 2, 950), cta_text, 
             fill=COLORS['accent_purple'], font=cta_font)
    
    img = gen.add_vignette(img, strength=0.25)
    return img


def generate_closing_frame(gen, time_offset, segment):
    """Generate closing/CTA frame."""
    img = gen.create_gradient_background(
        base_color=COLORS['bg_deep'],
        accent_color=(10, 15, 30),
        time_offset=time_offset
    )
    
    # Intense central glow
    gen.wave_function.update(0.15)
    gen.wave_function.draw(img, color=COLORS['accent_cyan'], time_offset=time_offset)
    
    # Secondary wave
    wf2 = WaveFunction(center=(960, 540), wavelength=30, amplitude=120)
    wf2.draw(img, color=COLORS['accent_purple'], time_offset=-time_offset * 1.5)
    
    gen.particle_system.update()
    gen.particle_system.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Quote marks
    quote_font = get_font(120)
    draw.text((150, 200), """, fill=COLORS['accent_cyan'] + (50,), font=quote_font)
    draw.text((VIDEO_WIDTH - 300, 600), """, fill=COLORS['accent_cyan'] + (50,), font=quote_font)
    
    # Main closing statement
    closing_lines = [
        "This is not science fiction.",
        "",
        "This is quantum advantage,",
        "deployed today,",
        "saving lives tomorrow.",
    ]
    
    line_y = 300
    main_font = get_font(44, bold=True)
    
    for line_idx, line in enumerate(closing_lines):
        if line:
            # Fade-in effect per line
            line_alpha = min(255, int(255 * (time_offset * 0.03 - line_idx * 2)))
            if line_alpha > 0:
                line_color = COLORS['text_primary'] if line_idx < 3 else COLORS['accent_cyan']
                
                line_bbox = draw.textbbox((0, 0), line, font=main_font)
                line_w = line_bbox[2] - line_bbox[0]
                draw.text(((VIDEO_WIDTH - line_w) // 2, line_y), line,
                         fill=line_color, font=main_font)
        line_y += 65
    
    # Company name final
    company_font = get_font(64, bold=True)
    company = "Quantum Therapeutics"
    co_bbox = draw.textbbox((0, 0), company, font=company_font)
    co_w = co_bbox[2] - co_bbox[0]
    
    # Glow effect on company name
    for glow in range(30, 5, -5):
        glow_alpha = int(20 * (1 - glow/30))
        glow_color = COLORS['accent_cyan'] + (glow_alpha,)
        draw.text(((VIDEO_WIDTH - co_w) // 2, 700), company,
                 fill=glow_color, font=get_font(64 + glow//2, bold=True))
    
    draw.text(((VIDEO_WIDTH - co_w) // 2, 700), company,
             fill=COLORS['accent_cyan'], font=company_font)
    
    # Tagline
    tag_font = get_font(28, italic=True)
    tagline = "Where Schrödinger's Equation Meets FDA Approval"
    tag_bbox = draw.textbbox((0, 0), tagline, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((VIDEO_WIDTH - tag_w) // 2, 790), tagline,
             fill=COLORS['accent_purple'], font=tag_font)
    
    # Bottom bar with web address
    draw.rectangle([0, VIDEO_HEIGHT-100, VIDEO_WIDTH, VIDEO_HEIGHT], 
                   fill=(0, 0, 0, 200))
    
    web_font = get_font(22)
    web_text = "🌐 scimspt.io/quantum-therapeutics  •  📧 invest@quantumtherapeutics.ai  •  ⚛ Validated by Science"
    web_bbox = draw.textbbox((0, 0), web_text, font=web_font)
    web_w = web_bbox[2] - web_bbox[0]
    draw.text(((VIDEO_WIDTH - web_w) // 2, VIDEO_HEIGHT-55), web_text,
             fill=COLORS['text_secondary'], font=web_font)
    
    img = gen.add_vignette(img, strength=0.4)
    img = gen.add_glow_effect(img, intensity=1.2)
    
    return img


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SciMSPT PREMIUM Video Generation System")
    print("Nature/TED-Ed/Kurzgesagt Quality Output")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT} (Full HD)")
    print(f"  Frame Rate: {FPS} fps")
    print(f"  Duration: {DURATION} seconds")
    print(f"  Total Frames: {DURATION * FPS}")
    print(f"  Output: {OUTPUT_DIR}")
    
    # Generate Quantum Therapeutics premium video
    output_video = generate_quantum_therapeutics_premium()
    
    print(f"\n✓ PREMIUM video generation complete!")
    print(f"  Output: {output_video}")
