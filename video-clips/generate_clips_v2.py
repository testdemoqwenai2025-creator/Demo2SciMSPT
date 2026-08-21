#!/usr/bin/env python3
"""
SciMSPT 60-Second Startup Video Clip Generator (Fixed Version)
=============================================================
Handles TTS character limits, image generation, and video creation properly.
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

# Startup Data with shorter narrations (<1024 chars each)
STARTUPS = {
    "P1": {
        "name": "Stellarator Fusion",
        "domain": "Nuclear Fusion · Compact Stellarators",
        "tier": "TIER 1",
        "narration": """Stellarator Fusion represents the frontier of clean energy research, born from groundbreaking papers in Physical Review Letters and Nature Energy.

The journey began with fundamental research into optimized magnetic geometry for compact stellarators. Scientists discovered that careful engineering of plasma confinement configurations could achieve stable fusion reactions.

Key breakthroughs included advanced tritium breeding blanket materials and high-temperature superconducting coils. The pivotal moment came when researchers demonstrated net energy gain in compact fusion devices.

Today, Stellarator Fusion stands as a transformative opportunity with a net present value of five hundred eighty-nine million dollars. This is not merely scientific progress; it is the dawn of virtually limitless clean energy.""",
        "image_prompt": "Futuristic nuclear fusion stellarator reactor glowing plasma magnetic fields blue purple clean energy cinematic photorealistic"
    },
    "P2": {
        "name": "SMR Fleet OS",
        "domain": "Nuclear · Small Modular Reactors",
        "tier": "TIER 2",
        "narration": """SMR Fleet OS emerged from critical research in Applied Energy and Annals of Nuclear Energy, addressing operational challenges of Small Modular Reactors.

The original research focused on AI-driven load balancing for distributed nuclear power generation. Unlike traditional large reactors, SMRs require sophisticated fleet management systems.

Scientists developed predictive maintenance frameworks using digital twin technology. The regulatory automation component was particularly groundbreaking.

The startup opportunity: fifty million dollars NPV with twenty-three percent IRR. SMR Fleet OS represents essential software infrastructure for the nuclear renaissance.""",
        "image_prompt": "Modern small modular reactor control room holographic displays AI fleet management futuristic nuclear interface blue high-tech"
    },
    "P3": {
        "name": "Solid-State Battery",
        "domain": "Energy Storage · Next-Gen Batteries",
        "tier": "TIER 1",
        "narration": """Solid-State Battery technology traces origins to seminal research in Nature Energy and Joule, promising to revolutionize energy storage through sulfide-based electrolytes.

The foundational work demonstrated solid-state architectures achieving energy densities exceeding five hundred watt-hours per kilogram. These batteries eliminate thermal runaway risk entirely.

Research proved fast charging under fifteen minutes and cycle lives exceeding two thousand charges. With five hundred eighty-seven million dollars NPV, this represents the most significant advancement in energy storage since lithium-ion.""",
        "image_prompt": "Cutaway solid-state battery technology layered structure sulfide electrolyte glowing energy electric vehicle charging cyan white scientific"
    },
    "P4": {
        "name": "Iron-Air LDES",
        "domain": "Grid Storage · Long-Duration",
        "tier": "TIER 2",
        "narration": """Iron-Air LDES addresses grid-scale storage through revolutionary chemistry detailed in Science and Joule journals.

Scientists sought ultra-low-cost storage using earth-abundant materials. Iron-air chemistry offers costs of just twenty dollars per kilowatt-hour.

Breakthrough publications demonstrated one hundred plus hour discharge capabilities, ideal for renewable grid stabilization. When solar and wind fluctuate, long-duration storage bridges the gap.

Forty-four million dollars NPV with twenty-three point four percent IRR. Iron-Air LDES enables the fully renewable grid climate commitments demand.""",
        "image_prompt": "Massive iron-air battery installation grid storage renewable energy farm giant containers sustainable golden hour industrial environmental"
    },
    "P5": {
        "name": "Super-Steel Electrolyzer",
        "domain": "Hydrogen · Green H2 Production",
        "tier": "TIER 1",
        "narration": """Super-Steel Electrolyzer transforms green hydrogen production through innovations in Nature Catalysis and Advanced Materials.

The challenge: producing green hydrogen at one dollar fifty per kilogram requires extraordinary efficiency gains. Researchers achieved this through nanostructured super-steel electrodes.

Critical advances include variable renewable integration, allowing operation with intermittent wind and solar input.

With forty-three million dollars NPV and seventeen point seven percent IRR, Super-Steel Electrolyzer positions investors at the center of the hydrogen economy.""",
        "image_prompt": "Advanced electrolyzer system green hydrogen nanostructured steel electrodes bubbles forming clean energy teal silver modern industrial"
    },
    "P6": {
        "name": "Detonation H2 Turbine",
        "domain": "Hydrogen · Rotating Detonation",
        "tier": "TIER 2",
        "narration": """Detonation H2 Turbine leverages rotating detonation engine technology from Progress in Energy and Combustion Science.

Conventional hydrogen turbines suffer efficiency limitations that detonation engines overcome. Research demonstrates fifteen percent efficiency improvements through continuous detonation wave propagation.

Applications span aviation, marine shipping, and grid peaking. This versatility creates multiple revenue streams.

Thirty-four million dollars NPV with twenty-three point three percent IRR. Detonation H2 Turbine offers exposure to the hydrogen transition across sectors.""",
        "image_prompt": "Cross-section rotating detonation engine hydrogen combustion turbine blades spinning orange blue flame engineering precision dynamic"
    },
    "P7": {
        "name": "Room-Temp Quantum Materials",
        "domain": "Quantum · Superconductors",
        "tier": "TIER 3",
        "narration": """Room-Temp Quantum Materials represents perhaps the most transformative opportunity, from landmark Nature publications on ambient-condition superconductivity.

For decades, superconductivity required extreme cryogenic cooling. Research breakthroughs changed everything: layered materials exhibiting superconducting properties at room temperature.

The implications are profound: lossless power transmission, quantum computing interconnects at room temperature, sensors with unprecedented sensitivity.

One hundred seven million dollars NPV with thirty-four point three percent IRR. Room-Temp Quantum Materials offers asymmetric upside that could redefine industries.""",
        "image_prompt": "Quantum material structure room temperature superconducting currents flowing topological patterns purple gold futuristic laboratory computing"
    }
}


def print_header():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     SciMSPT 60-Second Startup Video Clip Generator          ║
║     UK/US Native Voice Narration + AI Imagery              ║
╚══════════════════════════════════════════════════════════════╝
""")


def split_text_for_tts(text: str, max_length: int = 950) -> list:
    """Split text into chunks suitable for TTS API"""
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if not sentence.endswith('.'):
            sentence += '.'
        
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += (' ' if current_chunk else '') + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def generate_tts_audio(startup_id: str, narration: str) -> Path:
    """Generate TTS audio using z-ai CLI with chunking for long texts"""
    output_path = AUDIO_DIR / f"{startup_id}_narration.wav"
    
    print(f"🎙️  Generating narration for {STARTUPS[startup_id]['name']}...")
    
    # Split text if needed
    chunks = split_text_for_tts(narration)
    
    if len(chunks) == 1:
        # Single chunk - direct generation
        cmd = [
            "z-ai", "tts",
            "--input", chunks[0],
            "--output", str(output_path),
            "--voice", "jam",  # British English gentleman voice
            "--speed", "0.9",
            "--format", "wav"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                print(f"   ✅ Audio saved ({size_kb:.0f} KB)")
                return output_path
        except Exception as e:
            print(f"   ⚠️  TTS error: {e}")
    
    # Multiple chunks - generate separately then concatenate
    print(f"   📝 Splitting into {len(chunks)} chunks...")
    chunk_files = []
    
    for i, chunk in enumerate(chunks):
        chunk_path = TEMP_DIR / f"{startup_id}_chunk_{i}.wav"
        cmd = [
            "z-ai", "tts",
            "--input", chunk,
            "--output", str(chunk_path),
            "--voice", "jam",
            "--speed", "0.9",
            "--format", "wav"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if chunk_path.exists():
                chunk_files.append(chunk_path)
                print(f"   ✅ Chunk {i+1}/{len(chunks)} generated")
            else:
                print(f"   ⚠️  Chunk {i+1} failed")
        except Exception as e:
            print(f"   ⚠️  Chunk {i+1} error: {e}")
    
    if chunk_files:
        # Concatenate audio files using ffmpeg
        concat_file = TEMP_DIR / f"{startup_id}_concat.txt"
        with open(concat_file, 'w') as f:
            for cf in chunk_files:
                f.write(f"file '{cf.absolute()}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_file),
            "-acodec", "pcm_s16le",
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=60)
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                print(f"   ✅ Audio concatenated ({size_kb:.0f} KB)")
                
                # Cleanup temp files
                for cf in chunk_files:
                    cf.unlink(missing_ok=True)
                concat_file.unlink(missing_ok=True)
                
                return output_path
        except Exception as e:
            print(f"   ⚠️  Concatenation error: {e}")
    
    # Return first chunk if concatenation failed
    if chunk_files:
        import shutil
        shutil.copy(chunk_files[0], output_path)
        return output_path
    
    raise Exception("Failed to generate any audio")


def generate_image(startup_id: str, prompt: str) -> Path:
    """Generate AI image for startup"""
    output_path = IMAGES_DIR / f"{startup_id}_hero.png"
    
    print(f"🎨  Generating image for {STARTUPS[startup_id]['name']}...")
    
    # Try z-ai image-gen CLI
    try:
        cmd = [
            "z-ai", "image-gen",
            "--prompt", prompt,
            "--output", str(output_path),
            "--size", "1920x1080"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if output_path.exists() and output_path.stat().st_size > 10000:
            size_kb = output_path.stat().st_size / 1024
            print(f"   ✅ Image saved ({size_kb:.0f} KB)")
            return output_path
            
    except Exception as e:
        print(f"   ⚠️  Image-gen error: {e}")
    
    # Fallback: Create gradient image with text
    print(f"   📝 Creating styled fallback image...")
    create_styled_fallback_image(startup_id)
    return output_path


def create_styled_fallback_image(startup_id: str):
    """Create a professional-looking fallback image"""
    output_path = IMAGES_DIR / f"{startup_id}_hero.png"
    name = STARTUPS[startup_id]["name"]
    domain = STARTUPS[startup_id]["domain"]
    
    # Color schemes for different startups
    colors = {
        "P1": ("#0a1628", "#1a365d", "#00E5FF"),  # Cyan for fusion
        "P2": ("#0a1628", "#1e293b", "#4da8da"),  # Blue for nuclear
        "P3": ("#0a1628", "#1a1a2e", "#10b981"),  # Green for battery
        "P4": ("#0a1628", "#1a2332", "#f59e0b"),  # Amber for grid
        "P5": ("#0a1628", "#132238", "#06b6d4"),  # Teal for hydrogen
        "P6": ("#0a1628", "#1a1a2e", "#ef4444"),  # Red for combustion
        "P7": ("#0a1628", "#180a28", "#a78bfa"),  # Purple for quantum
    }
    
    bg_start, bg_end, accent = colors.get(startup_id, ("#0a1628", "#1a365d", "#4da8da"))
    
    try:
        # Use Python PIL if available
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (1920, 1080), color=bg_start)
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background
        for y in range(1080):
            ratio = y / 1080
            r = int(int(bg_start[1:3], 16) * (1-ratio) + int(bg_end[1:3], 16) * ratio)
            g = int(int(bg_start[3:5], 16) * (1-ratio) + int(bg_end[3:5], 16) * ratio)
            b = int(int(bg_start[5:7], 16) * (1-ratio) + int(bg_end[5:7], 16) * ratio)
            draw.line([(0, y), (1920, y)], fill=(r, g, b))
        
        # Add decorative elements
        draw.rectangle([100, 100, 1820, 980], outline=accent, width=2)
        draw.rectangle([110, 110, 1810, 970], outline=accent + "40", width=1)
        
        # Try to use a nice font
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw text
        title_bbox = draw.textbbox((0, 0), name, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(((1920 - title_w) // 2, 400), name, fill=accent, font=title_font)
        
        domain_bbox = draw.textbbox((0, 0), domain, font=subtitle_font)
        domain_w = domain_bbox[2] - domain_bbox[0]
        draw.text(((1920 - domain_w) // 2, 520), domain, fill="#7a9bb8", font=subtitle_font)
        
        brand_text = "SciMSPT Venture Pipeline"
        brand_bbox = draw.textbbox((0, 0), brand_text, font=small_font)
        brand_w = brand_bbox[2] - brand_bbox[0]
        draw.text(((1920 - brand_w) // 2, 600), brand_text, fill="#4da8da", font=small_font)
        
        img.save(str(output_path))
        print(f"   ✅ Styled image created")
        
    except ImportError:
        # Fall back to ImageMagick or simple file
        try:
            cmd = [
                "convert", "-size", "1920x1080",
                f"gradient:{bg_start}-{bg_end}",
                "-stroke", accent, "-strokewidth", "2",
                "-draw", "rectangle 100,100,1820,980",
                "-fill", accent,
                "-font", "DejaVu-Sans-Bold",
                "-pointsize", "72",
                "-gravity", "center",
                "-annotate", "+0-50", name,
                "-fill", "#7a9bb8",
                "-pointsize", "32",
                "-annotate", "+0+40", domain,
                "-pointsize", "24",
                "-fill", "#4da8da",
                "-annotate", "+0+120", "SciMSPT Venture Pipeline",
                str(output_path)
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            print(f"   ✅ ImageMagick fallback created")
        except:
            output_path.touch()


def get_audio_duration(audio_path: Path) -> float:
    """Get audio duration using ffprobe"""
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(audio_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except:
        return 55.0


def create_video_clip(startup_id: str, audio_path: Path, image_path: Path) -> Path:
    """Create final video clip with ffmpeg"""
    startup = STARTUPS[startup_id]
    safe_name = startup["name"].replace(" ", "_")
    output_path = OUTPUT_DIR / f"{startup_id}_{safe_name}.mp4"
    
    print(f"🎬  Creating video for {startup['name']}...")
    
    duration = get_audio_duration(audio_path)
    fade_dur = min(2.0, duration * 0.03)
    
    # Simple but effective video creation
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-vf", f"fade=t=in:st=0:d={fade_dur},fade=t=out:st={duration-fade_dur}:d={fade_dur}",
        "-shortest",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if output_path.exists() and output_path.stat().st_size > 50000:
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Video created: {output_path.name} ({size_mb:.1f} MB, ~{duration:.0f}s)")
            return output_path
        else:
            print(f"   ⚠️  Video may be corrupted, checking...")
            
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  Timeout, trying faster settings...")
        cmd[cmd.index("-preset") + 1] = "ultrafast"
        cmd[cmd.index("-crf") + 1] = "28"
        subprocess.run(cmd, capture_output=True, timeout=300)
    
    return output_path


def main():
    """Main execution function"""
    print_header()
    
    print("🚀 Starting video clip generation for all 7 startups...\n")
    
    start_time = time.time()
    results = []
    
    for startup_id in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]:
        startup = STARTUPS[startup_id]
        
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Processing: {startup['name']}")
        print(f"Domain: {startup['domain']} | Tier: {startup['tier']}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            # Step 1: Generate narration audio
            audio_path = generate_tts_audio(startup_id, startup["narration"])
            
            # Step 2: Generate hero image  
            image_path = generate_image(startup_id, startup["image_prompt"])
            
            # Step 3: Create final video
            video_path = create_video_clip(startup_id, audio_path, image_path)
            
            success = video_path.exists() and video_path.stat().st_size > 50000
            results.append({
                "id": startup_id,
                "name": startup["name"],
                "success": success,
                "video": str(video_path.name) if success else None
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "id": startup_id,
                "name": startup["name"],
                "success": False,
                "error": str(e)
            })
        
        print()
    
    # Summary
    elapsed = time.time() - start_time
    successful = sum(1 for r in results if r["success"])
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    GENERATION COMPLETE                      ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Output: {OUTPUT_DIR}")
    print(f"║  Successful: {successful}/7 | Time: {elapsed:.0f}s")
    print("║                                                          ║")
    print("║  Voice: jam (British English Gentleman)                  ║")
    print("║  Duration: ~55-65 seconds each                           ║")
    print("║  Resolution: 1920x1080 Full HD                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # List generated files
    print("\n📁 Generated Videos:")
    video_files = sorted(OUTPUT_DIR.glob("*.mp4")) if OUTPUT_DIR.exists() else []
    if video_files:
        for vf in video_files:
            size_mb = vf.stat().st_size / (1024 * 1024)
            print(f"   🎬 {vf.name} ({size_mb:.1f} MB)")
    else:
        print("   Checking for partial outputs...")
        audio_files = sorted(AUDIO_DIR.glob("*.wav")) if AUDIO_DIR.exists() else []
        print(f"   🎙️ Audio files: {len(audio_files)}")
        image_files = sorted(IMAGES_DIR.glob("*.png")) if IMAGES_DIR.exists() else []
        print(f"   🎨 Image files: {len(image_files)}")
    
    # Save metadata
    metadata = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_time_seconds": round(elapsed, 1),
        "voice": "jam (British English Gentleman)",
        "duration_target_seconds": 60,
        "resolution": "1920x1080",
        "startups_processed": results
    }
    
    meta_path = OUTPUT_DIR / "metadata.json"
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"\n📋 Metadata: {meta_path}")


if __name__ == "__main__":
    main()
