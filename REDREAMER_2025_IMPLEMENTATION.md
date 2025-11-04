# REDREAMER 2025: Implementation Guide

This guide provides step-by-step instructions and code examples for building a modern dream generation system using transformers and PyTorch.

---

## Quick Start (30 minutes)

### 1. Environment Setup

```bash
# Create conda environment
conda create -n redreamer2025 python=3.11 -y
conda activate redreamer2025

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install HuggingFace ecosystem
pip install transformers datasets accelerate peft bitsandbytes
pip install sentencepiece protobuf

# Install utilities
pip install wandb jupyter ipywidgets pandas numpy
pip install gradio streamlit  # For UI
```

### 2. Test Installation

```python
import torch
import transformers

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Transformers version: {transformers.__version__}")

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
```

---

## Option A: Zero-Shot Dream Generation (No Training)

Try this first to see what pre-trained models can do without any fine-tuning!

```python
from transformers import pipeline

# Load a creative text generation model
generator = pipeline(
    "text-generation",
    model="gpt2-medium",  # or "EleutherAI/gpt-neo-125M"
    device=0 if torch.cuda.is_available() else -1
)

# Craft a dream-like prompt
prompt = """I had a strange dream last night. In the dream, I found myself"""

# Generate with creative sampling
dreams = generator(
    prompt,
    max_length=200,
    temperature=1.1,      # Higher = more creative/random
    top_k=50,             # Consider top 50 tokens
    top_p=0.95,           # Nucleus sampling
    num_return_sequences=3,
    do_sample=True,
    repetition_penalty=1.2,
    pad_token_id=50256
)

for i, dream in enumerate(dreams, 1):
    print(f"\n{'='*60}")
    print(f"DREAM {i}")
    print(f"{'='*60}")
    print(dream['generated_text'])
```

**Expected Output:**
```
Dream 1: "...standing in a library where books flew like birds..."
Dream 2: "...walking through a city made entirely of glass..."
Dream 3: "...talking to my childhood pet who could speak fluent French..."
```

---

## Option B: Fine-Tune on DreamBank (Recommended)

### Step 1: Load DreamBank Dataset

```python
from datasets import load_dataset
from transformers import AutoTokenizer

# Load the DreamBank corpus from HuggingFace
print("Loading DreamBank dataset...")
dataset = load_dataset("gustavecortal/DreamBank-annotated")

# Explore the data
print(f"Total dreams: {len(dataset['train'])}")
print(f"\nExample dream:")
print(dataset['train'][0]['dream'])

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # GPT-2 doesn't have a pad token
```

### Step 2: Preprocess Data

```python
def preprocess_dreams(examples):
    """Format dreams as instruction-following examples"""
    texts = []
    for dream in examples['dream']:
        # Add special formatting
        text = f"### Dream:\n{dream}\n### End"
        texts.append(text)

    # Tokenize
    return tokenizer(
        texts,
        truncation=True,
        max_length=512,
        padding="max_length",
        return_tensors="pt"
    )

# Process the dataset
tokenized_dataset = dataset.map(
    preprocess_dreams,
    batched=True,
    remove_columns=dataset['train'].column_names,
    desc="Tokenizing dreams"
)

# Split into train/validation
split = tokenized_dataset['train'].train_test_split(test_size=0.1, seed=42)
train_dataset = split['train']
eval_dataset = split['test']

print(f"Training samples: {len(train_dataset)}")
print(f"Validation samples: {len(eval_dataset)}")
```

### Step 3: Load Model with LoRA

```python
from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# Load base model
model_name = "gpt2-medium"  # 355M parameters
print(f"Loading {model_name}...")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None,
)

# Configure LoRA for efficient fine-tuning
lora_config = LoraConfig(
    r=16,                              # Rank of the update matrices
    lora_alpha=32,                     # Scaling factor
    target_modules=["c_attn"],         # Which modules to adapt (GPT-2 specific)
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Print trainable parameters
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
all_params = sum(p.numel() for p in model.parameters())
print(f"Trainable params: {trainable_params:,} ({100 * trainable_params / all_params:.2f}%)")
```

### Step 4: Training Configuration

```python
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

# Training arguments
training_args = TrainingArguments(
    output_dir="./redreamer2025-checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,     # Effective batch size = 16
    learning_rate=2e-4,                # Higher LR for LoRA
    fp16=torch.cuda.is_available(),    # Mixed precision training
    logging_steps=50,
    eval_strategy="steps",
    eval_steps=200,
    save_steps=500,
    save_total_limit=3,
    warmup_steps=100,
    logging_dir="./logs",
    report_to="none",                  # Change to "wandb" if you want tracking
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    push_to_hub=False,
    dataloader_num_workers=2,
)

# Data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # Causal LM, not masked LM
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
)
```

### Step 5: Train!

```python
import time

print("Starting training...")
start_time = time.time()

# Train the model
trainer.train()

elapsed = time.time() - start_time
print(f"\nTraining completed in {elapsed/60:.1f} minutes!")

# Save the final model
trainer.save_model("./redreamer2025-final")
print("Model saved to ./redreamer2025-final")
```

### Step 6: Generate Dreams

```python
from transformers import pipeline

# Load your fine-tuned model
dream_generator = pipeline(
    "text-generation",
    model="./redreamer2025-final",
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

def generate_dream(prompt="I had a dream where", num_dreams=3):
    """Generate dream narratives"""

    formatted_prompt = f"### Dream:\n{prompt}"

    dreams = dream_generator(
        formatted_prompt,
        max_length=300,
        temperature=1.1,
        top_k=50,
        top_p=0.95,
        num_return_sequences=num_dreams,
        do_sample=True,
        repetition_penalty=1.2,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.encode("### End")[0],
    )

    return dreams

# Test generation
print("\nGenerating dreams...")
results = generate_dream("I was walking through a forest when suddenly")

for i, dream in enumerate(results, 1):
    text = dream['generated_text'].split("### End")[0]
    print(f"\n{'='*70}")
    print(f"DREAM {i}")
    print(f"{'='*70}")
    print(text)
```

---

## Option C: Custom Dataset Integration

If you want to include your own dream corpus:

```python
from datasets import Dataset
import pandas as pd

def load_custom_dreams(file_path):
    """Load dreams from a text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by double newlines (assuming dreams are separated this way)
    dreams = text.split('\n\n')
    dreams = [d.strip() for d in dreams if len(d.strip()) > 50]

    return dreams

# Load your custom dreams
custom_dreams = load_custom_dreams('./data/dreams1.txt')
print(f"Loaded {len(custom_dreams)} custom dreams")

# Create dataset
df = pd.DataFrame({'dream': custom_dreams})
custom_dataset = Dataset.from_pandas(df)

# Load DreamBank
dreambank = load_dataset("gustavecortal/DreamBank-annotated")

# Combine datasets
from datasets import concatenate_datasets

# Prepare DreamBank dreams
dreambank_formatted = dreambank['train'].map(lambda x: {'dream': x['dream']})

# Combine
combined = concatenate_datasets([dreambank_formatted, custom_dataset])
print(f"Total dreams: {len(combined)}")

# Continue with preprocessing as in Option B...
```

---

## Advanced: Sampling Strategies for Surrealism

Different sampling parameters create different dream "styles":

```python
def generate_dream_with_style(prompt, style="surreal"):
    """Generate dreams with different creative styles"""

    styles = {
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

    params = styles.get(style, styles["surreal"])

    dreams = dream_generator(
        f"### Dream:\n{prompt}",
        max_length=250,
        num_return_sequences=1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        **params
    )

    return dreams[0]['generated_text']

# Try different styles
for style in ["realistic", "surreal", "nightmare", "lucid"]:
    print(f"\n{'='*70}")
    print(f"STYLE: {style.upper()}")
    print(f"{'='*70}")
    dream = generate_dream_with_style("I was flying over a city", style=style)
    print(dream)
```

---

## Deployment Options

### Option 1: Gradio Web Interface

```python
import gradio as gr

def dream_interface(prompt, style, num_dreams):
    """Gradio interface for dream generation"""
    dreams = []
    for _ in range(num_dreams):
        result = generate_dream_with_style(prompt, style)
        dreams.append(result)
    return "\n\n---\n\n".join(dreams)

# Create Gradio interface
demo = gr.Interface(
    fn=dream_interface,
    inputs=[
        gr.Textbox(label="Dream Prompt", placeholder="I was walking through..."),
        gr.Dropdown(["realistic", "surreal", "nightmare", "lucid"], label="Dream Style"),
        gr.Slider(1, 5, value=3, step=1, label="Number of Dreams"),
    ],
    outputs=gr.Textbox(label="Generated Dreams", lines=20),
    title="REDREAMER 2025",
    description="Generate dream narratives using AI",
)

# Launch
demo.launch(share=True)
```

### Option 2: FastAPI REST API

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="REDREAMER 2025 API")

class DreamRequest(BaseModel):
    prompt: str
    style: str = "surreal"
    num_dreams: int = 1

class DreamResponse(BaseModel):
    dreams: list[str]

@app.post("/generate", response_model=DreamResponse)
async def generate_dreams(request: DreamRequest):
    """Generate dream narratives"""
    dreams = []
    for _ in range(request.num_dreams):
        dream = generate_dream_with_style(request.prompt, request.style)
        dreams.append(dream)
    return DreamResponse(dreams=dreams)

# Run with: uvicorn api:app --reload
```

### Option 3: Command-Line Interface

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="REDREAMER 2025 - Dream Generator")
    parser.add_argument("prompt", type=str, help="Dream prompt/seed")
    parser.add_argument("--style", choices=["realistic", "surreal", "nightmare", "lucid"],
                        default="surreal", help="Dream style")
    parser.add_argument("--num", type=int, default=1, help="Number of dreams to generate")
    parser.add_argument("--length", type=int, default=200, help="Maximum length")

    args = parser.parse_args()

    print(f"\nGenerating {args.num} {args.style} dream(s)...\n")

    for i in range(args.num):
        dream = generate_dream_with_style(args.prompt, args.style)
        print(f"\n{'='*70}")
        print(f"DREAM {i+1}")
        print(f"{'='*70}")
        print(dream)

if __name__ == "__main__":
    main()

# Usage: python redreamer_cli.py "I was flying over mountains" --style surreal --num 3
```

---

## Evaluation & Quality Metrics

```python
from transformers import pipeline
import numpy as np

# Load perplexity calculator
def calculate_perplexity(text, model, tokenizer):
    """Calculate perplexity of generated text"""
    encodings = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**encodings, labels=encodings["input_ids"])
        loss = outputs.loss

    perplexity = torch.exp(loss)
    return perplexity.item()

# Diversity metrics
def calculate_diversity(dreams):
    """Calculate lexical diversity"""
    all_words = []
    for dream in dreams:
        words = dream.lower().split()
        all_words.extend(words)

    unique_words = len(set(all_words))
    total_words = len(all_words)

    return unique_words / total_words  # Type-Token Ratio

# Dream-specific metrics
def dream_quality_score(dream_text):
    """Heuristic quality score for dreams"""
    score = 0

    # Check for surreal elements (bonus points)
    surreal_keywords = ["strange", "impossible", "floating", "flying", "transform",
                        "suddenly", "appeared", "disappeared", "shifted"]
    score += sum(1 for word in surreal_keywords if word in dream_text.lower())

    # Check for emotional content
    emotions = ["fear", "joy", "sad", "happy", "anxious", "peaceful", "terrified"]
    score += sum(1 for word in emotions if word in dream_text.lower()) * 2

    # Penalize very short dreams
    word_count = len(dream_text.split())
    if word_count < 50:
        score -= 5

    # Bonus for good length
    if 100 < word_count < 300:
        score += 3

    return max(0, score)

# Evaluate generated dreams
test_prompts = [
    "I was in a library",
    "I saw my childhood home",
    "I was running from something",
]

for prompt in test_prompts:
    dreams = generate_dream(prompt, num_dreams=3)

    print(f"\nPrompt: {prompt}")
    for i, dream in enumerate(dreams, 1):
        text = dream['generated_text']
        quality = dream_quality_score(text)
        print(f"  Dream {i} quality score: {quality}")
```

---

## Troubleshooting

### Out of Memory (OOM) Errors

```python
# Solution 1: Reduce batch size
training_args = TrainingArguments(
    per_device_train_batch_size=2,  # Reduce from 4
    gradient_accumulation_steps=8,  # Increase to maintain effective batch size
)

# Solution 2: Use 8-bit quantization
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

# Solution 3: Use gradient checkpointing
model.gradient_checkpointing_enable()
```

### Slow Generation

```python
# Solution: Use optimized generation
from transformers import GenerationConfig

generation_config = GenerationConfig(
    max_length=200,
    temperature=1.1,
    top_k=50,
    top_p=0.95,
    do_sample=True,
    pad_token_id=tokenizer.pad_token_id,
    use_cache=True,  # Enable KV cache
)

dreams = model.generate(
    input_ids,
    generation_config=generation_config,
)
```

### Repetitive Text

```python
# Solution: Adjust sampling parameters
dreams = generator(
    prompt,
    repetition_penalty=1.5,      # Increase penalty
    no_repeat_ngram_size=3,      # Prevent 3-gram repetitions
    early_stopping=True,
)
```

---

## Next Steps

1. **Experiment with different base models:**
   - GPT-2 Small/Medium/Large
   - GPT-Neo 125M/1.3B
   - LLaMA 2 7B (requires more GPU memory)

2. **Try advanced techniques:**
   - Multi-stage fine-tuning (general → dreams → personal)
   - Prompt engineering with few-shot examples
   - Classifier-free guidance for style control

3. **Build a dataset:**
   - Collect your own dreams over time
   - Fine-tune a personalized model
   - Track dream themes and patterns

4. **Share your work:**
   - Upload model to HuggingFace Hub
   - Create a Spaces demo
   - Write a blog post about your experience

---

## Resources

- **HuggingFace Transformers:** https://huggingface.co/docs/transformers
- **PEFT Library:** https://huggingface.co/docs/peft
- **DreamBank Dataset:** https://huggingface.co/datasets/gustavecortal/DreamBank-annotated
- **PyTorch Tutorials:** https://pytorch.org/tutorials/
- **Original REDREAMER:** https://github.com/lfhvn/REDREAMER

---

**Happy Dream Generating! 🌙✨**
