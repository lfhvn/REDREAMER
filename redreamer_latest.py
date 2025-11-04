#!/usr/bin/env python3
"""
REDREAMER 2025 - Latest Models Edition
Uses: gpt-oss-20b + Wan 2.2 / HunyuanVideo

The actual state-of-the-art for local dream generation (November 2025)
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import sys
from pathlib import Path
import re

class LatestDreamGenerator:
    """Dream generator using 2025 SOTA models"""

    def __init__(self, text_backend="gpt-oss", video_backend="wan2.2", use_ollama=False):
        """
        Initialize with latest models

        Args:
            text_backend: "gpt-oss" (20B) or "qwen2.5" (7B-72B)
            video_backend: "wan2.2", "hunyuan", "mochi", "ltx", or None
            use_ollama: Use Ollama for text generation (easier setup)
        """
        self.video_backend = video_backend
        self.use_ollama = use_ollama

        # Initialize text generation
        if use_ollama:
            self._init_ollama(text_backend)
        else:
            self._init_transformers(text_backend)

        # Initialize video generation if requested
        if video_backend:
            self._init_video(video_backend)

    def _init_ollama(self, model):
        """Initialize Ollama for text generation (easiest)"""
        try:
            import ollama
            self.ollama_client = ollama
            self.text_model_name = f"{model}:20b" if model == "gpt-oss" else f"{model}:72b"

            # Test connection
            response = self.ollama_client.chat(
                model=self.text_model_name,
                messages=[{'role': 'user', 'content': 'test'}]
            )
            print(f"✅ Ollama {self.text_model_name} connected")

        except ImportError:
            print("❌ Ollama not installed. Install with:")
            print("   curl -fsSL https://ollama.ai/install.sh | sh")
            print("   ollama pull gpt-oss:20b")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            print("Make sure Ollama is running and model is pulled:")
            print(f"   ollama pull {self.text_model_name}")
            sys.exit(1)

    def _init_transformers(self, model):
        """Initialize HuggingFace Transformers for text generation"""
        try:
            print(f"Loading {model}...")

            if model == "gpt-oss":
                model_id = "openai/gpt-oss-20b"
            elif model == "qwen2.5":
                model_id = "Qwen/Qwen2.5-7B-Instruct"
            else:
                model_id = model  # Custom model path

            self.text_model = AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True
            )

            self.text_tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                trust_remote_code=True
            )

            print(f"✅ {model_id} loaded")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("\nTry using --use-ollama for easier setup")
            sys.exit(1)

    def _init_video(self, backend):
        """Initialize video generation models"""
        try:
            print(f"Loading {backend} video model...")

            if backend == "wan2.2":
                from diffusers import WanPipeline
                self.video_pipe = WanPipeline.from_pretrained(
                    "Wan-AI/Wan2.2-T2V-A14B",
                    torch_dtype=torch.float16
                )
                self.video_pipe.to("cuda")
                self.fps = 24

            elif backend == "hunyuan":
                from diffusers import HunyuanVideoPipeline
                self.video_pipe = HunyuanVideoPipeline.from_pretrained(
                    "tencent/HunyuanVideo",
                    torch_dtype=torch.float16
                )
                self.video_pipe.to("cuda")
                self.fps = 24

            elif backend == "mochi":
                from diffusers import MochiPipeline
                self.video_pipe = MochiPipeline.from_pretrained(
                    "genmo/mochi-1",
                    torch_dtype=torch.float16
                )
                self.video_pipe.to("cuda")
                self.fps = 30

            elif backend == "ltx":
                from diffusers import LTXVideoPipeline
                self.video_pipe = LTXVideoPipeline.from_pretrained(
                    "Lightricks/LTX-Video",
                    torch_dtype=torch.float16
                )
                self.video_pipe.to("cuda")
                self.fps = 24

            else:
                print(f"Unknown video backend: {backend}")
                self.video_pipe = None
                return

            print(f"✅ {backend} video model loaded")

        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("Install with: pip install diffusers accelerate")
            self.video_pipe = None
        except Exception as e:
            print(f"❌ Error loading video model: {e}")
            print(f"\nVideo model {backend} may not be available yet.")
            print("Try: wan2.2, hunyuan, or install from GitHub")
            self.video_pipe = None

    def generate_dream_text(self, prompt, style="surreal", length=300):
        """
        Generate dream narrative

        Args:
            prompt: Starting prompt
            style: Dream style (surreal, nightmare, lucid, realistic)
            length: Maximum length in tokens

        Returns:
            Generated dream text
        """
        style_configs = {
            "realistic": {
                "description": "realistic and grounded",
                "temperature": 0.8,
            },
            "surreal": {
                "description": "surreal, dreamlike, with impossible logic and strange transformations",
                "temperature": 1.1,
            },
            "nightmare": {
                "description": "dark, unsettling nightmare with ominous atmosphere",
                "temperature": 1.0,
            },
            "lucid": {
                "description": "lucid dream where the dreamer has awareness and control",
                "temperature": 0.9,
            }
        }

        config = style_configs.get(style, style_configs["surreal"])

        system_prompt = f"""You are a creative dream narrator. Generate a vivid, {config['description']} dream narrative. Be descriptive and evocative."""

        user_prompt = f"Dream about: {prompt}"

        # Generate with appropriate backend
        if self.use_ollama:
            response = self.ollama_client.chat(
                model=self.text_model_name,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                options={
                    'temperature': config['temperature'],
                    'top_p': 0.95,
                    'num_predict': length
                }
            )
            dream_text = response['message']['content']

        else:
            full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nDream:"

            inputs = self.text_tokenizer(
                full_prompt,
                return_tensors="pt"
            ).to(self.text_model.device)

            outputs = self.text_model.generate(
                **inputs,
                max_new_tokens=length,
                temperature=config['temperature'],
                top_p=0.95,
                do_sample=True,
                repetition_penalty=1.2
            )

            full_output = self.text_tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract just the dream part
            if "Dream:" in full_output:
                dream_text = full_output.split("Dream:")[-1].strip()
            else:
                dream_text = full_output.replace(full_prompt, "").strip()

        return dream_text

    def extract_visual_scenes(self, dream_text, max_scenes=5):
        """Extract visual scenes from dream narrative"""
        # Split by sentences
        sentences = re.split(r'[.!?]+', dream_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        scenes = []
        for sentence in sentences:
            # Skip meta-commentary
            if any(skip in sentence.lower() for skip in
                   ['i felt', 'i thought', 'i realized', 'i wondered', 'i remembered']):
                continue

            # Prefer visual descriptions
            if any(visual in sentence.lower() for visual in
                   ['saw', 'looked', 'appeared', 'stood', 'walked', 'flew',
                    'room', 'place', 'light', 'color', 'figure', 'door',
                    'sky', 'ground', 'water', 'tree', 'building']):
                scenes.append(sentence)

        return scenes[:max_scenes]

    def enhance_prompt_for_video(self, scene_text):
        """Enhance scene for video generation"""
        # Remove first-person perspective
        scene_text = re.sub(r'^I (was|saw|found|walked|flew|stood)', '', scene_text, flags=re.IGNORECASE)
        scene_text = scene_text.strip()

        # Add video-specific keywords
        enhancements = [
            "cinematic shot",
            "dreamlike atmosphere",
            "surreal",
            "smooth camera movement",
            "ethereal lighting",
            "high quality",
            "detailed"
        ]

        enhanced = f"{scene_text}, {', '.join(enhancements)}"
        return enhanced

    def generate_video(self, prompt, duration_seconds=5):
        """Generate video from text prompt"""
        if not self.video_pipe:
            raise RuntimeError("No video model loaded")

        from diffusers.utils import export_to_video

        # Calculate frames
        num_frames = duration_seconds * self.fps

        print(f"  Generating {duration_seconds}s video at {self.fps}fps...")

        # Generate based on backend
        if self.video_backend == "wan2.2":
            video_frames = self.video_pipe(
                prompt=prompt,
                num_frames=min(num_frames, 360),  # Wan 2.2 max
                guidance_scale=7.5,
                num_inference_steps=50
            ).frames[0]

        elif self.video_backend == "hunyuan":
            video_frames = self.video_pipe(
                prompt=prompt,
                num_frames=min(num_frames, 360),  # HunyuanVideo max
                height=720,
                width=1280
            ).frames[0]

        elif self.video_backend == "mochi":
            video_frames = self.video_pipe(
                prompt=prompt,
                num_frames=min(num_frames, 162),  # Mochi max
                height=480,
                width=640
            ).frames[0]

        elif self.video_backend == "ltx":
            video_frames = self.video_pipe(
                prompt=prompt,
                num_frames=num_frames
            ).frames[0]

        return video_frames

    def create_dream_video(self, prompt, style="surreal", output_dir="output"):
        """Complete dream generation pipeline"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        print("="*70)
        print("REDREAMER 2025 - Latest Models Edition")
        print("="*70)

        # Generate dream text
        print(f"\n[1/3] Generating dream with gpt-oss-20b ({style} style)...")
        dream_text = self.generate_dream_text(prompt, style)

        # Save text
        text_path = output_dir / "dream_text.txt"
        text_path.write_text(dream_text)

        print(f"\n📖 Dream Text:\n{dream_text[:300]}...")
        print(f"\nFull text: {text_path}")

        # Extract scenes
        print(f"\n[2/3] Extracting visual scenes...")
        scenes = self.extract_visual_scenes(dream_text)
        print(f"Found {len(scenes)} visual scenes")

        # Generate videos
        video_paths = []
        if self.video_pipe and scenes:
            print(f"\n[3/3] Generating videos with {self.video_backend}...")

            for i, scene in enumerate(scenes, 1):
                print(f"\nScene {i}/{len(scenes)}:")
                print(f"  Text: {scene[:80]}...")

                try:
                    enhanced = self.enhance_prompt_for_video(scene)
                    print(f"  Enhanced: {enhanced[:80]}...")

                    video_frames = self.generate_video(enhanced, duration_seconds=5)

                    # Save video
                    from diffusers.utils import export_to_video
                    video_path = output_dir / f"scene_{i}.mp4"
                    export_to_video(video_frames, str(video_path), fps=self.fps)

                    video_paths.append(str(video_path))
                    print(f"  ✅ Saved: {video_path}")

                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    continue
        else:
            if not self.video_pipe:
                print("\n[3/3] Skipped (no video model loaded)")
            elif not scenes:
                print("\n[3/3] Skipped (no visual scenes found)")

        # Summary
        print("\n" + "="*70)
        print("COMPLETE")
        print("="*70)
        print(f"\n📖 Dream text: {text_path}")
        print(f"🎬 Videos generated: {len(video_paths)}")
        for path in video_paths:
            print(f"   - {path}")

        return {
            "text": str(text_path),
            "text_content": dream_text,
            "scenes": scenes,
            "videos": video_paths
        }


def main():
    parser = argparse.ArgumentParser(
        description="REDREAMER 2025 - Latest Models (gpt-oss-20b + Wan 2.2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Text only with Ollama (easiest)
  python redreamer_latest.py --prompt "flying through space" --use-ollama

  # Text only with HuggingFace
  python redreamer_latest.py --prompt "flying through space"

  # Text + Video with Wan 2.2 (best quality)
  python redreamer_latest.py --prompt "flying through space" --video wan2.2 --use-ollama

  # Text + Video with HunyuanVideo
  python redreamer_latest.py --prompt "library of flying books" --video hunyuan --use-ollama

  # Different dream styles
  python redreamer_latest.py --prompt "dark forest" --style nightmare --use-ollama
  python redreamer_latest.py --prompt "I know I'm dreaming" --style lucid --use-ollama

Setup:
  # Install Ollama (recommended)
  curl -fsSL https://ollama.ai/install.sh | sh
  ollama pull gpt-oss:20b

  # Install Python dependencies
  pip install torch transformers diffusers accelerate ollama
        """
    )

    parser.add_argument("--prompt", type=str, required=True,
                        help="Dream prompt")
    parser.add_argument("--style", choices=["realistic", "surreal", "nightmare", "lucid"],
                        default="surreal", help="Dream style")
    parser.add_argument("--text-model", choices=["gpt-oss", "qwen2.5"],
                        default="gpt-oss", help="Text generation model")
    parser.add_argument("--video", choices=["wan2.2", "hunyuan", "mochi", "ltx"],
                        help="Video generation backend (optional)")
    parser.add_argument("--use-ollama", action="store_true",
                        help="Use Ollama for text generation (recommended)")
    parser.add_argument("--output", type=str, default="output",
                        help="Output directory")

    args = parser.parse_args()

    # Initialize
    try:
        print(f"Initializing REDREAMER with:")
        print(f"  Text: {args.text_model} ({'Ollama' if args.use_ollama else 'HuggingFace'})")
        print(f"  Video: {args.video or 'None'}")
        print()

        generator = LatestDreamGenerator(
            text_backend=args.text_model,
            video_backend=args.video,
            use_ollama=args.use_ollama
        )

    except Exception as e:
        print(f"\n❌ Initialization error: {e}")
        sys.exit(1)

    # Generate
    try:
        results = generator.create_dream_video(
            prompt=args.prompt,
            style=args.style,
            output_dir=args.output
        )

        print("\n✨ Sweet dreams! 🌙")

    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
