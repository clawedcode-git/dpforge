# DpForge - Display Picture Forge

Forge your perfect avatar in seconds. A local-first web application for generating display pictures using Ollama AI.

![DpForge](https://img.shields.io/badge/DpForge-Avatar%20Generator-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Local-First**: All processing happens on your machine using Ollama
- **Privacy**: No data sent to external servers
- **Multiple Styles**: Realistic, Cartoon, Anime, and Abstract avatars
- **Quick Prompts**: One-click suggestions for inspiration
- **Instant Download**: Save your avatar in one click

## Prerequisites

1. **Python 3.9+**
2. **Ollama** installed and running
3. An image generation model (see below)

## Quick Start

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows - Download from https://ollama.ai/download
```

### 2. Pull an Image Generation Model

```bash
# Recommended: SDXL Turbo (fast, high quality)
ollama pull sdxl-turbo

# Alternative: Llava (vision model)
ollama pull llava
```

### 3. Install Python Dependencies

```bash
cd dpforge
pip install -r requirements.txt
```

### 4. Run the Server

```bash
python server.py
```

### 5. Open in Browser

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
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |

## Supported Models

The app works with Ollama's image generation models:
- `sdxl-turbo` - Recommended, fast and high quality
- `sd3` - Stable Diffusion 3
- `playwright` - Alternative model

Make sure to pull the model before use:
```bash
ollama pull sdxl-turbo
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /api/status` | GET | Check Ollama connection status |
| `POST /api/generate` | POST | Generate an avatar image |
| `GET /api/image/{filename}` | GET | Retrieve generated image |

## Troubleshooting

### "Ollama Offline" message
- Make sure Ollama is running: `ollama serve`
- Check if the model is pulled: `ollama list`

### Generation fails
- Ensure you have enough RAM (8GB+ recommended)
- Try a smaller model like `sdxl-turbo`

### Port already in use
```bash
# Change port in server.py
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## License

MIT License - feel free to use and modify!

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.
