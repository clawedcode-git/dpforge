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

PROVIDER = os.getenv("IMAGE_PROVIDER", "huggingface").lower()

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium"

class GenerateRequest(BaseModel):
    prompt: str
    style: str = "realistic"
    provider: str | None = None

class GenerateResponse(BaseModel):
    success: bool
    image_url: str | None = None
    error: str | None = None
    provider: str | None = None

class StatusResponse(BaseModel):
    status: str
    provider: str
    models: list[str] = []

def check_ollama():
    try:
        response = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        if response.status_code == 200:
            return "connected", [m.get("name", "") for m in response.json().get("models", [])]
    except:
        pass
    return "disconnected", []

def check_huggingface():
    global HF_TOKEN
    if not HF_TOKEN:
        HF_TOKEN = os.getenv("HF_TOKEN", "")
    if HF_TOKEN:
        return "configured"
    return "no_token"

@app.get("/api/status", response_model=StatusResponse)
async def check_status():
    provider = PROVIDER
    
    if provider == "ollama":
        status, models = check_ollama()
        return StatusResponse(
            status=status,
            provider="ollama",
            models=models
        )
    elif provider == "huggingface":
        hf_status = check_huggingface()
        return StatusResponse(
            status=hf_status,
            provider="huggingface",
            models=["stable-diffusion-3-medium", "stabilityai/stable-diffusion-xl-base-1.0"]
        )
    elif provider == "local":
        return StatusResponse(
            status="ready",
            provider="local",
            models=["local-diffusers"]
        )
    
    return StatusResponse(status="unknown", provider=provider)

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
        import falav5
        
        client = falav5.FalAV5(
            api_key=HF_TOKEN
        )
        
        image = client.image_generation(
            prompt=prompt,
            model_id="black-forest-labs/FLUX.1-schnell"
        )
        
        response = requests.get(image.images[0].url, timeout=60)
        
        if response.status_code == 200:
            return response.content
        raise Exception(f"Download failed: {response.status_code}")
        
    except ImportError:
        raise Exception("Install falav5: pip install falav5")
    except Exception as e:
        if "401" in str(e) or "Unauthorized" in str(e):
            raise Exception("HF_TOKEN needs 'Inference Providers' permission. Try using Ollama (local) instead - see AGENTS.md")
        raise Exception(f"HuggingFace error: {str(e)}")

def generate_with_ollama(prompt: str) -> str | None:
    payload = {
        "model": "sdxl-turbo",
        "prompt": prompt,
    }
    
    response = requests.post(
        f"{OLLAMA_BASE}/api/generate",
        json=payload,
        timeout=120
    )
    
    if response.status_code == 200:
        result = response.json()
        return result.get("images", [None])[0] or result.get("base64")
    raise Exception("Ollama generation failed")

def generate_with_local(prompt: str) -> bytes | None:
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        
        model_id = os.getenv("LOCAL_MODEL_ID", "stabilityai/stable-diffusion-xl-base-1.0")
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        
        image = pipe(prompt).images[0]
        
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        return img_bytes.getvalue()
    except ImportError:
        raise Exception("Install diffusers: pip install diffusers torch")
    except Exception as e:
        raise Exception(f"Local generation error: {str(e)}")

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest):
    try:
        provider = request.provider or PROVIDER
        enhanced_prompt = f"{request.prompt}, {STYLE_MODIFIERS.get(request.style, '')}, square format, portrait orientation"
        
        image_data = None
        
        if provider == "huggingface":
            image_data = generate_with_huggingface(enhanced_prompt)
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data)
        elif provider == "ollama":
            b64_data = generate_with_ollama(enhanced_prompt)
            image_data = base64.b64decode(b64_data)
        elif provider == "local":
            image_data = generate_with_local(enhanced_prompt)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        filename = f"dp_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%H%M%S')}.png"
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, "wb") as f:
            f.write(image_data)
        
        return GenerateResponse(
            success=True,
            image_url=f"/api/image/{filename}",
            provider=provider
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return GenerateResponse(success=False, error=str(e), provider=request.provider or PROVIDER)

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
    print(f"\n  Provider: {PROVIDER.upper()}")
    
    if PROVIDER == "huggingface":
        print("  Using: HuggingFace Inference API")
        print("  Set HF_TOKEN env var for faster access")
    elif PROVIDER == "ollama":
        print("  Using: Ollama (local)")
        print(f"  Endpoint: {OLLAMA_BASE}")
    else:
        print("  Using: Local Stable Diffusion")
    
    print(f"\n  Open: http://localhost:8000")
    print(f"{'='*40}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
