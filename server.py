import requests
import base64
import uuid
import os
from datetime import datetime
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    print("FastAPI not installed. Run: pip install fastapi uvicorn")

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

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

class GenerateRequest(BaseModel):
    prompt: str
    style: str = "realistic"

class GenerateResponse(BaseModel):
    success: bool
    image_url: str | None = None
    error: str | None = None

@app.get("/api/status")
async def check_status():
    try:
        response = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            has_image_model = any(
                "sdxl" in m.get("name", "").lower() or
                "llama" in m.get("name", "").lower() or
                "stable" in m.get("name", "").lower()
                for m in models
            )
            return {
                "status": "connected",
                "models": [m.get("name") for m in models],
                "has_image_model": has_image_model
            }
    except Exception as e:
        pass
    return {"status": "disconnected", "models": [], "has_image_model": False}

STYLE_MODIFIERS = {
    "realistic": "photorealistic portrait, high quality, 8k",
    "cartoon": "cartoon style avatar, vibrant colors, cute",
    "anime": "anime style, manga artwork, detailed",
    "abstract": "abstract art, geometric patterns, colorful"
}

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest):
    try:
        enhanced_prompt = f"{request.prompt}, {STYLE_MODIFIERS.get(request.style, '')}, square format, portrait orientation, clear face area"
        
        payload = {
            "model": "sdxl-turbo",
            "prompt": enhanced_prompt,
            "size": "1024x1024",
            "num_images": 1
        }
        
        response = requests.post(
            f"{OLLAMA_BASE}/api/generate",
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ollama generation failed")
        
        result = response.json()
        image_base64 = result.get("images", [None])[0]
        
        if not image_base64:
            if "base64" in result:
                image_base64 = result["base64"]
            else:
                raise HTTPException(status_code=500, detail="No image in response")
        
        filename = f"dp_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%H%M%S')}.png"
        filepath = OUTPUT_DIR / filename
        
        image_data = base64.b64decode(image_base64)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
