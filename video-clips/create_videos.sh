#!/bin/bash
# Quick video generation script for SciMSPT startup clips

cd /home/z/my-project/SciMSPT/video-clips

echo "🎬 Creating video clips..."
echo ""

# Create output directory if not exists
mkdir -p output

# Video creation function
create_video() {
    local id="$1"
    local name="$2"
    local image="./images/${id}_hero.png"
    local audio="./audio/${id}_narration.wav"
    local output="./output/${id}_${name// /_}.mp4"
    
    if [ ! -f "$audio" ]; then
        echo "⚠️  Skipping $id - no audio file"
        return 1
    fi
    
    echo "📹 Creating: $name"
    
    # Get duration
    local duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$audio" 2>/dev/null)
    duration=${duration%.*}
    
    # Use ultrafast preset for speed
    timeout 45 ffmpeg -y \
        -loop 1 \
        -i "$image" \
        -i "$audio" \
        -c:v libx264 \
        -tune stillimage \
        -preset ultrafast \
        -crf 28 \
        -c:a aac \
        -b:a 128k \
        -pix_fmt yuv420p \
        -r 24 \
        -t "$duration" \
        -shortest \
        -movflags +faststart \
        "$output" 2>/dev/null
    
    if [ $? -eq 0 ] && [ -f "$output" ]; then
        size=$(du -h "$output" | cut -f1)
        echo "   ✅ $name ($size, ${duration}s)"
    else
        echo "   ⚠️  $name failed or incomplete"
    fi
}

# Generate videos for each startup (only where audio exists)
create_video "P1" "Stellarator_Fusion"
create_video "P2" "SMR_Fleet_OS"
create_video "P3" "Solid-State_Battery"
create_video "P4" "Iron-Air_LDES"
create_video "P5" "Super-Steel_Electrolyzer"
create_video "P6" "Detonation_H2_Turbine"

echo ""
echo "📁 Generated files:"
ls -lh output/*.mp4 2>/dev/null || echo "   No MP4 files yet"

echo ""
echo "✅ Video generation complete!"
