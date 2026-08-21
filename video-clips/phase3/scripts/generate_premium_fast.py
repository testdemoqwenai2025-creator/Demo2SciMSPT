#!/usr/bin/env python3
"""
SciMSPT Phase 4: PREMIUM Video Generation (FAST Mode)
======================================================
Optimized for speed while maintaining visual quality.
Generates impressive scientific explainer videos with:
- Particle physics visualizations
- Quantum KPIs and technical metrics  
- Wave function probability distributions
- Professional scientific narrative quality
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
# CONFIGURATION - Optimized for Speed & Quality Balance
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = BASE_DIR / "video-clips" / "phase3" / "startups"
AUDIO_DIR = BASE_DIR / "video-clips" / "phase3" / "audio"
PREMIUM_DIR = BASE_DIR / "video-clips" / "phase3" / "premium"

VIDEO_WIDTH = 1280  # HD (optimized)
VIDEO_HEIGHT = 720
FPS = 24  # Smooth enough
DURATION = 45  # 45 seconds of premium content

for d in [OUTPUT_DIR, AUDIO_DIR, PREMIUM_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================================
# COLOR SYSTEM
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
}

def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def get_font(size, bold=False):
    paths = [
        f"/usr/share/fonts/truetype/dejavu/{'DejaVuSans-Bold' if bold else 'DejaVuSans'}.ttf",
        f"/usr/share/fonts/truetype/freefont/{'FreeSansBold' if bold else 'FreeSans'}.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

# ============================================================================
# VISUAL EFFECTS CLASSES (OPTIMIZED)
# ============================================================================

class FastParticleSystem:
    """Optimized particle system."""
    
    def __init__(self, count=80):
        self.count = count
        np.random.seed(42)
        self.x = np.random.uniform(0, VIDEO_WIDTH, count)
        self.y = np.random.uniform(0, VIDEO_HEIGHT, count)
        self.vx = np.random.uniform(-1.5, 1.5, count)
        self.vy = np.random.uniform(-1.5, 1.5, count)
        self.sizes = np.random.uniform(1, 3, count).astype(int)
        self.colors = [random.choice([COLORS['accent_cyan'], COLORS['accent_purple'], 
                                      COLORS['accent_pink']]) for _ in range(count)]
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.x %= VIDEO_WIDTH
        self.y %= VIDEO_HEIGHT
    
    def draw(self, img, time_offset=0):
        draw = ImageDraw.Draw(img, 'RGBA')
        for i in range(self.count):
            ox = math.sin(time_offset * 0.02 + i) * 3
            oy = math.cos(time_offset * 0.02 + i * 0.7) * 3
            x, y = int(self.x[i] + ox), int(self.y[i] + oy)
            alpha = int(80 + math.sin(time_offset * 0.03 + i) * 50)
            color = self.colors[i] + (max(0, alpha),)
            r = self.sizes[i] * 2
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)


class WaveFunctionViz:
    """Simplified wave function visualization."""
    
    def __init__(self, center=(640, 360)):
        self.center = center
    
    def draw(self, img, color=None, time_offset=0):
        if color is None: color = COLORS['accent_cyan']
        draw = ImageDraw.Draw(img, 'RGBA')
        cx, cy = self.center
        
        # Probability cloud with safe radius
        for r in range(120, 10, -8):
            fluctuation = math.sin(time_offset * 0.03 + r * 0.05) * 12
            actual_r = max(5, r + fluctuation)
            alpha = int(60 * math.exp(-actual_r / 50))
            t = min(1.0, actual_r / 120)
            current_color = lerp_color(color, COLORS['accent_purple'], t) + (max(0, alpha),)
            draw.ellipse([int(cx-actual_r), int(cy-actual_r), 
                         int(cx+actual_r), int(cy+actual_r)], fill=current_color)


class QuantumKPIDashboard:
    """Renders quantum KPI dashboard."""
    
    def __init__(self):
        self.kpis = [
            {"label": "Qubit Coherence", "value": "98.7%", "target": 99.9},
            {"label": "VQE Accuracy", "value": "94.2%", "target": 99.0},
            {"label": "Gate Fidelity", "value": "99.8%", "target": 99.9},
            {"label": "Quantum Volume", "value": "128", "target": 512},
            {"label": "Speedup Factor", "value": "40x", "target": 100},
            {"label": "Error Rate", "value": "0.001%", "target": 0.01},
        ]
    
    def draw_mini_gauge(self, img, x, y, radius, kpi, time_offset=0, accent=None):
        if accent is None: accent = COLORS['accent_cyan']
        draw = ImageDraw.Draw(img, 'RGBA')
        
        try:
            value = float(kpi["value"].replace('%', '').replace('x', ''))
            target = float(kpi["target"])
        except:
            value, target = 90, 100
        
        fill_pct = max(0, min(1, value/target))
        pulse = math.sin(time_offset * 0.05) * 0.02
        fill_pct = max(0, min(1, fill_pct + pulse))
        
        # Background arc
        bg_color = (30, 41, 59, 150)
        draw.arc([x-radius, y-radius, x+radius, y+radius], 135, 405, fill=bg_color, width=radius//4)
        
        # Foreground arc
        end_angle = 135 + (270 * fill_pct)
        fg_color = accent + (220,)
        draw.arc([x-radius, y-radius, x+radius, y+radius], 135, end_angle, fill=fg_color, width=radius//4)
        
        # Value text
        font_val = get_font(radius // 3, bold=True)
        font_lbl = get_font(radius // 5)
        
        bbox = draw.textbbox((0, 0), kpi["value"], font=font_val)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x - tw//2, y - th//2 - radius//6), kpi["value"], 
                 fill=COLORS['text_primary'], font=font_val)
        
        lbl_bbox = draw.textbbox((0, 0), kpi["label"], font=font_lbl)
        lw, lh = lbl_bbox[2] - lbl_bbox[0], lbl_bbox[3] - lbl_bbox[1]
        draw.text((x - lw//2, y + radius//3), kpi["label"], 
                 fill=COLORS['text_secondary'], font=font_lbl)


def create_gradient_bg(time_offset=0, base_color=None, accent_color=None):
    """Create gradient background efficiently."""
    if base_color is None: base_color = COLORS['bg_deep']
    if accent_color is None: accent_color = COLORS['bg_primary']
    
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), base_color)
    pixels = img.load()
    
    cx, cy = VIDEO_WIDTH // 2, VIDEO_HEIGHT // 2
    
    for y in range(0, VIDEO_HEIGHT, 2):  # Skip rows for speed
        for x in range(0, VIDEO_WIDTH, 2):
            dist = math.sqrt((x-cx)**2 + (y-cy)**2) / math.sqrt(cx**2 + cy**2)
            t = dist ** 0.8
            
            shift = int(math.sin(time_offset * 0.01 + x * 0.001) * 3)
            
            r = max(0, min(255, int(base_color[0]*(1-t) + accent_color[0]*t + shift)))
            g = max(0, min(255, int(base_color[1]*(1-t) + accent_color[1]*t)))
            b = max(0, min(255, int(base_color[2]*(1-t) + accent_color[2]*t)))
            
            pixels[x, y] = (r, g, b)
            if x+1 < VIDEO_WIDTH: pixels[x+1, y] = (r, g, b)
            if y+1 < VIDEO_HEIGHT: 
                pixels[x, y+1] = (r, g, b)
                if x+1 < VIDEO_WIDTH: pixels[x+1, y+1] = (r, g, b)
    
    return img


def add_vignette(img, strength=0.4):
    """Add vignette effect."""
    overlay = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = VIDEO_WIDTH//2, VIDEO_HEIGHT//2
    max_r = int(math.sqrt(cx**2 + cy**2))
    
    for r in range(max_r, 0, -20):
        alpha = int(strength * 255 * (1 - r/max_r))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(0, 0, 0, alpha))
    
    vignette = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0))
    vignette.paste(overlay, (0, 0), overlay)
    return Image.blend(img, vignette, strength * 0.4)


def add_grid_overlay(img, opacity=25, time_offset=0):
    """Add subtle grid."""
    draw = ImageDraw.Draw(img, 'RGBA')
    grid_color = COLORS['accent_cyan'] + (opacity,)
    offset = int(time_offset * 0.3) % 50
    
    for x in range(offset, VIDEO_WIDTH, 50):
        draw.line([(x, 0), (x, VIDEO_HEIGHT)], fill=grid_color, width=1)
    for y in range(offset, VIDEO_HEIGHT, 50):
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=grid_color, width=1)
    return img


# ============================================================================
# QUANTUM THERAPEUTICS CONTENT
# ============================================================================

QT_PREMIUM = {
    "id": "quantum_therapeutics",
    "name": "Quantum Therapeutics",
    "logo": "QT",
    "stage": "Seed+",
    "tagline": "Quantum-Accelerated Molecular Simulation Platform",
    "valuation": "$28M",
    "funding": "$4.2M Seed | $18M Series A Pipeline",
    
    "quantum_kpis": {
        "hardware": {
            "qubit_count": {"value": "127", "unit": "qubits", "desc": "IBM Eagle-class"},
            "coherence_t1": {"value": "300", "unit": "μs", "desc": "Transmon T1"},
            "gate_fidelity": {"value": "99.97", "unit": "%", "desc": "Single-qubit"},
            "two_qubit_fidelity": {"value": "99.5", "unit": "%", "desc": "CX gate"},
        },
        "algorithm": {
            "vqe_convergence": {"value": "94.2", "unit": "%", "desc": "Ground state"},
            "ansatz_depth": {"value": "12", "unit": "layers", "desc": "Efficient"},
            "error_mitigation": {"value": "10", "unit": "x", "desc": "ZNE factor"},
            "measurement_reduction": {"value": "98", "unit": "%", "desc": "Shadow tomography"},
        },
        "impact": {
            "speedup_classical": {"value": "40", "unit": "x", "desc": "vs DFT"},
            "hit_rate_improvement": {"value": "3.5", "unit": "x", "desc": "Lead ID"},
            "time_to_candidate": {"value": "8", "unit": "weeks", "desc": "Target→Candidate"},
            "binding_accuracy": {"value": "0.92", "unit": "R²", "desc": "vs experimental"},
        }
    },
    
    "narration_segments": [
        {
            "duration": 6,
            "text": "Welcome to the frontier of computational drug discovery. Quantum Therapeutics has achieved what was thought impossible: practical quantum advantage in pharmaceutical molecular simulation.",
            "visual": "title_hero"
        },
        {
            "duration": 8,
            "text": "Their quantum KPIs demonstrate exceptional performance. The platform achieves 94.2% VQE convergence rate on IBM's 127-qubit Eagle processor, delivering ground state energy calculations within chemical accuracy—1.6 millihartree—for drug-sized molecules.",
            "visual": "kpi_dashboard"
        },
        {
            "duration": 7,
            "text": "The breakthrough: their hardware-efficient ansatz uses only 12 parameterized layers while maintaining accuracy. Combined with classical shadow tomography, they've achieved 98% measurement reduction—a critical bottleneck solution.",
            "visual": "ansatz_viz"
        },
        {
            "duration": 8,
            "text": "Consider the wave function probability distribution of a drug-target binding site. Classical methods approximate this exponentially complex surface. Quantum computers natively represent it. Result? 40-fold speedup over Density Functional Theory.",
            "visual": "wave_function"
        },
        {
            "duration": 6,
            "text": "Their Zero-Noise Extrapolation achieves 10x fidelity improvement, bringing NISQ devices into practical pharmaceutical utility. Business impact: 3.5x better hit rates, reducing candidate discovery from months to eight weeks.",
            "visual": "business_impact"
        },
        {
            "duration": 6,
            "text": "With 4.2 million seed funding and 12 peer-reviewed validations, they're redefining quantum computing's path to market. This is not science fiction. This is quantum advantage deployed today.",
            "visual": "closing"
        }
    ],
    
    "primary_color": "#00E5FF"
}


# ============================================================================
# FRAME GENERATORS
# ============================================================================

def gen_title_frame(gen_particles, gen_wave, time_offset, segment):
    """Title hero frame."""
    img = create_gradient_bg(time_offset=time_offset)
    gen_particles.update()
    gen_particles.draw(img, time_offset)
    gen_wave.draw(img, color=COLORS['accent_cyan'], time_offset=time_offset)
    img = add_grid_overlay(img, opacity=20, time_offset=time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Logo with glow
    logo_font = get_font(140, bold=True)
    logo_text = "QT"
    bbox = draw.textbbox((0, 0), logo_text, font=logo_font)
    lw, lh = bbox[2]-bbox[0], bbox[3]-bbox[1]
    lx, ly = (VIDEO_WIDTH-lw)//2, 120
    
    # Glow effect
    for gr in range(60, 10, -5):
        glow_alpha = int(12 * (1-gr/60))
        draw.text([lx-gr//4, ly-gr//4], logo_text, fill=COLORS['accent_cyan']+(glow_alpha,),
                 font=get_font(140+gr//3, bold=True))
    
    draw.text((lx, ly), logo_text, fill=COLORS['accent_cyan'], font=logo_font)
    
    # Company name
    name_font = get_font(44, bold=True)
    name = QT_PREMIUM["name"]
    nb = draw.textbbox((0, 0), name, font=name_font)
    draw.text(((VIDEO_WIDTH-(nb[2]-nb[0]))//2, 300), name, fill=COLORS['text_primary'], font=name_font)
    
    # Tagline
    tag_font = get_font(24)
    tag = QT_PREMIUM["tagline"]
    tb = draw.textbbox((0, 0), tag, font=tag_font)
    draw.text(((VIDEO_WIDTH-(tb[2]-tb[0]))//2, 360), tag, fill=COLORS['accent_purple'], font=tag_font)
    
    # Stage badge
    stage_font = get_font(18)
    stage = f"Stage: {QT_PREMIUM['stage']}  |  Valuation: {QT_PREMIUM['valuation']}  |  {QT_PREMIUM['funding']}"
    sb = draw.textbbox((0, 0), stage, font=stage_font)
    draw.text(((VIDEO_WIDTH-(sb[2]-sb[0]))//2, 410), stage, fill=COLORS['text_secondary'], font=stage_font)
    
    # Data stream
    data_y = 480
    for i in range(30):
        char = random.choice("01{}[]<>αβγδ∫∂∑√π÷×±")
        flicker = int(80 + math.sin(time_offset*0.1 + i*0.3) * 70)
        draw.text((40 + i*40, data_y), char, fill=COLORS['accent_cyan']+(flicker,), font=get_font(20))
    
    # Footer bar
    draw.rectangle([0, VIDEO_HEIGHT-60, VIDEO_WIDTH, VIDEO_HEIGHT], fill=(0,0,0,180))
    footer_font = get_font(16)
    footer = "⚛ Quantum Computing  •  Drug Discovery  •  VQE Algorithm  •  Molecular Simulation"
    fb = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text(((VIDEO_WIDTH-(fb[2]-fb[0]))//2, VIDEO_HEIGHT-38), footer, 
             fill=COLORS['text_secondary']+(200,), font=footer_font)
    
    return add_vignette(img, 0.3)


def gen_kpi_frame(gen_particles, gen_wave, kpi_dash, time_offset, segment):
    """KPI Dashboard frame."""
    img = create_gradient_bg(time_offset=time_offset, base_color=(5, 8, 18))
    gen_particles.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(32, bold=True)
    title = "QUANTUM PERFORMANCE INDICATORS"
    tb = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_WIDTH-(tb[2]-tb[0]))//2, 25), title, fill=COLORS['accent_cyan'], font=title_font)
    
    sub_font = get_font(16)
    sub = "Real-time Hardware & Algorithm Metrics"
    sb = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((VIDEO_WIDTH-(sb[2]-sb[0]))//2, 65), sub, fill=COLORS['text_secondary'], font=sub_font)
    
    # KPI gauges grid
    positions = [
        (140, 200, 65), (380, 200, 65), (620, 200, 65), (860, 200, 65), (1100, 200, 65),
        (140, 380, 65), (380, 380, 65), (620, 380, 65), (860, 380, 65), (1100, 380, 65),
        (260, 550, 70), (500, 550, 70), (740, 550, 70), (980, 550, 70),
    ]
    
    colors_cycle = [COLORS['accent_cyan'], COLORS['accent_purple'], COLORS['accent_pink'], 
                   COLORS['accent_green'], COLORS['accent_gold']]
    
    for idx, kpi in enumerate(kpi_dash.kpis):
        if idx < len(positions):
            x, y, r = positions[idx]
            kpi_dash.draw_mini_gauge(img, x, y, r, kpi, time_offset, colors_cycle[idx % 5])
    
    # Live indicator
    pulse = int(130 + math.sin(time_offset*0.1)*100)
    draw.ellipse([VIDEO_WIDTH-50, 35, VIDEO_WIDTH-35, 50], fill=(255,50,50,pulse))
    live_font = get_font(14, bold=True)
    draw.text((VIDEO_WIDTH-95, 33), "LIVE", fill=(255,100,100), font=live_font)
    
    # Formula bar
    draw.rectangle([0, VIDEO_HEIGHT-50, VIDEO_WIDTH, VIDEO_HEIGHT], fill=(0,0,0,160))
    formula_font = get_font(18)
    formulas = "H|ψ⟩ = E|ψ⟩  •  E = ⟨ψ|H|ψ⟩  •  |ψ⟩ = Σᵢcᵢ|φᵢ⟩  •  VQE Convergence: 94.2%"
    fmb = draw.textbbox((0, 0), formulas, font=formula_font)
    draw.text(((VIDEO_WIDTH-(fmb[2]-fmb[0]))//2, VIDEO_HEIGHT-32), formulas, 
             fill=COLORS['accent_gold']+(200,), font=formula_font)
    
    return add_vignette(img, 0.25)


def gen_ansatz_frame(gen_particles, gen_wave, time_offset, segment):
    """Ansatz circuit visualization."""
    img = create_gradient_bg(time_offset=time_offset, base_color=(6, 6, 16))
    gen_particles.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    title_font = get_font(30, bold=True)
    title = "HARDWARE-EFFICIENT ANSATZ ARCHITECTURE"
    tb = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((VIDEO_WIDTH-(tb[2]-tb[0]))//2, 25), title, fill=COLORS['accent_purple'], font=title_font)
    
    # Circuit diagram
    circ_x, circ_y = 100, 110
    wire_spacing = 65
    num_qubits = 5
    
    # Qubit wires
    for q in range(num_qubits):
        y = circ_y + q * wire_spacing
        draw.line([(circ_x, y), (circ_x + 1050, y)], fill=COLORS['text_secondary']+(120,), width=2)
        label_font = get_font(16, bold=True)
        draw.text((circ_x - 45, y - 8), f"q[{q}]", fill=COLORS['accent_cyan'], font=label_font)
    
    # Gates
    gates = [
        (0, "H", COLORS['accent_cyan']),
        (1, "RX(θ)", COLORS['accent_purple']),
        (2, "RY(θ)", COLORS['accent_purple']),
        (3, "RZ(θ)", COLORS['accent_purple']),
        (0, "CX", COLORS['accent_green']),  # Control q0, target q1
        (2, "CX", COLORS['accent_green']),  # Control q2, target q3
        (1, "CX", COLORS['accent_green']),  # Control q1, target q2
        (4, "RZ(θ)", COLORS['accent_purple']),
    ]
    
    layer_width = 130
    for idx, (target, gate_name, color) in enumerate(gates):
        gx = circ_x + 80 + idx * layer_width
        gy = circ_y + target * wire_spacing
        
        gate_alpha = min(230, int(230 * max(0, time_offset*0.04 - idx*0.4)))
        if gate_alpha > 10:
            gate_color = color + (gate_alpha,)
            
            if gate_name == "CX":
                # CNOT (simplified as connected dots for target only)
                control_q = [0, 2, 1][gates[:idx].count(gates[idx])] if idx > 0 else 0
                # Just show target with circle
                draw.ellipse([gx-10, gy-10, gx+10, gy+10], fill=COLORS['bg_secondary'], outline=gate_color, width=2)
                draw.ellipse([gx-6, gy-6, gx+6, gy+6], fill=gate_color)
                # Vertical line to indicate connection
                draw.line([(gx, circ_y + control_q * wire_spacing), (gx, gy)], fill=gate_color, width=1)
            else:
                box_size = 38
                draw.rectangle([gx-box_size//2, gy-box_size//2, gx+box_size//2, gy+box_size//2],
                             fill=COLORS['bg_secondary']+(200,), outline=gate_color, width=2)
                gf = get_font(14, bold=True)
                gb = draw.textbbox((0, 0), gate_name, font=gf)
                draw.text((gx-(gb[2]-gb[0])//2, gy-(gb[3]-gb[1])//2), gate_name, fill=gate_color, font=gf)
    
    # Layer labels
    lf = get_font(14)
    for l in range(4):
        lx = circ_x + 80 + l * layer_width * 2
        draw.text((lx - 15, circ_y + num_qubits * wire_spacing + 20), f"Layer {l+1}", 
                 fill=COLORS['text_secondary'], font=lf)
    
    # Stats panel
    stats_x = 1180
    stats_y = 120
    draw.rectangle([stats_x, stats_y, stats_x+250, stats_y+400], 
                  fill=COLORS['bg_secondary']+(180,), outline=COLORS['accent_purple']+(100,), width=2)
    
    st_font = get_font(20, bold=True)
    draw.text((stats_x+15, stats_y+15), "CIRCUIT STATS", fill=COLORS['accent_purple'], font=st_font)
    
    stats = [
        ("Parameters:", "60"),
        ("Depth:", "12 layers"),
        ("Gate Count:", "47"),
        ("Qubits:", "5"),
        ("NISQ Opt:", "✓ Yes"),
        ("Expressive:", "✓ Yes"),
        ("Barren Plateau:", "✓ Free"),
    ]
    
    sy = stats_y + 55
    for label, val in stats:
        lf2 = get_font(16)
        draw.text((stats_x+20, sy), label, fill=COLORS['text_secondary'], font=lf2)
        vf = get_font(16, bold=True)
        draw.text((stats_x+140, sy), val, fill=COLORS['accent_cyan'], font=vf)
        sy += 42
    
    # Bottom info
    param_font = get_font(22, bold=True)
    param_text = "Total Parameters: 60  |  Depth: 12  |  Measurement Reduction: 98%"
    pb = draw.textbbox((0, 0), param_text, font=param_font)
    draw.text(((VIDEO_WIDTH-(pb[2]-pb[0]))//2, 560), param_text, fill=COLORS['accent_gold'], font=param_font)
    
    eff_font = get_font(18)
    eff_text = "✓ NISQ-Optimized  ✓ Expressible  ✓ Barren plateau-free"
    eb = draw.textbbox((0, 0), eff_text, font=eff_font)
    draw.text(((VIDEO_WIDTH-(eb[2]-eb[0]))//2, 600), eff_text, fill=COLORS['accent_green'], font=eff_font)
    
    return add_vignette(img, 0.28)


def gen_wavefunction_frame(gen_particles, gen_wave, time_offset, segment):
    """Wave function visualization."""
    img = create_gradient_bg(time_offset=time_offset, base_color=(4, 4, 12))
    
    # Dense particles
    dense = FastParticleSystem(count=120)
    dense.draw(img, time_offset)
    
    # Main wave function
    wf1 = WaveFunctionViz(center=(450, 340))
    wf1.draw(img, color=COLORS['accent_cyan'], time_offset=time_offset)
    
    # Entangled partner
    wf2 = WaveFunctionViz(center=(850, 340))
    wf2.draw(img, color=COLORS['accent_purple'], time_offset=-time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    tf = get_font(28, bold=True)
    title = "WAVE FUNCTION PROBABILITY DISTRIBUTION"
    tb = draw.textbbox((0, 0), title, font=tf)
    draw.text(((VIDEO_WIDTH-(tb[2]-tb[0]))//2, 15), title, fill=COLORS['accent_cyan'], font=tf)
    
    sf = get_font(17)
    sub = "|ψ⟩² — Born Rule Visualization for Binding Site Electron Cloud"
    sb = draw.textbbox((0, 0), sub, font=sf)
    draw.text(((VIDEO_WIDTH-(sb[2]-sb[0]))//2, 50), sub, fill=COLORS['text_secondary'], font=sf)
    
    # Formula box
    draw.rectangle([50, 560, 400, 680], fill=COLORS['bg_secondary']+(180,), 
                  outline=COLORS['accent_gold']+(100,), width=2)
    ff = get_font(20, bold=True)
    formulas = ["H|ψ⟩ = E|ψ⟩", "E = ⟨ψ|H|ψ⟩", "|ψ⟩ = Σᵢcᵢ|φᵢ⟩"]
    fy = 575
    for f in formulas:
        fc = COLORS['accent_gold']+(200+int(math.sin(time_offset*0.05+formulas.index(f))*55),)
        draw.text((70, fy), f, fill=fc, font=ff)
        fy += 32
    
    # Speed comparison
    spdf = get_font(24, bold=True)
    spd = "40× SPEEDUP vs Classical DFT"
    spdb = draw.textbbox((0, 0), spd, font=spdf)
    draw.text(((VIDEO_WIDTH-(spdb[2]-spdb[0]))//2, 640), spd, fill=COLORS['accent_green'], font=spdf)
    
    # Entanglement line
    ent_y = 500
    draw.line([(400, ent_y), (900, ent_y)], fill=COLORS['accent_purple']+(80,), width=2)
    ef = get_font(16, bold=True)
    etb = draw.textbbox((0, 0), "⟺ QUANTUM ENTANGLEMENT ⟺", font=ef)
    draw.text(((VIDEO_WIDTH-(etb[2]-etb[0]))//2, ent_y+5), "⟺ QUANTUM ENTANGLEMENT ⟺", 
             fill=COLORS['accent_purple'], font=ef)
    
    return add_vignette(img, 0.32)


def gen_business_frame(gen_particles, gen_wave, kpi_dash, time_offset, segment):
    """Business impact frame."""
    img = create_gradient_bg(time_offset=time_offset, base_color=(5, 12, 10))
    gen_particles.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Title
    tf = get_font(34, bold=True)
    title = "BUSINESS IMPACT & MARKET POSITION"
    tb = draw.textbbox((0, 0), title, font=tf)
    draw.text(((VIDEO_WIDTH-(tb[2]-tb[0]))//2, 25), title, fill=COLORS['accent_green'], font=tf)
    
    # Metric cards
    cards = [
        ("Hit Rate Improvement", "3.5×", "+250%", COLORS['accent_cyan']),
        ("Time-to-Candidate", "8 weeks", "-75%", COLORS['accent_green']),
        ("Screening Capacity", "10B", "compounds", COLORS['accent_purple']),
        ("Validation Papers", "12", "peer-reviewed", COLORS['accent_gold']),
        ("Seed Funding", "$4.2M", "$18M SA", COLORS['accent_pink']),
    ]
    
    card_w, card_h = 230, 200
    start_x, card_y = 35, 100
    spacing = 18
    
    for idx, (title, val, change, color) in enumerate(cards):
        x = start_x + idx * (card_w + spacing)
        
        # Card glow
        for gr in range(15, 3, -3):
            ga = int(10*(1-gr/15))
            draw.rounded_rectangle([x-gr, card_y-gr, x+card_w+gr, card_h+card_y+gr], 
                                  radius=10, fill=color+(ga,))
        
        # Card body
        draw.rounded_rectangle([x, card_y, x+card_w, card_h+card_y], radius=8,
                              fill=COLORS['bg_secondary']+(210,), outline=color+(130,), width=2)
        
        # Title
        ctf = get_font(14)
        ctb = draw.textbbox((0, 0), title, font=ctf)
        draw.text((x+(card_w-(ctb[2]-ctb[0]))//2, card_y+15), title, fill=COLORS['text_secondary'], font=ctf)
        
        # Value
        cvf = get_font(36, bold=True)
        cvb = draw.textbbox((0, 0), val, font=cvf)
        draw.text((x+(card_w-(cvb[2]-cvb[0]))//2, card_y+55), val, fill=color, font=cvf)
        
        # Change
        chf = get_font(16, bold=True)
        chc = COLORS['accent_green'] if "+" in change or "-" in change else COLORS['text_secondary']
        chb = draw.textbbox((0, 0), change, font=chf)
        draw.text((x+(card_w-(chb[2]-chb[0]))//2, card_h+card_y-35), change, fill=chc, font=chf)
    
    # Timeline
    tl_y = 330
    draw.line([(40, tl_y), (VIDEO_WIDTH-40, tl_y)], fill=COLORS['text_secondary']+(80,), width=2)
    
    tlf = get_font(20, bold=True)
    draw.text((50, tl_y+10), "TRACTION TIMELINE", fill=COLORS['text_primary'], font=tlf)
    
    milestones = [
        ("Q1 2024", "Founded"), ("Q2 2024", "First VQE"),
        ("Q3 2024", "Seed closed"), ("Q4 2024", "Pharma pilot"),
        ("Q1 2025", "Series A"), ("NOW", "Scaling"),
    ]
    
    ms_x = 100
    ms_sp = 190
    for mi, (date, event) in enumerate(milestones):
        mx = ms_x + mi * ms_sp
        is_now = date == "NOW"
        dc = COLORS['accent_gold'] if is_now else COLORS['accent_cyan']
        dr = 10 if not is_now else 16
        
        if is_now:
            pa = int(abs(math.sin(time_offset*0.08))*100)
            draw.ellipse([mx-dr-8, tl_y+55-dr-8, mx-dr+8, tl_y+55+dr+8], fill=COLORS['accent_gold']+(pa,))
        
        draw.ellipse([mx-dr, tl_y+55-dr, mx+dr, tl_y+55+dr], fill=dc)
        
        df = get_font(13, bold=True)
        draw.text((mx-20, tl_y+72), date, fill=dc, font=df)
        
        ef = get_font(12)
        eb = draw.textbbox((0, 0), event, font=ef)
        draw.text((mx-(eb[2]-eb[0])//2, tl_y+92), event, fill=COLORS['text_secondary'], font=ef)
    
    # CTA
    ctaf = get_font(20)
    cta = "Transforming Quantum Computing into Therapeutic Reality"
    ctab = draw.textbbox((0, 0), cta, font=ctaf)
    draw.text(((VIDEO_WIDTH-(ctab[2]-ctab[0]))//2, 650), cta, fill=COLORS['accent_purple'], font=ctaf)
    
    return add_vignette(img, 0.25)


def gen_closing_frame(gen_particles, gen_wave, time_offset, segment):
    """Closing frame."""
    img = create_gradient_bg(time_offset=time_offset, base_color=(8, 10, 22))
    
    # Intense wave functions
    wf1 = WaveFunctionViz(center=(640, 320))
    wf1.draw(img, color=COLORS['accent_cyan'], time_offset=time_offset)
    wf2 = WaveFunctionViz(center=(640, 360))
    wf2.draw(img, color=COLORS['accent_purple'], time_offset=-time_offset*1.3)
    
    gen_particles.draw(img, time_offset)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Quote marks
    qf = get_font(100)
    draw.text((100, 150), """, fill=COLORS['accent_cyan']+(40,), font=qf)
    draw.text((VIDEO_WIDTH-220, 420), """, fill=COLORS['accent_cyan']+(40,), font=qf)
    
    # Closing text
    lines = [
        "This is not science fiction.",
        "This is quantum advantage,",
        "deployed today,",
        "saving lives tomorrow.",
    ]
    
    ly = 240
    mf = get_font(34, bold=True)
    for li, line in enumerate(lines):
        if line:
            la = min(255, int(255*(time_offset*0.03 - li*1.5)))
            if la > 0:
                lc = COLORS['text_primary'] if li < 3 else COLORS['accent_cyan']
                lb = draw.textbbox((0, 0), line, font=mf)
                draw.text(((VIDEO_WIDTH-(lb[2]-lb[0]))//2, ly), line, fill=lc, font=mf)
        ly += 50
    
    # Company name
    cf = get_font(48, bold=True)
    company = "Quantum Therapeutics"
    cb = draw.textbbox((0, 0), company, font=cf)
    cox = (VIDEO_WIDTH-(cb[2]-cb[0]))//2
    coy = 520
    
    # Glow
    for gl in range(25, 5, -5):
        gla = int(15*(1-gl/25))
        draw.text((cox, coy), company, fill=COLORS['accent_cyan']+(gla,), 
                 font=get_font(48+gl//2, bold=True))
    
    draw.text((cox, coy), company, fill=COLORS['accent_cyan'], font=cf)
    
    # Tagline
    tgf = get_font(22, italic=True)
    tag = "Where Schrödinger's Equation Meets FDA Approval"
    tgb = draw.textbbox((0, 0), tag, font=tgf)
    draw.text(((VIDEO_WIDTH-(tgb[2]-tgb[0]))//2, 590), tag, fill=COLORS['accent_purple'], font=tgf)
    
    # Footer
    draw.rectangle([0, VIDEO_HEIGHT-70, VIDEO_WIDTH, VIDEO_HEIGHT], fill=(0,0,0,190))
    wbf = get_font(18)
    web = "🌐 scimspt.io/quantum-therapeutics  •  📧 invest@quantumtherapeutics.ai  •  ⚛ Validated by Science"
    wbb = draw.textbbox((0, 0), web, font=wbf)
    draw.text(((VIDEO_WIDTH-(wbb[2]-wbb[0]))//2, VIDEO_HEIGHT-45), web, 
             fill=COLORS['text_secondary'], font=wbf)
    
    return add_vignette(img, 0.4)


# ============================================================================
# MAIN GENERATION
# ============================================================================

def generate_premium_video():
    """Generate the premium video."""
    print("=" * 60)
    print("SciMSPT PREMIUM Video Generator (Fast Mode)")
    print("=" * 60)
    
    # Initialize generators
    particles = FastParticleSystem(count=80)
    wave = WaveFunctionViz(center=(640, 360))
    kpi_dash = QuantumKPIDashboard()
    
    frames_dir = PREMIUM_DIR / "qt_fast_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    audio_path = AUDIO_DIR / "qt_premium_narration.wav"
    video_output = OUTPUT_DIR / "quantum_therapeutics_premium.mp4"
    
    total_frames = DURATION * FPS
    
    # Generate narration
    print("\n[1/3] Generating narration...")
    full_text = " ".join([s["text"] for s in QT_PREMIUM["narration_segments"]])
    
    tts_cmd = ["edge-tts", "--voice", "en-US-GuyNeural", "--text", full_text,
               "--write-media", str(audio_path)]
    
    try:
        subprocess.run(tts_cmd, check=True, capture_output=True)
        print(f"      ✓ Audio saved")
    except Exception as e:
        print(f"      ! TTS issue, using silent: {e}")
        subproc.run(["ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-t", str(DURATION), "-y", str(audio_path)], capture_output=True)
    
    # Get audio duration
    probe = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
                          capture_output=True, text=True)
    audio_dur = float(probe.stdout.strip())
    print(f"      Duration: {audio_dur:.1f}s")
    
    # Generate frames
    print("\n[2/3] Generating frames...")
    
    frame_geners = {
        "title_hero": lambda to: gen_title_frame(particles, wave, to, None),
        "kpi_dashboard": lambda to: gen_kpi_frame(particles, wave, kpi_dash, to, None),
        "ansatz_viz": lambda to: gen_ansatz_frame(particles, wave, to, None),
        "wave_function": lambda to: gen_wavefunction_frame(particles, wave, to, None),
        "business_impact": lambda to: gen_business_frame(particles, wave, kpi_dash, to, None),
        "closing": lambda to: gen_closing_frame(particles, wave, to, None),
    }
    
    global_frame = 0
    for seg in QT_PREMIUM["narration_segments"]:
        seg_frames = int(seg["duration"] * FPS)
        vtype = seg["visual"]
        
        print(f"   → {vtype} ({seg['duration']}s, ~{seg_frames} frames)")
        
        for fi in range(seg_frames):
            to = global_frame / FPS * 100
            
            try:
                img = frame_geners[vtype](to)
                img.save(frames_dir / f"f_{global_frame:06d}.png", 'PNG')
            except Exception as ex:
                print(f"      Frame {global_frame} error: {ex}")
                # Fallback solid
                Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), COLORS['bg_deep']).save(
                    frames_dir / f"f_{global_frame:06d}.png", 'PNG')
            
            global_frame += 1
            
            if fi % max(1, seg_frames // 4) == 0:
                pct = global_frame / total_frames * 100
                print(f"      {global_frame}/{total_frames} ({pct:.0f}%)")
    
    print(f"\n      ✓ {global_frame} frames generated")
    
    # Assemble video
    print("\n[3/3] Assembling video...")
    
    concat_file = frames_dir / "concat.txt"
    with open(concat_file, 'w') as f:
        for i in range(global_frame):
            f.write(f"file 'f_{i:06d}.png'\n")
    
    ffmpeg_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
                  "-i", str(audio_path), "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
                  str(video_output)]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size_mb = video_output.stat().stsize / (1024*1024)
        print(f"\n      ✓ Video created: {video_output.name} ({size_mb:.1f} MB)")
    else:
        print(f"\n      ✗ FFmpeg error: {result.stderr[:300]}")
    
    # Cleanup
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)
    
    print("\n" + "=" * 60)
    print("PREMIUM GENERATION COMPLETE")
    print("=" * 60)
    
    return video_output


if __name__ == "__main__":
    generate_premium_video()
