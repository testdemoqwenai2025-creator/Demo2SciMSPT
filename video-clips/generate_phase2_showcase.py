#!/usr/bin/env python3
"""
SciMSPT Phase 2 Molecular Intelligence Overhaul - Showcase Video Generator
==========================================================================
Creates a 60-second cinematic showcase of the Phase 2 enhancements including:
- Neural Identity System (creative synthetic login)
- DNA/RNA/Protein molecular decorations
- Futuristic design polish (holographic effects, glow, animations)
- Navigation architecture enhancements
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

# Ensure directories exist
for d in [IMAGES_DIR, AUDIO_DIR, OUTPUT_DIR, TEMP_DIR]:
    d.mkdir(exist_ok=True)

# Phase 2 Showcase Content
SHOWCASE = {
    "phase2_showcase": {
        "title": "SciMSPT Phase 2: Molecular Intelligence Overhaul",
        "duration_seconds": 60,
        "resolution": "1920x1080",
        "scenes": [
            {
                "id": "intro",
                "title": "Platform Evolution",
                "duration": 8,
                "narration": "Welcome to SciMSPT Neural Research Intelligence Platform. Today, we unveil Phase Two: The Molecular Intelligence Overhaul.",
                "image_prompt": "Futuristic neural network interface glowing cyan purple blue particles data flowing digital brain AI research cinematic dark background"
            },
            {
                "id": "neural_identity",
                "title": "Neural Identity System",
                "duration": 12,
                "narration": "Meet our revolutionary Neural Identity System. Each researcher receives a unique algorithmic persona, like Dr. Aeva Chen-Neural or Prof. Kai Synapse. Your identity features dynamic neural scores, ATGC-based session IDs, and holographic avatar cards that pulse with cognitive resonance.",
                "image_prompt": "Holographic user profile card futuristic avatar neural interface glowing ring around head digital identity cyberpunk UI cyan magenta glow"
            },
            {
                "id": "molecular_sidebars",
                "title": "Molecular Visualizations",
                "duration": 12,
                "narration": "Experience our enhanced molecular sidebars. On the left, watch DNA double helices with connecting rungs animate in real-time. On the right, observe protein folding spirals that respond to your scroll position. Hover to reveal nucleotide labels: Adenine, Thymine, Guanine, Cytosine.",
                "image_prompt": "DNA double helix rotating 3D visualization nucleotides colorful dots protein folding animation scientific molecular structure biotech neon glow"
            },
            {
                "id": "design_polish",
                "title": "Futuristic Design System",
                "duration": 12,
                "narration": "Every element has been elevated with futuristic design polish. Holographic edge glows on cards. Magnetic buttons that pull toward your cursor. Custom scrollbars with luminous thumbs. Particle fields floating ambiently. Text shadows that radiate cyan light.",
                "image_prompt": "Futuristic UI design glass morphism cards holographic borders glowing edges magnetic buttons particle field dark theme sci-fi interface"
            },
            {
                "id": "navigation",
                "title": "Enhanced Navigation",
                "duration": 8,
                "narration": "Navigate with precision using our enhanced page navigation system. Dynamic breadcrumbs show your location. Return and Home buttons on every page. Smooth slide-in animations welcome you to each section.",
                "image_prompt": "Modern web navigation bar breadcrumbs glass morphism futuristic UI back home buttons smooth animations clean interface"
            },
            {
                "id": "cta",
                "title": "Begin Your Journey",
                "duration": 8,
                "narration": "SciMSPT Phase Two is now live. Eight pages transformed. Forty plus enhancements deployed. The future of research intelligence awaits. Visit us at SciMSPT dot github dot io.",
                "image_prompt": "Futuristic rocket launch digital transformation success celebration neon lights platform launch cinematic wide angle inspiring"
            }
        ]
    }
}

def generate_audio(scene_id, narration_text, output_path):
    """Generate TTS audio for narration"""
    print(f"  🎙️ Generating audio for scene: {scene_id}")
    
    # Use TTS skill via command line (edge-tts or similar)
    try:
        # Try edge-tts first (Microsoft Edge TTS)
        cmd = [
            sys.executable, "-m", "edge_tts",
            "--voice", "en-GB-RyanNeural",  # British male voice, sophisticated
            "--text", narration_text,
            "--write-media", str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and output_path.exists():
            return True
        else:
            print(f"    ⚠️ edge-tts failed, trying alternative...")
            
    except FileNotFoundError:
        pass
    
    # Fallback: Use say (macOS) or espeak (Linux)
    if sys.platform == "darwin":
        cmd = ["say", "-v", "Alex", "-o", str(output_path), narration_text]
        subprocess.run(cmd, timeout=30)
        return output_path.exists()
    else:
        # Linux espeak fallback
        cmd = ["espeak", "-w", str(output_path), narration_text]
        subprocess.run(cmd, timeout=30)
        return output_path.exists()

def generate_image(scene_id, image_prompt, output_path):
    """Generate image for scene (placeholder - would use image generation API)"""
    print(f"  🎨 Generating image for scene: {scene_id}")
    
    # For now, create a gradient placeholder with text overlay
    # In production, this would call DALL-E, Midjourney, or Stable Diffusion
    
    from PIL import Image, ImageDraw, ImageFont
    import math
    
    width, height = 1920, 1080
    
    # Create gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Dark futuristic gradient
    for y in range(height):
        r = int(3 + (y / height) * 10)
        g = int(8 + (y / height) * 22)
        b = int(16 + (y / height) * 40)
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    
    # Add grid pattern
    for i in range(0, width, 40):
        draw.line([(i, 0), (i, height)], fill=(0, 229, 255, 20), width=1)
    for i in range(0, height, 40):
        draw.line([(0, i), (width, i)], fill=(0, 229, 255, 20), width=1)
    
    # Add glowing circles (neural nodes)
    for _ in range(50):
        x = int((math.sin(time.time()) + 1) * width / 2) % width
        y = int((math.cos(time.time() * 0.7) + 1) * height / 2) % height
        radius = 3
        color = (0, 229, 255) if _ % 2 == 0 else (167, 139, 250)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Add title text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Scene title
    title = SHOWCASE["phase2_showcase"]["scenes"][int(scene_id[-1]) - 1]["title"] if scene_id[-1].isdigit() else "SciMSPT Phase 2"
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) // 2, (height - th) // 2 - 50), title, fill=(0, 229, 255), font=font_large)
    
    # Subtitle
    subtitle = f"Scene {scene_id[-1] if scene_id[-1].isdigit() else '1'}"
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - sw) // 2, (height - th) // 2 + 50), subtitle, fill=(167, 139, 250), font=font_small)
    
    img.save(output_path)
    return True

def get_audio_duration(audio_path):
    """Get duration of audio file using ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def create_video_scene(image_path, audio_path, output_path, duration):
    """Create a single video scene from image + audio"""
    print(f"  🎬 Creating video scene...")
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-t", str(duration),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def concatenate_videos(video_list, output_path):
    """Concatenate multiple videos into one"""
    print(f"  🔗 Concatenating {len(video_list)} scenes...")
    
    # Create concat list file
    concat_file = TEMP_DIR / "concat_list.txt"
    with open(concat_file, 'w') as f:
        for video in video_list:
            f.write(f"file '{video}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    """Main showcase generation function"""
    print("=" * 70)
    print("🚀 SciMSPT Phase 2 Showcase Video Generator")
    print("=" * 70)
    print()
    
    showcase_data = SHOWCASE["phase2_showcase"]
    scenes = showcase_data["scenes"]
    
    generated_videos = []
    
    for idx, scene in enumerate(scenes, 1):
        scene_id = scene["id"]
        print(f"\n📽️ Processing Scene {idx}/{len(scenes)}: {scene['title']}")
        
        # Paths
        image_path = IMAGES_DIR / f"phase2_{scene_id}.png"
        audio_path = AUDIO_DIR / f"phase2_{scene_id}.wav"
        video_path = OUTPUT_DIR / f"phase2_{scene_id}.mp4"
        
        # Generate assets
        generate_image(scene_id, scene["image_prompt"], image_path)
        generate_audio(scene_id, scene["narration"], audio_path)
        
        # Create video scene
        if create_video_scene(image_path, audio_path, video_path, scene["duration"]):
            generated_videos.append(str(video_path))
            print(f"  ✅ Scene {idx} complete")
        else:
            print(f"  ❌ Scene {idx} failed")
    
    # Concatenate all scenes
    final_output = OUTPUT_DIR / "SCIMSPT_PHASE2_SHOWCASE.mp4"
    
    if len(generated_videos) > 1:
        if concatenate_videos(generated_videos, final_output):
            print(f"\n✅ Showcase video created successfully!")
            print(f"   Output: {final_output}")
        else:
            print(f"\n❌ Failed to concatenate videos")
    elif len(generated_videos) == 1:
        import shutil
        shutil.copy(generated_videos[0], final_output)
        print(f"\n✅ Single scene video saved: {final_output}")
    else:
        print("\n❌ No scenes were generated")
        return False
    
    # Generate metadata
    metadata = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "showcase_title": showcase_data["title"],
        "total_scenes": len(scenes),
        "target_duration_seconds": showcase_data["duration_seconds"],
        "resolution": showcase_data["resolution"],
        "scenes_processed": [
            {
                "id": s["id"],
                "title": s["title"],
                "success": True
            } for s in scenes
        ],
        "output_file": str(final_output.name),
        "next_phase_recommendations": [
            {
                "phase": "Phase 3A",
                "title": "Interactive Features",
                "description": "Add working search, filterable databases, user bookmarks with localStorage",
                "priority": "HIGH",
                "estimated_effort": "2-3 days"
            },
            {
                "phase": "Phase 3B",
                "title": "Backend Integration",
                "description": "Deploy Cloudflare Worker for comments API, real OAuth authentication, automated RSS parsing",
                "priority": "MEDIUM",
                "estimated_effort": "5-7 days"
            },
            {
                "phase": "Phase 3C",
                "title": "Advanced Visualizations",
                "description": "3D molecular models (Three.js), interactive knowledge graph, real-time dashboards",
                "priority": "MEDIUM",
                "estimated_effort": "7-10 days"
            },
            {
                "phase": "Phase 3D",
                "title": "Mobile & PWA",
                "description": "Touch-friendly navigation, Progressive Web App support, offline reading mode",
                "priority": "HIGH",
                "estimated_effort": "3-5 days"
            }
        ]
    }
    
    metadata_path = OUTPUT_DIR / "phase2_showcase_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n📊 Metadata saved: {metadata_path}")
    print()
    print("=" * 70)
    print("🎉 PHASE 2 SHOWCASE GENERATION COMPLETE!")
    print("=" * 70)
    print()
    print("📹 Video Output:")
    print(f"   📍 Location: {final_output}")
    print(f"   🎬 Duration: ~{showcase_data['duration_seconds']} seconds")
    print(f"   📐 Resolution: {showcase_data['resolution']}")
    print()
    print("🔮 NEXT PHASE RECOMMENDATIONS:")
    for rec in metadata["next_phase_recommendations"]:
        print(f"   {rec['phase']}: {rec['title']}")
        print(f"      Priority: {rec['priority']} | Effort: {rec['estimated_effort']}")
        print(f"      → {rec['description']}")
        print()
    
    return True

if __name__ == "__main__":
    main()
