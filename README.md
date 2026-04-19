# DpForge

### Display Picture Forge

Forge your perfect avatar in seconds using AI image generation.

---

## Features

- **HuggingFace Inference** — FLUX.1-schnell model via Inference Providers
- **Multiple Styles** — Realistic, Cartoon, Anime, and Abstract avatars
- **Quick Prompts** — One-click suggestions for inspiration
- **Instant Download** — Save your avatar in one click

## Requirements

- Python 3.9+
- HuggingFace account with Inference Providers permission

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your HuggingFace token
export HF_TOKEN="your_token_here"

# 3. Run the server
python server.py
```

Then open **http://localhost:8000** in your browser.

## Usage

1. Enter a description (e.g., "a wise owl", "space explorer")
2. Select a style
3. Click "Forge Avatar"
4. Download your generated image

---

## Project Structure

```
dpforge/
├── server.py          # FastAPI backend
├── requirements.txt  # Python dependencies
├── AGENTS.md        # Developer docs
└── static/
    ├── index.html   # Frontend HTML
    ├── styles.css  # Styling
    └── app.js       # Frontend logic
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | — | HuggingFace API token (required) |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /api/status` | GET | Check provider connection |
| `POST /api/generate` | POST | Generate an avatar |
| `GET /api/image/{filename}` | GET | Retrieve generated image |

---

## Troubleshooting

**Token permission error:**
> Go to [HuggingFace Settings](https://huggingface.co/settings/tokens), create a new token, and enable **"Inference Providers"** permission.

**Model loading error:**
> Wait 30-60 seconds on first request — the model needs to warm up.

---

## License

MIT License

---

## Contributing

Open to contributions! Open issues or submit pull requests on [GitHub](https://github.com/clawedcode-git/dpforge).