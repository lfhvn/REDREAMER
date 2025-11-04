# REDREAMER 2025: Video Generation Integration

## Vision: From Dream Text to Dream Video

Transform REDREAMER from text-only to a **full multi-modal dream visualization system** that generates both narrative text and corresponding surreal video sequences.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DREAM GENERATION PIPELINE                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │   Stage 1: Text Generation           │
        │   (GPT-2 / LLaMA with Dream Corpus)  │
        └──────────────────────────────────────┘
                              │
                              ▼
        "I found myself in a library where books
         flew like birds through infinite corridors
         that defied geometry..."
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │   Stage 2: Scene Extraction          │
        │   (Parse dream into video scenes)    │
        └──────────────────────────────────────┘
                              │
                              ▼
        Scene 1: "library where books flew like birds"
        Scene 2: "infinite corridors defying geometry"
        Scene 3: "mysterious figure in shadows"
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │   Stage 3: Prompt Engineering        │
        │   (Optimize for video generation)    │
        └──────────────────────────────────────┘
                              │
                              ▼
        Enhanced prompts with style keywords:
        "cinematic dreamlike library, books flying like birds,
         surreal atmosphere, soft lighting, 4k, ethereal"
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │   Stage 4: Video Generation          │
        │   (Text-to-Video Model)              │
        └──────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        Open Source                 Commercial APIs
        • AnimateDiff              • Runway Gen-3
        • Stable Video             • Luma Dream Machine
        • HunyuanVideo             • Veo 3
                │                           │
                └─────────────┬─────────────┘
                              ▼
        ┌──────────────────────────────────────┐
        │   Stage 5: Post-Processing           │
        │   (Transitions, effects, audio)      │
        └──────────────────────────────────────┘
                              │
                              ▼
        Final Dream Video (.mp4)
        • 5-30 seconds per scene
        • Smooth transitions
        • Optional dreamy audio
        • Subtitles with dream text
```

---

## Text-to-Video Options (2025)

### Option A: Open Source (Self-Hosted)

#### 1. AnimateDiff + Stable Diffusion 1.5
**Best for:** Full control, customization, no usage limits

**Pros:**
- ✅ Free (after GPU cost)
- ✅ Complete control
- ✅ Can train custom models
- ✅ Privacy (local generation)
- ✅ No API rate limits

**Cons:**
- ❌ Complex setup (ComfyUI)
- ❌ Requires powerful GPU (16GB+ VRAM)
- ❌ Slower generation (2-5 min/video)
- ❌ Steep learning curve
- ❌ Quality varies

**Setup:**
```bash
# Install ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# Install AnimateDiff extension
cd custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
cd ..

# Download models
# Motion: guoyww/animatediff (HuggingFace)
# Checkpoint: realisticVisionV60B1_v51VAE
```

**Python Usage:**
```python
# Will require ComfyUI API or custom integration
# See implementation section below
```

**Cost:** $0 (local GPU) or $1-2/hour (cloud GPU)

---

#### 2. Stable Video Diffusion (SVD)
**Best for:** Image-to-video conversion

**Pros:**
- ✅ Simple HuggingFace integration
- ✅ Good quality
- ✅ Direct Python API
- ✅ Well documented

**Cons:**
- ❌ Requires input image first
- ❌ Shorter videos (2-4 seconds)
- ❌ Less control over content
- ❌ 16GB+ VRAM needed

**Python Usage:**
```python
from diffusers import StableVideoDiffusionPipeline
import torch

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")

# First generate an image from dream text
from diffusers import StableDiffusionPipeline
img_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
image = img_pipe("library where books fly like birds").images[0]

# Then convert to video
frames = pipe(image, num_frames=25).frames[0]
```

**Cost:** $0 (local) or $0.50-1/video (cloud)

---

#### 3. HuggingFace Diffusers (ModelScope)
**Best for:** Quick integration, Python-first

**Pros:**
- ✅ Direct text-to-video
- ✅ Simple API
- ✅ HuggingFace ecosystem
- ✅ Easy integration

**Cons:**
- ❌ Deprecated pipeline
- ❌ Lower quality
- ❌ Limited development
- ❌ 16GB+ VRAM

**Python Usage:**
```python
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video

pipe = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b",
    torch_dtype=torch.float16
)
pipe.to("cuda")

video_frames = pipe(
    "A library where books fly like birds through the air",
    num_frames=16,
    num_inference_steps=25
).frames[0]

video_path = export_to_video(video_frames, "dream_scene.mp4")
```

**Cost:** $0 (local) or $0.50/video (cloud)

---

### Option B: Commercial APIs (Recommended for Quality)

#### 1. Runway Gen-3 Alpha Turbo 🏆
**Best overall:** Quality + Speed + Reliability

**Pros:**
- ✅ Excellent quality
- ✅ Fast (20-30 seconds/video)
- ✅ Reliable API
- ✅ Good dream-like aesthetics
- ✅ Up to 10 seconds video

**Cons:**
- ❌ Costs $0.05-0.20/video
- ❌ Requires API key
- ❌ Rate limits
- ❌ No local option

**Pricing:**
- Standard: $15/month (625 credits)
- Pro: $35/month (2250 credits)
- ~1 credit per second of video

**API Usage:**
```python
import requests

def generate_runway_video(prompt, duration=5):
    """Generate video using Runway API"""

    response = requests.post(
        "https://api.runwayml.com/v1/generate",
        headers={
            "Authorization": f"Bearer {RUNWAY_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "prompt": prompt,
            "duration": duration,
            "model": "gen3-alpha-turbo",
            "options": {
                "style": "surreal",
                "quality": "high"
            }
        }
    )

    return response.json()["video_url"]
```

**Cost per dream:** $0.25-0.50 (5-10 second video)

---

#### 2. Luma Dream Machine
**Best for:** Surreal dream aesthetics

**Pros:**
- ✅ Specifically designed for "dreams"
- ✅ Excellent surreal style
- ✅ Good motion quality
- ✅ Free tier available

**Cons:**
- ❌ Newer service (less mature)
- ❌ Limited API documentation
- ❌ Slower than Runway
- ❌ Queue times

**Pricing:**
- Free: 30 generations/month
- Standard: $29.99/month (unlimited)

**Cost per dream:** $0 (free tier) or $0.10 (paid)

---

#### 3. Google Veo 3
**Best for:** Cutting edge quality

**Pros:**
- ✅ Latest technology
- ✅ Native audio generation
- ✅ Long videos (60+ seconds)
- ✅ High resolution

**Cons:**
- ❌ Limited availability (waitlist)
- ❌ Expensive
- ❌ Overkill for most uses
- ❌ Complex integration

**Status:** May require Google Cloud access

---

#### 4. OpenAI Sora 2
**Best for:** Integration with ChatGPT

**Pros:**
- ✅ High quality
- ✅ ChatGPT integration
- ✅ Good for prototyping
- ✅ Multimodal

**Cons:**
- ❌ US/Canada only
- ❌ Requires ChatGPT Plus/Pro
- ❌ Limited API access
- ❌ Expensive

**Pricing:**
- ChatGPT Plus: $20/month (50 videos at 480p)
- ChatGPT Pro: Unlimited slow, 500 fast/month

---

## Recommended Pipeline Architecture

### Tier 1: Budget/Local ($0-10/month)

```python
Dream Text (Fine-tuned GPT-2)
    ↓
Scene Extraction (Simple NLP)
    ↓
Stable Diffusion (Image per scene)
    ↓
AnimateDiff/SVD (Animate images)
    ↓
FFmpeg (Combine + transitions)
```

**Quality:** ⭐⭐⭐ (3/5)
**Cost:** $0-10/month
**Speed:** Slow (5-10 min per dream)

---

### Tier 2: Hybrid ($20-50/month) ⭐ RECOMMENDED

```python
Dream Text (Fine-tuned LLaMA 2 7B)
    ↓
Intelligent Scene Parser (GPT-4 or local LLM)
    ↓
Prompt Enhancement (Optimize for video)
    ↓
Runway Gen-3 API (Generate video)
    ↓
FFmpeg (Post-processing + effects)
```

**Quality:** ⭐⭐⭐⭐ (4/5)
**Cost:** $20-50/month (50-100 dreams)
**Speed:** Fast (30-60 seconds per dream)

---

### Tier 3: Production ($100-500/month)

```python
Dream Text (LLaMA 2 13B + Custom Fine-tune)
    ↓
Advanced Scene Director (GPT-4 + embeddings)
    ↓
Multi-Model Video Generation
    ├── Runway Gen-3 (primary)
    ├── Luma Dream Machine (surreal scenes)
    └── Veo 3 (complex scenes)
    ↓
Professional Post-Production
    ├── Color grading
    ├── Audio generation
    ├── Smooth transitions
    └── Title cards
```

**Quality:** ⭐⭐⭐⭐⭐ (5/5)
**Cost:** $100-500/month
**Speed:** Very fast (20-40 seconds per dream)

---

## Implementation: Complete Code

### Full Dream-to-Video Pipeline

```python
#!/usr/bin/env python3
"""
REDREAMER 2025: Dream-to-Video Pipeline
Generates dream text then creates video visualization
"""

import torch
from transformers import pipeline
from diffusers import DiffusionPipeline, StableVideoDiffusionPipeline
from diffusers.utils import export_to_video
import re
import requests
from pathlib import Path

class DreamToVideoGenerator:
    def __init__(self, text_model="gpt2-medium", video_backend="local"):
        """
        Initialize dream-to-video generator

        Args:
            text_model: Model for dream text generation
            video_backend: "local", "runway", "luma", or "hybrid"
        """
        self.video_backend = video_backend

        # Initialize text generation
        print("Loading text generation model...")
        self.text_generator = pipeline(
            "text-generation",
            model=text_model,
            device=0 if torch.cuda.is_available() else -1
        )

        # Initialize video generation
        if video_backend == "local":
            print("Loading local video generation models...")
            self._init_local_video()
        elif video_backend in ["runway", "luma"]:
            print(f"Using {video_backend} API for video generation")
            self.api_key = self._load_api_key(video_backend)

    def _init_local_video(self):
        """Initialize local video generation models"""
        # Load Stable Diffusion for image generation
        self.img_pipe = DiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16
        ).to("cuda")

        # Load Stable Video Diffusion for image-to-video
        self.vid_pipe = StableVideoDiffusionPipeline.from_pretrained(
            "stabilityai/stable-video-diffusion-img2vid-xt",
            torch_dtype=torch.float16,
            variant="fp16"
        ).to("cuda")

    def _load_api_key(self, service):
        """Load API key from environment or file"""
        import os
        key = os.getenv(f"{service.upper()}_API_KEY")
        if not key:
            raise ValueError(f"Set {service.upper()}_API_KEY environment variable")
        return key

    def generate_dream_text(self, prompt, style="surreal"):
        """Generate dream narrative text"""

        style_configs = {
            "realistic": {"temperature": 0.7, "top_p": 0.9},
            "surreal": {"temperature": 1.2, "top_p": 0.95},
            "nightmare": {"temperature": 1.0, "top_p": 0.92},
            "lucid": {"temperature": 0.9, "top_p": 0.93},
        }

        config = style_configs.get(style, style_configs["surreal"])

        formatted_prompt = f"I had a strange dream. {prompt}"

        result = self.text_generator(
            formatted_prompt,
            max_length=300,
            num_return_sequences=1,
            do_sample=True,
            repetition_penalty=1.2,
            **config
        )

        return result[0]["generated_text"]

    def extract_scenes(self, dream_text, max_scenes=5):
        """Extract visual scenes from dream text"""

        # Split by sentences
        sentences = re.split(r'[.!?]+', dream_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Take most visual/descriptive sentences
        scenes = []
        for sentence in sentences[:max_scenes]:
            # Skip meta-commentary
            if any(skip in sentence.lower() for skip in ['i was', 'i felt', 'i thought']):
                continue
            scenes.append(sentence)

        return scenes[:max_scenes]

    def enhance_prompt_for_video(self, scene_text):
        """Enhance scene description for better video generation"""

        # Add stylistic keywords
        enhancements = [
            "cinematic",
            "dreamlike atmosphere",
            "surreal",
            "soft lighting",
            "ethereal",
            "4k quality",
            "smooth motion"
        ]

        enhanced = f"{scene_text}, {', '.join(enhancements)}"
        return enhanced

    def generate_video_local(self, prompt, duration=2):
        """Generate video using local models (SD + SVD)"""

        print(f"Generating image for: {prompt[:50]}...")

        # Generate initial image
        image = self.img_pipe(
            prompt,
            num_inference_steps=25,
            guidance_scale=7.5
        ).images[0]

        print("Animating image to video...")

        # Convert to video
        frames = self.vid_pipe(
            image,
            num_frames=25,  # ~1 second at 25fps
            decode_chunk_size=8
        ).frames[0]

        return frames

    def generate_video_runway(self, prompt, duration=5):
        """Generate video using Runway API"""

        response = requests.post(
            "https://api.runwayml.com/v1/generate",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "duration": duration,
                "model": "gen3-alpha-turbo",
                "options": {"style": "surreal"}
            },
            timeout=120
        )

        if response.status_code == 200:
            return response.json()["video_url"]
        else:
            raise Exception(f"Runway API error: {response.text}")

    def generate_video_luma(self, prompt):
        """Generate video using Luma Dream Machine API"""

        response = requests.post(
            "https://api.lumalabs.ai/dream-machine/v1/generate",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={"prompt": prompt},
            timeout=180
        )

        if response.status_code == 200:
            return response.json()["video_url"]
        else:
            raise Exception(f"Luma API error: {response.text}")

    def create_dream_video(self, prompt, style="surreal", output_path="dream_video.mp4"):
        """
        Full pipeline: Generate dream text and create video

        Args:
            prompt: Starting prompt for dream
            style: Dream style (realistic, surreal, nightmare, lucid)
            output_path: Where to save final video

        Returns:
            Path to generated video file
        """

        print("="*70)
        print("REDREAMER 2025: Dream-to-Video Generation")
        print("="*70)

        # Step 1: Generate dream text
        print("\n[1/5] Generating dream narrative...")
        dream_text = self.generate_dream_text(prompt, style)
        print(f"\nDream Text:\n{dream_text}\n")

        # Step 2: Extract scenes
        print("[2/5] Extracting visual scenes...")
        scenes = self.extract_scenes(dream_text)
        print(f"Found {len(scenes)} scenes")

        # Step 3: Enhance prompts
        print("[3/5] Enhancing prompts for video generation...")
        enhanced_scenes = [self.enhance_prompt_for_video(s) for s in scenes]

        # Step 4: Generate videos for each scene
        print("[4/5] Generating videos...")
        video_paths = []

        for i, scene_prompt in enumerate(enhanced_scenes, 1):
            print(f"\n  Scene {i}/{len(enhanced_scenes)}: {scene_prompt[:60]}...")

            if self.video_backend == "local":
                frames = self.generate_video_local(scene_prompt)
                scene_path = f"scene_{i}.mp4"
                export_to_video(frames, scene_path)
                video_paths.append(scene_path)

            elif self.video_backend == "runway":
                url = self.generate_video_runway(scene_prompt)
                # Download video from URL
                video_paths.append(self._download_video(url, f"scene_{i}.mp4"))

            elif self.video_backend == "luma":
                url = self.generate_video_luma(scene_prompt)
                video_paths.append(self._download_video(url, f"scene_{i}.mp4"))

        # Step 5: Combine videos
        print("[5/5] Combining scenes into final video...")
        final_path = self._combine_videos(video_paths, output_path, dream_text)

        print(f"\n✅ Dream video saved to: {final_path}")
        return final_path

    def _download_video(self, url, filename):
        """Download video from URL"""
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename

    def _combine_videos(self, video_paths, output_path, dream_text=None):
        """Combine multiple video clips with transitions"""
        import subprocess

        # Create file list for ffmpeg
        with open("filelist.txt", "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        # Combine with ffmpeg
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", "filelist.txt",
            "-vf", "fade=t=in:st=0:d=0.5,fade=t=out:st=5:d=0.5",  # Fade transitions
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_path
        ]

        subprocess.run(cmd, check=True, capture_output=True)

        # Clean up
        Path("filelist.txt").unlink()
        for path in video_paths:
            Path(path).unlink()

        return output_path


# Example Usage
if __name__ == "__main__":
    # Initialize generator
    generator = DreamToVideoGenerator(
        text_model="gpt2-medium",
        video_backend="local"  # or "runway", "luma"
    )

    # Generate dream video
    video_path = generator.create_dream_video(
        prompt="I was walking through a forest when suddenly",
        style="surreal",
        output_path="my_dream.mp4"
    )

    print(f"Watch your dream: {video_path}")
```

---

## Advanced Features

### 1. Style Transfer
Apply consistent visual style across all scenes:

```python
def apply_dream_style(self, scene_prompts, style_reference):
    """Apply consistent visual style to all scenes"""
    style_keywords = {
        "watercolor": "watercolor painting, soft edges, flowing colors",
        "oil_painting": "oil painting, thick brushstrokes, rich colors",
        "anime": "anime style, cel shaded, vibrant colors",
        "noir": "film noir, high contrast, black and white",
        "cyberpunk": "cyberpunk aesthetic, neon lights, dark atmosphere"
    }

    style = style_keywords.get(style_reference, "")
    return [f"{prompt}, {style}" for prompt in scene_prompts]
```

### 2. Audio Generation
Add atmospheric soundscape:

```python
from audiocraft.models import MusicGen

def add_dream_audio(video_path, prompt="dreamy ambient soundscape"):
    """Generate and add audio to dream video"""
    model = MusicGen.get_pretrained('small')
    audio = model.generate([prompt], duration=30)

    # Combine with ffmpeg
    # ... implementation
```

### 3. Narrative Voice-Over
Add narration of dream text:

```python
from TTS.api import TTS

def add_narration(video_path, dream_text):
    """Add voice narration of dream"""
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    tts.tts_to_file(text=dream_text, file_path="narration.wav")

    # Mix with video
    # ... implementation
```

---

## Cost Analysis: Video Generation

### Per Dream Video (5-10 seconds, 3-5 scenes)

| Backend | Setup Cost | Per Dream | Quality | Speed |
|---------|------------|-----------|---------|-------|
| **Local (AnimateDiff)** | $0 | $0 | ⭐⭐⭐ | 5-10 min |
| **Local (SVD)** | $0 | $0 | ⭐⭐⭐ | 3-5 min |
| **Runway Gen-3** | $15-35/mo | $0.25-0.50 | ⭐⭐⭐⭐ | 30-60 sec |
| **Luma Dream** | $30/mo | $0.10 | ⭐⭐⭐⭐ | 2-3 min |
| **Veo 3** | TBD | $1-2 | ⭐⭐⭐⭐⭐ | 1-2 min |

### Monthly Cost Estimates

| Use Case | Dreams/Month | Recommended | Monthly Cost |
|----------|--------------|-------------|--------------|
| **Personal** | 10-20 | Local or Luma | $0-30 |
| **Hobbyist** | 50-100 | Runway Standard | $35-50 |
| **Creator** | 200-500 | Runway Pro | $75-150 |
| **Production** | 1000+ | Mixed backends | $200-500 |

---

## Deployment Architectures

### Architecture 1: Full Local
```
User → Gradio UI → Dream Text (Local LLM)
                  ↓
              Scene Parser
                  ↓
          AnimateDiff (Local GPU)
                  ↓
              FFmpeg Assembly
                  ↓
            Final Video → User
```
**Pros:** Privacy, no ongoing costs
**Cons:** Slow, requires powerful hardware

---

### Architecture 2: Hybrid (Recommended)
```
User → Web UI (Cloud) → Dream Text (Cloud GPU)
                       ↓
                   Scene Parser (CPU)
                       ↓
               Runway API (Cloud)
                       ↓
             Post-process (Cloud CPU)
                       ↓
       Cloud Storage → CDN → User
```
**Pros:** Fast, scalable, good quality
**Cons:** Ongoing API costs

---

### Architecture 3: Microservices
```
API Gateway
    ├── Text Service (Kubernetes pod)
    ├── Video Service (GPU pod with queue)
    ├── Storage Service (S3)
    └── CDN Distribution

Queue System (RabbitMQ)
    ├── Text generation queue
    ├── Video generation queue
    └── Post-processing queue
```
**Pros:** Scalable, professional
**Cons:** Complex, expensive

---

## Getting Started: Quick Implementation

### Minimal Working Example (30 minutes)

```python
# Install
pip install torch transformers diffusers accelerate

# Simple pipeline
from transformers import pipeline
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video

# Generate dream text
text_gen = pipeline("text-generation", model="gpt2")
dream = text_gen("I had a dream where")[0]['generated_text']

# Generate video
video_pipe = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b"
)
frames = video_pipe(dream).frames[0]
export_to_video(frames, "dream.mp4")
```

---

## Next Steps

1. **Week 1:** Implement text generation (done!)
2. **Week 2:** Add single-scene video generation
3. **Week 3:** Implement scene extraction and multi-scene
4. **Week 4:** Add post-processing and UI
5. **Month 2:** Deploy and iterate based on feedback

---

## Resources

### Video Generation
- **Runway:** https://runwayml.com/
- **Luma:** https://lumalabs.ai/dream-machine
- **AnimateDiff:** https://github.com/guoyww/AnimateDiff
- **Stable Video:** https://huggingface.co/stabilityai/stable-video-diffusion-img2vid

### Tutorials
- AnimateDiff: https://www.stablediffusiontutorials.com/
- HuggingFace Diffusers: https://huggingface.co/docs/diffusers/

### Communities
- r/StableDiffusion
- ComfyUI Discord
- HuggingFace Forums

---

**This is cutting-edge stuff! Let's make dreams visible! 🌙✨🎬**
