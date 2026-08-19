#!/usr/bin/env python3
"""
SciMSPT Phase 3: Optimized Video Generation (Fast Mode)
=======================================================
Generates MP4 videos with TTS narration - optimized for speed.
Creates professional scientific explainer clips.
"""

import os
import sys
import json
import subprocess
import math
import tempfile
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Configuration
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
AUDIO_DIR = BASE_DIR / "audio"
STARTUPS_DIR = BASE_DIR / "startups"
RESEARCH_DIR = BASE_DIR / "research"
AI_REVIEW_DIR = BASE_DIR / "ai-review"

VIDEO_WIDTH = 1280  # Reduced for speed
VIDEO_HEIGHT = 720
FPS = 24  # Reduced for faster generation
DURATION = 30  # Shorter videos

COLORS = {
    'bg_deep': '#030810',
    'bg_primary': '#0a1628',
    'accent_cyan': '#00E5FF',
    'accent_purple': '#a78bfa',
    'accent_pink': '#f472b6',
    'accent_green': '#10b981',
    'accent_gold': '#f59e0b',
    'text_primary': '#e8f4fc',
    'text_secondary': '#94a3b8',
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

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

# Startup Data (simplified)
STARTUPS = [
    {
        "id": "quantum_therapeutics", "name": "Quantum Therapeutics",
        "logo": "Q", "stage": "Seed", 
        "tagline": "Quantum-accelerated drug discovery using VQE",
        "metrics": {"Validation": "94%", "Raised": "$4.2M", "Papers": "12"},
        "tags": ["Quantum Computing", "Drug Discovery"],
        "narration": "Quantum Therapeutics pioneers quantum-accelerated drug discovery. Their VQE platform achieves 40x speedup in molecular simulations, validated by 12 peer-reviewed papers. With 4.2 million in seed funding, they're making quantum computing practical for pharmaceutical research.",
        "primary_color": "#00E5FF"
    },
    {
        "id": "neurosynth_labs", "name": "NeuroSynth Labs",
        "logo": "N", "stage": "Series A",
        "tagline": "Neuromorphic computing with 100x efficiency gains",
        "metrics": {"Validation": "97%", "Raised": "$18M", "Papers": "28"},
        "tags": ["Neuromorphic", "AI Hardware"],
        "narration": "NeuroSynth Labs builds brain-inspired neuromorphic chips achieving 100x efficiency gains over GPUs. Their Series A raise of 18 million supports production of spiking neural network processors for edge AI inference applications.",
        "primary_color": "#a78bfa"
    },
    {
        "id": "solaris_materials", "name": "Solaris Materials",
        "logo": "S", "stage": "Series B",
        "tagline": "34% efficient perovskite tandem solar cells",
        "metrics": {"Validation": "99%", "Raised": "$45M", "Papers": "42"},
        "tags": ["Solar Energy", "Perovskite"],
        "narration": "Solaris Materials achieved record 34% efficiency with perovskite-silicon tandem solar cells. Their novel defect passivation solves the stability problem that has limited perovskite commercialization for a decade.",
        "primary_color": "#10b981"
    },
    {
        "id": "genomeforge", "name": "GenomeForge",
        "logo": "G", "stage": "Seed",
        "tagline": "AI-designed CRISPR guide RNAs",
        "metrics": {"Validation": "91%", "Raised": "$2.8M", "Papers": "19"},
        "tags": ["CRISPR", "Gene Therapy"],
        "narration": "GenomeForge combines AI with CRISPR gene editing to design precision therapeutics. Their transformer model predicts editing outcomes with 98% accuracy, targeting previously undruggable genetic diseases.",
        "primary_color": "#f59e0b"
    },
    {
        "id": "fusion_dynamics", "name": "Fusion Dynamics",
        "logo": "F", "stage": "Growth",
        "tagline": "ML-optimized compact stellarator reactors",
        "metrics": {"Validation": "96%", "Raised": "$120M", "Papers": "67"},
        "tags": ["Fusion Energy", "Plasma Physics"],
        "narration": "Fusion Dynamics develops compact stellarator fusion reactors using ML-optimized magnetic confinement. With 120 million raised, they're bringing practical nuclear fusion power closer to reality.",
        "primary_color": "#06b6d4"
    },
    {
        "id": "bionexus_ai", "name": "BioNexus AI",
        "logo": "B", "stage": "Series A",
        "tagline": "Biomedical foundation model for drug discovery",
        "metrics": {"Validation": "93%", "Raised": "$22M", "Papers": "35"},
        "tags": ["Foundation Models", "Bioinformatics"],
        "narration": "BioNexus AI trains multi-modal foundation models exclusively on biomedical literature. Their platform generates hypotheses and identifies drug targets with explainable AI reasoning.",
        "primary_color": "#ec4899"
    }
]

# Research Papers Data
PAPERS = [
    {
        "id": "vqe_drug_discovery",
        "title": "Variational Quantum Eigensolvers for Drug Discovery",
        "authors": "Chen et al., MIT | arXiv:2401.08742",
        "domain": "Quantum Computing",
        "score": "94%",
        "citations": "34",
        "narration": "MIT's Chen team presents the most comprehensive VQE benchmark for pharmaceutical applications. Their 40x speedup in molecular energy calculations validates quantum computing's potential for drug discovery, with novel error mitigation techniques for near-term devices.",
        "primary_color": "#00E5FF"
    },
    {
        "id": "crispr_rna_design",
        "title": "CRISPR-Cas13 RNA Design Using Transformers",
        "authors": "Patel et al., Stanford | Nature Biotechnology",
        "domain": "Biotechnology",
        "score": "97%",
        "citations": "89",
        "narration": "Stanford's breakthrough transformer model designs CRISPR guide RNAs with 98% accuracy. This dramatically reduces off-target effects, accelerating safe gene therapy development for previously untreatable genetic diseases.",
        "primary_color": "#a78bfa"
    },
    {
        "id": "perovskite_solar",
        "title": "Perovskite Tandem Cells: 34% Efficiency Achievement",
        "authors": "Kim et al., NREL | Science Advances",
        "domain": "Energy",
        "score": "99%",
        "citations": "56",
        "narration": "NREL achieved record 34% efficiency with perovskite-silicon tandems using novel defect passivation. This breakthrough could reduce solar costs below 20 cents per watt, dramatically accelerating clean energy adoption.",
        "primary_color": "#10b981"
    },
    {
        "id": "neuromorphic_computing",
        "title": "Neuromorphic Computing for Edge AI Inference",
        "authors": "Rodriguez et al., Intel Labs | IEEE Micro",
        "domain": "Neuroscience",
        "score": "91%",
        "citations": "23",
        "narration": "Intel Labs demonstrates 100x energy efficiency gains with neuromorphic chips for edge AI. Their comprehensive benchmark validates spiking neural networks for production deployment in battery-constrained devices.",
        "primary_color": "#f59e0b"
    }
]

# AI Reviewers
REVIEWERS = [
    {
        "id": "dr_synthia_turing", "name": "Dr. Synthia Turing",
        "title": "Theoretical CS & Quantum Algorithms Expert",
        "avatar": "ST", "color": "#00E5FF",
        "focus": ["Algorithmic complexity", "Mathematical rigor", "Theoretical novelty"],
        "background": "Dr. Turing evaluates papers through computational complexity theory, identifying gaps between claims and proofs."
    },
    {
        "id": "prof_helix_bio", "name": "Prof. Helix Bio",
        "title": "Computational Biologist & Translational Medicine Expert",
        "avatar": "HB", "color": "#10b981",
        "focus": ["Biological plausibility", "Clinical translation", "Therapeutic impact"],
        "background": "Prof. Bio bridges computational innovation and bedside medicine, assessing real-world therapeutic applicability."
    },
    {
        "id": "architect_nova", "name": "Architect Nova",
        "title": "Systems Engineer & ML Infrastructure Specialist",
        "avatar": "AN", "color": "#f59e0b",
        "focus": ["Implementation feasibility", "Scalability", "Production readiness"],
        "background": "Nova evaluates research through the lens of engineering practicality and deployment at scale."
    }
]

def create_frame(title, content_lines, color, frame_num=0, total_frames=100, is_title=False):
    """Generate a single video frame."""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), hex_to_rgb(COLORS['bg_deep']))
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(VIDEO_HEIGHT):
        r = int(hex_to_rgb(COLORS['bg_deep'])[0] * (1-y/VIDEO_HEIGHT) + hex_to_rgb(COLORS['bg_primary'])[0] * y/VIDEO_HEIGHT)
        g = int(hex_to_rgb(COLORS['bg_deep'])[1] * (1-y/VIDEO_HEIGHT) + hex_to_rgb(COLORS['bg_primary'])[1] * y/VIDEO_HEIGHT)
        b = int(hex_to_rgb(COLORS['bg_deep'])[2] * (1-y/VIDEO_HEIGHT) + hex_to_rgb(COLORS['bg_primary'])[2] * y/VIDEO_HEIGHT)
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=(r, g, b))
    
    # Decorative elements
    rgb_color = hex_to_rgb(color)
    
    # Animated glow
    glow = int(abs(math.sin(frame_num * 0.08)) * 40)
    
    if is_title:
        # Title card style
        font_title = get_font(48, bold=True)
        font_sub = get_font(24)
        
        # Center box
        box_padding = 60
        draw.rounded_rectangle(
            [box_padding, VIDEO_HEIGHT//2 - 100, VIDEO_WIDTH-box_padding, VIDEO_HEIGHT//2 + 100],
            radius=20,
            fill=(*hex_to_rgb(COLORS['bg_primary']), 230),
            outline=(*rgb_color, glow + 50),
            width=3
        )
        
        # Title text (wrapped)
        words = title.split()
        lines = []
        current = []
        for w in words:
            current.append(w)
            if len(current) > 5:
                lines.append(' '.join(current))
                current = []
        if current:
            lines.append(' '.join(current))
        
        font_large = get_font(40, bold=True)
        y_pos = VIDEO_HEIGHT // 2 - 60
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_large)
            x = (VIDEO_WIDTH - bbox[2] + bbox[0]) // 2
            draw.text((x, y_pos), line, fill=rgb_color, font=font_large)
            y_pos += 55
        
        # Subtitle
        if content_lines:
            sub_text = content_lines[0] if content_lines else ""
            bbox = draw.textbbox((0, 0), sub_text[:80], font=font_sub)
            x = (VIDEO_WIDTH - bbox[2] + bbox[0]) // 2
            draw.text((x, y_pos + 20), sub_text[:80], fill=hex_to_rgb(COLORS['text_secondary']), font=font_sub)
    else:
        # Content card style
        font_content = get_font(26)
        font_header = get_font(32, bold=True)
        
        # Header bar
        draw.rectangle([0, 0, VIDEO_WIDTH, 80], fill=(*rgb_color, 30))
        draw.text((40, 25), title if title else "Details", fill=rgb_color, font=font_header)
        
        # Content area
        y_pos = 110
        for line in content_lines[:12]:
            if line.startswith("## "):
                draw.text((40, y_pos), line[3:], fill=rgb_color, font=font_header)
                y_pos += 45
            elif line.startswith("- "):
                draw.ellipse([40, y_pos+8, 52, y_pos+20], fill=rgb_color)
                draw.text((65, y_pos), line[2:], fill=hex_to_rgb(COLORS['text_primary']), font=font_content)
                y_pos += 40
            else:
                # Word wrap
                words = line.split()
                current = []
                for w in words:
                    current.append(w)
                    test = ' '.join(current)
                    if draw.textlength(test, font=font_content) > VIDEO_WIDTH - 100:
                        current.pop()
                        draw.text((40, y_pos), ' '.join(current), fill=hex_to_rgb(COLORS['text_primary']), font=font_content)
                        y_pos += 38
                        current = [w]
                if current:
                    draw.text((40, y_pos), ' '.join(current), fill=hex_to_rgb(COLORS['text_primary']), font=font_content)
                    y_pos += 38
    
    # Progress bar
    progress = frame_num / max(total_frames, 1)
    draw.rectangle([0, VIDEO_HEIGHT-4, int(VIDEO_WIDTH * progress), VIDEO_HEIGHT], fill=rgb_color)
    
    return img

def generate_tts(text, output_path, voice="en-US-GuyNeural"):
    """Generate TTS audio using edge-tts."""
    try:
        cmd = ["edge-tts", "--voice", voice, "--text", text, "--write-media", str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        return result.returncode == 0
    except Exception as e:
        print(f"TTS error: {e}")
        return False

def create_video(frames_data, audio_path, output_path, title="Video"):
    """Create video from frames data list."""
    print(f"Creating: {title}")
    
    total_frames = len(frames_data)
    
    with tempfile.TemporaryDirectory() as frame_dir:
        # Generate frames
        for i, (frame_type, title_text, content, color) in enumerate(frames_data):
            frame = create_frame(title_text, content, color, i, total_frames, is_title=(frame_type=='title'))
            frame.save(Path(frame_dir) / f"frame_{i:04d}.png")
            
            if (i+1) % 100 == 0:
                print(f"  Frame {i+1}/{total_frames}")
        
        # Ensure audio exists
        if not Path(audio_path).exists():
            # Create silent audio
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", str(DURATION), "-acodec", "pcm_s16le", str(audio_path)
            ], capture_output=True)
        
        # Assemble with FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", f"{frame_dir}/frame_%04d.png",
            "-i", str(audio_path),
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            size_mb = Path(output_path).stat().st_size / (1024*1024)
            print(f"✓ {title} created ({size_mb:.1f} MB)")
            return True
        else:
            print(f"✗ FFmpeg error: {result.stderr[:200]}")
            return False

def generate_startup_video(startup, output_dir):
    """Generate startup explainer video."""
    output_path = Path(output_dir) / f"{startup['id']}_explainer.mp4"
    audio_path = AUDIO_DIR / f"{startup['id']}_narration.wav"
    color = startup.get('primary_color', COLORS['accent_cyan'])
    
    # Generate narration
    print(f"\nGenerating TTS for: {startup['name']}")
    generate_tts(startup['narration'], audio_path)
    
    # Build frames sequence
    frames = []
    
    # Intro (25%)
    intro_frames = max(20, FPS * 8)
    for i in range(intro_frames):
        frames.append(('title', startup['name'], [startup['tagline'], f"{startup['stage']} Stage"], color))
    
    # Content sections
    narration_parts = startup['narration'].split('. ')
    content_frames_per_part = max(15, (FPS * DURATION - intro_frames) // max(len(narration_parts), 1) // 2)
    
    for part in narration_parts:
        if part.strip():
            lines = [f"- {part.strip()}"]
            for _ in range(min(content_frames_per_part, 30)):
                frames.append(('content', startup['name'], lines, color))
    
    # Metrics (15%)
    metrics = startup.get('metrics', {})
    metrics_lines = [f"## Key Metrics"] + [f"- {k}: {v}" for k, v in metrics.items()]
    for _ in range(max(15, FPS * 5)):
        frames.append(('content', startup['name'], metrics_lines, color))
    
    # Outro
    for _ in range(max(10, FPS * 3)):
        frames.append(('title', startup['name'], ["Learn more about this innovative company"], color))
    
    return create_video(frames, audio_path, output_path, f"Startup: {startup['name']}")

def generate_paper_video(paper, output_dir):
    """Generate research paper explainer video."""
    output_path = Path(output_dir) / f"{paper['id']}_explainer.mp4"
    audio_path = AUDIO_DIR / f"{paper['id']}_narration.wav"
    color = paper.get('primary_color', COLORS['accent_cyan'])
    
    print(f"\nGenerating TTS for: {paper['title'][:40]}...")
    generate_tts(paper['narration'], audio_path, voice="en-US-JennyNeural")
    
    frames = []
    
    # Title intro
    intro_frames = max(25, FPS * 8)
    for i in range(intro_frames):
        frames.append(('title', paper['title'], [paper['authors'], paper['domain']], color))
    
    # Content
    parts = paper['narration'].split('. ')
    content_frames = max(15, (FPS * DURATION - intro_frames) // max(len(parts), 1) // 2)
    
    for part in parts:
        if part.strip():
            for _ in range(min(content_frames, 25)):
                frames.append(('content', paper['title'][:50], [f"- {part.strip()}"], color))
    
    # Stats
    stats_lines = [
        "## Paper Metrics",
        f"- Domain: {paper['domain']}",
        f"- Validation Score: {paper['score']}",
        f"- Citations: {paper['citations']}"
    ]
    for _ in range(max(15, FPS * 5)):
        frames.append(('content', "Paper Analysis", stats_lines, color))
    
    return create_video(frames, audio_path, output_path, f"Paper: {paper['title'][:40]}")

def generate_reviewer_video(reviewer, output_dir):
    """Generate AI reviewer introduction video."""
    output_path = Path(output_dir) / f"{reviewer['id']}_intro.mp4"
    audio_path = AUDIO_DIR / f"{reviewer['id']}_intro.wav"
    color = reviewer.get('color', COLORS['accent_cyan'])
    
    script = f"Meet {reviewer['name']}, {reviewer['title']}. {reviewer['background']} Focus areas include: {'; '.join(reviewer['focus'][:3])}."
    
    voices = {"dr_synthia_turing": "en-US-AriaNeural", "prof_helix_bio": "en-US-JennyNeural", "architect_nova": "en-US-GuyNeural"}
    
    print(f"\nGenerating TTS for: {reviewer['name']}")
    generate_tts(script, audio_path, voice=voices.get(reviewer['id'], "en-US-AriaNeural"))
    
    frames = []
    total = FPS * 25  # 25 seconds
    
    for i in range(total):
        content = [
            f"## {reviewer['title']}",
            f"- {reviewer['background']}",
            "## Review Focus",
        ] + [f"- {f}" for f in reviewer['focus']]
        frames.append(('title', reviewer['name'], content, color))
    
    return create_video(frames, audio_path, output_path, f"Reviewer: {reviewer['name']}")

def main():
    print("="*60)
    print("SciMSPT Phase 3: Fast Video Generation")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Create directories
    for d in [OUTPUT_DIR, AUDIO_DIR, STARTUPS_DIR, RESEARCH_DIR, AI_REVIEW_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    results = {'startups': [], 'papers': [], 'reviewers': []}
    
    # Generate ALL startup videos
    print("\n[1/3] Generating Startup Videos...")
    for startup in STARTUPS:  # Generate all 6
        try:
            output_path = Path(STARTUPS_DIR) / f"{startup['id']}_explainer.mp4"
            # Skip if already exists
            if output_path.exists():
                print(f"  Skipping {startup['name']} (already exists)")
                results['startups'].append(startup['id'])
                continue
            if generate_startup_video(startup, STARTUPS_DIR):
                results['startups'].append(startup['id'])
        except Exception as e:
            print(f"Error: {e}")
    
    # Generate ALL paper videos
    print("\n[2/3] Generating Research Paper Videos...")
    for paper in PAPERS:  # Generate all 4
        try:
            output_path = Path(RESEARCH_DIR) / f"{paper['id']}_explainer.mp4"
            # Skip if already exists
            if output_path.exists():
                print(f"  Skipping {paper['title'][:30]}... (already exists)")
                results['papers'].append(paper['id'])
                continue
            if generate_paper_video(paper, RESEARCH_DIR):
                results['papers'].append(paper['id'])
        except Exception as e:
            print(f"Error: {e}")
    
    # Generate reviewer intros
    print("\n[3/3] Generating AI Reviewer Intros...")
    for reviewer in REVIEWERS:
        try:
            output_path = Path(AI_REVIEW_DIR) / f"{reviewer['id']}_intro.mp4"
            # Skip if already exists
            if output_path.exists():
                print(f"  Skipping {reviewer['name']} (already exists)")
                results['reviewers'].append(reviewer['id'])
                continue
            if generate_reviewer_video(reviewer, AI_REVIEW_DIR):
                results['reviewers'].append(reviewer['id'])
        except Exception as e:
            print(f"Error: {e}")
    
    # Save metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'results': results,
        'videos': {
            'startups': [str(STARTUPS_DIR / f"{s['id']}_explainer.mp4") for s in STARTUPS if s['id'] in results['startups']],
            'papers': [str(RESEARCH_DIR / f"{p['id']}_explainer.mp4") for p in PAPERS if p['id'] in results['papers']],
            'reviewers': [str(AI_REVIEW_DIR / f"{r['id']}_intro.mp4") for r in REVIEWERS if r['id'] in results['reviewers']]
        }
    }
    
    with open(OUTPUT_DIR / "phase3_fast_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print(f"Startups: {len(results['startups'])} videos")
    print(f"Papers: {len(results['papers'])} videos")
    print(f"Reviewers: {len(results['reviewers'])} videos")
    print("="*60)
    
    return results

if __name__ == "__main__":
    main()
