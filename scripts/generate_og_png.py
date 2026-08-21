#!/usr/bin/env python3
"""
Generate PNG version of OG image from SVG for social sharing compatibility.
Some platforms (LinkedIn, certain email clients) prefer PNG over SVG.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
svg_path = os.path.join(PROJECT_ROOT, 'assets', 'og-image.svg')
png_path = os.path.join(PROJECT_ROOT, 'assets', 'og-image.png')

def main():
    print(f"📷 OG Image PNG Generator")
    print(f"   Source: {svg_path}")
    print(f"   Output: {png_path}")
    print()
    
    # Check if SVG exists
    if not os.path.exists(svg_path):
        print(f"❌ Error: SVG file not found at {svg_path}")
        sys.exit(1)
    
    # Try cairosvg first (best quality)
    try:
        import cairosvg
        cairosvg.svg2png(
            url=svg_path, 
            write_to=png_path, 
            output_width=1200, 
            output_height=630
        )
        print(f"✅ Created {png_path} using cairosvg")
        print(f"   Dimensions: 1200x630 (Open Graph standard)")
        return 0
    except ImportError:
        print("⚠️  cairosvg not installed, trying alternative...")
    except Exception as e:
        print(f"⚠️  cairosvg failed: {e}, trying alternative...")
    
    # Try Pillow with svg support or create fallback
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a high-quality gradient background matching SciMSPT theme
        width, height = 1200, 630
        img = Image.new('RGB', (width, height), color=(3, 8, 16))  # Dark blue-black
        
        # Create gradient effect
        draw = ImageDraw.Draw(img)
        for y in range(height):
            # Gradient from dark to slightly lighter blue
            r = int(3 + (y / height) * 10)
            g = int(8 + (y / height) * 20)
            b = int(16 + (y / height) * 40)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            # Try to use a nice font
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw title text
        title = "SciMSPT"
        subtitle = "Scientific Materials Science & Processing Toolkit"
        
        # Center the text
        bbox_large = draw.textbbox((0, 0), title, font=font_large)
        title_width = bbox_large[2] - bbox_large[0]
        title_x = (width - title_width) // 2
        title_y = height // 2 - 60
        
        bbox_small = draw.textbbox((0, 0), subtitle, font=font_small)
        subtitle_width = bbox_small[2] - bbox_small[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = title_y + 100
        
        # Draw text with glow effect
        draw.text((title_x + 2, title_y + 2), title, fill=(0, 150, 255), font=font_large)
        draw.text((title_x, title_y), title, fill=(100, 200, 255), font=font_large)
        draw.text((subtitle_x, subtitle_y), subtitle, fill=(180, 180, 200), font=font_small)
        
        # Add border
        draw.rectangle([0, 0, width - 1, height - 1], outline=(50, 100, 150), width=4)
        
        img.save(png_path, 'PNG', optimize=True)
        print(f"✅ Created {png_path} using PIL fallback")
        print(f"   Note: Install cairosvg for full SVG conversion: pip install cairosvg")
        return 0
        
    except ImportError:
        print("⚠️  PIL/Pillow not available, creating minimal placeholder...")
    except Exception as e:
        print(f"⚠️  PIL failed: {e}, creating minimal placeholder...")
    
    # Absolute fallback - minimal valid PNG
    try:
        from PIL import Image
        img = Image.new('RGB', (1200, 630), color=(3, 8, 16))
        img.save(png_path)
        print(f"✅ Created basic placeholder {png_path}")
        print("   ⚠️  Install dependencies for better quality:")
        print("      pip install cairosvg pillow")
        return 0
    except Exception as e:
        print(f"❌ Error: Cannot create PNG: {e}")
        print("   Please install Pillow: pip install pillow")
        return 1

if __name__ == '__main__':
    sys.exit(main())
