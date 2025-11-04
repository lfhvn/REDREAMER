#!/usr/bin/env python3
"""
REDREAMER 2025 - Quick Start Script
Modern dream generation using transformers

Usage:
    python redreamer2025_quickstart.py
"""

import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import argparse
import sys

def check_setup():
    """Check if environment is properly configured"""
    print("="*70)
    print("REDREAMER 2025 - Environment Check")
    print("="*70)

    print(f"\n✓ Python version: {sys.version.split()[0]}")
    print(f"✓ PyTorch version: {torch.__version__}")
    print(f"✓ CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
        print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠ No GPU detected - will use CPU (slower)")

    print("\n" + "="*70 + "\n")

def generate_dreams_zero_shot(prompt, num_dreams=3, style="surreal"):
    """
    Generate dreams without fine-tuning using a pre-trained model

    Args:
        prompt: Starting text for the dream
        num_dreams: Number of dreams to generate
        style: Dream style (realistic, surreal, nightmare, lucid)
    """
    print(f"Loading pre-trained model (GPT-2)...")

    # Load generator
    generator = pipeline(
        "text-generation",
        model="gpt2-medium",
        device=0 if torch.cuda.is_available() else -1
    )

    # Style configurations
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

    # Format prompt
    formatted_prompt = f"I had a strange dream. {prompt}"

    print(f"\nGenerating {num_dreams} {style} dream(s)...\n")

    # Generate
    dreams = generator(
        formatted_prompt,
        max_length=200,
        num_return_sequences=num_dreams,
        do_sample=True,
        pad_token_id=50256,
        **config
    )

    return dreams

def display_dreams(dreams, style):
    """Display generated dreams in a formatted way"""
    print("="*70)
    print(f"GENERATED DREAMS ({style.upper()} style)")
    print("="*70)

    for i, dream in enumerate(dreams, 1):
        print(f"\n--- Dream {i} ---\n")
        print(dream['generated_text'])
        print()

def demo_mode():
    """Run a demo with multiple prompts and styles"""
    print("\n" + "="*70)
    print("DEMO MODE: Generating dreams with different styles")
    print("="*70 + "\n")

    prompts = [
        "I was walking through a forest when suddenly",
        "I found myself in my childhood home, but everything was different",
        "I was flying over a city made of glass and light",
    ]

    styles = ["realistic", "surreal", "nightmare"]

    for prompt, style in zip(prompts, styles):
        print(f"\n📝 Prompt: '{prompt}'")
        print(f"🎨 Style: {style}")
        dreams = generate_dreams_zero_shot(prompt, num_dreams=1, style=style)
        display_dreams(dreams, style)
        print("\n" + "-"*70 + "\n")

def interactive_mode():
    """Interactive mode for custom dream generation"""
    print("\n" + "="*70)
    print("INTERACTIVE MODE")
    print("="*70 + "\n")

    print("Enter your dream prompts (or 'quit' to exit)")
    print("Example: 'I was swimming in an ocean of stars'\n")

    while True:
        prompt = input("\n🌙 Dream prompt: ").strip()

        if prompt.lower() in ['quit', 'exit', 'q']:
            print("\nSweet dreams! 💤")
            break

        if not prompt:
            print("Please enter a prompt!")
            continue

        # Ask for style
        print("\nChoose style:")
        print("  1. Realistic")
        print("  2. Surreal")
        print("  3. Nightmare")
        print("  4. Lucid")

        style_choice = input("Style (1-4, default=2): ").strip() or "2"
        style_map = {"1": "realistic", "2": "surreal", "3": "nightmare", "4": "lucid"}
        style = style_map.get(style_choice, "surreal")

        # Generate
        dreams = generate_dreams_zero_shot(prompt, num_dreams=1, style=style)
        display_dreams(dreams, style)

def main():
    parser = argparse.ArgumentParser(
        description="REDREAMER 2025 - Modern Dream Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run demo mode
  python redreamer2025_quickstart.py --demo

  # Generate custom dream
  python redreamer2025_quickstart.py --prompt "I was flying" --style surreal --num 3

  # Interactive mode
  python redreamer2025_quickstart.py --interactive
        """
    )

    parser.add_argument("--demo", action="store_true",
                        help="Run demo with preset prompts")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Run in interactive mode")
    parser.add_argument("--prompt", type=str,
                        help="Dream prompt/seed text")
    parser.add_argument("--style", choices=["realistic", "surreal", "nightmare", "lucid"],
                        default="surreal", help="Dream style (default: surreal)")
    parser.add_argument("--num", type=int, default=3,
                        help="Number of dreams to generate (default: 3)")

    args = parser.parse_args()

    # Check environment
    check_setup()

    # Run appropriate mode
    if args.demo:
        demo_mode()
    elif args.interactive:
        interactive_mode()
    elif args.prompt:
        dreams = generate_dreams_zero_shot(args.prompt, args.num, args.style)
        display_dreams(dreams, args.style)
    else:
        # Default: run demo
        print("No arguments provided. Running demo mode...\n")
        print("(Use --help to see all options)\n")
        demo_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Sweet dreams! 💤")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install torch transformers")
        sys.exit(1)
