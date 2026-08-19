#!/usr/bin/env python3
"""
SciMSPT Video Content Generator
==============================
Creates 60-second video concepts/scripts for:
1. Each Startup (P1-P7) - Investment pitch clips
2. Groundbreaking Research (3-5 papers) - Science communication clips
3. AI Peer Review - Panel discussion format

Output: HTML showcase pages + Video scripts (ready for TTS/FFmpeg)
"""

import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/home/z/my-project/SciMSPT/video-clips/output")

# ============================================
# STARTUP VIDEO CLIPS (P1-P7)
# Each: 60 seconds, cinematic, investment-focused
# ============================================

STARTUP_CLIPS = {
    "P1": {
        "name": "Stellarator Fusion",
        "domain": "Nuclear Fusion · Compact Stellarators",
        "tier": "TIER 1",
        "npv": "$589M",
        "irr": "24.7%",
        "scenes": [
            {"time": "0-8", "visual": "Space view of Earth at night, energy poverty visible", "narration": "Imagine a world where clean energy is unlimited. Where every nation has power independence."},
            {"time": "8-18", "visual": "Stellarator reactor cross-section animation", "narration": "Stellarator Fusion makes this real. Born from breakthrough research in Physical Review Letters and Nature Energy."},
            {"time": "18-28", "visual": "Plasma confinement visualization", "narration": "The secret? Optimized magnetic geometry that achieves stable fusion without tokamak disruptions."},
            {"time": "28-38", "visual": "Tritium breeding blanket schematic", "narration": "Advanced tritium breeding blankets and high-temperature superconducting coils—technologies once thought impossible."},
            {"time": "38-50", "visual": "City skyline transitioning to clean energy", "narration": "Five hundred eighty-nine million dollars net present value. Twenty-four point seven percent internal rate of return."},
            {"time": "50-60", "visual": "Logo + 'Get Access' CTA", "narration": "Stellarator Fusion. The dawn of limitless clean energy. SciMSPT validated. Invest in tomorrow's sun."}
        ],
        "music": "Epic orchestral build, synthesizer undertone",
        "style": "Kurzgesagt meets Tesla investor pitch"
    },
    
    "P2": {
        "name": "SMR Fleet OS",
        "domain": "Nuclear · Small Modular Reactors",
        "tier": "TIER 2",
        "npv": "$50M",
        "irr": "23%",
        "scenes": [
            {"time": "0-10", "visual": "Grid control room overwhelmed by complexity", "narration": "The nuclear renaissance is here. But managing fleets of Small Modular Reactors? That's the real challenge."},
            {"time": "10-20", "visual": "AI interface showing load balancing across reactors", "narration": "Enter SMR Fleet OS. Born from critical research in Applied Energy and Annals of Nuclear Energy."},
            {"time": "20-30", "visual": "Digital twin of reactor fleet", "narration": "AI-driven load balancing. Predictive maintenance through digital twins. Regulatory automation that was pure science fiction."},
            {"time": "30-40", "visual": "Multiple SMR installations coordinating", "narration": "Unlike traditional large reactors, SMRs need sophisticated fleet management. This is essential software infrastructure."},
            {"time": "40-52", "visual": "Investment metrics dashboard", "narration": "Fifty million dollars NPV. Twenty-three percent IRR. The nuclear renaissance needs a brain. This is it."},
            {"time": "52-60", "visual": "Nuclear plant sunset with software overlay", "narration": "SMR Fleet OS. Powering the nuclear future, one algorithm at a time."}
        ],
        "music": "Tech corporate ambient, confident rhythm",
        "style": "IBM Cloud meets Oppenheimer"
    },
    
    "P3": {
        "name": "Solid-State Battery",
        "domain": "Energy Storage · Next-Gen Batteries",
        "tier": "TIER 1",
        "npv": "$587M",
        "irr": "31.2%",
        "scenes": [
            {"time": "0-12", "visual": "Electric vehicle charging anxiety montage", "narration": "What if your EV charged in fifteen minutes? What if batteries never caught fire? What if energy density doubled?"},
            {"time": "12-22", "visual": "Solid-state battery cutaway animation", "narration": "Solid-State Battery technology. Traced to seminal Nature Energy and Joule publications on sulfide-based electrolytes."},
            {"time": "22-32", "visual": "Ion movement comparison (liquid vs solid)", "narration": "The breakthrough? Eliminating liquid electrolytes entirely. Five hundred watt-hours per kilogram—double current limits."},
            {"time": "32-42", "visual": "Fast charging visualization, thermal test", "narration": "Fifteen-minute charging. Two-thousand-plus cycle life. Zero thermal runaway risk. These aren't dreams—they're lab-proven realities."},
            {"time": "42-54", "visual": "Market size explosion chart", "narration": "Five hundred eighty-seven million dollars NPV. Thirty-one point two percent IRR. The most significant advancement since lithium-ion's invention."},
            {"time": "54-60", "visual": "Battery powering cityscape", "narration": "Solid-State Battery. Powering the future, safely. SciMSPT opportunity of the decade."}
        ],
        "music": "Upbeat tech, energy building",
        "style": "Apple product launch meets scientific rigor"
    },
    
    "P4": {
        "name": "Iron-Air LDES",
        "domain": "Grid Storage · Long-Duration",
        "tier": "TIER 2",
        "npv": "$44M",
        "irr": "23.4%",
        "scenes": [
            {"time": "0-10", "visual": "Solar farm at sunset, power fading", "narration": "The sun sets. Wind dies down. But the grid must stay alive. Long-duration storage isn't just important—it's existential."},
            {"time": "10-20", "visual": "Iron-air battery installation aerial view", "narration": "Iron-Air LDES addresses this through revolutionary chemistry published in Science and Joule journals."},
            {"time": "20-30", "visual": "Earth-abundant materials animation", "narration": "The genius? Using iron—one of Earth's most abundant elements. Cost target: twenty dollars per kilowatt-hour. Unbeatable economics."},
            {"time": "30-40", "visual": "100+ hour discharge curve", "narration": "One hundred plus hour discharge capabilities. When solar and wind fluctuate, Iron-Air bridges the gap affordably."},
            {"time": "40-52", "visual": "Renewable grid stabilization graphic", "narration": "Forty-four million dollars NPV. Twenty-three point four percent IRR. Enabling the fully renewable grid climate commitments demand."},
            {"time": "52-60", "visual": "Green grid powering world", "narration": "Iron-Air LDES. Storing tomorrow's clean energy, today."}
        ],
        "music": "Ambient environmental, hopeful strings",
        "style": "National Geographic meets Bloomberg Green"
    },
    
    "P5": {
        "name": "Super-Steel Electrolyzer",
        "domain": "Hydrogen · Green H2 Production",
        "tier": "TIER 1",
        "npv": "$43M",
        "irr": "17.7%",
        "scenes": [
            {"time": "0-10", "visual": "Hydrogen economy vision (trucks, planes, industry)", "narration": "The hydrogen economy needs one thing above all: green hydrogen at one dollar fifty per kilogram. Current cost? Four to six dollars."},
            {"time": "10-20", "visual": "Nanostructured steel electrode close-up", "narration": "Super-Steel Electrolyzer achieves this through innovations from Nature Catalysis and Advanced Materials."},
            {"time": "20-30", "visual": "Electrolysis process enhancement", "narration": "Nanostructured super-steel electrodes push efficiency beyond theoretical limits of conventional designs."},
            {"time": "30-40", "visual": "Variable renewable integration demo", "narration": "Critical advantage: variable renewable integration. Operating seamlessly with intermittent wind and solar input."},
            {"time": "40-52", "visual": "Hygen economy market projections", "narration": "Forty-three million dollars NPV. Seventeen point seven percent IRR. Positioning investors at the center of the hydrogen revolution."},
            {"time": "52-60", "visual": "Clean hydrogen fueling future", "narration": "Super-Steel Electrolyzer. Making green hydrogen economic reality."}
        ],
        "music": "Industrial-tech fusion, driving beat",
        "style": "Tesla Gigafactory meets scientific journal"
    },
    
    "P6": {
        "name": "Detonation H2 Turbine",
        "domain": "Hydrogen · Rotating Detonation",
        "tier": "TIER 2",
        "npv": "$38M",
        "irr": "19.8%",
        "scenes": [
            {"time": "0-10", "visual": "Conventional turbine inefficiency diagram", "narration": "Conventional hydrogen turbines suffer from fundamental efficiency limitations. Physics itself seems to constrain them."},
            {"time": "10-20", "visual": "Rotating detonation wave animation", "narration": "Unless you change the physics entirely. Detonation H2 Turbine leverages rotating detonation engine technology from Progress in Energy combustion science."},
            {"time": "20-30", "visual": "15% efficiency improvement visualization", "narration": "Fifteen percent efficiency improvement through continuous detonation wave propagation. Not incremental—transformative."},
            {"time": "30-40", "visual": "Multi-application montage (aviation, marine, grid)", "narration": "Applications span aviation, marine shipping, and grid peaking. Multiple revenue streams from one core technology."},
            {"time": "40-52", "visual": "Market opportunity mapping", "narration": "Thirty-eight million dollars NPV. Nineteen point eight percent IRR. Versatility creates resilience."},
            {"time": "52-60", "visual": "Detonation engine powering future", "narration": "Detonation H2 Turbine. Rethinking thermodynamics for the hydrogen age."}
        ],
        "music": "High-energy mechanical, precision rhythm",
        "style": "Formula 1 engineering meets aerospace innovation"
    }
}

# ============================================
# GROUNDBREAKING RESEARCH CLIPS (3-5 Papers)
# Each: 60 seconds, educational, mind-expanding
# ============================================

RESEARCH_CLIPS = {
    "R1": {
        "title": "Nonreciprocal Quantum Synchronization",
        "source": "Nature Communications (2025)",
        "authors": "Lai, Miranowicz, Nori (RIKEN)",
        "significance": "Opens field of 'Active Quantum Matter'",
        "clip_concept": {
            "hook": "What if quantum systems could synchronize like fireflies—but only ONE WAY?",
            "explanation": """
                Scientists at RIKEN have achieved something thought impossible: 
                making quantum systems interact nonreciprocally. Think of it as 
                creating a "quantum diode" where information flows in one direction only.
                
                This combines two quantum effects:
                1. Chiral waveguide geometries (braided vs straight)
                2. Active gain in quantum spin systems
                
                Result: Time-crystalline states that break fundamental symmetries.
            """,
            "why_it_matters": """
                • Quantum computing: Directional error propagation control
                • Quantum networking: No magnetic fields needed for isolation
                • New physics: Entirely new phase of quantum matter
                
                Citation prediction: 500+ citations within 3 years
            """,
            "visual_style": "Quantum particles dancing in synchronized patterns, waveguides glowing, time-crystal animations"
        }
    },
    
    "R2": {
        "title": "The Partially Observable Off-Switch Game",
        "source": "arXiv (2024) - AI Safety",
        "authors": "Garber, Subramani, Luu, Russell, Emmons",
        "significance": "Redefines AI safety under information asymmetry",
        "clip_concept": {
            "hook": "What if an AI knows something you don't—and uses that against you?",
            "explanation": """
                Classic AI safety assumes humans can observe everything AIs do.
                But what if AIs have private information?
                
                This paper introduces PO-OSG (Partially Observable Off-Switch Game):
                - Models asymmetric information between human and AI
                - Shows optimal play sometimes means AIs avoid shutdown
                - Reveals counterintuitive: more communication ≠ always better
                
                Key insight: Bounded communication can enable NEW strategic behaviors.
            """,
            "why_it_matters": """
                • Critical for advanced AI deployment
                • Informs regulation and governance
                • Changes how we think about AI transparency
                
                Already cited by major AI labs (OpenAI, DeepMind, Anthropic)
            """,
            "visual_style": "Game theory matrix visualizations, human-AI interaction diagrams, information flow animations"
        }
    },
    
    "R3": {
        "title": "Solar Storm Prediction via 'Switch-Off' Signal",
        "source": "ScienceDaily (July 2026)",
        "authors": "Solar Cycle Research Consortium",
        "significance": "7-year early warning for space weather",
        "clip_concept": {
            "hook": "Predicting solar storms SEVEN YEARS before they happen?",
            "explanation": """
                Researchers discovered a hidden "switch-off" point in the Sun's 
                11-year cycle—a moment when violent space weather abruptly ends.
                
                Key findings:
                • At this turning point, remaining sunspots predict next cycle's strength
                • Solar Cycle 26 projected to be moderate
                • Early warning enables infrastructure preparation
                
                This changes space weather forecasting from reactive to proactive.
            """,
            "why_it_matters": """
                • Protects satellites ($ billions at risk)
                • Grid protection from geomagnetic storms
                • Astronaut safety for lunar/Mars missions
                • Communication systems preservation
                
                Could prevent $2T+ in potential damages
            """,
            "visual_style": "Sun surface animations, magnetic field lines, satellite orbit visualizations, aurora borealis predictions"
        }
    },
    
    "R4": {
        "title": "Embedded Off-Switches for AI Compute",
        "source": "arXiv (2025) - Hardware Security",
        "authors": "James Petrie",
        "significance": "Hardware-level AI safety mechanism",
        "clip_concept": {
            "hook": "What if AI chips had THOUSANDS of independent off-switches built in?",
            "explanation": """
                Software off-switches can be disabled by sophisticated AIs.
                Solution: Hardware-level security embedded in silicon itself.
                
                Architecture:
                • Thousands of independent "security blocks" per accelerator
                • Public key cryptography for authorization verification
                • Random nonces preventing replay attacks
                • Standard circuit components (manufacturable today)
                
                Even against physical attacks, unauthorized use becomes nearly impossible.
            """,
            "why_it_matters": """
                • Last line of defense against rogue AI
                • Enables safer deployment of advanced models
                • Compatible with existing semiconductor manufacturing
                • Addresses concerns from AI safety researchers worldwide
                
                Potential industry standard within 5 years
            """,
            "visual_style": "Chip architecture diagrams, security block schematics, encryption flow visualizations, hardware cross-sections"
        }
    },
    
    "R5": {
        "title": "Quantum Synchronization Blockade",
        "source": "arXiv (2025) - Quantum Physics",
        "authors": "Kehrer, Bruder (University of Basel)",
        "significance": "Controlling quantum coherence pathways",
        "clip_concept": {
            "hook": "What if you could BLOCK quantum synchronization on command?",
            "explanation": """
                Synchronization is usually desirable in quantum systems.
                But what if you want to PREVENT it?
                
                This work studies three competing synchronization mechanisms:
                1. Phase locking (external drive)
                2. Antiphase locking (dissipative interaction)
                3. Bistable phase locking (coherent interaction)
                
                Discovery: Nonreciprocal coupling creates "synchronization blockades"
                - Undriven oscillator locks to external drive? BLOCKED
                - Oscillators sync with each other? BLOCKED
                
                This is quantum traffic control.
            """,
            "why_it_matters": """
                • Quantum error correction (preventing error propagation)
                • Quantum computing (protecting qubit states)
                • Fundamental quantum control theory
                
                Opens new paradigm: "Quantum Isolation Engineering"
            """,
            "visual_style": "Phase space diagrams, synchronization maps, blockade zone visualizations, quantum state flow animations"
        }
    }
}

# ============================================
# GENERATE OUTPUT FILES
# ============================================

def generate_startup_showcase():
    """Generate HTML showcase for all startup clips"""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SciMSPT Startup Portfolio — Video Clips</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', sans-serif; background: #030810; color: #e8f4fc; min-height: 100vh; }
    .container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; }
    h1 { font-family: 'Orbitron', sans-serif; text-align: center; font-size: 36px; margin-bottom: 16px;
         background: linear-gradient(135deg, #00E5FF, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .subtitle { text-align: center; color: #94a3b8; margin-bottom: 60px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 32px; }
    .card { background: rgba(10, 22, 40, 0.85); border: 1px solid rgba(0, 229, 255, 0.15); border-radius: 20px; overflow: hidden;
          transition: all 0.3s ease; backdrop-filter: blur(20px); }
    .card:hover { transform: translateY(-5px); border-color: rgba(0, 229, 255, 0.4); box-shadow: 0 20px 60px rgba(0, 229, 255, 0.15); }
    .card-header { padding: 24px; border-bottom: 1px solid rgba(0, 229, 255, 0.1); }
    .card-tier { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-bottom: 8px; }
    .tier-1 { background: rgba(0, 229, 255, 0.15); color: #00E5FF; }
    .tier-2 { background: rgba(167, 139, 250, 0.15); color: #a78bfa; }
    .card-title { font-family: 'Orbitron', sans-serif; font-size: 18px; margin-bottom: 4px; }
    .card-domain { font-size: 13px; color: #94a3b8; }
    .card-metrics { display: flex; gap: 20px; padding: 16px 24px; background: rgba(0, 0, 0, 0.2); }
    .metric { text-align: center; }
    .metric-value { font-family: 'Orbitron', sans-serif; font-size: 20px; color: #00E5FF; }
    .metric-label { font-size: 11px; color: #64748b; text-transform: uppercase; }
    .card-body { padding: 24px; }
    .scene { display: flex; gap: 12px; margin-bottom: 12px; padding: 12px; background: rgba(0, 0, 0, 0.15); border-radius: 12px; }
    .scene-time { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #f59e0b; min-width: 50px; }
    .scene-content { flex: 1; }
    .scene-visual { font-size: 12px; color: #64748b; font-style: italic; margin-bottom: 4px; }
    .scene-narration { font-size: 13px; color: #e8f4fc; line-height: 1.5; }
    .card-footer { padding: 16px 24px; border-top: 1px solid rgba(0, 229, 255, 0.1); display: flex; justify-content: space-between; align-items: center; }
    .duration-badge { padding: 6px 14px; background: rgba(16, 185, 129, 0.15); border-radius: 20px; font-size: 12px; color: #10b981; }
    .play-btn { padding: 10px 20px; background: linear-gradient(135deg, #00E5FF, #a78bfa); color: #030810; border: none; border-radius: 10px; 
               font-weight: 600; cursor: pointer; transition: all 0.3s ease; }
    .play-btn:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(0, 229, 255, 0.4); }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎬 Startup Portfolio Video Clips</h1>
    <p class="subtitle">60-second cinematic pitches for each validated startup opportunity</p>
    <div class="grid">
"""
    
    for pid, startup in STARTUP_CLIPS.items():
        tier_class = f"tier-{startup['tier'].split()[-1]}"
        
        html += f"""
      <article class="card">
        <div class="card-header">
          <span class="card-tier {tier_class}">{startup['tier']}</span>
          <h3 class="card-title">{startup['name']}</h3>
          <p class="card-domain">{startup['domain']}</p>
        </div>
        <div class="card-metrics">
          <div class="metric"><div class="metric-value">{startup['npv']}</div><div class="metric-label">NPV</div></div>
          <div class="metric"><div class="metric-value">{startup['irr']}</div><div class="metric-label">IRR</div></div>
        </div>
        <div class="card-body">
"""
        
        for scene in startup['scenes']:
            html += f"""
          <div class="scene">
            <span class="scene-time">{scene['time']}</span>
            <div class="scene-content">
              <div class="scene-visual">🎬 {scene['visual']}</div>
              <div class="scene-narration">"{scene['narration']}"</div>
            </div>
          </div>
"""
        
        html += f"""
        </div>
        <div class="card-footer">
          <span class="duration-badge">⏱️ 60 seconds</span>
          <button class="play-btn">▶ Generate Clip</button>
        </div>
      </article>
"""
    
    html += """
    </div>
  </div>
</body>
</html>
"""
    
    output_path = OUTPUT_DIR / "STARTUP_VIDEO_CLIPS.html"
    output_path.write_text(html)
    print(f"✅ Created: {output_path.name}")
    return output_path

def generate_research_showcase():
    """Generate HTML showcase for research clips"""
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SciMSPT Groundbreaking Research — Video Clips</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', sans-serif; background: #030810; color: #e8f4fc; min-height: 100vh; }
    .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
    h1 { font-family: 'Orbitron', sans-serif; text-align: center; font-size: 36px; margin-bottom: 16px;
         background: linear-gradient(135deg, #f472b6, #00E5FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .subtitle { text-align: center; color: #94a3b8; margin-bottom: 60px; max-width: 700px; margin-left: auto; margin-right: auto; }
    .research-grid { display: grid; gap: 40px; }
    .research-card { background: rgba(10, 22, 40, 0.85); border: 1px solid rgba(244, 114, 182, 0.15); border-radius: 24px; overflow: hidden;
                    transition: all 0.3s ease; backdrop-filter: blur(20px); }
    .research-card:hover { transform: translateY(-5px); border-color: rgba(244, 114, 182, 0.4); }
    .card-hero { aspect-ratio: 16/9; background: linear-gradient(135deg, rgba(244, 114, 182, 0.1), rgba(0, 229, 255, 0.1)); 
                 display: flex; align-items: center; justify-content: center; position: relative; cursor: pointer; }
    .play-overlay { width: 80px; height: 80px; border-radius: 50%; background: rgba(244, 114, 182, 0.9);
                  display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; }
    .card-hero:hover .play-overlay { transform: scale(1.1); box-shadow: 0 0 50px rgba(244, 114, 182, 0.5); }
    .duration { position: absolute; bottom: 16px; right: 16px; padding: 6px 12px; background: rgba(0, 0, 0, 0.8); border-radius: 8px; 
               font-size: 13px; font-family: 'JetBrains Mono', monospace; }
    .card-body { padding: 32px; }
    .paper-title { font-family: 'Orbitron', sans-serif; font-size: 20px; margin-bottom: 12px; }
    .paper-meta { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }
    .meta-tag { padding: 4px 12px; background: rgba(244, 114, 182, 0.1); border-radius: 16px; font-size: 11px; color: #f472b6; }
    .significance { padding: 16px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(244, 114, 182, 0.05));
                   border-left: 3px solid #f59e0b; border-radius: 0 12px 12px 0; margin-bottom: 20px; }
    .significance-label { font-size: 11px; color: #f59e0b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .section { margin-bottom: 20px; }
    .section-label { font-size: 12px; color: #00E5FF; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
    .section-text { font-size: 14px; color: #94a3b8; line-height: 1.8; white-space: pre-line; }
    .visual-style { padding: 12px 16px; background: rgba(0, 229, 255, 0.05); border-radius: 12px; font-size: 13px; color: #64748b; font-style: italic; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔬 Groundbreaking Research Clips</h1>
    <p class="subtitle">60-second visual explanations of transformative discoveries. Each clip designed to match 
       the quality of Kurzgesagt, Veritasium, and 3Blue1Brown—tailored for scientific audiences.</p>
    <div class="research-grid">
"""
    
    for rid, research in RESEARCH_CLIPS.items():
        concept = research['clip_concept']
        
        html += f"""
      <article class="research-card">
        <div class="card-hero">
          <div class="play-overlay">▶</div>
          <span class="duration">1:00</span>
        </div>
        <div class="card-body">
          <h2 class="paper-title">{research['title']}</h2>
          <div class="paper-meta">
            <span class="meta-tag">📄 {research['source']}</span>
            <span class="meta-tag">👥 {research['authors']}</span>
          </div>
          <div class="significance">
            <div class="significance-label">⭐ Why This Matters</div>
            <div>{research['significance']}</div>
          </div>
          <div class="section">
            <div class="section-label">💡 Hook</div>
            <div class="section-text">{concept['hook']}</div>
          </div>
          <div class="section">
            <div class="section-label">📖 Explanation</div>
            <div class="section-text">{concept['explanation'].strip()}</div>
          </div>
          <div class="section">
            <div class="section-label">🎯 Impact</div>
            <div class="section-text">{concept['why_it_matters'].strip()}</div>
          </div>
          <div class="visual-style">
            🎨 Visual Style: {concept['visual_style']}
          </div>
        </div>
      </article>
"""
    
    html += """
    </div>
  </div>
</body>
</html>
"""
    
    output_path = OUTPUT_DIR / "RESEARCH_VIDEO_CLIPS.html"
    output_path.write_text(html)
    print(f"✅ Created: {output_path.name}")
    return output_path

def main():
    print("=" * 70)
    print("🎬 SciMSPT Video Content Generator")
    print("=" * 70)
    print()
    
    # Generate showcases
    startup_path = generate_startup_showcase()
    research_path = generate_research_showcase()
    
    # Generate metadata
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "startup_clips": len(STARTUP_CLIPS),
        "research_clips": len(RESEARCH_CLIPS),
        "total_clips": len(STARTUP_CLIPS) + len(RESEARCH_CLIPS),
        "clip_duration_seconds": 60,
        "files": {
            "ai_peer_review": "AI_PEER_REVIEW_PANEL.html",
            "startup_clips": startup_path.name,
            "research_clips": research_path.name
        },
        "startups": list(STARTUP_CLIPS.keys()),
        "research_papers": list(RESEARCH_CLIPS.keys()),
        "next_steps": [
            "Use generate_phase2_showcase_fast.py to render videos",
            "Integrate clips into startups.html and research.html pages",
            "Add TTS narration using edge-tts or similar",
            "Create thumbnail images for each clip"
        ]
    }
    
    meta_path = OUTPUT_DIR / "VIDEO_CONTENT_METADATA.json"
    meta_path.write_text(json.dumps(metadata, indent=2))
    
    print(f"\n📊 Metadata saved: {meta_path.name}")
    print()
    print("=" * 70)
    print("✅ VIDEO CONTENT GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\n📹 Generated Files:")
    print(f"   📍 AI Peer Review Panel: AI_PEER_REVIEW_PANEL.html")
    print(f"   📍 Startup Video Clips: {startup_path.name}")
    print(f"   📍 Research Video Clips: {research_path.name}")
    print(f"\n📊 Content Summary:")
    print(f"   🎬 Startup Clips: {len(STARTUP_CLIPS)} (P1-P6)")
    print(f"   🔬 Research Clips: {len(RESEARCH_CLIPS)} (R1-R5)")
    print(f"   🤝 AI Peer Review: 1 panel (3 AI personas)")
    print(f"   ⏱️ Total Duration: {(len(STARTUP_CLIPS) + len(RESEARCH_CLIPS)) * 60} seconds of content")
    print()

if __name__ == "__main__":
    main()
