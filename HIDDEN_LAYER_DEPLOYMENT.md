# Deploying REDREAMER 2025 to hidden-layer Repository

This guide explains how to deploy the REDREAMER 2025 Video Edition to the `lfhvn/hidden-layer` repository.

---

## Quick Deploy

### Option 1: Copy Core Files

```bash
# Clone hidden-layer repo (if not already cloned)
git clone https://github.com/lfhvn/hidden-layer
cd hidden-layer

# Create redreamer directory
mkdir -p redreamer2025

# Copy essential files from REDREAMER repo
cp ../REDREAMER/redreamer_video.py redreamer2025/
cp ../REDREAMER/redreamer2025_quickstart.py redreamer2025/
cp ../REDREAMER/requirements_2025.txt redreamer2025/
cp ../REDREAMER/README_VIDEO_EDITION.md redreamer2025/README.md

# Copy documentation
cp ../REDREAMER/IMPLEMENTATION_COMPARISON.md redreamer2025/docs/
cp ../REDREAMER/VIDEO_GENERATION_DESIGN.md redreamer2025/docs/
cp ../REDREAMER/RESEARCH_PAPERS.md redreamer2025/docs/
cp ../REDREAMER/REDREAMER_2025_ASSESSMENT.md redreamer2025/docs/
cp ../REDREAMER/REDREAMER_2025_IMPLEMENTATION.md redreamer2025/docs/

# Commit
git add redreamer2025/
git commit -m "Add REDREAMER 2025 video dream generation"
git push
```

---

### Option 2: Git Subtree (Advanced)

```bash
# In hidden-layer repo
git subtree add --prefix=redreamer2025 \
    https://github.com/lfhvn/REDREAMER.git main --squash
```

---

### Option 3: Submodule

```bash
# In hidden-layer repo
git submodule add https://github.com/lfhvn/REDREAMER.git redreamer
git commit -m "Add REDREAMER as submodule"
```

---

## Recommended Structure for hidden-layer

```
hidden-layer/
├── README.md (main repo README)
├── redreamer2025/
│   ├── README.md (Video Edition README)
│   ├── redreamer_video.py (main script)
│   ├── redreamer2025_quickstart.py (quickstart)
│   ├── requirements.txt (-> requirements_2025.txt)
│   │
│   ├── docs/
│   │   ├── IMPLEMENTATION_COMPARISON.md
│   │   ├── VIDEO_GENERATION_DESIGN.md
│   │   ├── RESEARCH_PAPERS.md
│   │   ├── REDREAMER_2025_ASSESSMENT.md
│   │   └── REDREAMER_2025_IMPLEMENTATION.md
│   │
│   ├── examples/
│   │   ├── basic_text_generation.py
│   │   ├── video_with_runway.py
│   │   ├── local_video_generation.py
│   │   └── batch_processing.py
│   │
│   ├── models/ (optional)
│   │   └── .gitkeep
│   │
│   └── output/ (optional)
│       └── .gitkeep
│
└── [other hidden-layer content]
```

---

## Integration with Existing hidden-layer Code

If `hidden-layer` already has ML infrastructure:

### Use as Module

```python
# In hidden-layer project
from redreamer2025.redreamer_video import DreamVideoGenerator

# Initialize
generator = DreamVideoGenerator(
    text_model="gpt2-medium",
    video_backend="runway",
    api_key=os.getenv("RUNWAY_API_KEY")
)

# Generate
results = generator.create_dream_video(
    prompt="I was flying through space",
    style="surreal"
)
```

### Integration Points

```python
# If hidden-layer has:

# 1. Model registry
from hidden_layer.models import ModelRegistry
registry = ModelRegistry()
registry.register("dream-generator", DreamVideoGenerator)

# 2. API endpoints
from hidden_layer.api import APIRouter
router = APIRouter()

@router.post("/generate-dream")
def generate_dream(prompt: str, style: str):
    generator = DreamVideoGenerator()
    return generator.create_dream_video(prompt, style)

# 3. Task queue
from hidden_layer.tasks import celery_app

@celery_app.task
def generate_dream_async(prompt, style):
    generator = DreamVideoGenerator()
    return generator.create_dream_video(prompt, style)
```

---

## Configuration

### Environment Variables

Create `.env` in `redreamer2025/`:

```bash
# Text Generation
TEXT_MODEL=gpt2-medium
# or: TEXT_MODEL=meta-llama/Llama-2-7b-hf

# Video Generation
VIDEO_BACKEND=runway
# Options: local, runway, luma, none

# API Keys
RUNWAY_API_KEY=your_runway_key_here
LUMA_API_KEY=your_luma_key_here

# Paths
MODEL_CACHE_DIR=./models
OUTPUT_DIR=./output

# Performance
USE_GPU=true
GPU_MEMORY_FRACTION=0.8
```

### Load in Code

```python
from dotenv import load_dotenv
import os

load_dotenv()

generator = DreamVideoGenerator(
    text_model=os.getenv("TEXT_MODEL", "gpt2-medium"),
    video_backend=os.getenv("VIDEO_BACKEND"),
    api_key=os.getenv(f"{os.getenv('VIDEO_BACKEND').upper()}_API_KEY")
)
```

---

## Docker Deployment (hidden-layer Infrastructure)

### Dockerfile

```dockerfile
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_2025.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY redreamer_video.py .
COPY redreamer2025_quickstart.py .

# Set entrypoint
ENTRYPOINT ["python", "redreamer_video.py"]
```

### Build & Run

```bash
# Build
docker build -t hidden-layer/redreamer2025 .

# Run (text only)
docker run hidden-layer/redreamer2025 \\
    --prompt "I was flying" --style surreal

# Run (with Runway API)
docker run -e RUNWAY_API_KEY=$RUNWAY_API_KEY \\
    hidden-layer/redreamer2025 \\
    --prompt "I was flying" --backend runway --api-key $RUNWAY_API_KEY

# Run (with GPU)
docker run --gpus all \\
    hidden-layer/redreamer2025 \\
    --prompt "I was flying" --backend local
```

---

## Kubernetes Deployment (if hidden-layer uses K8s)

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redreamer-config
data:
  text-model: "gpt2-medium"
  video-backend: "runway"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: redreamer-secrets
type: Opaque
stringData:
  runway-api-key: "your_key_here"
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redreamer-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: redreamer
  template:
    metadata:
      labels:
        app: redreamer
    spec:
      containers:
      - name: redreamer
        image: hidden-layer/redreamer2025:latest
        env:
        - name: TEXT_MODEL
          valueFrom:
            configMapKeyRef:
              name: redreamer-config
              key: text-model
        - name: RUNWAY_API_KEY
          valueFrom:
            secretKeyRef:
              name: redreamer-secrets
              key: runway-api-key
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
```

---

## API Server (FastAPI Integration)

If `hidden-layer` uses FastAPI:

```python
# hidden-layer/api/redreamer_routes.py

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from redreamer2025.redreamer_video import DreamVideoGenerator
import os

router = APIRouter(prefix="/api/redreamer", tags=["dreams"])

# Initialize generator (could be dependency injected)
generator = DreamVideoGenerator(
    video_backend=os.getenv("VIDEO_BACKEND", "runway"),
    api_key=os.getenv("RUNWAY_API_KEY")
)

class DreamRequest(BaseModel):
    prompt: str
    style: str = "surreal"
    generate_video: bool = False

class DreamResponse(BaseModel):
    dream_id: str
    dream_text: str
    status: str
    video_urls: list[str] = []

@router.post("/generate", response_model=DreamResponse)
async def generate_dream(request: DreamRequest, background_tasks: BackgroundTasks):
    """Generate a dream (text and optionally video)"""

    try:
        # Generate dream text immediately
        dream_text = generator.generate_dream_text(request.prompt, request.style)

        # Create response
        dream_id = str(uuid.uuid4())
        response = DreamResponse(
            dream_id=dream_id,
            dream_text=dream_text,
            status="text_complete"
        )

        # Queue video generation if requested
        if request.generate_video:
            background_tasks.add_task(
                generate_video_async,
                dream_id,
                dream_text,
                request.style
            )
            response.status = "generating_video"

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dream/{dream_id}")
async def get_dream(dream_id: str):
    """Get dream status and videos"""
    # Check database/cache for dream status
    # Return video URLs when ready
    pass

async def generate_video_async(dream_id: str, dream_text: str, style: str):
    """Background task for video generation"""
    # Generate videos
    # Upload to storage (S3, etc.)
    # Update database with URLs
    pass
```

---

## Testing Suite

```python
# redreamer2025/tests/test_generation.py

import pytest
from redreamer_video import DreamVideoGenerator

@pytest.fixture
def generator():
    return DreamVideoGenerator(text_model="gpt2")

def test_text_generation(generator):
    dream = generator.generate_dream_text("I was flying", style="surreal")
    assert len(dream) > 50
    assert "flying" in dream.lower() or "fly" in dream.lower()

def test_scene_extraction(generator):
    text = "I saw a door. It opened slowly. A figure appeared."
    scenes = generator.extract_visual_scenes(text)
    assert len(scenes) >= 2

def test_prompt_enhancement(generator):
    scene = "A door in the darkness"
    enhanced = generator.enhance_prompt_for_video(scene)
    assert "cinematic" in enhanced
    assert "dreamlike" in enhanced

@pytest.mark.gpu
def test_local_video(generator_with_gpu):
    # Only run if GPU available
    video_path = generator_with_gpu.generate_video_local(
        "A surreal landscape",
        "test.mp4"
    )
    assert Path(video_path).exists()
```

---

## CI/CD Pipeline

```yaml
# .github/workflows/redreamer-ci.yml

name: REDREAMER CI

on:
  push:
    paths:
      - 'redreamer2025/**'
  pull_request:
    paths:
      - 'redreamer2025/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd redreamer2025
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          cd redreamer2025
          pytest tests/ --cov=./ --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          cd redreamer2025
          docker build -t hidden-layer/redreamer2025:${{ github.sha }} .

      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push hidden-layer/redreamer2025:${{ github.sha }}
```

---

## Monitoring & Logging

```python
# Integration with hidden-layer monitoring

from hidden_layer.monitoring import metrics, logger

class MonitoredDreamGenerator(DreamVideoGenerator):
    """DreamVideoGenerator with monitoring"""

    @metrics.count("dreams.generated")
    @metrics.time("dreams.generation_time")
    def create_dream_video(self, prompt, style="surreal", output_dir="output"):
        logger.info(f"Generating dream: prompt={prompt}, style={style}")

        try:
            result = super().create_dream_video(prompt, style, output_dir)
            metrics.increment("dreams.success")
            logger.info(f"Dream generated successfully: {result}")
            return result

        except Exception as e:
            metrics.increment("dreams.error")
            logger.error(f"Dream generation failed: {e}")
            raise
```

---

## Documentation Updates

### Update hidden-layer README.md

Add section:

```markdown
## REDREAMER 2025: Dream Generation

Generate AI dreams as text and video.

### Quick Start

\`\`\`bash
cd redreamer2025
python redreamer_video.py --prompt "I was flying"
\`\`\`

See [redreamer2025/README.md](redreamer2025/README.md) for full documentation.
```

---

## Maintenance

### Update Schedule

- **Weekly:** Check for security updates in dependencies
- **Monthly:** Update base models if available
- **Quarterly:** Review and update video generation backends

### Health Checks

```python
# Add to hidden-layer health check endpoint
@app.get("/health/redreamer")
def check_redreamer_health():
    try:
        generator = DreamVideoGenerator()
        test_dream = generator.generate_dream_text("test", "surreal")
        return {"status": "healthy", "version": "2025.1"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## Migration Checklist

- [ ] Clone/navigate to hidden-layer repository
- [ ] Copy REDREAMER files to appropriate locations
- [ ] Install dependencies: `pip install -r requirements_2025.txt`
- [ ] Set up environment variables
- [ ] Run basic test: `python redreamer_video.py --prompt "test"`
- [ ] Integrate with existing hidden-layer infrastructure
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring and logging
- [ ] Update documentation
- [ ] Deploy to staging
- [ ] Run integration tests
- [ ] Deploy to production
- [ ] Monitor for issues

---

## Support

For issues specific to REDREAMER:
- Original repo: https://github.com/lfhvn/REDREAMER
- Documentation: See `docs/` folder

For issues specific to hidden-layer integration:
- Create issue in hidden-layer repo
- Tag with `redreamer` label

---

**Ready to deploy! 🚀**
