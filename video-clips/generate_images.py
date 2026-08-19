#!/usr/bin/env python3
"""
Generate professional-looking images for SciMSPT startup video clips
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

IMAGES_DIR = Path("/home/z/my-project/SciMSPT/video-clips/images")
IMAGES_DIR.mkdir(exist_ok=True)

# Startup visual configurations
STARTUPS = {
    "P1": {
        "name": "Stellarator Fusion",
        "domain": "Nuclear Fusion · Compact Stellarators",
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (26, 54, 93), "accent": (0, 229, 255), "accent_name": "#00E5FF"},
        "icon": "⚛️",
        "tagline": "$589M NPV | 65.7% P(IRR>15%)"
    },
    "P2": {
        "name": "SMR Fleet OS",
        "domain": "Nuclear · Small Modular Reactors", 
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (30, 41, 59), "accent": (77, 168, 218), "accent_name": "#4da8da"},
        "icon": "🏭",
        "tagline": "$50M NPV | 23.0% IRR"
    },
    "P3": {
        "name": "Solid-State Battery",
        "domain": "Energy Storage · Next-Gen Batteries",
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (26, 26, 46), "accent": (16, 185, 129), "accent_name": "#10b981"},
        "icon": "🔋",
        "tagline": "$587M NPV | Tier 1"
    },
    "P4": {
        "name": "Iron-Air LDES",
        "domain": "Grid Storage · Long-Duration",
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (26, 35, 50), "accent": (245, 158, 11), "accent_name": "#f59e0b"},
        "icon": "⚡",
        "tagline": "$44M NPV | 100+ Hour Discharge"
    },
    "P5": {
        "name": "Super-Steel Electrolyzer",
        "domain": "Hydrogen · Green H2 Production",
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (19, 34, 56), "accent": (6, 182, 212), "accent_name": "#06b6d4"},
        "icon": "💧",
        "tagline": "$43M NPV | $1.50/kg H2"
    },
    "P6": {
        "name": "Detonation H2 Turbine",
        "domain": "Hydrogen · Rotating Detonation",
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (26, 26, 46), "accent": (239, 68, 68), "accent_name": "#ef4444"},
        "icon": "🔥",
        "tagline": "$34M NPV | +15% Efficiency"
    },
    "P7": {
        "name": "Room-Temp Quantum Materials",
        "domain": "Quantum · Superconductors",
        "colors": {"bg_top": (10, 22, 40), "bg_bottom": (24, 10, 40), "accent": (167, 139, 250), "accent_name": "#a78bfa"},
        "icon": "✨",
        "tagline": "$107M NPV | 34.3% IRR"
    }
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def interpolate_color(color1, color2, factor):
    """Interpolate between two colors"""
    return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

def draw_gradient(draw, width, height, color_top, color_bottom):
    """Draw vertical gradient"""
    for y in range(height):
        factor = y / height
        color = interpolate_color(color_top, color_bottom, factor)
        draw.line([(0, y), (width, y)], fill=color)

def create_startup_image(startup_id):
    """Create a professional image for a startup"""
    config = STARTUPS[startup_id]
    
    # Create image
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    bg_top = config["colors"]["bg_top"]
    bg_bottom = config["colors"]["bg_bottom"]
    accent = config["colors"]["accent"]
    
    draw_gradient(draw, width, height, bg_top, bg_bottom)
    
    # Draw decorative border frame
    margin = 80
    # Outer glow
    for i in range(20, 0, -2):
        alpha = int(10 * (1 - i/20))
        glow_color = (*accent[:3],) if len(accent) == 3 else accent
        draw.rectangle(
            [margin-i, margin-i, width-margin+i, height-margin+i],
            outline=(*glow_color[:3],),
            width=1
        )
    
    # Main border
    draw.rectangle(
        [margin, margin, width-margin, height-margin],
        outline=(*accent[:3],),
        width=3
    )
    
    # Inner border
    inner_margin = margin + 15
    draw.rectangle(
        [inner_margin, inner_margin, width-inner_margin, height-inner_margin],
        outline=(*[min(c+30, 255) for c in accent[:3]],),
        width=1
    )
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 84)
        domain_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        id_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except Exception as e:
        print(f"   Font loading: {e}")
        title_font = ImageFont.load_default()
        domain_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()
        id_font = ImageFont.load_default()
    
    # Draw content centered
    center_x = width // 2
    
    # Startup ID badge
    id_text = f"{startup_id} · STARTUP"
    id_bbox = draw.textbbox((0, 0), id_text, font=id_font)
    id_width = id_bbox[2] - id_bbox[0]
    draw.text((center_x - id_width//2, 180), id_text, fill=accent, font=id_font)
    
    # Main title
    name = config["name"]
    title_bbox = draw.textbbox((0, 0), name, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((center_x - title_width//2, 280), name, fill=(255, 255, 255), font=title_font)
    
    # Accent line under title
    line_y = 400
    line_width = min(400, title_width)
    draw.line(
        [(center_x - line_width//2, line_y), (center_x + line_width//2, line_y)],
        fill=accent,
        width=4
    )
    
    # Domain/subtitle
    domain = config["domain"]
    domain_bbox = draw.textbbox((0, 0), domain, font=domain_font)
    domain_width = domain_bbox[2] - domain_bbox[0]
    draw.text((center_x - domain_width//2, 450), domain, fill=(122, 155, 184), font=domain_font)
    
    # Tagline/metrics
    tagline = config["tagline"]
    tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    
    # Tagline background box
    pad = 20
    box_y = 550
    draw.rounded_rectangle(
        [center_x - tagline_width//2 - pad, box_y - pad//2,
         center_x + tagline_width//2 + pad, box_y + tagline_bbox[3] - tagline_bbox[1] + pad//2],
        radius=10,
        fill=(*[c//4 for c in accent[:3]],),
        outline=accent
    )
    draw.text((center_x - tagline_width//2, box_y), tagline, fill=accent, font=tagline_font)
    
    # Brand footer
    brand_text = "SciMSPT Venture Pipeline — From Research to Investment"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_width = brand_bbox[2] - brand_bbox[0]
    draw.text((center_x - brand_width//2, height - 150), brand_text, fill=(77, 168, 218), font=brand_font)
    
    # Decorative corner elements
    corner_size = 60
    corner_positions = [
        (margin + 20, margin + 20),
        (width - margin - corner_size - 20, margin + 20),
        (margin + 20, height - margin - corner_size - 20),
        (width - margin - corner_size - 20, height - margin - corner_size - 20)
    ]
    
    for cx, cy in corner_positions:
        draw.line([(cx, cy), (cx + corner_size, cy)], fill=accent, width=2)
        draw.line([(cx, cy), (cx, cy + corner_size)], fill=accent, width=2)
    
    # Save image
    output_path = IMAGES_DIR / f"{startup_id}_hero.png"
    img.save(str(output_path), 'PNG', quality=95)
    
    size_kb = output_path.stat().st_size / 1024
    print(f"   ✅ {config['name']}: {output_path.name} ({size_kb:.0f} KB)")
    
    return output_path


def main():
    print("🎨 Generating professional images for all startups...\n")
    
    for startup_id in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]:
        try:
            create_startup_image(startup_id)
        except Exception as e:
            print(f"   ❌ {startup_id} failed: {e}")
    
    print(f"\n✅ All images saved to: {IMAGES_DIR}")


if __name__ == "__main__":
    main()
