import os
import base64
import uuid
import io
from datetime import datetime
from pathlib import Path

import requests

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("FastAPI not installed. Run: pip install fastapi uvicorn")
    raise

app = FastAPI(title="DpForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path("generated")
OUTPUT_DIR.mkdir(exist_ok=True)

HF_TOKEN = os.getenv("HF_TOKEN", "")

class GenerateRequest(BaseModel):
    prompt: str
    style: str = "realistic"

class GenerateResponse(BaseModel):
    success: bool
    image_url: str | None = None
    error: str | None = None

class StatusResponse(BaseModel):
    status: str
    provider: str
    models: list[str] = []

def check_huggingface():
    global HF_TOKEN
    if not HF_TOKEN:
        HF_TOKEN = os.getenv("HF_TOKEN", "")
    if HF_TOKEN:
        return "configured"
    return "no_token"

@app.get("/api/status", response_model=StatusResponse)
async def check_status():
    hf_status = check_huggingface()
    return StatusResponse(
        status=hf_status,
        provider="huggingface",
        models=["black-forest-labs/FLUX.1-schnell"]
    )

STYLE_MODIFIERS = {
    "realistic": "photorealistic portrait, high quality, 8k",
    "cartoon": "cartoon style avatar, vibrant colors, cute",
    "anime": "anime style, manga artwork, detailed",
    "abstract": "abstract art, geometric patterns, colorful"
}

def generate_with_huggingface(prompt: str) -> bytes | None:
    global HF_TOKEN
    
    if not HF_TOKEN:
        raise Exception("HF_TOKEN required. Set the HF_TOKEN environment variable.")
    
    try:
        from huggingface_hub import InferenceClient
        
        client = InferenceClient(provider="fal-ai", api_key=HF_TOKEN)
        
        model = os.getenv("HF_MODEL", "black-forest-labs/FLUX.1-schnell")
        
        image = client.text_to_image(prompt, model=model)
        
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        return img_bytes.getvalue()
        
    except ImportError:
        raise Exception("Install huggingface_hub: pip install huggingface_hub")
    except Exception as e:
        raise Exception(f"HuggingFace error: {str(e)}")

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest):
    try:
        enhanced_prompt = f"{request.prompt}, {STYLE_MODIFIERS.get(request.style, '')}, square format, portrait orientation"
        
        image_data = generate_with_huggingface(enhanced_prompt)
        
        filename = f"dp_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%H%M%S')}.png"
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, "wb") as f:
            f.write(image_data)
        
        return GenerateResponse(
            success=True,
            image_url=f"/api/image/{filename}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return GenerateResponse(success=False, error=str(e))

@app.get("/api/image/{filename}")
async def get_image(filename: str):
    filepath = OUTPUT_DIR / filename
    if not filepath.exists() or not filepath.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(filepath, media_type="image/png")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    static_dir = Path("static")
    file = static_dir / file_path
    if file.exists() and file.is_file():
        media_type = "text/html"
        if file_path.endswith(".css"):
            media_type = "text/css"
        elif file_path.endswith(".js"):
            media_type = "application/javascript"
        return FileResponse(file, media_type=media_type)
    return None

if __name__ == "__main__":
    print(f"\n{'='*40}")
    print("  DpForge - Display Picture Forge")
    print(f"{'='*40}")
    print(f"\n  Provider: HuggingFace")
    print("  Model: black-forest-labs/FLUX.1-schnell")
    print("\n  Set HF_TOKEN env var to use")
    print(f"\n  Open: http://localhost:8000")
    print(f"{'='*40}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)