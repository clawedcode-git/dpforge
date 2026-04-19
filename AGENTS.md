# AGENTS.md - DpForge

## Running the app

```bash
python server.py
```
Opens at http://localhost:8000

## Required environment variables

| Variable | Provider | Description |
|---------|---------|-------------|
| `HF_TOKEN` | huggingface | HuggingFace API token (get from huggingface.co/settings/tokens) |
| `IMAGE_PROVIDER` | all | `huggingface` (default), `ollama`, or `local` |

## Provider-specific setup

### HuggingFace (default, free tier)
```bash
export HF_TOKEN="your_token"
export IMAGE_PROVIDER="huggingface"
python server.py
```

### Ollama (local)
```bash
ollama pull sdxl-turbo
export IMAGE_PROVIDER="ollama"
python server.py
```

### Local Stable Diffusion (GPU required, 8GB+ VRAM)
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
export IMAGE_PROVIDER="local"
python server.py
```

## Project structure

- `server.py` - FastAPI backend, entry point
- `static/` - Frontend (HTML, CSS, JS)
- `generated/` - Output images directory (created at runtime)

## API endpoints

- `GET /api/status` - Check provider connection
- `POST /api/generate` - Generate avatar
- `GET /api/image/{filename}` - Retrieve image

## Notes

- First HuggingFace request may be slow (model "warmup")
- Free tier has rate limits
- Output images saved to `generated/` with unique filenames