#!/usr/bin/env python3
"""
REDREAMER 2025 Video Edition
Complete dream-to-video generation pipeline

Usage:
    python redreamer_video.py --prompt "I was flying" --style surreal --backend local
    python redreamer_video.py --prompt "I was flying" --backend runway --api-key YOUR_KEY
"""

import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import argparse
import sys
import re
from pathlib import Path

class DreamVideoGenerator:
    """Generate dream text and optionally create videos"""

    def __init__(self, text_model="gpt2-medium", video_backend=None, api_key=None):
        """
        Initialize the generator

        Args:
            text_model: Model for text generation ("gpt2-medium", "gpt2", etc.)
            video_backend: None, "local", "runway", "luma", "api_placeholder"
            api_key: API key for commercial services
        """
        self.video_backend = video_backend
        self.api_key = api_key

        print(f"Loading text generation model: {text_model}")
        self.text_generator = pipeline(
            "text-generation",
            model=text_model,
            device=0 if torch.cuda.is_available() else -1
        )

        if video_backend == "local":
            self._init_local_video_models()
        elif video_backend in ["runway", "luma"]:
            if not api_key:
                print(f"Warning: No API key provided for {video_backend}")

    def _init_local_video_models(self):
        """Initialize local video generation models"""
        try:
            from diffusers import DiffusionPipeline, StableVideoDiffusionPipeline

            print("Loading Stable Diffusion for image generation...")
            self.img_pipe = DiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16
            ).to("cuda")

            print("Loading Stable Video Diffusion for animation...")
            self.vid_pipe = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid-xt",
                torch_dtype=torch.float16,
                variant="fp16"
            ).to("cuda")

            print("Video generation models loaded successfully!")

        except ImportError:
            print("Error: diffusers library not installed")
            print("Install with: pip install diffusers accelerate")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading video models: {e}")
            print("This requires a CUDA-capable GPU with 16GB+ VRAM")
            sys.exit(1)

    def generate_dream_text(self, prompt, style="surreal", length=200):
        """
        Generate dream narrative text

        Args:
            prompt: Starting prompt
            style: Dream style (realistic, surreal, nightmare, lucid)
            length: Maximum length in tokens

        Returns:
            Generated dream text
        """
        style_configs = {
            "realistic": {
                "temperature": 0.7,
                "top_k": 40,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
            },
            "surreal": {
                "temperature": 1.2,
                "top_k": 60,
                "top_p": 0.95,
                "repetition_penalty": 1.3,
            },
            "nightmare": {
                "temperature": 1.0,
                "top_k": 50,
                "top_p": 0.92,
                "repetition_penalty": 1.2,
            },
            "lucid": {
                "temperature": 0.9,
                "top_k": 45,
                "top_p": 0.93,
                "repetition_penalty": 1.15,
            }
        }

        config = style_configs.get(style, style_configs["surreal"])

        formatted_prompt = f"I had a strange dream. {prompt}"

        result = self.text_generator(
            formatted_prompt,
            max_length=length,
            num_return_sequences=1,
            do_sample=True,
            pad_token_id=50256,
            **config
        )

        return result[0]["generated_text"]

    def extract_visual_scenes(self, dream_text, max_scenes=5):
        """
        Extract visual scenes from dream narrative

        Args:
            dream_text: Generated dream text
            max_scenes: Maximum number of scenes to extract

        Returns:
            List of scene descriptions
        """
        # Split by sentences
        sentences = re.split(r'[.!?]+', dream_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        scenes = []
        for sentence in sentences:
            # Skip meta-commentary
            if any(skip in sentence.lower() for skip in
                   ['i felt', 'i thought', 'i realized', 'i wondered']):
                continue

            # Prefer visually descriptive sentences
            if any(visual in sentence.lower() for visual in
                   ['saw', 'looked', 'appeared', 'stood', 'walked',
                    'room', 'place', 'light', 'color', 'figure']):
                scenes.append(sentence)

        return scenes[:max_scenes]

    def enhance_prompt_for_video(self, scene_text):
        """
        Enhance scene description for video generation

        Args:
            scene_text: Original scene description

        Returns:
            Enhanced prompt with video keywords
        """
        enhancements = [
            "cinematic",
            "dreamlike atmosphere",
            "surreal",
            "soft lighting",
            "ethereal mood",
            "smooth camera movement",
            "4k quality"
        ]

        # Remove first-person perspective
        scene_text = re.sub(r'^I (was|saw|found|walked)', '', scene_text, flags=re.IGNORECASE)
        scene_text = scene_text.strip()

        enhanced = f"{scene_text}, {', '.join(enhancements)}"
        return enhanced

    def generate_video_local(self, scene_prompt, output_path="scene.mp4"):
        """
        Generate video using local models (Stable Diffusion + SVD)

        Args:
            scene_prompt: Enhanced scene description
            output_path: Where to save video

        Returns:
            Path to generated video
        """
        if not hasattr(self, 'img_pipe'):
            raise RuntimeError("Local video models not initialized")

        from diffusers.utils import export_to_video

        print(f"  Generating image from prompt...")

        # Generate seed image
        image = self.img_pipe(
            scene_prompt,
            num_inference_steps=25,
            guidance_scale=7.5
        ).images[0]

        print(f"  Animating image to video...")

        # Animate to video
        frames = self.vid_pipe(
            image,
            num_frames=25,  # ~1 second at 25fps
            decode_chunk_size=8
        ).frames[0]

        # Export video
        export_to_video(frames, output_path, fps=25)

        return output_path

    def generate_video_api(self, scene_prompt, backend, output_path="scene.mp4"):
        """
        Generate video using commercial API

        Args:
            scene_prompt: Enhanced scene description
            backend: "runway" or "luma"
            output_path: Where to save video

        Returns:
            Path to downloaded video
        """
        import requests

        if backend == "runway":
            url = "https://api.runwayml.com/v1/generate"
            payload = {
                "prompt": scene_prompt,
                "duration": 5,
                "model": "gen3-alpha-turbo"
            }
        elif backend == "luma":
            url = "https://api.lumalabs.ai/dream-machine/v1/generate"
            payload = {"prompt": scene_prompt}
        else:
            raise ValueError(f"Unknown backend: {backend}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        print(f"  Sending request to {backend}...")
        response = requests.post(url, headers=headers, json=payload, timeout=180)

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        # Download video
        video_url = response.json().get("video_url")
        if video_url:
            print(f"  Downloading video...")
            video_response = requests.get(video_url, stream=True)
            with open(output_path, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)

        return output_path

    def create_dream_video(self, prompt, style="surreal", output_dir="output"):
        """
        Full pipeline: Generate dream text and create video(s)

        Args:
            prompt: Starting dream prompt
            style: Dream style
            output_dir: Directory to save outputs

        Returns:
            Dictionary with paths to generated files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        print("="*70)
        print("REDREAMER 2025 VIDEO EDITION")
        print("="*70)

        # Step 1: Generate dream text
        print("\n[1/4] Generating dream narrative...")
        dream_text = self.generate_dream_text(prompt, style)

        # Save dream text
        text_path = output_dir / "dream_text.txt"
        text_path.write_text(dream_text)
        print(f"\nDream Text Preview:\n{dream_text[:200]}...")
        print(f"\nFull text saved to: {text_path}")

        # Step 2: Extract scenes
        print("\n[2/4] Extracting visual scenes...")
        scenes = self.extract_visual_scenes(dream_text)
        print(f"Found {len(scenes)} visual scenes")

        if not scenes:
            print("Warning: No visual scenes extracted. Using full text.")
            scenes = [dream_text[:200]]

        # Step 3: Enhance for video
        print("\n[3/4] Enhancing prompts for video generation...")
        enhanced_scenes = [self.enhance_prompt_for_video(s) for s in scenes]

        for i, (original, enhanced) in enumerate(zip(scenes, enhanced_scenes), 1):
            print(f"\nScene {i}:")
            print(f"  Original: {original[:80]}...")
            print(f"  Enhanced: {enhanced[:80]}...")

        # Step 4: Generate videos (if backend specified)
        video_paths = []
        if self.video_backend:
            print(f"\n[4/4] Generating videos using {self.video_backend} backend...")

            for i, scene_prompt in enumerate(enhanced_scenes, 1):
                print(f"\nScene {i}/{len(enhanced_scenes)}:")

                output_path = output_dir / f"scene_{i}.mp4"

                try:
                    if self.video_backend == "local":
                        video_path = self.generate_video_local(
                            scene_prompt,
                            str(output_path)
                        )
                    elif self.video_backend in ["runway", "luma"]:
                        video_path = self.generate_video_api(
                            scene_prompt,
                            self.video_backend,
                            str(output_path)
                        )
                    else:
                        print(f"Unknown backend: {self.video_backend}")
                        continue

                    video_paths.append(video_path)
                    print(f"  ✓ Saved to: {video_path}")

                except Exception as e:
                    print(f"  ✗ Error generating video: {e}")
                    continue
        else:
            print("\n[4/4] Video generation skipped (no backend specified)")
            print("To generate videos, use --backend option")

        # Summary
        print("\n" + "="*70)
        print("GENERATION COMPLETE")
        print("="*70)
        print(f"\nDream text: {text_path}")
        print(f"Scenes extracted: {len(scenes)}")
        if video_paths:
            print(f"Videos generated: {len(video_paths)}")
            for path in video_paths:
                print(f"  - {path}")
        else:
            print("\nTo generate videos, run again with:")
            print(f"  --backend local  (requires GPU)")
            print(f"  --backend runway --api-key YOUR_KEY")

        return {
            "text": str(text_path),
            "scenes": scenes,
            "enhanced_prompts": enhanced_scenes,
            "videos": video_paths
        }


def main():
    parser = argparse.ArgumentParser(
        description="REDREAMER 2025 Video Edition - Dream-to-Video Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Generate dream text only (fast)
  python redreamer_video.py --prompt "I was flying over mountains"

  # Generate text + video using local models (requires GPU)
  python redreamer_video.py --prompt "I was flying" --backend local

  # Generate text + video using Runway API
  python redreamer_video.py --prompt "I was in a library" \\
      --backend runway --api-key YOUR_RUNWAY_KEY

  # Different dream styles
  python redreamer_video.py --prompt "I saw a shadow" --style nightmare
  python redreamer_video.py --prompt "I was aware I was dreaming" --style lucid
        """
    )

    parser.add_argument("--prompt", type=str, required=True,
                        help="Starting prompt for the dream")
    parser.add_argument("--style", choices=["realistic", "surreal", "nightmare", "lucid"],
                        default="surreal", help="Dream style (default: surreal)")
    parser.add_argument("--backend", choices=["local", "runway", "luma"],
                        help="Video generation backend (optional)")
    parser.add_argument("--api-key", type=str,
                        help="API key for commercial video services")
    parser.add_argument("--output", type=str, default="output",
                        help="Output directory (default: output)")
    parser.add_argument("--model", type=str, default="gpt2-medium",
                        help="Text generation model (default: gpt2-medium)")

    args = parser.parse_args()

    # Validate
    if args.backend in ["runway", "luma"] and not args.api_key:
        parser.error(f"--api-key required for {args.backend} backend")

    # Initialize generator
    try:
        generator = DreamVideoGenerator(
            text_model=args.model,
            video_backend=args.backend,
            api_key=args.api_key
        )
    except Exception as e:
        print(f"Error initializing generator: {e}")
        sys.exit(1)

    # Generate
    try:
        results = generator.create_dream_video(
            prompt=args.prompt,
            style=args.style,
            output_dir=args.output
        )

        print("\n✅ All done! Sweet dreams! 🌙✨")

    except KeyboardInterrupt:
        print("\n\nInterrupted. Partial results may be in output directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
