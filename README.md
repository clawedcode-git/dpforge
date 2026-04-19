# DpForge

**Display Picture Forge** — AI-powered avatar generator built with FastAPI and HuggingFace Inference Providers.

Generate unique, high-quality avatars from text descriptions in seconds.

---

## Features

| Feature | Description |
|---------|-------------|
| **AI-Powered** | FLUX.1-schnell model for fast, high-quality generation |
| **Multiple Styles** | Realistic, Cartoon, Anime, and Abstract |
| **One-Click Download** | Instantly save PNG images |
| **REST API** | Programmatic access via built-in endpoints |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your HuggingFace token
export HF_TOKEN="your_token_here"

# 3. Run the server
python server.py
```

Open **http://localhost:8000** in your browser.

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HF_TOKEN` | Yes | HuggingFace API token with Inference Providers permission |

Get your token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens). Ensure **"Inference Providers"** is enabled.

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Check provider connection status |
| `/api/generate` | POST | Generate an avatar from a prompt |
| `/api/image/{filename}` | GET | Retrieve a generated image |

### Generate Endpoint

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a wise owl", "style": "realistic"}'
```

---

## Project Structure

```
dpforge/
├── server.py          # FastAPI backend
├── requirements.txt   # Python dependencies
├── AGENTS.md         # Developer documentation
└── static/
    ├── index.html   # Frontend HTML
    ├── styles.css   # Styling
    └── app.js       # Frontend logic
```

---

## Troubleshooting

### 401 Unauthorized Error
Your token lacks Inference Providers permission. Create a new token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and enable the permission.

### Slow First Request
The model requires 30-60 seconds to load on first request. Subsequent requests are faster.

---

## License

MIT License. See [LICENSE](LICENSE) for details.