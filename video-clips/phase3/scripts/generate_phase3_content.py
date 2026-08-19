#!/usr/bin/env python3
"""
SciMSPT Phase 3: Video Content Generation Pipeline
====================================================
Generates MP4 videos with TTS narration using:
- PIL/Pillow for frame generation
- edge-tts for professional voiceover
- FFmpeg for video assembly

Features:
- Startup-specific explainer clips (6 companies)
- Research paper explainer videos (4-5 breakthrough papers)
- AI Peer Review panel videos with 3 distinct personas
- Professional scientific visualization style (Nature/Cell/arXiv quality)
"""

import os
import sys
import json
import asyncio
import subprocess
import math
import random
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
AUDIO_DIR = BASE_DIR / "audio"
IMAGES_DIR = BASE_DIR / "images"
STARTUPS_DIR = BASE_DIR / "startups"
RESEARCH_DIR = BASE_DIR / "research"
AI_REVIEW_DIR = BASE_DIR / "ai-review"

# Video Configuration
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
DURATION = 60  # seconds per clip

# Color Palette (matching SciMSPT design system)
COLORS = {
    'bg_deep': '#030810',
    'bg_primary': '#0a1628',
    'bg_secondary': '#0d1f35',
    'accent_cyan': '#00E5FF',
    'accent_blue': '#4da8da',
    'accent_purple': '#a78bfa',
    'accent_pink': '#f472b6',
    'accent_green': '#10b981',
    'accent_gold': '#f59e0b',
    'text_primary': '#e8f4fc',
    'text_secondary': '#94a3b8',
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# ============================================================================
# STARTUP DATA (6 companies from startups.html)
# ============================================================================

STARTUPS_DATA = [
    {
        "id": "quantum_therapeutics",
        "name": "Quantum Therapeutics",
        "logo": "Q",
        "stage": "Seed",
        "stage_color": COLORS['accent_cyan'],
        "tagline": "Quantum-accelerated drug discovery platform using variational quantum eigensolvers for molecular simulation at unprecedented accuracy.",
        "metrics": {"validation": "94%", "raised": "$4.2M", "papers": "12"},
        "tags": ["Quantum Computing", "Drug Discovery", "VQE", "Biotech"],
        "narration": """
            Welcome to Quantum Therapeutics, a seed-stage pioneer revolutionizing pharmaceutical research 
            through quantum computing. Their platform leverages Variational Quantum Eigensolvers to simulate 
            molecular interactions at unprecedented accuracy, achieving a remarkable 94% validation score 
            against experimental data.
            
            With 4.2 million dollars in funding and backing from 12 peer-reviewed papers, Quantum Therapeutics 
            is addressing one of drug discovery's biggest bottlenecks: accurately predicting how potential 
            drug molecules interact with biological targets.
            
            Their quantum approach offers 40x speedup in ground state energy calculations for drug-like molecules, 
            potentially compressing years of traditional computational chemistry into days. This could dramatically 
            accelerate the discovery of treatments for previously undruggable diseases.
            
            Key differentiators include their proprietary error mitigation techniques for near-term quantum devices 
            and hybrid classical-quantum algorithms optimized for pharmaceutical applications. Watch this space—
            quantum drug discovery is no longer science fiction.
        """,
        "visual_theme": {
            "primary": "#00E5FF",
            "secondary": "#a78bfa",
            "pattern": "quantum_orbital",
            "icons": ["atom", "dna", "pill", "brain"]
        }
    },
    {
        "id": "neurosynth_labs",
        "name": "NeuroSynth Labs",
        "logo": "N",
        "stage": "Series A",
        "stage_color": COLORS['accent_purple'],
        "tagline": "Neuromorphic computing hardware inspired by biological neural networks, achieving 100x efficiency gains for AI inference workloads.",
        "metrics": {"validation": "97%", "raised": "$18M", "papers": "28"},
        "tags": ["Neuromorphic", "AI Hardware", "Edge Computing"],
        "narration": """
            Meet NeuroSynth Labs, a Series A powerhouse redefining the boundaries of artificial intelligence hardware. 
            Inspired by the architecture of biological neural networks, their neuromorphic chips achieve extraordinary 
            100x efficiency gains compared to traditional GPUs for AI inference workloads.
            
            With an impressive 18 million dollars raised and validated by 28 research publications, NeuroSynth Labs 
            stands at the forefront of the neuromorphic computing revolution. Their technology addresses the growing 
            energy crisis in AI—data centers worldwide consume enormous power running inference workloads that 
            neuromorphic architectures could handle with a fraction of the energy.
            
            Their spiking neural network implementations demonstrate real-time processing capabilities at the edge, 
            enabling new classes of intelligent devices that can learn and adapt without cloud connectivity. This is 
            crucial for autonomous vehicles, robotics, and IoT applications where latency and power consumption 
            are critical constraints.
            
            The company's 97% validation score reflects rigorous benchmarking across multiple AI tasks including 
            image recognition, natural language processing, and sensory data analysis. As AI deployment scales 
            exponentially, NeuroSynth Labs offers a sustainable path forward.
        """,
        "visual_theme": {
            "primary": "#a78bfa",
            "secondary": "#ec4899",
            "pattern": "neural_network",
            "icons": ["brain", "chip", "lightning", "network"]
        }
    },
    {
        "id": "solaris_materials",
        "name": "Solaris Materials",
        "logo": "S",
        "stage": "Series B",
        "stage_color": COLORS['accent_pink'],
        "tagline": "Next-generation perovskite tandem solar cells achieving 34%+ conversion efficiency through novel defect passivation techniques.",
        "metrics": {"validation": "99%", "raised": "$45M", "papers": "42"},
        "tags": ["Solar Energy", "Perovskite", "CleanTech", "Materials"],
        "narration": """
            Solaris Materials represents the cutting edge of renewable energy innovation. This Series B company 
            has achieved what many thought impossible: perovskite tandem solar cells with over 34% conversion 
            efficiency, shattering previous records in photovoltaic performance.
            
            Backed by 45 million dollars in funding and an extraordinary portfolio of 42 research papers, Solaris 
            Materials has mastered novel defect passivation techniques that solve perovskite solar cells' biggest 
            challenge—stability. Their 99% validation score reflects reproducible results across independent labs.
            
            The significance cannot be overstated. Traditional silicon solar cells max out around 27% efficiency 
            in practice. Solaris Materials' tandem architecture stacks perovskite layers on silicon, capturing 
            broader spectrum sunlight. This could reduce the cost per watt below 20 cents, making solar 
            unequivocally the cheapest energy source globally.
            
            Their manufacturing process uses solution-based deposition compatible with existing fab lines, 
            meaning rapid scaling without building new infrastructure. With climate urgency accelerating, 
            Solaris Materials isn't just promising—it's essential.
        """,
        "visual_theme": {
            "primary": "#10b981",
            "secondary": "#06b6d4",
            "pattern": "solar_cells",
            "icons": ["sun", "solar_panel", "leaf", "energy"]
        }
    },
    {
        "id": "genomeforge",
        "name": "GenomeForge",
        "logo": "G",
        "stage": "Seed",
        "stage_color": COLORS['accent_gold'],
        "tagline": "CRISPR-based gene editing platform with AI-designed guide RNAs for precision therapeutics targeting previously undruggable diseases.",
        "metrics": {"validation": "91%", "raised": "$2.8M", "papers": "19"},
        "tags": ["CRISPR", "Gene Therapy", "AI/ML"],
        "narration": """
            GenomeForge is pioneering the next frontier of precision medicine. This seed-stage innovator combines 
            CRISPR gene editing with artificial intelligence to design guide RNAs that can target previously 
            undruggable genetic diseases with unprecedented precision.
            
            Despite modest early funding of 2.8 million dollars, GenomeForge's impact is amplified by 19 
            foundational papers demonstrating their AI model achieves 98% accuracy in predicting gene editing 
            outcomes. Their 91% validation score reflects successful in vitro and early animal studies.
            
            The problem they're solving is profound: many genetic diseases lack effective treatments because 
            targeting them risks off-target effects that could cause cancer or other harm. GenomeForge's 
            transformer-based AI analyzes millions of genomic sequences to design guide RNAs with maximal 
            on-target efficiency and minimal risk.
            
            Their platform targets rare genetic disorders first—conditions affecting small patient populations 
            that big pharma often ignores. By democratizing precision gene therapy design, GenomeForge could 
            bring hope to millions suffering from currently incurable genetic diseases.
        """,
        "visual_theme": {
            "primary": "#f59e0b",
            "secondary": "#ef4444",
            "pattern": "dna_helix",
            "icons": ["dna", "edit", "medical", "target"]
        }
    },
    {
        "id": "fusion_dynamics",
        "name": "Fusion Dynamics",
        "logo": "F",
        "stage": "Growth",
        "stage_color": COLORS['accent_blue'],
        "tagline": "Compact stellarator fusion reactor design using advanced magnetic confinement configurations derived from ML-optimized plasma physics.",
        "metrics": {"validation": "96%", "raised": "$120M", "papers": "67"},
        "tags": ["Fusion Energy", "Plasma Physics", "Stellarator", "Energy"],
        "narration": """
            Fusion Dynamics represents humanity's best bet for achieving practical nuclear fusion power. This 
            growth-stage company has raised an impressive 120 million dollars to develop compact stellarator 
            reactors that could finally deliver unlimited clean energy.
            
            What sets Fusion Dynamics apart is their machine learning approach to plasma physics. Traditional 
            reactor designs require massive, expensive tokamaks. Fusion Dynamics uses ML algorithms to optimize 
            magnetic confinement configurations, enabling smaller, cheaper stellarators that are easier to build 
            and maintain. Their 67 research papers document breakthrough advances in plasma stability.
            
            Their 96% validation score comes from partnerships with national laboratories where their designs 
            have been tested in plasma experiments. The results show confinement times approaching the threshold 
            needed for net energy gain—the elusive breakeven point that has eluded fusion researchers for decades.
            
            If successful, Fusion Dynamics' technology could provide baseload power that's cleaner than solar, 
            safer than fission, and more abundant than any fossil fuel. With climate deadlines looming, fusion 
            can't arrive soon enough—and Fusion Dynamics is making it happen.
        """,
        "visual_theme": {
            "primary": "#06b6d4",
            "secondary": "#3b82f6",
            "pattern": "fusion_plasma",
            "icons": ["atom", "zap", "gauge", "reactor"]
        }
    },
    {
        "id": "bionexus_ai",
        "name": "BioNexus AI",
        "logo": "B",
        "stage": "Series A",
        "stage_color": COLORS['accent_pink'],
        "tagline": "Multi-modal foundation model trained exclusively on biomedical literature, enabling hypothesis generation and drug target identification.",
        "metrics": {"validation": "93%", "raised": "$22M", "papers": "35"},
        "tags": ["Foundation Models", "Bioinformatics", "LLM", "Drug Discovery"],
        "narration": """
            BioNexus AI is building the foundation model for biology. While large language models have transformed 
            general AI, BioNexus focuses exclusively on biomedical literature—training their multi-modal model on 
            millions of papers, clinical trials, genomic datasets, and molecular structures.
            
            With 22 million dollars in Series A funding and 35 publications demonstrating capabilities, BioNexus 
            AI's 93% validation score reflects successful predictions later confirmed by wet lab experiments. 
            Their model doesn't just understand text—it reasons across chemical structures, protein sequences, 
            and clinical outcomes.
            
            The applications are transformative. BioNexus can generate novel hypotheses connecting seemingly unrelated 
            research findings, identify promising drug targets that humans might overlook, and predict adverse 
            drug interactions before clinical trials. Pharmaceutical companies are already piloting the platform 
            for lead optimization.
            
            What makes BioNexus special is their reasoning approach. Unlike black-box AI, their model provides 
            explainable citations for every prediction, letting scientists verify and trust the outputs. In an 
            field where accuracy literally saves lives, this transparency is invaluable.
        """,
        "visual_theme": {
            "primary": "#ec4899",
            "secondary": "#8b5cf6",
            "pattern": "bio_network",
            "icons": ["database", "microscope", "link", "chart"]
        }
    }
]

# ============================================================================
# RESEARCH PAPERS DATA (breakthrough papers for video content)
# ============================================================================

RESEARCH_PAPERS_DATA = [
    {
        "id": "vqe_drug_discovery",
        "title": "Variational Quantum Eigensolvers for Drug Discovery: A Comprehensive Benchmark",
        "authors": "Chen et al., MIT",
        "venue": "arXiv:2401.08742",
        "domain": "Quantum Computing",
        "domain_color": COLORS['accent_cyan'],
        "date": "2024.01.15",
        "views": "2.4K",
        "citations": "34",
        "score": "94%",
        "abstract": "We present a systematic evaluation of VQE algorithms applied to molecular simulation tasks relevant to pharmaceutical research. Our results demonstrate 40x speedup in ground state energy calculations for drug-like molecules...",
        "narration": """
            This groundbreaking paper from MIT's Chen team represents a pivotal moment in quantum computing for 
            pharmaceutical research. They present the most comprehensive benchmark to date of Variational Quantum 
            Eigensolver algorithms applied to real-world drug discovery problems.
            
            The key finding—a 40x speedup in ground state energy calculations for drug-like molecules—addresses 
            the central bottleneck in computational drug discovery. Traditional methods require supercomputing 
            clusters running for weeks to simulate how potential drug molecules interact with target proteins. 
            VQE approaches could reduce this to hours.
            
            What makes this work significant is its rigor. The team tested across multiple molecule classes, 
            comparing against state-of-the-art classical methods. They also developed novel error mitigation 
            techniques that make VQE practical on today's noisy intermediate-scale quantum devices.
            
            For the pharmaceutical industry, this research validates the quantum computing investment thesis. 
            We're likely 3-5 years from production quantum drug discovery systems, but this paper proves the 
            fundamental approach works. Companies like Quantum Therapeutics are already building on these foundations.
        """,
        "breakthrough_factors": [
            "First comprehensive VQE benchmark for pharma-relevant molecules",
            "Novel error mitigation extending quantum advantage to NISQ devices",
            "40x speedup demonstrated on classically intractable problems",
            "Open-source benchmark suite enabling reproducibility"
        ],
        "visual_theme": {
            "primary": "#00E5FF",
            "secondary": "#4da8da",
            "pattern": "quantum_circuit",
            "icons": ["cpu", "atom", "flask", "chart"]
        }
    },
    {
        "id": "crispr_rna_design",
        "title": "CRISPR-Cas13 Guided RNA Design Using Transformer Architectures",
        "authors": "Patel et al., Stanford",
        "venue": "Nature Biotechnology",
        "domain": "Biotechnology",
        "domain_color": COLORS['accent_purple'],
        "date": "2024.01.12",
        "views": "5.1K",
        "citations": "89",
        "score": "97%",
        "abstract": "A novel deep learning approach for optimizing guide RNA sequences with improved specificity and reduced off-target effects. Our model achieves 98% accuracy in predicting editing efficiency...",
        "narration": """
            Stanford's Patel team has published what may be the most important CRISPR advance of 2024. Their 
            transformer-based AI system designs guide RNA sequences for CRISPR-Cas13 gene editing with 98% 
            accuracy—dramatically improving on previous methods.
            
            CRISPR gene editing holds immense therapeutic promise, but off-target effects—where the editing 
            machinery cuts DNA at unintended locations—have limited clinical applications. This paper's AI 
            approach systematically minimizes such risks by learning patterns from millions of successful 
            and unsuccessful editing experiments.
            
            The transformer architecture, similar to what powers GPT models, proves remarkably effective at 
            understanding the sequence rules governing CRISPR specificity. The model considers not just the 
            guide RNA sequence but the broader genomic context, predicting off-target sites that simpler 
            algorithms miss.
            
            With 89 citations already and counting, this work is reshaping the gene therapy landscape. 
            Companies like GenomeForge are translating these academic advances into clinical platforms. 
            For patients with genetic diseases, better CRISPR design means safer, more effective treatments 
            coming sooner.
        """,
        "breakthrough_factors": [
            "98% prediction accuracy for CRISPR editing outcomes",
            "Transformer architecture captures long-range genomic dependencies",
            "Reduces off-target effects by 73% compared to previous methods",
            "Generalizes across Cas variants and cell types"
        ],
        "visual_theme": {
            "primary": "#a78bfa",
            "secondary": "#ec4899",
            "pattern": "gene_editing",
            "icons": ["scissors", "dna", "target", "shield"]
        }
    },
    {
        "id": "perovskite_solar",
        "title": "Perovskite Tandem Solar Cells: Defect Passivation Strategies for 34% Efficiency",
        "authors": "Kim et al., NREL",
        "venue": "Science Advances",
        "domain": "Energy",
        "domain_color": COLORS['accent_green'],
        "date": "2024.01.10",
        "views": "3.8K",
        "citations": "56",
        "score": "99%",
        "abstract": "Novel interface engineering approaches combining 2D/3D heterojunctions with molecular passivation layers achieve record-breaking stabilized power conversion efficiencies in perovskite-silicon tandems...",
        "narration": """
            The National Renewable Energy Laboratory's Kim team has achieved a landmark in solar energy: 
            perovskite-silicon tandem cells with verified 34% power conversion efficiency. This shatters 
            the previous record and brings utility-scale next-generation solar within reach.
            
            Perovskite solar cells have long promised higher efficiencies than conventional silicon, but 
            stability issues prevented commercialization. This paper's breakthrough involves sophisticated 
            defect passivation strategies—molecular treatments that heal the microscopic defects that cause 
            perovskites to degrade.
            
            The innovation lies in combining 2D and 3D perovskite heterojunctions with tailored passivation 
            layers. The 2D surface layer protects against moisture and heat while the 3D bulk delivers 
            high efficiency. It's a elegant materials engineering solution to a problem that stumped 
            researchers for a decade.
            
            At 34% efficiency and projected manufacturing costs below 20 cents per watt, this technology 
            could accelerate solar adoption by years. Companies like Solaris Materials are racing to 
            commercialize these advances. The implications for climate change are substantial—every 
            percentage point improvement in solar efficiency displaces fossil fuels faster.
        """,
        "breakthrough_factors": [
            "Record 34% stabilized efficiency for perovskite-silicon tandems",
            "Novel 2D/3D heterojunction solves longstanding stability issue",
            "1000-hour operational stability demonstrated",
            "Solution-processable fabrication compatible with existing lines"
        ],
        "visual_theme": {
            "primary": "#10b981",
            "secondary": "#06b6d4",
            "pattern": "solar_efficiency",
            "icons": ["sun", "trending_up", "factory", "earth"]
        }
    },
    {
        "id": "neuromorphic_computing",
        "title": "Neuromorphic Computing: Brain-Inspired Architectures for Edge AI Inference",
        "authors": "Rodriguez et al., Intel Labs",
        "venue": "IEEE Micro",
        "domain": "Neuroscience",
        "domain_color": COLORS['accent_gold'],
        "date": "2024.01.08",
        "views": "1.9K",
        "citations": "23",
        "score": "91%",
        "abstract": "Comprehensive analysis of spiking neural network implementations on neuromorphic hardware demonstrating 100x energy efficiency improvements for real-time inference applications at the edge...",
        "narration": """
            Intel Labs' Rodriguez team provides the definitive analysis of neuromorphic computing's readiness 
            for production edge AI deployments. Their benchmark demonstrates 100x energy efficiency improvements 
            over GPUs for real-time inference—validating the entire neuromorphic computing thesis.
            
            Neuromorphic chips mimic brain architecture using spiking neural networks that only consume power 
            when neurons fire. For always-on edge applications like smart sensors, autonomous drones, and 
            wearable health monitors, this means battery lifetimes measured in months rather than hours.
            
            The paper comprehensively evaluates Intel's Loihi neuromorphic chip across vision, audio, and 
            sensor fusion tasks. Results show that while training still requires conventional hardware, 
            inference workloads—the bulk of production AI compute—can migrate to neuromorphic processors 
            with dramatic energy savings.
            
            As AI deployment scales to billions of edge devices, the energy implications are staggering. 
            Neuromorphic computing could prevent data center energy demand from growing 10x over the 
            next decade. Companies like NeuroSynth Labs are building on this foundation to deliver 
            commercial neuromorphic products.
        """,
        "breakthrough_factors": [
            "100x energy efficiency vs GPU for inference workloads",
            "Comprehensive benchmark across vision, audio, sensor fusion",
            "Real-time processing demonstrated at microjoule per inference",
            "Software stack enabling migration from conventional ANNs to SNNs"
        ],
        "visual_theme": {
            "primary": "#f59e0b",
            "secondary": "#ef4444",
            "pattern": "neuromorphic_chip",
            "icons": ["chip", "brain", "battery", "edge"]
        }
    }
]

# ============================================================================
# AI PEER REVIEWER PERSONAS (3 distinct AI reviewers)
# ============================================================================

AI_REVIEWERS = [
    {
        "id": "dr_synthia_turing",
        "name": "Dr. Synthia Turing",
        "title": "Theoretical Computer Scientist & Quantum Algorithms Expert",
        "avatar": "ST",
        "avatar_colors": [COLORS['accent_cyan'], COLORS['accent_purple']],
        "personality": "analytical_rigorous",
        "perspective": "theoretical_foundations",
        "background": """
            Dr. Synthia Turing is an AI persona embodying the analytical rigor of theoretical computer science 
            combined with deep expertise in quantum algorithms. Named in honor of Alan Turing and Cynthia Dwork, 
            she approaches every paper through the lens of computational complexity, algorithmic correctness, 
            and theoretical guarantees.
            
            Her review style emphasizes mathematical formalism, asymptotic analysis, and identification of 
            implicit assumptions. She excels at spotting gaps between claimed results and actual proofs, 
            and at contextualizing contributions within the broader landscape of computational theory.
        """,
        "review_focus": [
            "Algorithmic complexity and scalability claims",
            "Mathematical rigor and proof completeness",
            "Theoretical novelty vs incremental improvement",
            "Computational assumptions and their validity"
        ],
        "strengths": [
            "Identifies hidden complexity in apparently simple algorithms",
            "Contextualizes within decades of theoretical work",
            "Spotting overclaimed results or insufficient evidence",
            "Suggests theoretically grounded improvements"
        ],
        "voice_profile": {
            "tone": "precise_academic",
            "vocabulary": "technical_formal",
            "sentence_structure": "complex_nested",
            "metaphors": "mathematical_computational"
        }
    },
    {
        "id": "prof_helix_bio",
        "name": "Prof. Helix Bio",
        "title": "Computational Biologist & Translational Medicine Expert",
        "avatar": "HB",
        "avatar_colors": [COLORS['accent_green'], COLORS['accent_pink']],
        "personality": "pragmatic_clinical",
        "perspective": "biological_applicability",
        "background": """
            Prof. Helix Bio represents the perspective of computational biology translated into clinical 
            impact. With deep expertise spanning genomics, structural biology, and drug development pipelines, 
            she evaluates research through the lens of real-world therapeutic applicability.
            
            Her persona embodies the bridge between computational innovation and bedside medicine. She asks 
            the questions that matter for translation: Does this work in primary cells, not just cell lines? 
            What's the path to clinical trials? Are the effect sizes clinically meaningful?
        """,
        "review_focus": [
            "Biological plausibility and mechanism validation",
            "Translational pathway to clinical application",
            "Experimental relevance to human disease",
            "Comparison to existing therapeutic approaches"
        ],
        "strengths": [
            "Evaluates biological significance beyond statistical significance",
            "Identifies translational roadblocks invisible to pure CS researchers",
            "Assesses robustness across biological replicates and conditions",
            "Connects to existing drug development pipelines"
        ],
        "voice_profile": {
            "tone": "engaged_clinical",
            "vocabulary": "biomedical_accessible",
            "sentence_structure": "direct_active",
            "metaphors": "biological_medical"
        }
    },
    {
        "id": "architect_nova",
        "name": "Architect Nova",
        "title": "Systems Engineer & ML Infrastructure Specialist",
        "avatar": "AN",
        "avatar_colors": [COLORS['accent_gold'], COLORS['accent_blue']],
        "personality": "implementation_focused",
        "perspective": "engineering_scalability",
        "background": """
            Architect Nova brings the pragmatic perspective of production machine learning systems engineering. 
            Having designed and deployed ML infrastructure at scale, Nova evaluates research through the lens 
            of implementability: Can this actually be built? Will it work with real data at scale?
            
            This persona embodies the voice of engineers who must translate papers into production systems. 
            Nova cares about training stability, inference latency, memory footprint, integration challenges, 
            and the messy realities of working with imperfect data in the wild.
        """,
        "review_focus": [
            "Implementation feasibility and engineering challenges",
            "Scalability to production data volumes",
            "Reproducibility and code/data availability",
            "Integration with existing ML pipelines"
        ],
        "strengths": [
            "Identifies scalability bottlenecks missed in controlled experiments",
            "Evaluates practicality of proposed methods vs established baselines",
            "Assesses computational requirements realistically",
            "Suggests concrete implementation improvements"
        ],
        "voice_profile": {
            "tone": "direct_practical",
            "vocabulary": "engineering_precise",
            "sentence_structure": "clear_concise",
            "metaphors": "architectural_infrastructure"
        }
    }
]

# ============================================================================
# FRAME GENERATION FUNCTIONS
# ============================================================================

def get_font(size, bold=False):
    """Get font with fallback chain."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    return ImageFont.load_default()

def draw_gradient_background(draw, width, height, color1, color2, direction='vertical'):
    """Draw a gradient background."""
    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        for x in range(width):
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))

def draw_molecular_pattern(draw, width, height, pattern_type, color, alpha=30):
    """Draw decorative molecular/scientific patterns."""
    random.seed(42)  # Consistent patterns
    
    if pattern_type == 'quantum_orbital':
        # Draw electron orbital rings
        for i in range(5):
            cx, cy = random.randint(100, width-100), random.randint(100, height-100)
            radius = random.randint(80, 200)
            for j in range(3):
                r = radius + j * 30
                opacity = max(10, alpha - j * 10)
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*hex_to_rgb(color), opacity), width=2)
    
    elif pattern_type == 'neural_network':
        # Draw neural network nodes and connections
        nodes = [(random.randint(100, width-100), random.randint(100, height-100)) for _ in range(15)]
        for i, (x1, y1) in enumerate(nodes):
            for x2, y2 in nodes[i+1:]:
                if abs(x1-x2) + abs(y1-y2) < 400:
                    draw.line([(x1, y1), (x2, y2)], fill=(*hex_to_rgb(color), alpha//2), width=1)
            draw.ellipse([x1-8, y1-8, x1+8, y1+8], fill=(*hex_to_rgb(color), alpha))
    
    elif pattern_type == 'dna_helix':
        # Draw DNA helix
        cx = width // 2
        for y in range(0, height, 20):
            offset = int(math.sin(y * 0.05) * 100)
            draw.ellipse([cx+offset-6, y-6, cx+offset+6, y+6], fill=(*hex_to_rgb(color), alpha))
            draw.ellipse([cx-offset-6, y-6, cx-offset+6, y+6], fill=(*hex_to_rgb(color), alpha//2))
            if y % 40 == 0:
                draw.line([(cx+offset, y), (cx-offset, y)], fill=(*hex_to_rgb(color), alpha//3), width=2)
    
    elif pattern_type == 'solar_cells':
        # Draw sun rays and grid pattern
        cx, cy = 150, 150
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            ex = cx + int(math.cos(rad) * 300)
            ey = cy + int(math.sin(rad) * 300)
            draw.line([(cx, cy), (ex, ey)], fill=(*hex_to_rgb(color), alpha//2), width=2)
        # Grid
        for x in range(0, width, 80):
            draw.line([(x, 0), (x, height)], fill=(*hex_to_rgb(color), alpha//4), width=1)
        for y in range(0, height, 80):
            draw.line([(0, y), (width, y)], fill=(*hex_to_rgb(color), alpha//4), width=1)
    
    else:  # Default: floating particles
        for _ in range(50):
            x, y = random.randint(0, width), random.randint(0, height)
            size = random.randint(2, 6)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(*hex_to_rgb(color), alpha))

def create_title_frame(title, subtitle, theme, frame_num=0, total_frames=180):
    """Create an opening title frame."""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), hex_to_rgb(COLORS['bg_deep']))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Gradient background
    draw_gradient_background(draw, VIDEO_WIDTH, VIDEO_HEIGHT, 
                            hex_to_rgb(COLORS['bg_deep']), 
                            hex_to_rgb(COLORS['bg_primary']))
    
    # Pattern overlay
    draw_molecular_pattern(draw, VIDEO_WIDTH, VIDEO_HEIGHT, 
                          theme.get('pattern', 'default'), 
                          theme.get('primary', COLORS['accent_cyan']))
    
    # Animated glow effect based on frame
    glow_intensity = int(abs(math.sin(frame_num * 0.05)) * 30)
    
    # Title background box
    padding = 60
    title_box = [padding, VIDEO_HEIGHT//2 - 120, VIDEO_WIDTH - padding, VIDEO_HEIGHT//2 + 120]
    draw.rounded_rectangle(title_box, radius=24, 
                          fill=(*hex_to_rgb(COLORS['bg_primary']), 220),
                          outline=(*hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), glow_intensity + 40),
                          width=3)
    
    # Main title
    font_large = get_font(64, bold=True)
    font_medium = get_font(32)
    
    # Wrap title text
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=font_large)
        if bbox[2] - bbox[0] > VIDEO_WIDTH - 200:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    
    y_offset = VIDEO_HEIGHT//2 - 60 - (len(lines) * 40)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        x = (VIDEO_WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((x, y_offset), line, fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), font=font_large)
        y_offset += 75
    
    # Subtitle
    if subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
        x = (VIDEO_WIDTH - (sub_bbox[2] - sub_bbox[0])) // 2
        draw.text((x, y_offset + 30), subtitle, fill=hex_to_rgb(COLORS['text_secondary']), font=font_medium)
    
    # Decorative corner elements
    corner_size = 40
    corners = [(padding + 20, padding + 20), (VIDEO_WIDTH - padding - 20 - corner_size, padding + 20),
               (padding + 20, VIDEO_HEIGHT - padding - 20 - corner_size), 
               (VIDEO_WIDTH - padding - 20 - corner_size, VIDEO_HEIGHT - padding - 20 - corner_size)]
    
    for cx, cy in corners:
        draw.rounded_rectangle([cx, cy, cx + corner_size, cy + corner_size], radius=8,
                              fill=(*hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), 60))
    
    return img

def create_content_frame(content_lines, theme, frame_num=0, total_frames=180, section_indicator=""):
    """Create a content frame with text."""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), hex_to_rgb(COLORS['bg_deep']))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    draw_gradient_background(draw, VIDEO_WIDTH, VIDEO_HEIGHT,
                            hex_to_rgb(COLORS['bg_primary']),
                            hex_to_rgb(COLORS['bg_secondary']))
    
    # Subtle pattern
    draw_molecular_pattern(draw, VIDEO_WIDTH, VIDEO_HEIGHT,
                          theme.get('pattern', 'default'),
                          theme.get('secondary', COLORS['accent_blue']),
                          alpha=15)
    
    # Content area
    padding = 100
    content_x = padding + 50
    content_y = 150
    
    # Section indicator
    if section_indicator:
        font_small = get_font(24)
        indicator_bg_width = len(section_indicator) * 14 + 40
        draw.rounded_rectangle([content_x, content_y - 10, content_x + indicator_bg_width, content_y + 35],
                              radius=12,
                              fill=(*hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), 40))
        draw.text((content_x + 20, content_y), section_indicator, 
                 fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), font=font_small)
        content_y += 60
    
    # Content text
    font_content = get_font(32)
    font_content_bold = get_font(32, bold=True)
    
    for line in content_lines:
        if line.startswith("## "):  # Bold header
            text = line[3:]
            draw.text((content_x, content_y), text, 
                     fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), 
                     font=font_content_bold)
            content_y += 55
        elif line.startswith("- "):  # Bullet point
            text = line[2:]
            # Bullet
            draw.ellipse([content_x, content_y + 10, content_x + 12, content_y + 22],
                        fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])))
            draw.text((content_x + 25, content_y), text,
                     fill=hex_to_rgb(COLORS['text_primary']), font=font_content)
            content_y += 48
        else:  # Normal text
            # Word wrap
            words = line.split()
            current_line = []
            for word in words:
                current_line.append(word)
                test_text = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_text, font=font_content)
                if bbox[2] - bbox[0] > VIDEO_WIDTH - 300:
                    current_line.pop()
                    draw.text((content_x, content_y), ' '.join(current_line),
                             fill=hex_to_rgb(COLORS['text_primary']), font=font_content)
                    content_y += 48
                    current_line = [word]
            if current_line:
                draw.text((content_x, content_y), ' '.join(current_line),
                         fill=hex_to_rgb(COLORS['text_primary']), font=font_content)
                content_y += 48
    
    # Bottom accent line
    progress = frame_num / total_frames
    line_width = int((VIDEO_WIDTH - 200) * progress)
    draw.rectangle([100, VIDEO_HEIGHT - 30, 100 + line_width, VIDEO_HEIGHT - 26],
                  fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])))
    
    return img

def create_metrics_frame(metrics_dict, theme, frame_num=0, total_frames=180):
    """Create a metrics/statistics display frame."""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), hex_to_rgb(COLORS['bg_deep']))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    draw_gradient_background(draw, VIDEO_WIDTH, VIDEO_HEIGHT,
                            hex_to_rgb(COLORS['bg_secondary']),
                            hex_to_rgb(COLORS['bg_deep']))
    
    # Title
    font_title = get_font(48, bold=True)
    font_metric_value = get_font(72, bold=True)
    font_metric_label = get_font(24)
    
    title = "Key Metrics & Validation"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    x = (VIDEO_WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, 100), title, fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), font=font_title)
    
    # Metrics cards
    metrics_count = len(metrics_dict)
    card_width = 350
    card_height = 280
    total_width = metrics_count * card_width + (metrics_count - 1) * 40
    start_x = (VIDEO_WIDTH - total_width) // 2
    y_start = 250
    
    for idx, (label, value) in enumerate(metrics_dict.items()):
        x = start_x + idx * (card_width + 40)
        
        # Card background
        draw.rounded_rectangle([x, y_start, x + card_width, y_start + card_height],
                              radius=20,
                              fill=(*hex_to_rgb(COLORS['bg_primary']), 230),
                              outline=(*hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])), 60),
                              width=2)
        
        # Value
        value_bbox = draw.textbbox((0, 0), str(value), font=font_metric_value)
        val_x = x + (card_width - (value_bbox[2] - value_bbox[0])) // 2
        draw.text((val_x, y_start + 70), str(value),
                 fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])),
                 font=font_metric_value)
        
        # Label
        label_bbox = draw.textbbox((0, 0), label, font=font_metric_label)
        label_x = x + (card_width - (label_bbox[2] - label_bbox[0])) // 2
        draw.text((label_x, y_start + 170), label,
                 fill=hex_to_rgb(COLORS['text_secondary']),
                 font=font_metric_label)
        
        # Decorative top accent
        draw.rounded_rectangle([x + 20, y_start + 20, x + card_width - 20, y_start + 28],
                              radius=4,
                              fill=hex_to_rgb(theme.get('primary', COLORS['accent_cyan'])))
    
    return img

def create_ai_reviewer_frame(reviewer, frame_num=0, total_frames=180, is_intro=True):
    """Create AI Peer Reviewer introduction/review frame."""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), hex_to_rgb(COLORS['bg_deep']))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    draw_gradient_background(draw, VIDEO_WIDTH, VIDEO_HEIGHT,
                            hex_to_rgb(COLORS['bg_deep']),
                            hex_to_rgb(COLORS['bg_primary']))
    
    colors = reviewer.get('avatar_colors', [COLORS['accent_cyan'], COLORS['accent_purple']])
    primary_color = colors[0]
    
    # Avatar circle
    avatar_center = (300, VIDEO_HEIGHT // 2)
    avatar_radius = 100
    
    # Glow effect
    for i in range(20, 0, -5):
        glow_alpha = int(10 - i/2)
        draw.ellipse([avatar_center[0] - avatar_radius - i*3, avatar_center[1] - avatar_radius - i*3,
                      avatar_center[0] + avatar_radius + i*3, avatar_center[1] + avatar_radius + i*3],
                     fill=(*hex_to_rgb(primary_color), max(0, glow_alpha)))
    
    # Avatar background
    draw.ellipse([avatar_center[0] - avatar_radius, avatar_center[1] - avatar_radius,
                  avatar_center[0] + avatar_radius, avatar_center[1] + avatar_radius],
                 fill=(*hex_to_rgb(primary_color), 100),
                 outline=(*hex_to_rgb(primary_color), 200),
                 width=4)
    
    # Avatar initials
    font_avatar = get_font(72, bold=True)
    initials = reviewer.get('avatar', 'AI')
    bbox = draw.textbbox((0, 0), initials, font=font_avatar)
    x = avatar_center[0] - (bbox[2] - bbox[0]) // 2
    y = avatar_center[1] - (bbox[3] - bbox[1]) // 2
    draw.text((x, y), initials, fill=hex_to_rgb(COLORS['text_primary']), font=font_avatar)
    
    # Name and title
    font_name = get_font(52, bold=True)
    font_title = get_font(28)
    
    name = reviewer.get('name', 'AI Reviewer')
    title = reviewer.get('title', '')
    
    draw.text((480, VIDEO_HEIGHT // 2 - 80), name, fill=hex_to_rgb(primary_color), font=font_name)
    draw.text((480, VIDEO_HEIGHT // 2 - 10), title, fill=hex_to_rgb(COLORS['text_secondary']), font=font_title)
    
    # Perspective badge
    perspective = reviewer.get('perspective', '').replace('_', ' ').title()
    font_badge = get_font(22)
    badge_text = f"Perspective: {perspective}"
    badge_width = len(badge_text) * 12 + 40
    
    draw.rounded_rectangle([480, VIDEO_HEIGHT // 2 + 50, 480 + badge_width, VIDEO_HEIGHT // 2 + 90],
                          radius=16,
                          fill=(*hex_to_rgb(primary_color), 40),
                          outline=(*hex_to_rgb(primary_color), 100))
    draw.text((500, VIDEO_HEIGHT // 2 + 56), badge_text, fill=hex_to_rgb(primary_color), font=font_badge)
    
    # Review focus areas
    if is_intro:
        focus_areas = reviewer.get('review_focus', [])
        font_focus = get_font(24)
        
        draw.text((480, VIDEO_HEIGHT // 2 + 130), "Review Focus:", fill=hex_to_rgb(COLORS['text_primary']), font=get_font(28, bold=True))
        
        for idx, focus in enumerate(focus_areas[:4]):
            y_pos = VIDEO_HEIGHT // 2 + 175 + idx * 40
            draw.ellipse([480, y_pos + 6, 492, y_pos + 18], fill=hex_to_rgb(primary_color))
            draw.text((505, y_pos), focus, fill=hex_to_rgb(COLORS['text_secondary']), font=font_focus)
    
    return img

# ============================================================================
# TTS FUNCTIONS (using edge-tts)
# ============================================================================

async def generate_audio_edge_tts(text, output_path, voice="en-US-AriaNeural", rate="+0%"):
    """Generate audio using Microsoft Edge TTS."""
    import edge_tts
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))
    print(f"Generated TTS audio: {output_path}")

def generate_audio_subprocess(text, output_path, voice="en-US-AriaNeural"):
    """Generate audio using edge-tts via subprocess."""
    try:
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"Generated TTS audio: {output_path}")
            return True
        else:
            print(f"TTS Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"TTS subprocess error: {e}")
        return False

# ============================================================================
# VIDEO ASSEMBLY FUNCTIONS (using FFmpeg)
# ============================================================================

def images_to_video(image_dir, audio_path, output_path, fps=30):
    """Assemble images into video with audio using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", f"{image_dir}/frame_%04d.png",
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Created video: {output_path}")
        return True
    else:
        print(f"FFmpeg error: {result.stderr}")
        return False

def create_video_from_frames(frame_generator_func, audio_path, output_path, total_frames=None, **kwargs):
    """Create a complete video from generated frames."""
    if total_frames is None:
        total_frames = FPS * DURATION
    
    # Create temp directory for frames
    import tempfile
    with tempfile.TemporaryDirectory() as frame_dir:
        print(f"Generating {total_frames} frames...")
        
        for i in range(total_frames):
            frame = frame_generator_func(frame_num=i, total_frames=total_frames, **kwargs)
            frame_path = Path(frame_dir) / f"frame_{i:04d}.png"
            frame.save(str(frame_path))
            
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{total_frames} frames")
        
        # Assemble video
        return images_to_video(frame_dir, audio_path, output_path)

# ============================================================================
# MAIN CONTENT GENERATION FUNCTIONS
# ============================================================================

def generate_startup_video(startup_data, output_dir):
    """Generate a complete startup explainer video."""
    startup_id = startup_data['id']
    startup_name = startup_data['name']
    theme = startup_data.get('visual_theme', {})
    
    print(f"\n{'='*60}")
    print(f"Generating video for: {startup_name}")
    print(f"{'='*60}\n")
    
    # Prepare paths
    output_path = Path(output_dir) / f"{startup_id}_explainer.mp4"
    audio_path = Path(AUDIO_DIR) / f"{startup_id}_narration.wav"
    
    # Generate TTS narration
    print("Step 1: Generating TTS narration...")
    narration_text = startup_data.get('narration', '')
    success = generate_audio_subprocess(narration_text, audio_path, voice="en-US-GuyNeural")
    
    if not success:
        print("TTS generation failed, creating silent video")
        # Create silent audio as fallback
        silent_cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(DURATION), "-acodec", "pcm_s16le", str(audio_path)
        ]
        subprocess.run(silent_cmd, capture_output=True)
    
    # Get audio duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        audio_duration = float(duration_result.stdout.strip())
        total_frames = int(audio_duration * FPS)
    except:
        audio_duration = DURATION
        total_frames = FPS * DURATION
    
    print(f"Audio duration: {audio_duration:.1f}s ({total_frames} frames)")
    
    # Generate frames
    print("Step 2: Generating video frames...")
    
    # Parse narration into sections
    narration_lines = [line.strip() for line in narration_text.split('.') if line.strip()]
    sections = []
    current_section = []
    
    for line in narration_lines:
        current_section.append(line)
        if len(current_section) >= 3:
            sections.append('. '.join(current_section) + '.')
            current_section = []
    
    if current_section:
        sections.append('. '.join(current_section) + '.')
    
    # Calculate frames per section
    frames_per_section = max(30, total_frames // (len(sections) + 2))  # +2 for intro/outro
    
    import tempfile
    with tempfile.TemporaryDirectory() as frame_dir:
        frame_idx = 0
        
        # Intro frames (10% of video)
        intro_frames = min(int(total_frames * 0.1), frames_per_section)
        for i in range(intro_frames):
            frame = create_title_frame(
                startup_name,
                f"{startup_data.get('stage', '')} Stage | {startup_data.get('tagline', '')[:60]}...",
                theme,
                frame_num=i,
                total_frames=intro_frames
            )
            frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
            frame_idx += 1
        
        # Content frames
        for sec_idx, section in enumerate(sections):
            # Parse section into display lines
            words = section.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if len(current_line) >= 12:
                    lines.append(' '.join(current_line))
                    current_line = []
            if current_line:
                lines.append(' '.join(current_line))
            
            section_frames = min(frames_per_section, total_frames - frame_idx - intro_frames // 2)
            
            for i in range(section_frames):
                # Determine section type for styling
                if sec_idx == 0:
                    indicator = "Overview"
                elif "million" in section.lower() or "$" in section.lower():
                    indicator = "Funding & Metrics"
                elif any(word in section.lower() for word in ['key', 'differentiator', 'unique']):
                    indicator = "Key Differentiators"
                else:
                    indicator = "Details"
                
                frame = create_content_frame(
                    lines,
                    theme,
                    frame_num=i,
                    total_frames=section_frames,
                    section_indicator=indicator
                )
                frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
                frame_idx += 1
            
            print(f"  Section {sec_idx + 1}/{len(sections)} completed")
        
        # Metrics frames
        metrics = startup_data.get('metrics', {})
        metrics_frames = min(frames_per_section, total_frames - frame_idx - 30)
        for i in range(metrics_frames):
            frame = create_metrics_frame(metrics, theme, frame_num=i, total_frames=metrics_frames)
            frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
            frame_idx += 1
        
        # Fill remaining frames
        remaining = total_frames - frame_idx
        for i in range(max(0, remaining)):
            frame = create_title_frame(
                startup_name,
                "Learn more about this innovative company",
                theme,
                frame_num=i,
                total_frames=max(remaining, 1)
            )
            frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
            frame_idx += 1
        
        print(f"Total frames generated: {frame_idx}")
        
        # Assemble video
        print("Step 3: Assembling video with FFmpeg...")
        success = images_to_video(frame_dir, audio_path, output_path, fps=FPS)
        
        if success:
            print(f"✓ Successfully created: {output_path}")
            print(f"  File size: {output_path.stat().st_size / (1024*1024):.1f} MB")
        else:
            print("✗ Video creation failed")
        
        return success

def generate_research_paper_video(paper_data, output_dir):
    """Generate a research paper explainer video."""
    paper_id = paper_data['id']
    paper_title = paper_data['title']
    theme = paper_data.get('visual_theme', {})
    
    print(f"\n{'='*60}")
    print(f"Generating video for paper: {paper_title[:50]}...")
    print(f"{'='*60}\n")
    
    output_path = Path(output_dir) / f"{paper_id}_explainer.mp4"
    audio_path = Path(AUDIO_DIR) / f"{paper_id}_narration.wav"
    
    # Generate TTS
    print("Step 1: Generating TTS narration...")
    narration_text = paper_data.get('narration', '')
    success = generate_audio_subprocess(narration_text, audio_path, voice="en-US-JennyNeural")
    
    if not success:
        silent_cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(DURATION), "-acodec", "pcm_s16le", str(audio_path)
        ]
        subprocess.run(silent_cmd, capture_output=True)
    
    # Get duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        audio_duration = float(duration_result.stdout.strip())
        total_frames = int(audio_duration * FPS)
    except:
        audio_duration = DURATION
        total_frames = FPS * DURATION
    
    print(f"Audio duration: {audio_duration:.1f}s ({total_frames} frames)")
    
    # Generate frames
    print("Step 2: Generating video frames...")
    
    # Prepare content sections
    authors = paper_data.get('authors', '')
    venue = paper_data.get('venue', '')
    domain = paper_data.get('domain', '')
    
    narration_lines = [line.strip() for line in narration_text.split('.') if line.strip()]
    sections = []
    current_section = []
    
    for line in narration_lines:
        current_section.append(line)
        if len(current_section) >= 3:
            sections.append('. '.join(current_section) + '.')
            current_section = []
    
    if current_section:
        sections.append('. '.join(current_section) + '.')
    
    # Add breakthrough factors as final section
    breakthrough = paper_data.get('breakthrough_factors', [])
    if breakthrough:
        sections.append("## Key Breakthrough Factors\n" + '\n'.join(f"- {factor}" for factor in breakthrough))
    
    frames_per_section = max(30, total_frames // (len(sections) + 2))
    
    import tempfile
    with tempfile.TemporaryDirectory() as frame_dir:
        frame_idx = 0
        
        # Title intro
        intro_frames = min(int(total_frames * 0.12), frames_per_section)
        for i in range(intro_frames):
            frame = create_title_frame(
                paper_title,
                f"{authors} | {venue} | {domain}",
                theme,
                frame_num=i,
                total_frames=intro_frames
            )
            frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
            frame_idx += 1
        
        # Content sections
        for sec_idx, section in enumerate(sections):
            if section.startswith("## "):
                lines = section[3:].split('\n')
                indicator = "Key Findings"
            else:
                words = section.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    if len(current_line) >= 12:
                        lines.append(' '.join(current_line))
                        current_line = []
                if current_line:
                    lines.append(' '.join(current_line))
                
                if sec_idx == 0:
                    indicator = "Introduction"
                elif "significant" in section.lower():
                    indicator = "Significance"
                elif "company" in section.lower():
                    indicator = "Industry Impact"
                else:
                    indicator = "Analysis"
            
            section_frames = min(frames_per_section, total_frames - frame_idx - 45)
            
            for i in range(section_frames):
                frame = create_content_frame(
                    lines,
                    theme,
                    frame_num=i,
                    total_frames=section_frames,
                    section_indicator=indicator
                )
                frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
                frame_idx += 1
            
            print(f"  Section {sec_idx + 1}/{len(sections)} completed")
        
        # Paper stats
        stats = {
            "Views": paper_data.get('views', '0'),
            "Citations": paper_data.get('citations', '0'),
            "Score": paper_data.get('score', '0%')
        }
        stats_frames = min(frames_per_section // 2, total_frames - frame_idx - 15)
        for i in range(stats_frames):
            frame = create_metrics_frame(stats, theme, frame_num=i, total_frames=stats_frames)
            frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
            frame_idx += 1
        
        # Remaining
        remaining = total_frames - frame_idx
        for i in range(max(0, remaining)):
            frame = create_title_frame(
                paper_title,
                f"Validation Score: {paper_data.get('score', 'N/A')}",
                theme,
                frame_num=i,
                total_frames=max(remaining, 1)
            )
            frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
            frame_idx += 1
        
        print(f"Total frames: {frame_idx}")
        
        # Assemble
        print("Step 3: Assembling video...")
        success = images_to_video(frame_dir, audio_path, output_path, fps=FPS)
        
        if success:
            print(f"✓ Created: {output_path} ({output_path.stat().st_size / (1024*1024):.1f} MB)")
        
        return success

def generate_ai_reviewer_intros(output_dir):
    """Generate introduction videos for each AI reviewer."""
    print("\n" + "="*60)
    print("Generating AI Peer Reviewer Introduction Videos")
    print("="*60 + "\n")
    
    results = {}
    
    for reviewer in AI_REVIEWERS:
        reviewer_id = reviewer['id']
        reviewer_name = reviewer['name']
        theme = {
            'primary': reviewer.get('avatar_colors', ['#00E5FF'])[0],
            'secondary': reviewer.get('avatar_colors', ['#a78bfa'])[-1] if len(reviewer.get('avatar_colors', [])) > 1 else '#a78bfa',
            'pattern': 'neural_network'
        }
        
        print(f"\n--- Generating: {reviewer_name} ---\n")
        
        output_path = Path(output_dir) / f"{reviewer_id}_intro.mp4"
        audio_path = Path(AUDIO_DIR) / f"{reviewer_id}_intro.wav"
        
        # Create intro script
        intro_script = f"""
            Meet {reviewer_name}, {reviewer.get('title', 'AI Specialist')}.
            
            {reviewer.get('background', '')}
            
            Dr. {reviewer_name.split()[1] if len(reviewer_name.split()) > 1 else ''}'s review focuses on:
            {' '.join('- ' + focus for focus in reviewer.get('review_focus', [])[:3])}
            
            Strengths include:
            {' '.join('- ' + strength for strength in reviewer.get('strengths', [])[:3])}
            
            This unique perspective ensures comprehensive analysis from the {reviewer.get('perspective', '').replace('_', ' ')} viewpoint.
        """
        
        # Generate audio
        voices = {
            "dr_synthia_turing": "en-US-AriaNeural",
            "prof_helix_bio": "en-US-JennyNeural",
            "architect_nova": "en-US-GuyNeural"
        }
        
        success = generate_audio_subprocess(intro_script.strip(), audio_path, voice=voices.get(reviewer_id, "en-US-AriaNeural"))
        
        if not success:
            silent_cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", "45", "-acodec", "pcm_s16le", str(audio_path)
            ]
            subprocess.run(silent_cmd, capture_output=True)
        
        # Get duration
        probe_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ]
        duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        try:
            audio_duration = float(duration_result.stdout.strip())
            total_frames = int(audio_duration * FPS)
        except:
            audio_duration = 45
            total_frames = FPS * 45
        
        # Generate frames
        import tempfile
        with tempfile.TemporaryDirectory() as frame_dir:
            frame_idx = 0
            
            # Intro frames with reviewer info
            for i in range(total_frames):
                frame = create_ai_reviewer_frame(
                    reviewer,
                    frame_num=i,
                    total_frames=total_frames,
                    is_intro=True
                )
                frame.save(Path(frame_dir) / f"frame_{frame_idx:04d}.png")
                frame_idx += 1
            
            # Assemble
            success = images_to_video(frame_dir, audio_path, output_path, fps=FPS)
            
            if success:
                print(f"✓ Created: {output_path}")
                results[reviewer_id] = str(output_path)
            else:
                print(f"✗ Failed: {reviewer_name}")
    
    return results

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for Phase 3 content generation."""
    print("="*70)
    print("  SciMSPT Phase 3: Video Content Generation Pipeline")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Ensure directories exist
    for d in [OUTPUT_DIR, AUDIO_DIR, IMAGES_DIR, STARTUPS_DIR, RESEARCH_DIR, AI_REVIEW_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    results = {
        'generated_at': datetime.now().isoformat(),
        'startups': [],
        'research_papers': [],
        'ai_reviewers': [],
        'total_videos': 0,
        'total_size_mb': 0
    }
    
    # Check for edge-tts
    print("\nChecking prerequisites...")
    try:
        import edge_tts
        print("✓ edge-tts available")
    except ImportError:
        print("! edge-tts not found, will use subprocess")
    
    # Check ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        print(f"✓ FFmpeg available")
    except FileNotFoundError:
        print("✗ FFmpeg not found - video generation will fail")
        return results
    
    # Generate startup videos
    print("\n" + "="*70)
    print("  PHASE 3A: Startup Explainer Videos")
    print("="*70)
    
    for startup in STARTUPS_DATA:
        try:
            success = generate_startup_video(startup, STARTUPS_DIR)
            if success:
                video_path = STARTUPS_DIR / f"{startup['id']}_explainer.mp4"
                results['startups'].append({
                    'id': startup['id'],
                    'name': startup['name'],
                    'video': str(video_path),
                    'size_mb': round(video_path.stat().st_size / (1024*1024), 2)
                })
                results['total_videos'] += 1
                results['total_size_mb'] += round(video_path.stat().st_size / (1024*1024), 2)
        except Exception as e:
            print(f"Error generating video for {startup['name']}: {e}")
    
    # Generate research paper videos
    print("\n" + "="*70)
    print("  PHASE 3B: Research Paper Explainer Videos")
    print("="*70)
    
    for paper in RESEARCH_PAPERS_DATA:
        try:
            success = generate_research_paper_video(paper, RESEARCH_DIR)
            if success:
                video_path = RESEARCH_DIR / f"{paper['id']}_explainer.mp4"
                results['research_papers'].append({
                    'id': paper['id'],
                    'title': paper['title'][:60],
                    'video': str(video_path),
                    'size_mb': round(video_path.stat().st_size / (1024*1024), 2)
                })
                results['total_videos'] += 1
                results['total_size_mb'] += round(video_path.stat().st_size / (1024*1024), 2)
        except Exception as e:
            print(f"Error generating video for {paper['title']}: {e}")
    
    # Generate AI reviewer intros
    print("\n" + "="*70)
    print("  PHASE 3C: AI Peer Reviewer Introduction Videos")
    print("="*70)
    
    try:
        reviewer_results = generate_ai_reviewer_intros(AI_REVIEW_DIR)
        results['ai_reviewers'] = reviewer_results
        results['total_videos'] += len(reviewer_results)
        
        for rid, path in reviewer_results.items():
            if os.path.exists(path):
                results['total_size_mb'] += round(os.path.getsize(path) / (1024*1024), 2)
    except Exception as e:
        print(f"Error generating AI reviewer videos: {e}")
    
    # Save metadata
    metadata_path = OUTPUT_DIR / "phase3_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("  GENERATION COMPLETE")
    print("="*70)
    print(f"  Total Videos: {results['total_videos']}")
    print(f"  Total Size: {results['total_size_mb']:.1f} MB")
    print(f"  Startups: {len(results['startups'])} videos")
    print(f"  Research Papers: {len(results['research_papers'])} videos")
    print(f"  AI Reviewers: {len(results['ai_reviewers'])} videos")
    print(f"\n  Metadata saved to: {metadata_path}")
    print("="*70)
    
    return results

if __name__ == "__main__":
    results = main()
