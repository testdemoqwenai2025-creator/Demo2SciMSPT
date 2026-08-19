#!/usr/bin/env python3
"""
SciMSPT Phase 2 Showcase Video Generator (Optimized)
====================================================
Creates a 60-second showcase with synthesized visuals and background music
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
IMAGES_DIR = SCRIPT_DIR / "images"
AUDIO_DIR = SCRIPT_DIR / "audio"
OUTPUT_DIR = SCRIPT_DIR / "output"
TEMP_DIR = SCRIPT_DIR / "temp"

for d in [IMAGES_DIR, AUDIO_DIR, OUTPUT_DIR, TEMP_DIR]:
    d.mkdir(exist_ok=True)

# Phase 2 Showcase Scenes
SCENES = [
    {
        "id": "01_intro",
        "title": "Platform Evolution",
        "text": "SCI MSPT\nPHASE 2\nMolecular Intelligence Overhaul",
        "duration": 10,
        "color": (0, 229, 255),  # Cyan
        "icon": "🧬"
    },
    {
        "id": "02_neural",
        "title": "Neural Identity System",
        "text": "NEURAL IDENTITY\nAlgorithmic Personas\nATGC Session IDs\nHolographic Avatars",
        "duration": 10,
        "color": (167, 139, 250),  # Purple
        "icon": "🧠"
    },
    {
        "id": "03_molecular",
        "title": "Molecular Visualizations",
        "text": "DNA DOUBLE HELIX\nProtein Folding\nNucleotide Labels\nScroll Effects",
        "duration": 10,
        "color": (244, 114, 182),  # Pink
        "icon": "🔬"
    },
    {
        "id": "04_design",
        "title": "Futuristic Design",
        "text": "HOLOGRAPHIC GLOW\nMagnetic Buttons\nParticle Fields\nCustom Scrollbars",
        "duration": 10,
        "color": (16, 185, 129),  # Green
        "icon": "✨"
    },
    {
        "id": "05_nav",
        "title": "Enhanced Navigation",
        "text": "BREADCRUMBS\nBack/Home Buttons\nDynamic Page Names\nSmooth Animations",
        "duration": 10,
        "color": (245, 158, 11),  # Gold
        "icon": "🧭"
    },
    {
        "id": "06_cta",
        "title": "Begin Your Journey",
        "text": "8 PAGES TRANSFORMED\n40+ ENHANCEMENTS\nLIVE NOW\nscimspt.github.io",
        "duration": 10,
        "color": (0, 229, 255),  # Cyan
        "icon": "🚀"
    }
]

def create_scene_image(scene, output_path):
    """Create futuristic scene image"""
    from PIL import Image, ImageDraw, ImageFont
    import math
    
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), color=(3, 8, 16))
    draw = ImageDraw.Draw(img)
    
    # Background gradient
    for y in range(height):
        r = int(3 + (y / height) * 15)
        g = int(8 + (y / height) * 30)
        b = int(16 + (y / height) * 50)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Grid pattern
    for i in range(0, width, 60):
        draw.line([(i, 0), (i, height)], fill=(*scene["color"], 15), width=1)
    for i in range(0, height, 60):
        draw.line([(0, i), (width, i)], fill=(*scene["color"], 15), width=1)
    
    # Animated particles (static positions based on scene id)
    hash_val = hash(scene["id"]) % 1000
    for i in range(30):
        x = int((math.sin(hash_val + i * 0.5) + 1) * width / 2) % width
        y = int((math.cos(hash_val + i * 0.7) + 1) * height / 2) % height
        radius = 2 + (i % 4)
        
        # Glow effect
        for r_offset in range(3, 0, -1):
            alpha = int(50 / r_offset)
            glow_color = tuple(min(255, c + alpha) for c in scene["color"])
            draw.ellipse([x-radius-r_offset, y-radius-r_offset, 
                         x+radius+r_offset, y+radius+r_offset], 
                        fill=(*glow_color[:3],))
    
    # DNA helix decoration on left side
    helix_x = 150
    for i in range(20):
        y_pos = int((i / 20) * height)
        offset = int(math.sin(i * 0.8 + hash_val) * 40)
        nucleotide_colors = [(0, 229, 255), (244, 114, 182), (167, 139, 250), (16, 185, 129)]
        color = nucleotide_colors[i % 4]
        
        # Left strand
        draw.ellipse([helix_x + offset - 6, y_pos - 6, 
                     helix_x + offset + 6, y_pos + 6], fill=color)
        # Right strand  
        draw.ellipse([helix_x - offset - 6, y_pos - 6, 
                     helix_x - offset + 6, y_pos + 6], fill=color)
        # Connecting rung
        if i % 2 == 0:
            draw.line([(helix_x + offset, y_pos), (helix_x - offset, y_pos)], 
                     fill=(*color, 100), width=1)
    
    # Main content area (glass morphism card)
    card_left, card_top = 400, 200
    card_width, card_height = 1120, 680
    
    # Card background with transparency effect (simulated)
    for i in range(20):
        offset = i * 2
        alpha = 10 - i // 2
        if alpha > 0:
            draw.rounded_rectangle(
                [card_left - offset, card_top - offset, 
                 card_left + card_width + offset, card_top + card_height + offset],
                radius=24,
                fill=(*scene["color"],)
            )
    
    draw.rounded_rectangle(
        [card_left, card_top, card_left + card_width, card_top + card_height],
        radius=24,
        fill=(10, 22, 40),
        outline=scene["color"],
        width=2
    )
    
    # Try to load fonts
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = font_title
    
    # Scene number badge
    scene_num = SCENES.index(scene) + 1
    draw.rounded_rectangle([card_left + 40, card_top + 40, card_left + 120, card_top + 120], 
                          radius=12, fill=scene["color"])
    draw.text((card_left + 65, card_top + 70), f"{scene_num:02d}", fill=(3, 8, 16), 
             font=font_title, anchor="mm")
    
    # Title
    title = scene["title"]
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text((card_left + (card_width - tw) // 2, card_top + 160), title, 
             fill=scene["color"], font=font_title)
    
    # Content text
    lines = scene["text"].split("\n")
    y_offset = card_top + 300
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_text)
        lw = bbox[2] - bbox[0]
        draw.text((card_left + (card_width - lw) // 2, y_offset), line, 
                 fill=(232, 244, 252), font=font_text)
        y_offset += 80
    
    # Progress bar at bottom
    progress = (SCENES.index(scene) + 1) / len(SCENES)
    bar_width = int(card_width * 0.8)
    bar_left = card_left + (card_width - bar_width) // 2
    bar_y = card_top + card_height - 60
    
    # Background bar
    draw.rounded_rectangle([bar_left, bar_y, bar_left + bar_width, bar_y + 8], 
                          radius=4, fill=(30, 50, 70))
    # Progress fill
    draw.rounded_rectangle([bar_left, bar_y, bar_left + int(bar_width * progress), bar_y + 8], 
                          radius=4, fill=scene["color"])
    
    # Scene indicator dots
    dot_start_x = card_left + (card_width - (len(SCENES) * 30)) // 2
    for i, s in enumerate(SCENES):
        dot_x = dot_start_x + i * 30
        if i <= SCENES.index(scene):
            draw.ellipse([dot_x, bar_y + 20, dot_x + 12, bar_y + 32], fill=s["color"])
        else:
            draw.ellipse([dot_x, bar_y + 20, dot_x + 12, bar_y + 32], fill=(50, 70, 90))
    
    img.save(output_path, quality=95)
    return True

def generate_silent_audio(duration, output_path):
    """Generate silent audio track of specified duration"""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(duration),
        "-acodec", "pcm_s16le",
        str(output_path)
    ]
    subprocess.run(cmd, capture_output=True)
    return output_path.exists()

def create_video_from_image(image_path, duration, output_path):
    """Create video from static image"""
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-r", "30",
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def add_background_music(video_path, output_path):
    """Add ambient background music to video"""
    # Generate ambient tone
    audio_path = TEMP_DIR / "ambient_tone.wav"
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=f=220:b=4:d=60",  # Low A note, 60 seconds
        "-af", "volume=0.05,afade=t=in:st=0:d=3,afade=t=out:st=57:d=3",
        str(audio_path)
    ]
    subprocess.run(cmd, capture_output=True)
    
    if audio_path.exists():
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    return False

def concatenate_videos(video_list, output_path):
    """Concatenate videos"""
    concat_file = TEMP_DIR / "concat_list.txt"
    with open(concat_file, 'w') as f:
        for v in video_list:
            f.write(f"file '{v}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    print("=" * 70)
    print("🚀 SciMSPT Phase 2 Showcase Video Generator (Optimized)")
    print("=" * 70)
    
    generated_clips = []
    
    for idx, scene in enumerate(SCENES, 1):
        print(f"\n📽️ Creating Scene {idx}/{len(SCENES)}: {scene['title']}")
        
        image_path = IMAGES_DIR / f"phase2_{scene['id']}.png"
        clip_path = OUTPUT_DIR / f"phase2_{scene['id']}.mp4"
        
        # Generate image
        create_scene_image(scene, image_path)
        print(f"   ✅ Image created: {image_path.name}")
        
        # Create video clip
        if create_video_from_image(image_path, scene["duration"], clip_path):
            generated_clips.append(str(clip_path))
            print(f"   ✅ Clip created: {clip_path.name} ({scene['duration']}s)")
    
    # Concatenate all clips
    final_video = OUTPUT_DIR / "SCIMSPT_PHASE2_SHOWCASE.mp4"
    temp_concat = OUTPUT_DIR / "temp_showcase.mp4"
    
    if len(generated_clips) > 1:
        print("\n🔗 Concatenating scenes...")
        concatenate_videos(generated_clips, temp_concat)
        
        # Add ambient music
        print("🎵 Adding ambient soundtrack...")
        add_background_music(temp_concat, final_video)
        
        # Cleanup temp file
        temp_concat.unlink(missing_ok=True)
    
    # Get final video info
    if final_video.exists():
        size_mb = final_video.stat().st_size / (1024 * 1024)
        print(f"\n{'='*70}")
        print("✅ SHOWCASE VIDEO CREATED SUCCESSFULLY!")
        print(f"{'='*70}")
        print(f"\n📹 Output File:")
        print(f"   📍 {final_video}")
        print(f"   📊 Size: {size_mb:.1f} MB")
        print(f"   ⏱️ Duration: ~60 seconds")
        print(f"   📐 Resolution: 1920x1080")
        
        # Save metadata
        metadata = {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "video_file": str(final_video.name),
            "total_scenes": len(SCENES),
            "duration_seconds": sum(s["duration"] for s in SCENES),
            "resolution": "1920x1080",
            "file_size_mb": round(size_mb, 2),
            "next_phase_recommendations": [
                {
                    "phase": "Phase 3A",
                    "name": "Interactive Features",
                    "priority": "HIGH",
                    "effort": "2-3 days",
                    "description": "Working search, filterable databases, user bookmarks with localStorage persistence"
                },
                {
                    "phase": "Phase 3B", 
                    "name": "Backend Integration",
                    "priority": "MEDIUM",
                    "effort": "5-7 days",
                    "description": "Cloudflare Worker API, real OAuth authentication, automated RSS parsing"
                },
                {
                    "phase": "Phase 3C",
                    "name": "Advanced Visualizations",
                    "priority": "MEDIUM", 
                    "effort": "7-10 days",
                    "description": "3D molecular models (Three.js), interactive knowledge graphs, real-time dashboards"
                },
                {
                    "phase": "Phase 3D",
                    "name": "Mobile & PWA",
                    "priority": "HIGH",
                    "effort": "3-5 days",
                    "description": "Touch navigation, Progressive Web App support, offline reading mode"
                }
            ],
            "scenes": [
                {"id": s["id"], "title": s["title"], "duration": s["duration"]} 
                for s in SCENES
            ]
        }
        
        meta_path = OUTPUT_DIR / "phase2_showcase_metadata.json"
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📊 Metadata saved: {meta_path}")
        print(f"\n🔮 RECOMMENDED NEXT PHASES:")
        for rec in metadata["next_phase_recommendations"]:
            print(f"\n   📌 {rec['phase']}: {rec['name']}")
            print(f"      Priority: {rec['priority']} | Effort: {rec['effort']}")
            print(f"      → {rec['description']}")
        
        return True
    else:
        print("❌ Video creation failed")
        return False

if __name__ == "__main__":
    main()
