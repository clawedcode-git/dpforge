# DpForge - Display Picture Forge

Forge your perfect avatar in seconds. A web application for generating display pictures using AI image generation.

![DpForge](https://img.shields.io/badge/DpForge-Avatar%20Generator-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **HuggingFace Inference**: Uses FLUX.1-schnell model via Inference Providers
- **Multiple Styles**: Realistic, Cartoon, Anime, and Abstract avatars
- **Quick Prompts**: One-click suggestions for inspiration
- **Instant Download**: Save your avatar in one click

## Prerequisites

1. **Python 3.9+**
2. **HuggingFace account** with Inference Providers permission

## Quick Start

### 1. Install Python Dependencies

```bash
cd dpforge
pip install -r requirements.txt
```

### 2. Setup HuggingFace

1. Get a token from [HuggingFace](https://huggingface.co/settings/tokens)
2. Make sure the token has **"Inference Providers"** permission
3. Set the environment variable:

```bash
export HF_TOKEN="your_token_here"
python server.py
```

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
├── AGENTS.md         # Developer documentation
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
| `HF_TOKEN` | - | HuggingFace API token (required) |
| `HF_MODEL` | `black-forest-labs/FLUX.1-schnell` | HuggingFace model ID |

### Available Models

- `black-forest-labs/FLUX.1-schnell` (default, fast)
- `black-forest-labs/FLUX.1-dev` (higher quality, slower)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /api/status` | GET | Check provider connection status |
| `POST /api/generate` | POST | Generate an avatar image |
| `GET /api/image/{filename}` | GET | Retrieve generated image |

## Troubleshooting

### "HF_TOKEN needs Inference Providers permission"

1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a new token or edit an existing one
3. Enable **"Inference Providers"** permission

### "Model is loading" error

- The model needs to warm up on first request
- Wait 30-60 seconds and try again
- Models stay loaded for a period after use

### Rate limit reached

- Wait a few minutes
- HF free tier has rate limits

## License

MIT License - feel free to use and modify!

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.