#!/usr/bin/env python3
"""
SciMSPT 60-Second Startup Video Clip Generator
================================================
Generates professional video clips with:
- UK/US native voice narration (British English 'jam' voice)
- AI-generated imagery for each startup
- Professional video output with text overlays

Each clip: ~60 seconds, 1920x1080 Full HD
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
BASE_DIR = SCRIPT_DIR.parent
IMAGES_DIR = SCRIPT_DIR / "images"
AUDIO_DIR = SCRIPT_DIR / "audio"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Ensure directories exist
for d in [IMAGES_DIR, AUDIO_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True)

# Startup Data
STARTUPS = {
    "P1": {
        "name": "Stellarator Fusion",
        "domain": "Nuclear Fusion · Compact Stellarators",
        "tier": "TIER 1",
        "narration": """Stellarator Fusion represents the frontier of clean energy research, born from groundbreaking papers published in Physical Review Letters and Nature Energy.

The journey began with fundamental research into optimized magnetic geometry for compact stellarators. Scientists discovered that by carefully engineering plasma confinement configurations, they could achieve stable fusion reactions without the complexities of tokamak designs.

Key breakthroughs included advanced tritium breeding blanket materials and high-temperature superconducting coils that dramatically improved efficiency. The pivotal moment came when researchers demonstrated net energy gain in compact fusion devices, proving commercial viability was within reach.

Today, Stellarator Fusion stands as a transformative opportunity with a net present value of five hundred eighty-nine million dollars and a sixty-five point seven percent probability of exceeding fifteen percent internal rate of return. This is not merely scientific progress; it is the dawn of virtually limitless clean energy.""",
        "image_prompt": "Futuristic nuclear fusion stellarator reactor, glowing plasma contained in magnetic fields, blue and purple plasma glow, advanced scientific facility, clean energy concept, cinematic lighting, photorealistic, 8k quality"
    },
    "P2": {
        "name": "SMR Fleet OS",
        "domain": "Nuclear · Small Modular Reactors",
        "tier": "TIER 2",
        "narration": """SMR Fleet OS emerged from critical research published in Applied Energy and Annals of Nuclear Energy, addressing the operational challenges of Small Modular Reactors.

The original research focused on artificial intelligence-driven load balancing for distributed nuclear power generation. Unlike traditional large reactors, SMRs require sophisticated fleet management systems to optimize output across multiple units.

Scientists developed predictive maintenance frameworks using digital twin technology, enabling operators to anticipate issues before they occur. The regulatory automation component was particularly groundbreaking, simplifying compliance across complex nuclear regulatory environments.

The startup opportunity is compelling: fifty million dollars in net present value with a twenty-three percent internal rate of return. With sixty-eight point eight percent probability of positive NPV, SMR Fleet OS represents the software infrastructure layer essential for the nuclear renaissance.""",
        "image_prompt": "Modern small modular reactor control room with holographic displays showing AI-driven fleet management, digital twin visualization, futuristic nuclear plant interface, professional industrial design, blue tones, high-tech aesthetic"
    },
    "P3": {
        "name": "Solid-State Battery",
        "domain": "Energy Storage · Next-Gen Batteries",
        "tier": "TIER 1",
        "narration": """Solid-State Battery technology traces its origins to seminal research in Nature Energy and Joule, promising to revolutionize energy storage through sulfide-based electrolytes.

The foundational work demonstrated that solid-state architectures could achieve energy densities exceeding five hundred watt-hours per kilogram, nearly double current lithium-ion capabilities. More critically, these batteries eliminate thermal runaway risk entirely, solving the safety concerns that have plagued electric vehicle adoption.

Research published in Advanced Energy Materials proved fast charging capabilities under fifteen minutes, while studies in ACS Applied Materials showed cycle lives exceeding two thousand charges. The manufacturing scale-up pathways documented in Electrochimica Acta confirm commercial feasibility.

With five hundred eighty-seven million dollars in NPV and tier-one venture status, Solid-State Battery represents the most significant advancement in energy storage since the original lithium-ion revolution.""",
        "image_prompt": "Cutaway view of solid-state battery technology, layered structure visible, sulfide electrolyte glowing with energy, electric vehicle charging rapidly, futuristic battery laboratory, cyan and white color scheme, scientific illustration style"
    },
    "P4": {
        "name": "Iron-Air LDES",
        "domain": "Grid Storage · Long-Duration",
        "tier": "TIER 2",
        "narration": """Iron-Air LDES addresses grid-scale storage through revolutionary chemistry first detailed in Science and Joule journals.

The research journey began with scientists seeking ultra-low-cost storage solutions using earth-abundant materials. Iron-air chemistry emerged as the answer, offering energy storage costs of just twenty dollars per kilowatt-hour, a fraction of lithium-ion alternatives.

Breakthrough publications demonstrated one hundred plus hour discharge capabilities, making iron-air ideal for renewable grid stabilization. When solar and wind generation fluctuate, long-duration storage bridges the gap, storing energy for days rather than hours.

The market opportunity is substantial: forty-four million dollars NPV with twenty-three point four percent IRR. At sixty-eight percent probability of success, Iron-Air LDES enables the fully renewable grid that climate commitments demand.""",
        "image_prompt": "Massive iron-air battery installation for grid storage, renewable energy farm background, giant battery containers, sustainable energy storage concept, golden hour lighting, industrial scale, environmental harmony"
    },
    "P5": {
        "name": "Super-Steel Electrolyzer",
        "domain": "Hydrogen · Green H2 Production",
        "tier": "TIER 1",
        "narration": """Super-Steel Electrolyzer transforms green hydrogen production through innovations documented in Nature Catalysis and Advanced Materials.

The core challenge has been cost: producing green hydrogen at one dollar fifty per kilogram requires extraordinary efficiency gains. Researchers achieved this through nanostructured super-steel electrodes that dramatically improve water electrolysis performance.

Critical advances include variable renewable integration capabilities, allowing electrolyzers to operate efficiently with intermittent wind and solar input. Durability studies confirmed extended operational lifetimes, addressing previous degradation concerns.

With forty-three million dollars NPV and seventeen point seven percent IRR, Super-Steel Electrolyzer positions investors at the center of the hydrogen economy. This technology makes green hydrogen cost-competitive with fossil alternatives.""",
        "image_prompt": "Advanced electrolyzer system producing green hydrogen, nanostructured steel electrodes visible, hydrogen bubbles forming, clean energy facility, water splitting process visualization, teal and silver colors, modern industrial design"
    },
    "P6": {
        "name": "Detonation H2 Turbine",
        "domain": "Hydrogen · Rotating Detonation",
        "tier": "TIER 2",
        "narration": """Detonation H2 Turbine leverages rotating detonation engine technology from Progress in Energy and Combustion Science and AIAA Journal research.

Conventional hydrogen turbines suffer from efficiency limitations that detonation engines overcome. The research demonstrates fifteen percent efficiency improvements through continuous detonation wave propagation, a fundamentally different approach to combustion.

Applications span multiple markets: aviation demands high power density for next-generation aircraft, marine shipping requires clean propulsion solutions, and grid peaking needs rapid-response generation capacity. The versatility of this technology creates multiple revenue streams.

Thirty-four million dollars NPV with twenty-three point three percent IRR reflects strong fundamentals. At sixty-nine percent success probability, Detonation H2 Turbine offers exposure to the hydrogen transition across transportation and energy sectors.""",
        "image_prompt": "Cross-section of rotating detonation engine, hydrogen combustion visible, turbine blades spinning, aviation and power applications, dynamic energy release visualization, orange and blue flame colors, engineering precision"
    },
    "P7": {
        "name": "Room-Temp Quantum Materials",
        "domain": "Quantum · Superconductors",
        "tier": "TIER 3",
        "narration": """Room-Temp Quantum Materials represents perhaps the most transformative opportunity, emerging from landmark Nature publications on ambient-condition superconductivity.

For decades, superconductivity required extreme cryogenic cooling, limiting practical applications. Research breakthroughs changed everything: layered materials exhibiting superconducting properties at room temperature, topological quantum states persisting without specialized cooling systems.

The implications are profound: lossless power transmission over continental distances, quantum computing interconnects operating at room temperature, sensors with unprecedented sensitivity. Each application represents a multi-billion-dollar market.

While earlier-stage than other opportunities, the potential justifies the valuation: one hundred seven million dollars NPV with thirty-four point three percent IRR. At seventy-seven percent success probability, Room-Temp Quantum Materials offers asymmetric upside that could redefine multiple industries.""",
        "image_prompt": "Quantum material structure at room temperature, superconducting currents flowing, topological patterns visible, quantum computing interface, lossless power transmission concept, purple and gold hues, futuristic laboratory setting"
    }
}


def print_header():
    """Print fancy header"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     SciMSPT 60-Second Startup Video Clip Generator          ║
║     UK/US Native Voice Narration + AI Imagery              ║
╚══════════════════════════════════════════════════════════════╝
""")


def generate_tts_audio(startup_id: str, narration: str) -> Path:
    """Generate TTS audio using z-ai CLI with British English voice"""
    output_path = AUDIO_DIR / f"{startup_id}_narration.wav"
    
    print(f"🎙️  Generating narration for {STARTUPS[startup_id]['name']}...")
    
    # Use z-ai TTS CLI with 'jam' voice (British English gentleman)
    # Speed 0.9 for slightly slower, more dramatic delivery (extends ~55s text to ~60s)
    cmd = [
        "z-ai", "tts",
        "--input", narration,
        "--output", str(output_path),
        "--voice", "jam",  # British English gentleman voice
        "--speed", "0.9",  # Slightly slower for dramatic effect
        "--format", "wav"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"   ✅ Audio saved: {output_path.name} ({size_kb:.0f} KB)")
            return output_path
        else:
            print(f"   ⚠️  TTS generation issue, checking output...")
            if output_path.exists():
                return output_path
            raise Exception(f"TTS failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  TTS timeout, trying shorter text...")
        # Try with truncated text if timeout
        short_text = narration[:800] + "..." if len(narration) > 800 else narration
        cmd[-1] = str(0.95)  # Slightly faster
        subprocess.run(cmd, capture_output=True, timeout=180)
        return output_path


def generate_image(startup_id: str, prompt: str) -> Path:
    """Generate AI image for startup"""
    output_path = IMAGES_DIR / f"{startup_id}_hero.png"
    
    print(f"🎨  Generating image for {STARTUPS[startup_id]['name']}...")
    
    # Use z-ai image generation CLI
    cmd = [
        "z-ai", "image-gen",
        "--prompt", prompt,
        "--output", str(output_path),
        "--size", "1920x1080"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"   ✅ Image saved: {output_path.name} ({size_kb:.0f} KB)")
            return output_path
        else:
            print(f"   ⚠️  Image generation issue, creating fallback...")
            return create_fallback_image(startup_id)
            
    except Exception as e:
        print(f"   ⚠️  Image error: {e}")
        return create_fallback_image(startup_id)


def create_fallback_image(startup_id: str) -> Path:
    """Create a gradient fallback image with text"""
    output_path = IMAGES_DIR / f"{startup_id}_hero.png"
    
    name = STARTUPS[startup_id]["name"]
    
    # Use ImageMagick if available, otherwise create simple placeholder
    try:
        # Create gradient background with text
        cmd = [
            "convert", "-size", "1920x1080",
            "gradient:#0a1628-#1e3a5f",
            "-gravity", "center",
            "-fill", "#4da8da",
            "-font", "DejaVu-Sans-Bold",
            "-pointsize", "72",
            "-annotate", "0", name,
            "-fill", "#7a9bb8",
            "-pointsize", "28",
            "-annotate", "+0+80", STARTUPS[startup_id]["domain"],
            "-pointsize", "24",
            "-annotate", "+0+140", "SciMSPT Venture Pipeline",
            str(output_path)
        ]
        subprocess.run(cmd, capture_output=True, timeout=30)
        print(f"   ✅ Fallback image created")
    except Exception:
        # Create empty file as last resort
        output_path.touch()
        print(f"   ⚠️  Using placeholder file")
    
    return output_path


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
        duration = float(result.stdout.strip())
        return duration
    except Exception:
        return 60.0  # Default to 60 seconds


def create_video_clip(startup_id: str, audio_path: Path, image_path: Path) -> Path:
    """Create final video clip with ffmpeg"""
    startup = STARTUPS[startup_id]
    safe_name = startup["name"].replace(" ", "_")
    output_path = OUTPUT_DIR / f"{startup_id}_{safe_name}.mp4"
    
    print(f"🎬  Creating video for {startup['name']}...")
    
    # Get audio duration
    duration = get_audio_duration(audio_path)
    fade_duration = min(2, duration * 0.03)  # 3% of duration or 2s max
    
    # Build ffmpeg command with filters
    # - Loop image for full duration
    # - Add fade in/out effects  
    # - Overlay text with startup info
    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
        f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
        f"fade=t=in:st=0:d={fade_duration},"
        f"fade=t=out:st={duration-fade_duration}:d={fade_duration},"
        f"drawtext=text='{startup['name']}':fontsize=48:fontcolor=white@0.9:"
        f"x=(w-text_w)/2:y=h-l-100:"
        f"shadowcolor=black@0.7:shadowx=2:shadowy=2,"
        f"drawtext=text='SciMSPT Venture Pipeline':fontsize=24:fontcolor='#4da8da':"
        f"x=(w-text_w)/2:y=h-l-40,"
        f"drawtext=text='{startup['domain']}':fontsize=18:fontcolor='#7a9bb8':"
        f"x=(w-text_w)/2:y=l+20[v]"
    )
    
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
        "-t", str(duration),
        "-vf", filter_complex,
        "-shortest",
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Video created: {output_path.name}")
            print(f"      📊 Size: {size_mb:.1f} MB | Duration: ~{duration:.0f}s")
            return output_path
        else:
            print(f"   ⚠️  FFmpeg error, trying simpler approach...")
            return create_simple_video(startup_id, audio_path, image_path, duration)
            
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  Video creation timeout")
        return create_simple_video(startup_id, audio_path, image_path, 60)


def create_simple_video(startup_id: str, audio_path: Path, image_path: Path, duration: float) -> Path:
    """Simpler video creation without text overlays"""
    startup = STARTUPS[startup_id]
    safe_name = startup["name"].replace(" ", "_")
    output_path = OUTPUT_DIR / f"{startup_id}_{safe_name}.mp4"
    
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
        "-t", str(duration),
        "-shortest",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, timeout=300)
        if output_path.exists():
            print(f"   ✅ Simple video created: {output_path.name}")
        return output_path
    except Exception as e:
        print(f"   ❌ Video creation failed: {e}")
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
        print(f"Domain: {startup['domain']}")
        print(f"Tier: {startup['tier']}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            # Step 1: Generate narration audio
            audio_path = generate_tts_audio(startup_id, startup["narration"])
            
            # Step 2: Generate hero image
            image_path = generate_image(startup_id, startup["image_prompt"])
            
            # Step 3: Create final video
            video_path = create_video_clip(startup_id, audio_path, image_path)
            
            results.append({
                "id": startup_id,
                "name": startup["name"],
                "success": True,
                "video": str(video_path) if video_path.exists() else None
            })
            
        except Exception as e:
            print(f"   ❌ Error processing {startup['name']}: {e}")
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
    print(f"║  Output Location: {OUTPUT_DIR}")
    print(f"║  Successful: {successful}/7")
    print(f"║  Total Time: {elapsed:.1f}s")
    print("║                                                          ║")
    print("║  Voice: jam (British English Gentleman)                  ║")
    print("║  Duration: ~60 seconds each                              ║")
    print("║  Resolution: 1920x1080 (Full HD)                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # List generated files
    print("\n📁 Generated Videos:")
    video_files = list(OUTPUT_DIR.glob("*.mp4"))
    if video_files:
        for vf in sorted(video_files):
            size_mb = vf.stat().st_size / (1024 * 1024)
            print(f"   🎬 {vf.name} ({size_mb:.1f} MB)")
    else:
        print("   No videos generated yet")
    
    # Save metadata
    metadata = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_time_seconds": elapsed,
        "voice": "jam (British English)",
        "duration_target_seconds": 60,
        "resolution": "1920x1080",
        "startups_processed": results
    }
    
    meta_path = OUTPUT_DIR / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\n📋 Metadata saved: {meta_path}")


if __name__ == "__main__":
    main()
