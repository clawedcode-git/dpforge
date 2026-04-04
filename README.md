# DpForge - Display Picture Forge

Forge your perfect avatar in seconds. A web application for generating display pictures using AI image generation models.

![DpForge](https://img.shields.io/badge/DpForge-Avatar%20Generator-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Multiple Backends**: Use HuggingFace API, Ollama, or local Stable Diffusion
- **Free Tier Support**: Works with HuggingFace's free inference API
- **Multiple Styles**: Realistic, Cartoon, Anime, and Abstract avatars
- **Quick Prompts**: One-click suggestions for inspiration
- **Instant Download**: Save your avatar in one click

## Prerequisites

1. **Python 3.9+**
2. An image generation provider (see below)

## Quick Start

### 1. Install Python Dependencies

```bash
cd dpforge
pip install -r requirements.txt
```

### 2. Choose Your Image Generation Provider

#### Option A: HuggingFace API (Recommended - Free Tier)

1. Get a free token from [HuggingFace](https://huggingface.co/settings/tokens)
2. Set the environment variable:

```bash
export HF_TOKEN="your_token_here"
export IMAGE_PROVIDER="huggingface"
python server.py
```

**Note**: Free tier has rate limits. Models may need to "warm up" on first use.

#### Option B: Ollama (Local)

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull sdxl-turbo

# Run with Ollama provider
export IMAGE_PROVIDER="ollama"
python server.py
```

#### Option C: Local Stable Diffusion (GPU Required)

Requires a CUDA-compatible GPU with 8GB+ VRAM.

**Setup:**

1. **Install CUDA Toolkit** (if not already installed)
   - Download from [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)

2. **Install PyTorch with CUDA support:**
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

3. **Run the app:**
   ```bash
   export IMAGE_PROVIDER="local"
   python server.py
   ```

**Recommended Models:**
- `stabilityai/stable-diffusion-xl-base-1.0` (default, good balance)
- `stabilityai/sd-turbo` (faster, lower quality)

Set model via: `export LOCAL_MODEL_ID="stabilityai/sd-turbo"`

**Hardware Requirements:**
- NVIDIA GPU with 8GB+ VRAM (RTX 3070 or better recommended)
- 16GB+ RAM
- 20GB+ disk space for models

### 3. Open in Browser

Navigate to: **http://localhost:8000**

## Usage

1. Enter a description of your desired avatar (e.g., "a wise owl", "space explorer")
2. Select a style (Realistic, Cartoon, Anime, or Abstract)
3. Click "Forge Avatar"
4. Download your generated image!

## Project Structure

```
dpforge/
├── server.py          # FastAPI backend server
├── requirements.txt   # Python dependencies
├── SPEC.md           # Design specification
├── README.md         # This file
└── static/
    ├── index.html    # Main HTML page
    ├── styles.css    # Styling
    └── app.js        # Frontend logic
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `IMAGE_PROVIDER` | `huggingface` | Provider: `huggingface`, `ollama`, or `local` |
| `HF_TOKEN` | - | HuggingFace API token (required for HuggingFace) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `HF_MODEL` | `stabilityai/stable-diffusion-3-medium` | HuggingFace model ID |

### Provider Comparison

| Provider | Cost | Speed | Quality | Setup |
|----------|------|-------|---------|-------|
| HuggingFace API | Free tier | Medium | High | Easy |
| Ollama | Free | Fast (local) | High | Medium |
| Local SD | Free | Fast (GPU) | High | Complex |

### Recommended HuggingFace Models

- `stabilityai/stable-diffusion-3-medium` - Latest, best quality
- `stabilityai/stable-diffusion-xl-base-1.0` - Stable, reliable

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /api/status` | GET | Check provider connection status |
| `POST /api/generate` | POST | Generate an avatar image |
| `GET /api/image/{filename}` | GET | Retrieve generated image |

## Troubleshooting

### HuggingFace Issues

**"Model is loading" error**
- The model needs to warm up on first request
- Wait 30-60 seconds and try again
- Models stay loaded for a period after use

**Rate limit reached**
- Wait a few minutes
- Consider upgrading to Pro tier

### Ollama Issues

**"Ollama Offline" message**
- Make sure Ollama is running: `ollama serve`
- Check if the model is pulled: `ollama list`

### Local Generation Issues

**Out of memory**
- Use a smaller model
- Reduce image resolution
- Ensure sufficient GPU VRAM (8GB+ recommended)

### Port already in use

```bash
# Edit server.py line 152:
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## License

MIT License - feel free to use and modify!

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.
