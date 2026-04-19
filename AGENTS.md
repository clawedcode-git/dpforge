# AGENTS.md - DpForge

## Running the app

```bash
python server.py
```
Opens at http://localhost:8000

## Required environment variables

| Variable | Description |
|---------|-------------|
| `HF_TOKEN` | HuggingFace API token with "Inference Providers" permission (get from huggingface.co/settings/tokens) |

## Setup

```bash
export HF_TOKEN="your_token"
python server.py
```

**Note:** Token must have "Inference Providers" permission enabled in your HuggingFace account settings.

## Project structure

- `server.py` - FastAPI backend, entry point
- `static/` - Frontend (HTML, CSS, JS)
- `generated/` - Output images directory (created at runtime)

## API endpoints

- `GET /api/status` - Check provider connection
- `POST /api/generate` - Generate avatar
- `GET /api/image/{filename}` - Retrieve image

## Notes

- Uses HuggingFace Inference Providers (fal-ai backend) for image generation
- Uses black-forest-labs/FLUX.1-schnell model
- First request may be slow (model warmup)
- Output images saved to `generated/` with unique filenames