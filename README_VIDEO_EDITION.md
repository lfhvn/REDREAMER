# REDREAMER 2025 Video Edition 🌙✨🎬

**Generate AI dreams as both text AND video**

Transform textual dream narratives into surreal video visualizations using state-of-the-art language models and text-to-video generation.

---

## ⚡ Quick Start (3 Minutes)

```bash
# Install dependencies
pip install torch transformers

# Generate a dream (text only)
python redreamer_video.py --prompt "I was flying over a city of glass"

# Output: dream_text.txt with full narrative
```

That's it! You now have AI-generated dream text.

---

## 🎬 Generate Videos Too

### Option 1: Local Generation (Free, requires GPU)

```bash
# Install video dependencies
pip install diffusers accelerate

# Generate dream + video
python redreamer_video.py \
    --prompt "I was walking through a forest of crystal trees" \
    --backend local
```

**Requirements:** NVIDIA GPU with 16GB+ VRAM

---

### Option 2: Runway API (Best Quality)

```bash
# Set API key
export RUNWAY_API_KEY="your_key_here"

# Generate dream + video
python redreamer_video.py \
    --prompt "I found myself in a library where books flew like birds" \
    --backend runway \
    --api-key $RUNWAY_API_KEY
```

**Cost:** ~$0.25-0.50 per dream video

---

### Option 3: Luma Dream Machine (Dream-Focused)

```bash
export LUMA_API_KEY="your_key_here"

python redreamer_video.py \
    --prompt "I was swimming through clouds" \
    --backend luma \
    --api-key $LUMA_API_KEY
```

**Cost:** $30/month unlimited or free tier (30/month)

---

## 🎨 Dream Styles

Choose the mood of your dream:

```bash
# Surreal (default) - Weird dream logic
python redreamer_video.py --prompt "I saw a door" --style surreal

# Nightmare - Dark, scary atmosphere
python redreamer_video.py --prompt "I was being chased" --style nightmare

# Lucid - Clear, controlled dreaming
python redreamer_video.py --prompt "I was aware I was dreaming" --style lucid

# Realistic - More grounded dream
python redreamer_video.py --prompt "I was at my old school" --style realistic
```

---

## 📁 What Gets Generated

```
output/
├── dream_text.txt           # Full dream narrative
├── scene_1.mp4             # Video for scene 1
├── scene_2.mp4             # Video for scene 2
└── scene_3.mp4             # Video for scene 3
```

---

## 🏗️ Architecture

### Text Generation
- **Model:** GPT-2 Medium (355M params) or custom fine-tuned
- **Dataset:** Can be fine-tuned on DreamBank (27K dreams)
- **Sampling:** Creative parameters for surreal output

### Video Generation
- **Local:** Stable Diffusion → Stable Video Diffusion
- **Runway:** Gen-3 Alpha Turbo API
- **Luma:** Dream Machine API

### Pipeline
```
User Prompt
    ↓
Dream Text Generation (LLM)
    ↓
Scene Extraction (NLP)
    ↓
Prompt Enhancement (Add cinematic keywords)
    ↓
Video Generation (Text-to-Video)
    ↓
Post-Processing (FFmpeg)
    ↓
Final Dream Video
```

---

## 📦 Installation

### Minimal (Text Only)
```bash
pip install torch transformers
```

### Full (Local Video)
```bash
pip install torch transformers diffusers accelerate
pip install opencv-python ffmpeg-python
```

### From Requirements
```bash
pip install -r requirements_2025.txt
```

---

## 🔧 Advanced Usage

### Custom Model
```bash
python redreamer_video.py \
    --prompt "I was..." \
    --model "path/to/your/finetuned-model"
```

### Multiple Dreams
```bash
for prompt in "flying" "falling" "running"; do
    python redreamer_video.py --prompt "I was $prompt" --style surreal
done
```

### Batch Processing
```python
from redreamer_video import DreamVideoGenerator

generator = DreamVideoGenerator(video_backend="runway", api_key="...")

prompts = ["I was flying", "I saw a door", "I was falling"]
for prompt in prompts:
    generator.create_dream_video(prompt, output_dir=f"dream_{i}")
```

---

## 💰 Cost Comparison

| Backend | Setup | Per Dream | Quality | Speed | GPU Needed |
|---------|-------|-----------|---------|-------|------------|
| **Text Only** | $0 | $0 | - | 5s | No |
| **Local Video** | $0 | $0 | ⭐⭐⭐ | 5-10min | Yes (16GB+) |
| **Runway** | $15-35/mo | $0.25-0.50 | ⭐⭐⭐⭐ | 30-60s | No |
| **Luma** | $30/mo | $0.10 | ⭐⭐⭐⭐ | 2-3min | No |

---

## 🎓 Learn More

### Documentation
- **[Implementation Comparison](IMPLEMENTATION_COMPARISON.md)** - Which approach to choose
- **[Video Generation Design](VIDEO_GENERATION_DESIGN.md)** - Full technical design
- **[Research Papers](RESEARCH_PAPERS.md)** - Latest academic research
- **[2025 Assessment](REDREAMER_2025_ASSESSMENT.md)** - Complete modernization plan

### Examples
See `examples/` directory for:
- Custom model fine-tuning
- Batch dream generation
- Style transfer
- Audio integration

---

## 🌟 Features

### Current
- ✅ Text generation with multiple styles
- ✅ Scene extraction from narratives
- ✅ Local video generation (SD + SVD)
- ✅ Runway API integration
- ✅ Luma API integration
- ✅ Command-line interface

### Coming Soon
- 🔜 Web UI (Gradio)
- 🔜 Audio generation
- 🔜 Voice narration
- 🔜 Multi-video compilation
- 🔜 Style transfer
- 🔜 Dream interpretation mode

---

## 🤝 Contributing

This is an open research project! Contributions welcome:

1. Fine-tune on larger dream corpora
2. Add new video backends
3. Improve scene extraction
4. Create better prompts
5. Build UI/UX

---

## 📊 Quality Examples

### Input Prompt
```
"I was walking through a library"
```

### Generated Text
```
I was walking through a library where the books flew like birds through
infinite corridors. The shelves stretched upward into darkness, defying
all geometry. A mysterious figure stood in the shadows, holding a book
that glowed with an ethereal light. When I approached, the figure dissolved
into pages that scattered like leaves in an impossible wind.
```

### Extracted Scenes
1. "library where books flew like birds through infinite corridors"
2. "shelves stretched upward into darkness defying geometry"
3. "mysterious figure in shadows holding glowing book"
4. "figure dissolved into pages scattered like leaves"

### Enhanced for Video
1. "library where books fly like birds through infinite corridors, cinematic,
    dreamlike atmosphere, surreal, soft lighting, ethereal mood, 4k quality"

...and so on for each scene.

---

## 🐛 Troubleshooting

### "CUDA out of memory"
```bash
# Use smaller batch size or CPU
python redreamer_video.py --prompt "..." --backend runway
# (API doesn't use your GPU)
```

### "API key invalid"
```bash
# Check your API key
echo $RUNWAY_API_KEY

# Or pass directly
python redreamer_video.py --api-key "sk-..."
```

### "No scenes extracted"
The dream text might be too abstract. Try:
- More specific prompts
- Different styles
- Adjust scene extraction logic

---

## 📄 License

MIT License - see LICENSE file

Original REDREAMER by [@lfhvn](https://github.com/lfhvn)
2025 Video Edition modernization

---

## 🙏 Acknowledgments

### Research
- DreamBank corpus (27K dreams)
- OpenAI GPT architecture
- Stability AI (Stable Diffusion)
- Meta AI (LLaMA models)

### Video Generation
- Runway ML (Gen-3)
- Luma Labs (Dream Machine)
- Stability AI (SVD)

### Community
- HuggingFace team
- r/StableDiffusion
- Dream research community

---

## 📚 Citation

If you use this in research:

```bibtex
@software{redreamer2025,
  title={REDREAMER 2025: Dream-to-Video Generation},
  author={[Your Name]},
  year={2025},
  url={https://github.com/lfhvn/REDREAMER}
}
```

---

## 🌙 Examples Gallery

*Coming soon: See our gallery of generated dream videos*

- Surreal landscapes
- Impossible architecture
- Dream logic sequences
- Nightmare atmospheres
- Lucid dream visualizations

---

**Sweet dreams! 🌙✨🎬**

*For questions, issues, or to share your dream videos, open an issue on GitHub.*
