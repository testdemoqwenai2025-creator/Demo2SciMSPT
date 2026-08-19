#!/bin/bash

# SciMSPT 60-Second Startup Video Clip Generator
# Generates professional video clips with UK/US native narration and AI imagery

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
IMAGES_DIR="$SCRIPT_DIR/images"
AUDIO_DIR="$SCRIPT_DIR/audio"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Ensure directories exist
mkdir -p "$IMAGES_DIR" "$AUDIO_DIR" "$OUTPUT_DIR"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     SciMSPT 60-Second Startup Video Clip Generator          ║"
echo "║     UK/US Native Voice Narration + AI Imagery              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Define startups array with their details
declare -A STARTUP_NAMES=(
    ["P1"]="Stellarator Fusion"
    ["P2"]="SMR Fleet OS"
    ["P3"]="Solid-State Battery"
    ["P4"]="Iron-Air LDES"
    ["P5"]="Super-Steel Electrolyzer"
    ["P6"]="Detonation H2 Turbine"
    ["P7"]="Room-Temp Quantum Materials"
)

declare -A STARTUP_DOMAINS=(
    ["P1"]="Nuclear Fusion · Compact Stellarators"
    ["P2"]="Nuclear · Small Modular Reactors"
    ["P3"]="Energy Storage · Next-Gen Batteries"
    ["P4"]="Grid Storage · Long-Duration"
    ["P5"]="Hydrogen · Green H2 Production"
    ["P6"]="Hydrogen · Rotating Detonation"
    ["P7"]="Quantum · Superconductors"
)

# Narration Scripts (~150 words each for 60 seconds at normal speaking pace)
declare -A NARRATION_SCRIPTS=(
["P1"]="Stellarator Fusion represents the frontier of clean energy research, born from groundbreaking papers published in Physical Review Letters and Nature Energy.

The journey began with fundamental research into optimized magnetic geometry for compact stellarators. Scientists discovered that by carefully engineering plasma confinement configurations, they could achieve stable fusion reactions without the complexities of tokamak designs.

Key breakthroughs included advanced tritium breeding blanket materials and high-temperature superconducting coils that dramatically improved efficiency. The pivotal moment came when researchers demonstrated net energy gain in compact fusion devices, proving commercial viability was within reach.

Today, Stellarator Fusion stands as a transformative opportunity with a net present value of five hundred eighty-nine million dollars and a sixty-five point seven percent probability of exceeding fifteen percent internal rate of return. This is not merely scientific progress; it is the dawn of virtually limitless clean energy."

["P2"]="SMR Fleet OS emerged from critical research published in Applied Energy and Annals of Nuclear Energy, addressing the operational challenges of Small Modular Reactors.

The original research focused on artificial intelligence-driven load balancing for distributed nuclear power generation. Unlike traditional large reactors, SMRs require sophisticated fleet management systems to optimize output across multiple units.

Scientists developed predictive maintenance frameworks using digital twin technology, enabling operators to anticipate issues before they occur. The regulatory automation component was particularly groundbreaking, simplifying compliance across complex nuclear regulatory environments.

The startup opportunity is compelling: fifty million dollars in net present value with a twenty-three percent internal rate of return. With sixty-eight point eight percent probability of positive NPV, SMR Fleet OS represents the software infrastructure layer essential for the nuclear renaissance."

["P3"]="Solid-State Battery technology traces its origins to seminal research in Nature Energy and Joule, promising to revolutionize energy storage through sulfide-based electrolytes.

The foundational work demonstrated that solid-state architectures could achieve energy densities exceeding five hundred watt-hours per kilogram, nearly double current lithium-ion capabilities. More critically, these batteries eliminate thermal runaway risk entirely, solving the safety concerns that have plagued electric vehicle adoption.

Research published in Advanced Energy Materials proved fast charging capabilities under fifteen minutes, while studies in ACS Applied Materials showed cycle lives exceeding two thousand charges. The manufacturing scale-up pathways documented in Electrochimica Acta confirm commercial feasibility.

With five hundred eighty-seven million dollars in NPV and tier-one venture status, Solid-State Battery represents the most significant advancement in energy storage since the original lithium-ion revolution."

["P4"]="Iron-Air LDES addresses grid-scale storage through revolutionary chemistry first detailed in Science and Joule journals.

The research journey began with scientists seeking ultra-low-cost storage solutions using earth-abundant materials. Iron-air chemistry emerged as the answer, offering energy storage costs of just twenty dollars per kilowatt-hour, a fraction of lithium-ion alternatives.

Breakthrough publications demonstrated one hundred plus hour discharge capabilities, making iron-air ideal for renewable grid stabilization. When solar and wind generation fluctuate, long-duration storage bridges the gap, storing energy for days rather than hours.

The market opportunity is substantial: forty-four million dollars NPV with twenty-three point four percent IRR. At sixty-eight percent probability of success, Iron-Air LDES enables the fully renewable grid that climate commitments demand."

["P5"]="Super-Steel Electrolyzer transforms green hydrogen production through innovations documented in Nature Catalysis and Advanced Materials.

The core challenge has been cost: producing green hydrogen at one dollar fifty per kilogram requires extraordinary efficiency gains. Researchers achieved this through nanostructured super-steel electrodes that dramatically improve water electrolysis performance.

Critical advances include variable renewable integration capabilities, allowing electrolyzers to operate efficiently with intermittent wind and solar input. Durability studies confirmed extended operational lifetimes, addressing previous degradation concerns.

With forty-three million dollars NPV and seventeen point seven percent IRR, Super-Steel Electrolyzer positions investors at the center of the hydrogen economy. This technology makes green hydrogen cost-competitive with fossil alternatives."

["P6"]="Detonation H2 Turbine leverages rotating detonation engine technology from Progress in Energy and Combustion Science and AIAA Journal research.

Conventional hydrogen turbines suffer from efficiency limitations that detonation engines overcome. The research demonstrates fifteen percent efficiency improvements through continuous detonation wave propagation, a fundamentally different approach to combustion.

Applications span multiple markets: aviation demands high power density for next-generation aircraft, marine shipping requires clean propulsion solutions, and grid peaking needs rapid-response generation capacity. The versatility of this technology creates multiple revenue streams.

Thirty-four million dollars NPV with twenty-three point three percent IRR reflects strong fundamentals. At sixty-nine percent success probability, Detonation H2 Turbine offers exposure to the hydrogen transition across transportation and energy sectors."

["P7"]="Room-Temp Quantum Materials represents perhaps the most transformative opportunity, emerging from landmark Nature publications on ambient-condition superconductivity.

For decades, superconductivity required extreme cryogenic cooling, limiting practical applications. Research breakthroughs changed everything: layered materials exhibiting superconducting properties at room temperature, topological quantum states persisting without specialized cooling systems.

The implications are profound: lossless power transmission over continental distances, quantum computing interconnects operating at room temperature, sensors with unprecedented sensitivity. Each application represents a multi-billion-dollar market.

While earlier-stage than other opportunities, the potential justifies the valuation: one hundred seven million dollars NPV with thirty-four point three percent IRR. At seventy-seven percent success probability, Room-Temp Quantum Materials offers asymmetric upside that could redefine multiple industries."
)

# Image prompts for each startup (for AI image generation)
declare -A IMAGE_PROMPTS=(
["P1"]="Futuristic nuclear fusion stellarator reactor, glowing plasma contained in magnetic fields, blue and purple plasma glow, advanced scientific facility, clean energy concept, cinematic lighting, photorealistic, 8k quality"

["P2"]="Modern small modular reactor control room with holographic displays showing AI-driven fleet management, digital twin visualization, futuristic nuclear plant interface, professional industrial design, blue tones, high-tech aesthetic"

["P3"]="Cutaway view of solid-state battery technology, layered structure visible, sulfide electrolyte glowing with energy, electric vehicle charging rapidly, futuristic battery laboratory, cyan and white color scheme, scientific illustration style"

["P4"]="Massive iron-air battery installation for grid storage, renewable energy farm background, giant battery containers, sustainable energy storage concept, golden hour lighting, industrial scale, environmental harmony"

["P5"]="Advanced electrolyzer system producing green hydrogen, nanostructured steel electrodes visible, hydrogen bubbles forming, clean energy facility, water splitting process visualization, teal and silver colors, modern industrial design"

["P6"]="Cross-section of rotating detonation engine, hydrogen combustion visible, turbine blades spinning, aviation and power applications, dynamic energy release visualization, orange and blue flame colors, engineering precision"

["P7"]="Quantum material structure at room temperature, superconducting currents flowing, topological patterns visible, quantum computing interface, lossless power transmission concept, purple and gold hues, futuristic laboratory setting"
)

# Function to generate TTS audio using z-ai CLI
generate_audio() {
    local startup_id="$1"
    local script="$2"
    local output_path="$AUDIO_DIR/${startup_id}_narration.wav"
    
    echo "🎙️  Generating narration for ${STARTUP_NAMES[$startup_id]}..."
    
    # Use z-ai TTS CLI with 'jam' voice (British English gentleman)
    # Speed 0.9 for slightly slower, more dramatic delivery
    z-ai tts \
        --input "$script" \
        --output "$output_path" \
        --voice jam \
        --speed 0.9 \
        --format wav
    
    if [ $? -eq 0 ]; then
        echo "✅ Audio saved: $output_path"
    else
        echo "❌ Failed to generate audio for $startup_id"
        return 1
    fi
}

# Function to generate images using z-ai CLI
generate_image() {
    local startup_id="$1"
    local prompt="$2"
    local output_path="$IMAGES_DIR/${startup_id}_hero.png"
    
    echo "🎨  Generating image for ${STARTUP_NAMES[$startup_id]}..."
    
    # Use z-ai image generation CLI
    z-ai image-gen \
        --prompt "$prompt" \
        --output "$output_path" \
        --size 1920x1080
    
    if [ $? -eq 0 ]; then
        echo "✅ Image saved: $output_path"
    else
        echo "⚠️  Using fallback image for $startup_id"
        # Create a gradient placeholder if image gen fails
        convert -size 1920x1080 \
            gradient:'#0a1628'-'#1a365d' \
            -gravity center \
            -fill '#4da8da' \
            -font 'DejaVu-Sans-Bold' \
            -pointsize 72 \
            -annotate 0 "${STARTUP_NAMES[$startup_id]}" \
            "$output_path" 2>/dev/null || touch "$output_path"
    fi
}

# Function to create video clip using ffmpeg
create_video() {
    local startup_id="$1"
    local audio_path="$AUDIO_DIR/${startup_id}_narration.wav"
    local image_path="$IMAGES_DIR/${startup_id}_hero.png"
    local video_path="$OUTPUT_DIR/${startup_id}_${STARTUP_NAMES[$startup_id]// /_}.mp4"
    
    echo "🎬  Creating video for ${STARTUP_NAMES[$startup_id]}..."
    
    # Get audio duration
    local duration=$(ffprobe -i "$audio_path" -show_entries format=duration -v quiet -of csv="p=0" 2>/dev/null || echo "60")
    duration=${duration%.*}  # Remove decimal
    
    # Create video with:
    # - Loop image for full audio duration
    # - Add fade effects
    # - Overlay text with startup name
    ffmpeg -y \
        -loop 1 \
        -i "$image_path" \
        -i "$audio_path" \
        -c:v libx264 \
        -tune stillimage \
        -c:a aac \
        -b:a 192k \
        -pix_fmt yuv420p \
        -t "$duration" \
        -vf "
            scale=1920:1080:force_original_aspect_ratio=decrease,
            pad=1920:1080:(ow-iw)/2:(oh-ih)/2,
            fade=t=in:st=0:d=2,
            fade=t=out:st=$(echo "$duration - 2" | bc):d=2,
            drawtext=text='${STARTUP_NAMES[$startup_id]}':fontsize=48:fontcolor=white@0.9:
            x=(w-text_w)/2:y=h-l-100:
            fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:
            shadowcolor=black@0.7:shadowx=2:shadowy=2,
            drawtext=text='SciMSPT Venture Pipeline':fontsize=24:fontcolor='#4da8da':
            x=(w-text_w)/2:y=h-l-40:
            fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
        " \
        -shortest \
        "$video_path" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Video created: $video_path"
        
        # Get file size
        local size=$(du -h "$video_path" | cut -f1)
        echo "   📊 Size: $size | Duration: ~${duration}s"
    else
        echo "❌ Failed to create video for $startup_id"
        return 1
    fi
}

# Main execution loop
echo ""
echo "🚀 Starting video clip generation for all 7 startups..."
echo ""

for P in P1 P2 P3 P4 P5 P6 P7; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Processing: ${STARTUP_NAMES[$P]}"
    echo "Domain: ${STARTUP_DOMAINS[$P]}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Step 1: Generate narration audio
    generate_audio "$P" "${NARRATION_SCRIPTS[$P]}"
    
    # Step 2: Generate hero image
    generate_image "$P" "${IMAGE_PROMPTS[$P]}"
    
    # Step 3: Create final video
    create_video "$P"
    
    echo ""
done

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    GENERATION COMPLETE                      ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Output Location: $OUTPUT_DIR"
echo "║  Total Videos Generated: 7                                ║"
echo "║                                                          ║"
echo "║  Voice: jam (British English Gentleman)                  ║"
echo "║  Duration: ~60 seconds each                              ║"
echo "║  Resolution: 1920x1080 (Full HD)                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# List generated files
echo "📁 Generated Files:"
ls -lh "$OUTPUT_DIR/" 2>/dev/null || echo "No files found"
